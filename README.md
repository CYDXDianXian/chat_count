# chat_count

一款适用于hoshino的群聊关键消息记录插件

仓库地址：[CYDXDianXian/chat_count: 适用hoshino的群聊关键字记录插件 (github.com)](https://github.com/CYDXDianXian/chat_count)

该插件可记录群聊中某关键字的触发次数、时间、与完整消息，并可对储存记录的消息方便的进行读取，以查看群友们都围绕该关键字说了什么

感谢[@A-kirami (明见)](https://github.com/A-kirami)大佬帮助完善与优化代码

使用效果预览：

![](https://github.com/CYDXDianXian/chat_count/blob/main/img/IMG_0652.JPG)

![](https://github.com/CYDXDianXian/chat_count/blob/main/img/IMG_0654.JPG)

## 安装方法

1. 将chat_count文件夹放到`HoshinoBot/hoshino/modules`目录下
2. 安装依赖 `pip install -r requirements.txt`
3. 在`HoshinoBot/hoshino/config/__bot__.py`中添加chat_count模块
4. 重启Hoshino

## 指令列表

- `[查询xxx]` 查询xxx的关键字消息记录
- `[清空本群xxx数据]` 清空本群xxx的关键字消息记录数据（仅限群主与管理）
- `[清空全部数据]` 清空全部群的全部关键字消息数据（仅限主人）
- `[清空全部xxx数据]` 清空全部群的xxx关键字消息数据（仅限主人）

## 使用说明

- 增加或修改python文件中的关键字即可自定义想要记录的消息
- 文件中已经预置了三组消息示例，使用前请进行关键字更改
- 每组消息记录模块包含4个函数，分别对应消息记录、查询、清空本群和清空全部群4个功能，复制模块时记得将其全部复制并逐个设定新的触发指令，文件中已用分割线标注
- 注意定时清理消息数据，否则数据会越来越大