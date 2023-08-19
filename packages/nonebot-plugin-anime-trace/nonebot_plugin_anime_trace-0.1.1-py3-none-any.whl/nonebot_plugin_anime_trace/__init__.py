import json
from io import BytesIO
import os

from httpx import AsyncClient
from PIL import Image

from nonebot import logger, on_keyword, get_driver
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    Message,
    MessageSegment,
    PrivateMessageEvent,
    GroupMessageEvent,
    MessageEvent,
)
from nonebot.adapters.onebot.v11.helpers import extract_image_urls
from nonebot.params import Arg
from nonebot.rule import Rule
from nonebot.exception import ActionFailed
from nonebot.internal.matcher import Matcher
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="识别动漫gal角色",
    description="通过ai.animedb.cn的api识别动漫、galgame角色",
    usage="""命令: {#} {识别|角色|人物} [gal|动漫]
示例: #识别gal
大括号内{}为必要关键字, 中括号内[]为可选参数, 默认为动漫模型
附带一张图片、或回复一张图片、或再发送一张图片
可以自定义命令符、命令关键字""",
    type="application",
    homepage="https://github.com/tomorinao-www/nonebot-plugin-anime-trace",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

config: Config = Config.parse_obj(get_driver().config)


async def _cmd_check(bot: Bot, event: MessageEvent):
    txt_msg = event.message.extract_plain_text().strip()
    if config.animetrace_cmd in txt_msg:
        return True


acg_trace = on_keyword(
    config.animetrace_keyword,
    rule=Rule(_cmd_check),
    priority=config.animetrace_priority,
    block=True,
)


@acg_trace.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher, state: T_State):
    # 选择模型
    txt_msg = event.message.extract_plain_text().strip()
    if "gal" in txt_msg:
        state["model"] = config.animetrace_model_gal
        state["mode"] = "galgame"
    else:
        state["model"] = config.animetrace_model_anime
        state["mode"] = "动漫"
    # 获取图片链接
    message = event.reply.message if event.reply else event.message
    if imgs := message["image"]:
        matcher.set_arg("imgs", imgs)


@acg_trace.got("imgs", prompt="请发送需要识别的图片")
async def get_image(state: T_State, imgs: Message = Arg()):
    img_urls = extract_image_urls(imgs)
    if not img_urls:
        await acg_trace.reject("没有找到图片, 请重新发送")
    state["img_urls"] = img_urls


@acg_trace.handle()
async def main(bot: Bot, event: Event, state: T_State):
    # 拿到图片
    img_urls = state["img_urls"]
    files = {"image": None}
    async with AsyncClient(trust_env=False) as client:
        res = await client.get(img_urls[0])
        if res.is_error:
            await acg_trace.finish("获取图片失败")
        base_img = Image.open(BytesIO(res.content)).convert("RGB")
        img_path = os.path.join(os.path.dirname(__file__), "tmp_img.png")
        base_img.save(img_path)
        files["image"] = open(img_path, "rb")

    # 发送请求
    model = state["model"]
    url = f"https://aiapiv2.animedb.cn/ai/api/detect?force_one=1&model={model}&ai_detect=0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
    }
    try:
        async with AsyncClient(trust_env=False, proxies=None) as client:
            res = await client.post(
                url=url, headers=headers, data=None, files=files, timeout=30
            )
            content = json.loads(res.content)
            if res.is_error:
                await acg_trace.finish("识别失败，可能是网络问题~", at_sender=True)
    except Exception as e:
        logger.exception(f"post({url})失败{repr(e)}")
        await acg_trace.finish(f"{repr(e)}识别失败，可能是网络问题~", at_sender=True)
    finally:
        files["image"].close()
        os.remove(img_path)

    # 检查识别结果
    if content["code"] != 0:
        await acg_trace.finish(f"出错啦~可能是图里角色太多了~\ncontent:{content}", at_sender=True)
    char_nums = len(content["data"])
    if char_nums == 0:
        await acg_trace.finish(f"没有识别到任何角色\ncontent:{content}", at_sender=True)

    # 构造消息
    res_start_msg = Message(f"共识别到{char_nums}个角色\n更多模型请访问:https://ai.animedb.cn")
    message_list = [res_start_msg]
    mode = state["mode"]
    for item in content["data"]:
        width, height = base_img.size
        box = item["box"]
        box = (box[0] * width, box[1] * height, box[2] * width, box[3] * height)
        img_bytes = BytesIO()
        item_img = base_img.crop(box)
        item_img.save(img_bytes, format="JPEG", quality=int(item["box"][4] * 100))
        char = item["char"]
        may_num = min(config.animetrace_max_num, len(char))
        msg_txt = Message(f"该角色有{may_num}种可能\n")
        for i in range(may_num):
            msg_txt += Message(
                f"{i+1}\n角色:{char[i]['name']}\n来自{mode}:{char[i]['cartoonname']}\n"
            )
        message = msg_txt + MessageSegment.image(img_bytes.getvalue())
        message_list.append(message)

    # 发送消息
    try:
        msgs = [
            {
                "type": "node",
                "data": {
                    "name": config.nickname[0],
                    "uin": bot.self_id,
                    "content": msg,
                },
            }
            for msg in message_list
        ]
        # 发送转发消息
        await bot.send_forward_msg(
            user_id=event.user_id if isinstance(event, PrivateMessageEvent) else 0,
            group_id=event.group_id if isinstance(event, GroupMessageEvent) else 0,
            messages=msgs,
        )
    except ActionFailed as e:
        logger.warning(e)
        await acg_trace.finish(
            message=Message("消息被风控了~合并消息发送失败"),
            at_sender=True,
        )
