# RYM Top 100 数据整理操作记录 2026-07-25

## 项目目标

把 Rate Your Music（RYM）历史专辑榜前 100 名整理成 CSV 文件，并上传到 GitHub 项目仓库。

最终生成文件：

```text
data/rym_top100.csv
```

---

## 一、项目结构

```text
album-ranking-project/
├─ data/
│  ├─ rym_chart.html
│  ├─ rym_chart_page_2.html
│  ├─ rym_chart_page_3.html
│  └─ rym_top100.csv
├─ scripts/
│  └─ parse_rym_html.py
└─ README.md
```

---

## 二、保存 RYM 前三页网页

RYM 每页显示 40 张专辑，因此获取 Top 100 需要前三页：

- 第 1 页：1–40
- 第 2 页：41–80
- 第 3 页：81–120，最后只保留前 20 条

由于 Playwright 打开的浏览器被 Cloudflare 拦截，最终采用：

> 手动保存网页 + Python 解析本地 HTML

分别保存为：

```text
data/rym_chart.html
data/rym_chart_page_2.html
data/rym_chart_page_3.html
```

网页离线打开时，即使样式、图片加载失败，只要专辑名、艺人、日期等文字仍然存在，通常就可以继续解析。

---

## 三、Python 解析逻辑

解析脚本读取三个 HTML 文件，使用 BeautifulSoup 查找榜单条目，并提取：

- rank：排名
- artist：艺人
- album：专辑名
- year：年份
- release_date：完整发行日期

主要流程：

```text
读取三个 HTML
→ 找到每页榜单条目
→ 合并全部条目
→ 只保留前 100 条
→ 写入 CSV
```

运行脚本后，终端应显示类似：

```text
rym_chart.html：找到 40 个榜单条目
rym_chart_page_2.html：找到 40 个榜单条目
rym_chart_page_3.html：找到 40 个榜单条目
三页合计找到 120 个榜单条目
成功保存 100 条数据
```

生成：

```text
data/rym_top100.csv
```

---

## 四、检查 CSV

用 WPS 或其他表格软件打开：

```text
data/rym_top100.csv
```

检查：

- 第一行表头是否为：
  ```text
  rank,artist,album,year,release_date
  ```
- 是否有 100 条数据
- 最后一条排名是否为 100
- 专辑名、艺人、年份是否正常

表格中显示不全，通常只是列宽太窄，不代表数据丢失。

---

## 五、GitHub Desktop 操作

### 1. Commit

Commit 表示：

> 把本次改动记录到本地 Git 仓库。

提交说明：

```text
Add RYM top 100 album data
```

### 2. Push

Push 表示：

> 把本地 commit 上传到 GitHub 网页。

如果出现：

```text
Recv failure: Connection was reset
```

通常是网络或代理连接中断。

处理方法：

```text
关闭报错
→ 检查代理和网络
→ 重新点击 Push origin
```

不需要重新生成 CSV，也不需要重复 commit。

### 3. 网页确认

进入 GitHub 仓库，确认：

- `data/rym_top100.csv` 已出现
- 最新 commit 已出现
- 文件内容可以正常查看

---

## 六、更新 README 进度

在 GitHub 网页打开 `README.md`，点击铅笔图标编辑。

把：

```markdown
- [ ] 添加 RYM 榜单数据
```

改成：

```markdown
- [x] 添加 RYM 榜单数据
```

提交说明可以写：

```text
Update README progress
```

---

## 七、本次遇到的问题

### 1. Playwright 无法正常打开 RYM

原因：

- Cloudflare 验证
- 自动化浏览器被拦截

最终方案：

```text
用正常浏览器手动保存网页
```

### 2. 下载 HTML 被 Edge 阻止

可能出现：

- 自动取消
- 下载速度 0 B/s
- 提示文件不受信任

处理：

- 尝试“保留”或“仍然保留”
- 直接用 Ctrl + S 保存网页
- 即使图片被阻止，只要 HTML 文字内容存在即可

### 3. 离线网页显示很奇怪

原因：

- CSS、图片、脚本没有加载
- 页面结构仍然保留

结论：

> 解析 HTML 不需要网页看起来完整，只要数据存在即可。

### 4. GitHub Push 失败

原因：

- 网络被重置
- 代理节点不稳定

处理：

```text
恢复网络
→ 再次 Push
```

Commit 不会因此丢失。

---

## 八、这次真正掌握的流程

```text
确定数据目标
→ 获取网页
→ 保存本地 HTML
→ Python 解析
→ 导出 CSV
→ 检查结果
→ Git commit
→ Git push
→ 更新 README
```

---

## 九、下一步：AOTY Top 100

下一阶段目标：

```text
整理 AOTY 前 100 张专辑
```

开始前先判断：

- AOTY 每页显示多少条
- 是否需要翻页
- 是否能直接抓取
- 是否也需要保存本地 HTML
- 页面结构和 RYM 是否相似
- 最终 CSV 字段是否与 RYM 保持一致

建议先复用本次结构，不要从零开始。

---

## 当前进度

- [x] 创建 GitHub 仓库
- [x] 添加 RYM 榜单数据
- [ ] 添加 AOTY 榜单数据
- [ ] 添加个人收藏状态
- [ ] 检查重复数据
- [ ] 生成购买清单
