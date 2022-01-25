import traceback
import asyncio
from pathlib import Path

import time
from typing import Any, Dict, Optional

# ↓导入ujson 没装就用json
try:
    import ujson as json
except ImportError:
    import json

from hoshino import Service, priv
from hoshino.typing import HoshinoBot, CQEvent

sv_help = '''
这是一个群聊关键字记录插件，
可记录次数与储存消息。

[查询xxx] 查询xxx的关键字消息记录
[清空本群xxx数据] 清空本群xxx的关键字消息记录数据（仅限群主与管理）
[清空全部数据] 清空全部群的全部关键字消息数据（仅限主人）
[清空全部xxx数据] 清空全部群的xxx关键字消息数据（仅限主人）
'''.strip()

sv = Service(
    name = '群聊关键字记录',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #可见性
    enable_on_default = True, #默认启用
    bundle = '娱乐', #分组归类
    help_ = sv_help #帮助说明
    )

# ====== 指定用户才能触发的关键字 ======
@sv.on_keyword('可怜酱') # 设置触发关键字
async def 关键字计数器(bot: HoshinoBot, ev: CQEvent):
    keyword = '可怜酱' # 设置关键字
    user_name = '缘酱' # 设置指定的触发者名称
    
    if ev.user_id != 123456789:  # 指定触发者QQ
        return
    await chat_count(bot, ev, keyword, user_name)

@sv.on_fullmatch('查询可怜酱') # 设置关键字
async def 查询关键字数据(bot: HoshinoBot, ev: CQEvent):
    keyword = '可怜酱' # 设置关键字
    await Query_keyword(bot, ev, keyword)

@sv.on_fullmatch('清空本群可怜酱数据') # 设置关键字
async def 清空关键字数据(bot: HoshinoBot, ev: CQEvent):
    keyword = '可怜酱' # 设置关键字
    await clear_group_keyword(bot, ev, keyword)

@sv.on_fullmatch('清空全部可怜酱数据') # 设置关键字
async def 清空全部消息记录(bot: HoshinoBot, ev: CQEvent):
    keyword = '可怜酱' # 设置关键字
    await clear_keyword(bot, ev, keyword)

# ====== 所有人都能触发的关键字 ======
@sv.on_keyword('风酱') # 设置触发关键字
async def 关键字计数器(bot: HoshinoBot, ev: CQEvent):
    keyword = '风酱' # 设置关键字
    await chat_count(bot, ev, keyword)

@sv.on_fullmatch('查询风酱') # 设置关键字
async def 查询关键字数据(bot: HoshinoBot, ev: CQEvent):
    keyword = '风酱' # 设置关键字
    await Query_keyword(bot, ev, keyword)

@sv.on_fullmatch('清空本群风酱数据') # 设置关键字
async def 清空关键字数据(bot: HoshinoBot, ev: CQEvent):
    keyword = '风酱' # 设置关键字
    await clear_group_keyword(bot, ev, keyword)

@sv.on_fullmatch('清空全部风酱数据') # 设置关键字
async def 清空全部消息记录(bot: HoshinoBot, ev: CQEvent):
    keyword = '风酱' # 设置关键字
    await clear_keyword(bot, ev, keyword)

# ====== 所有人都能触发的关键字 ======
@sv.on_keyword('时代')
async def 关键字计数器(bot: HoshinoBot, ev: CQEvent):
    keyword = '时代'
    await chat_count(bot, ev, keyword)

@sv.on_fullmatch('查询时代')
async def 查询关键字数据(bot: HoshinoBot, ev: CQEvent):
    keyword = '时代'
    await Query_keyword(bot, ev, keyword)

@sv.on_fullmatch('清空本群时代数据')
async def 清空关键字数据(bot: HoshinoBot, ev: CQEvent):
    keyword = '时代'
    await clear_group_keyword(bot, ev, keyword)

@sv.on_fullmatch('清空全部时代数据')
async def 清空全部消息记录(bot: HoshinoBot, ev: CQEvent):
    keyword = '时代'
    await clear_keyword(bot, ev, keyword)


# ====== 仅限超级管理员才能进行的操作 ======
@sv.on_fullmatch("清空全部数据")  # 注意！该操作将会清空全部群的群聊记录！！！
async def 清空全部消息记录(bot: HoshinoBot, ev: CQEvent):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.send(ev, "对不起，您的权限不足，仅bot主人才能进行该操作!")
    else:
        save_data({})  # 保存data中的数据到json

        await bot.send(ev, "消息记录已全部清空")


# ===== 以下全部是各种数据处理模块，若不熟悉请勿随意改动！！！=====
data_path = Path(__file__).parent / "chat_count.json"


# 保存数据模块
def save_data(data: Dict[str, Any]) -> None:
    # ->常常出现在python函数定义的函数名后面，为函数添加元数据,描述函数的返回类型，从而方便开发人员使用
    try:  # 对可能发生异常的代码处进行 try 捕获
        json_data = json.dumps(
            data, indent=4, ensure_ascii=False
        )  # 将python字典转化为json字符串
        data_path.write_text(json_data, encoding="utf-8")
    except:  # 发生异常时执行 except 代码块，finally 代码块是无论什么情况都会执行
        traceback.print_exc()
        # Python使用traceback.print_exc()来代替print(e) 来输出详细的异常信息，print(e) 该异常捕获只能捕获到错误原因，traceback.print_exc()该异常捕获方式不但可以捕获到异常原因，同样可以捕获异常发生的位置【具体python文件和行数】


