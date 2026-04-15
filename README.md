<div align="center">

# 浅草寺.skill

> 把尘声放在阶前，让木签先替你说话。

![Codex Skill](https://img.shields.io/badge/Codex-Skill-2F5D50?style=flat-square)
![Asakusa Omikuji](https://img.shields.io/badge/Asakusa-Omikuji-BF8B30?style=flat-square)
![Chinese First](https://img.shields.io/badge/Language-Chinese%20First-7B3F00?style=flat-square)
![Ritual UX](https://img.shields.io/badge/Experience-Ritual%20First-5C6B73?style=flat-square)
![Real Lots 1-100](https://img.shields.io/badge/Lots-Real%201--100-556B2F?style=flat-square)

<p align="center">
  <a href="#缘起">缘起</a> ·
  <a href="#它做什么">它做什么</a> ·
  <a href="#仪式流程">仪式流程</a> ·
  <a href="#体验气质">体验气质</a> ·
  <a href="#app-形态">App 形态</a> ·
  <a href="#快速试签">快速试签</a> ·
  <a href="#文件结构">文件结构</a>
</p>

<p align="center">
  一份为 <strong>浅草寺观音灵签</strong> 所写的 Codex skill。<br />
  它不喧哗，不追问，不替人争辩命运，只在檐下递出签筒，然后安静地揭开一纸吉凶。
</p>

</div>

---

## 缘起

有些抽签体验一打开，就像热闹的按钮游戏。  
而浅草寺这一类签，不该只是“随机结果”，它更像一件需要被郑重对待的小事。

于是有了这份 `浅草寺.skill`。

它想做的，不是把签文讲得神神叨叨，也不是把古意磨成平庸的功能说明，而是尽量保留一种更安静的秩序:

- 先让用户把心放稳
- 再由木签开口
- 若签意不佳，也只留一扇窄门，允许“纳签重请”
- 若重请之后仍不佳，便劝人止于此，不再反复追逐一纸之变

换句话说，这不是一个“帮你测答案”的 skill。  
它更像一个会在雷门风里替你扶一下衣袖，然后把签筒递到手边的引路人。

## 它做什么

这份 skill 提供的是一套完整的浅草寺式启签体验：

- 直接抽取真实的浅草寺 1-100 签，不凭空编造结果
- 在开场、揭签、收尾处维持统一而克制的仪式感中文
- 将 `签号`、`吉凶`、`诗曰` 放在前面，让签面先说话
- 完整展示原签里的 `解曰`，保留它本来的条目结构
- 当签气偏弱时，只委婉提供一次 `纳签重请`
- 若重请之后新签仍不佳，则收束为“今日宜止于此”，不鼓励继续刷签

## 仪式流程

### 1. 初请一签

第一句话不是“你抽到了什么”，而是先把人轻轻带到檐下。

它会这样开始：

> 风从雷门外过，尘声渐歇，像有人把一整日的杂念都缓缓拂落。你不必急着把心事说破，只需把目光放低，把呼吸放稳。余下的，交给这一支签来开口。

随后才揭出：

- 第几签
- 吉凶
- 诗曰
- 四句解说
- 完整解曰

### 2. 纳签重请

只有当签气偏弱时，这份 skill 才会把“再启一回”的门留出来。

它不会在首页就把这条分支提前说破，也不会鼓动用户无限重抽。  
它真正保留的是一种更接近寺院习惯的意思：

> 旧签可以留下提醒，却未必要继续贴身。  
> 若你愿意，也可把这一纸滞气纳去，再请一签，看此后该如何行路。

而所谓“转势”，在这里并不是轻飘飘地宣称命运被彻底改写。  
它更像是说:

- 旧签所示的滞、急、逆，留在旧纸上
- 新签所照见的，是你从此刻起携带怎样的心气继续往前

## 体验气质

这份 README 若只写“功能列表”，其实配不上这份 skill 的脾气。

它最在意的几件事是：

- 不把抽签写成热闹的娱乐互动
- 不把文采写成浮夸的玄学黑话
- 不把不顺的签写成恐吓
- 不把“重请”写成无限重开
- 不让用户像在填表单，而是像在檐下站定片刻

所以它追求的并不是“像算命”，而是“像有分寸的签”。

## App 形态

这份仓库现在还多带了一层移动端优先的网页 app，位于 `app/` 目录。

它不是把命令行结果简单贴进网页，而是把整个体验重新做成了更像“启签现场”的界面：

- 首页先造景，再递出签筒
- 抽签过程有节奏与动画，而不是瞬间跳结果
- 揭签页把 `吉凶`、`诗曰`、`解曰` 摆成可阅读的签纸结构
- 若签意偏弱，再引出 `纳签重请`
- 若重请后仍不佳，则收束为“今日宜止”
- 现在也支持作为 PWA 安装到手机主屏，并缓存基础壳与签文数据

本地运行：

```bash
python3 scripts/serve_app.py
```

然后打开：

```text
http://127.0.0.1:4173/app/
```

## 快速试签

在本地目录中可以直接运行：

```bash
python3 scripts/draw_omikuji.py
```

若想看指定签号：

```bash
python3 scripts/draw_omikuji.py --sign-no 17
```

若要模拟一次纳签重请：

```bash
python3 scripts/draw_omikuji.py --redraw-from-sign 69
```

## 文件结构

```text
asakusa-omikuji-skill/
├── README.md
├── SKILL.md
├── agents/openai.yaml
├── app/
├── data/asakusa_omikuji_part*.json
├── scripts/draw_omikuji.py
├── scripts/serve_app.py
└── tests/test_draw_omikuji.py
```

各文件职责很清楚：

- `SKILL.md`：定义触发条件、语气、流程与纳签重请规则
- `agents/openai.yaml`：提供技能在 UI 中显示的元数据
- `app/`：移动端优先的网页 app 界面与交互体验
- `data/asakusa_omikuji_part*.json`：分片存放浅草寺 1-100 签原始内容，运行时自动合并读取
- `scripts/draw_omikuji.py`：负责真实抽签、揭签与重请逻辑
- `scripts/serve_app.py`：本地启动 app 的静态服务器
- `tests/test_draw_omikuji.py`：覆盖基本抽签与重请行为

## 最后一页

若你把它推上 GitHub，希望别人第一眼看到的，不只是“这是个能抽签的 skill”。  
更希望他们看到的是：

这份小小的东西，知道什么叫留白，知道什么叫止语，也知道什么叫在一纸吉凶之外，仍旧把人的心轻轻放回自己的脚下。
