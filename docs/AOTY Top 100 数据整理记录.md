# Album Ranking Project - AOTY Top 100 数据整理记录

日期：2026-07-25

## 项目背景

这是我的第一个 GitHub 实际项目。

目标： 将音乐网站中的高评分专辑榜单整理成结构化数据，并与个人 CD
收藏情况结合。

数据来源： - Rate Your Music (RYM) - Album of The Year (AOTY)

------------------------------------------------------------------------

# 一、阶段成果

## 已完成

✅ 创建 GitHub 仓库

项目： `album-ranking-project`

## RYM Top 100

完成： - 保存 RYM 榜单网页 - 分析 HTML 结构 - 使用 BeautifulSoup
提取数据 - 生成 CSV 文件

输出：

    data/rym_top100.csv

字段：

    rank
    artist
    album
    year
    release_date

## AOTY Top 100

完成： - 保存 AOTY 榜单前四页 HTML - 分析页面结构 - 找到专辑列表容器
`div.albumListRow` - 编写解析脚本 - 提取 100 张专辑数据

输出：

    data/aoty_top100.csv

字段：

    rank
    artist
    album
    year
    release_date
    user_score
    ratings_count
    genres

------------------------------------------------------------------------

# 二、AOTY 数据采集流程

## 1. 保存网页

由于直接访问网页存在限制：

采用浏览器保存 HTML 文件。

保存：

    data/
    ├── aoty_chart.html
    ├── aoty_chart_page_2.html
    ├── aoty_chart_page_3.html
    └── aoty_chart_page_4.html

## 2. 分析 HTML

使用：

    inspect_aoty_html.py

发现：

    div.albumListRow

为每个专辑条目的主要容器。

## 3. 提取字段

标题：

    .albumListTitle

日期：

    .albumListDate

评分：

    .scoreValue

评分人数：

    .scoreText

风格：

    .albumListGenre

------------------------------------------------------------------------

# 三、遇到的问题与解决

## GitHub Push 问题

问题：

    Recv failure: Connection was reset

解决：

重新 Push，最终成功。

## 网页访问问题

问题：

RYM / AOTY 页面加载异常。

解决：

保存 HTML 文件，本地解析。

## Python 文件路径问题

问题：

运行命令找不到文件。

原因：

脚本文件名与命令不一致。

解决：

确认实际文件名后运行。

------------------------------------------------------------------------

# 四、项目结构

    album-ranking-project/

    ├── data/
    │   ├── rym_top100.csv
    │   └── aoty_top100.csv
    │
    ├── scripts/
    │   ├── parse_rym_html.py
    │   ├── parse_aoty_html.py
    │   └── inspect_aoty_html.py
    │
    ├── notes/
    │
    └── README.md

------------------------------------------------------------------------

# 五、GitHub 使用记录

学习内容：

-   Repository：仓库管理
-   Commit：保存版本
-   Push：同步到 GitHub

示例：

    Add RYM top 100 album data

    Add AOTY top 100 album data

------------------------------------------------------------------------

# 六、下一阶段计划

-   [ ] 合并 RYM 与 AOTY 数据
-   [ ] 检查重复专辑
-   [ ] 建立统一专辑数据库
-   [ ] 添加个人收藏状态

收藏状态：

    owned
    wishlist
    not_buy

------------------------------------------------------------------------

# 七、个人总结

今天完成了第一次完整的数据采集流程：

网页\
↓\
HTML\
↓\
结构分析\
↓\
Python解析\
↓\
CSV数据\
↓\
GitHub管理

最大的收获不是获得100张专辑列表，而是掌握了一套数字工作流程。

以后面对其他网站数据，可以重复：

1.  获取数据
2.  分析结构
3.  编写解析器
4.  保存结构化结果
5.  使用 Git 管理版本

这是数字工作流能力培养的重要一步。