# 读取数据模块
def load_data() -> Optional[Dict[str, Any]]:
    try:
        return json.loads(data_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except:
        traceback.print_exc()  # 输出详细异常，同上


# 关键字消息记录模块
async def chat_count(bot: HoshinoBot, ev: CQEvent, keyword: str, user_name: str = None) -> None:
    uid = str(ev.user_id)  # 获取用户QQ，一定要转换为字符串，否则写入键值对时会出现bug
    gid = str(ev.group_id)  # 获取群号

    data = load_data()  # 读取json文件，转化为python字典

    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # ↓ 检查要监控的关键字是否存在，若不存在，则创建一个空字典
    if keyword not in data:
        data[keyword] = {}

    qq_s = str(
        ev.message.extract_plain_text()
    )  # 触发关键词的内容，str()强制转化为字符串类型，以防？等特殊符号无法正常记录的bug发生
    s = {
        "消息": qq_s,
        "时间": now_time,
    }

    if gid not in data[keyword]:
        data[keyword][gid] = {}

    group_data = data[keyword][gid]  # 群消息数据
    if uid in group_data:  # 若uid存在，则追加项目，否则创建列表。
        if s not in group_data[uid]:  # 若要追加的内容不相同，则进行追加操作，否则不执行任何操作
            group_data[uid].append(s)
    else:
        group_data[uid] = [s]  # 创建列表，包含初始内容s。uid是键，列表[s]是值，在字典中创建新的键值对

    save_data(data)  # 保存data中的数据到json

    # ↓ 将每个用户的消息统计数字放入一个列表中
    num_list = [len(v) for v in group_data.values()]  # 生成统计数字列表

    su = sum(num_list)  # sum()方法对序列进行求和计算
    msg = f"{keyword}在本群被{user_name or '大家'}呼唤{su}次"
    await bot.send(ev, msg)

# 关键字消息记录查询模块
async def Query_keyword(bot: HoshinoBot, ev: CQEvent, keyword: str) -> None:
    gid = str(ev.group_id)  # 获取群号

    data = load_data()  # 读取json文件，转化为python字典

    if keyword not in data:
        await bot.finish(ev, f'抱歉，关键字"{keyword}"尚未被记录')
    elif not data[keyword]:
        await bot.finish(ev, f'抱歉，"{keyword}"的相关消息记录为空')
    elif gid not in data[keyword]:
        await bot.finish(ev, f'抱歉，本群{gid}的"{keyword}"相关消息尚未被记录')
    elif not data[keyword][gid]:
        await bot.finish(ev, f'抱歉，本群{gid}的"{keyword}"相关消息记录为空')

    group_data = data[keyword][gid]  # 访问字典中keyword键对应的值

    for k, v in group_data.items():
        msg_list = [f"【{i['时间']}】\n{i['消息']}" for i in v]
        msg = f"[CQ:at,qq={k}]的消息记录: \n" + "\n".join(msg_list)  # 将消息记录拼接成字符串
        await bot.send(ev, msg)
        await asyncio.sleep(2)  # 异步 sleep 避免堵塞

# 清空群内关键字消息模块
async def clear_group_keyword(bot: HoshinoBot, ev: CQEvent, keyword: str) -> None:
    gid = str(ev.group_id) # 获取群号

    data = load_data()  # 读取json文件，转化为python字典

    if not priv.check_priv(ev, priv.ADMIN):
        await bot.send(ev, '抱歉，您的权限不足，只有群主和管理才能清空本群消息记录')
    else:
        if keyword not in data.keys():
            await bot.send(ev, f'抱歉，本群{gid}的消息为空，清空失败')
        if gid not in data[keyword].keys():
            await bot.send(ev, f'抱歉，本群{gid}的消息尚未被记录，清空失败')
        else:
            group_data = data[keyword][gid] # 访问字典中keyword键对应的值
            group_data.clear() # 清空字典
            save_data(data) # 保存data中的数据到json

            await bot.send(ev, f'本群{gid}的"{keyword}"相关消息记录已清空')

# 清空关键字消息模块
async def clear_keyword(bot: HoshinoBot, ev: CQEvent, keyword: str) -> None:
    data = load_data()  # 读取json文件，转化为python字典
    
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.send(ev, '抱歉，您的权限不足，只有bot主人才能进行该操作！')
    else:
        if keyword not in data.keys():
            await bot.send(ev, f'抱歉，无"{keyword}"的相关消息记录，清空失败')
        else:
            keyword_data = data[keyword] # 访问字典中keyword键对应的值
            keyword_data.clear() # 清空字典
            save_data(data) # 保存data中的数据到json

            await bot.send(ev, f'有关"{keyword}"的全部群相关消息记录已清空')
