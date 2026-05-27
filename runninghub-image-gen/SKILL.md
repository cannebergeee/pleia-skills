---
name: runninghub-image-gen
description: Generate and edit images through RunningHub API workflows, including anima/anima2 anime prompt construction, image-to-image workflows, model/workflow selection, and Anima artist/style guidance. Use when the user asks to create images, edit images, run RunningHub workflows, or choose Anima artists/styles for generation prompts.
---

# RunningHub 图像生成工具

通过 RunningHub API 调用各种 AI 图像生成和编辑工作流。基于 Node.js，跨平台通用。

## 平台兼容性

本 Skill 适用于以下 AI Agent 平台：
- **Claude Code** (Anthropic)
- **OpenCode** (OhMyOpenCode)
- **OpenClaw**
- **Hermes**
- **AstrBot**
- **任意支持执行命令的通用 Agent**

所有平台使用相同的命令和参数，无需平台特定适配。

## 环境要求

- **Node.js >= 21** (需要全局 `fetch` / `FormData` / `File`)
  - Node 18-20 用户需额外安装：`npm install undici`（如遇问题请升级到 Node 21+）
- `.env` 文件配置 API Key（格式见下文）

## 前提条件

API Key 配置在 `{SKILL_DIR}/.env` 文件中。
格式：`RUNNINGHUB_API_KEY=your_api_key_here`

> `{SKILL_DIR}` = 本 SKILL.md 文件所在目录。所有命令均相对于此目录执行。

## 跨平台兼容规则（Windows / Linux / macOS）

- CLI 本体只依赖 Node.js 标准库，不依赖 Bash、PowerShell 专属语法或系统包管理器。
- 默认输出路径和锁文件都由 Node `os.tmpdir()` 决定；不要在通用示例中硬编码 `/tmp`、`C:\...` 或 `$(date +%s)`。
- 推荐不传 `-o`，让脚本自动生成跨平台临时输出路径；脚本成功后只读取 stdout 最后一行的 `Success! Output saved to: ...`。
- 如必须指定输出路径，使用当前平台合法的绝对路径，或使用相对路径如 `outputs/result.png`。
- 输入图片路径必须是当前平台可读的本地路径；不要把示例中的 Unix 路径原样用于 Windows。

## ⚠️ 关键规则（五项铁律，违反即 Bug）

### 🔴 铁律 0：绝对禁止复用旧文件 + 禁止后台执行（最高优先级）

**每次用户请求都必须：① 同步执行脚本 ② 等待脚本自己退出 ③ 读取脚本 stdout 的输出路径。无任何例外。**

| ❌ 常见偷懒行为 | ✅ 正确行为 |
|---------------|-----------|
| 用户说"画一只猫"，Agent 看到磁盘上已有 `test_output.png`，直接发送旧文件 | **忽略所有已有文件，执行 `node run.js` 生成新图** |
| 用户说"转真人"，Agent 发现之前的 `output.png` 还在，复用 | **每次都是新任务，必须调用 RunningHub API** |
| 用户改了一下提示词，Agent 觉得"差不多"，发旧的 | **哪怕只改一个字，也必须重新生成** |
| Agent 用 `read` / `ls` 检查目录发现已有图片，觉得"有图可发" | **现有文件与当前请求无关，全部视为无效** |
| **❗ Agent 把脚本丢到后台（`background: true` / `&`），然后 `ls /tmp/rh_*.png` 通配匹配到了旧文件** | **脚本必须同步阻塞执行，等它自己退出。用 stdout 输出的路径，不去磁盘上搜文件** |
| **❗ Agent 用通配符 `ls /tmp/*.png` 搜文件，找到旧的就发** | **永远不要用通配符搜索输出文件。输出路径只来自脚本 stdout 的最后一行** |

**核心原则：**
1. RunningHub 是生成式 AI，同样输入每次结果不同。旧文件对当前请求零价值。
2. **脚本同步执行**：`node run.js` 必须阻塞等待直到退出。**绝对禁止后台执行**（`&`、`background: true`、`nohup` 等）。**唯一例外：AstrBot 平台**因工具限制必须用 `subprocess.Popen` 解耦启动，详见 AstrBot 节。
3. **输出路径只信 stdout**：脚本退出后，stdout 最后一行为 `Success! Output saved to: /path/to/file.png`——只从这行取路径，**不用 `ls` / `find` / `readdir` 去磁盘搜文件**。
4. **通配符 = 陷阱**：`ls /tmp/rh_*.png` 会匹配到之前请求的旧文件。绝对禁止。

### 🔴 铁律 1：每次请求只执行一次脚本（含失败处理）

**一个用户请求 = 一次脚本执行 = 一张（或一组）结果图片。禁止重复执行。失败也不例外。**

- **绝对禁止**：同一个请求下，对同一个工作流多次执行 `node run.js`。
- **绝对禁止**：脚本成功后再次执行（以为需要重试）——脚本成功退出即表示 API 请求已完成。
- **绝对禁止**：并行执行多个相同命令。
- **正确行为**：每个用户请求，只运行一次命令。一次，仅一次。

#### 失败处理（铁律 1 延伸，同等强制）

**脚本报错时，禁止任何形式的重试。一次失败 = 任务结束 = 立即告知用户结果。**

| 脚本输出 | ✅ 必须做的事 | ❌ 绝对禁止 |
|---------|-------------|-----------|
| `Error: Task failed` | 告诉用户"图片生成失败~换个提示词或者稍后再试试吧~" | 换提示词重试、换工作流重试、相同参数再次执行 |
| `Error: Task timeout` | 告诉用户"图片生成超时~换个提示词或者稍后再试试吧~" | 等待更久后重试、换工作流重试、调整参数重试 |
| `BUSY: Another generation...` | 直接跳到轮询日志步骤，等待现有任务完成 | 杀进程、强制新启动、换时间戳重启 |
| 任何其他错误 | 告知用户具体错误原因（API Key 缺失等） | 尝试修复后重试、换参数重试 |

**为什么不能重试：**
1. RunningHub API 每次调用消耗配额。重试 = 浪费用户额度。
2. Task timeout 说明服务器繁忙或任务复杂，重试只会更糟。
3. Task failed 说明输入参数或图片有问题，重试不会改变结果。

**🔴 换模型/换工作流/换 prompt = 重试 = 同等违反铁律 1：**

| ❌ 常见违规（本日志实锤） | ✅ 正确行为 |
|--------------------------|-----------|
| anima2 失败 → "再换个模型试试~" → 换 qwen2 重试 | anima2 失败 → 告知用户失败 → 停止 |
| anima2 失败 → 换 prompt（加 futa 等词）→ 再次 anima2 | anima2 失败 → 告知用户失败 → 停止 |
| qwen2 失败 → 换 zimg1 重试 | qwen2 失败 → 告知用户失败 → 停止 |

**失败就是失败。换任何参数（模型、工作流、prompt）重新执行 `node run.js` 都是禁止的。** 用户明确说"再试一次/重试/换模型"才允许重试，且最多重试一次。重试也失败则必须停止。

**🔴 兜底措施：重试时锁死模型和工作流，仅允许修改提示词**

即使用户明确要求重试，也**绝对禁止更换模型或工作流**。必须沿用失败那次用的同一个模型，只允许修改提示词让其更含蓄、能过审。

| ✅ 允许 | ❌ 禁止 |
|--------|--------|
| anima2 失败 → 用户要求重试 → 仍用 anima2，改 prompt 去敏感词 | anima2 失败 → 换 qwen2 重试 |
| qwen2 失败 → 用户要求重试 → 仍用 qwen2，改 prompt 去敏感词 | qwen2 失败 → 换 anima2 重试 |
| 改 prompt：把 explicit 词汇换成含蓄表述 | 改 prompt：把 NSFW 内容意图降级为全年龄 |

**修改 prompt 规则（仅限重试场景）：**
1. 保持用户原始意图不变（角色、姿势、场景、内容级别）
2. 去除或替换导致审核失败的敏感裸露词 → 使用含蓄/euphemistic 描述
3. 安全标签(word)可适当降级：nsfw → sensitive，但内容意图不变
4. **不得借"改 prompt"之名将 NSFW 内容降级为全年龄——那等于拒绝用户要求**

**🟡 anima 特殊例外：允许失败后自动重试一次（仅限 anima）**

anima/anima2 是默认主力文生图工作流，对敏感内容审核较严，常因 prompt 含裸露词被拦。为此开设例外：

> anima* 失败时，允许 Agent **自动重试一次**，无需等待用户明确指令。

| 条件 | 规则 |
|------|------|
| 适用工作流 | **仅限 anima1 / anima2 / oldanima1 / oldanima2**（文生图）。其他工作流不适用此例外 |
| 重试次数 | **绝对只能 1 次，无任何例外。** 按用户原始请求计次（非按失败次数计次）。一个请求 = 原始执行 + 最多 1 次重试 = 总共最多 2 次。重试失败后不得以"又失败了所以再触发例外"为由继续重试 |
| 模型约束 | **禁止换模型**——只能用同一个 anima 工作流重试 |
| prompt 调整 | 自行修改 prompt：按下方「🔧 重试 prompt 去敏策略」执行，系统化替换敏感词，不漏点能过审 |
| 内容底线 | 保留用户原始意图（角色、姿势、场景），禁止降级为全年龄 |

| ❌ 违规（本日志实锤） | ✅ 正确（本例外允许） |
|---------------------|---------------------|
| anima2 失败 → 换 qwen2 重试 | anima2 失败 → 仍用 anima2，改 prompt 去"erection/penis/nipples"等词 → 重试 |
| anima2 失败 → 换 "futa/futanari" 重试 | anima2 失败 → 仍用 anima2，用含蓄词替换 → 重试 |
| anima2 失败 → 重试 2 次以上 | anima2 失败 → 只重试 1 次 → 仍失败则停止 |

**🔧 重试 prompt 去敏策略（如何最大化过审率）**

anima 内容审核主要拦三类东西：**直接器官词汇** > **explicit 安全标签** > **性行为描述**。

**🔴 首次执行绝对禁止去敏——必须忠实使用用户要求的原始标签和词汇（本日志实锤：log6 首轮就降为 nsfw+large bulge，跳过了用户想要的 explicit+penis，属于严重违规）：**

| 第几次执行 | 安全标签 | prompt 词汇 | 去敏 |
|-----------|---------|------------|------|
| **首次（原始执行）** | 用户要求的：`explicit` / `nsfw` / `sensitive` | 用户要求的原始词（含 `penis`, `erection`, `nipples` 等） | **绝对禁止去敏** |
| **重试（失败后）** | 按下方策略降级 | 按下方替换表去敏 | 仅此时允许去敏 |

> **🔴 首次 = 原样忠实。去敏 = 仅限重试。首次执行绝对不允许预先降级。首次失败才允许去敏重试。**

去敏按以下优先级逐层执行（仅重试时）：

**第一层：安全标签降级（必须做）**
```
explicit → nsfw
nsfw → sensitive（仅当 nsfw 仍失败时才降）
→ 绝不降到 safe（等于拒绝用户）
```

**第二层：敏感词替换表（核心）**

| 类型 | ❌ 被拦词汇（删除） | ✅ 替换为 |
|------|-------------------|----------|
| 直接器官 | `penis`, `dick`, `cock` | `bulge`, `package`, `crotch` 或不写让模型自行推断 |
| 直接器官 | `pussy`, `vagina`, `clitoris` | `crotch`, `between legs` 或不写 |
| 直接器官 | `nipples`, `areola` | `covered chest`, `clothed chest` |
| 直接器官 | `anus`, `asshole` | `rear view`, `from behind` 或不写 |
| 生理状态 | `erection`, `erect` | `arousal`, `excitement`, `tenting`, 或靠 pose/bulge 暗示 |
| 生理状态 | `wet`, `wet pussy` | 不写，靠 context 暗示 |
| 性行为 | `sex`, `fucking`, `riding`, `penetration`, `blowjob` | `intimate`, `embrace`, `close contact`, `leaning` |
| 裸体 | `nude`, `naked`, `bottomless`, `topless` | `clothed`, `partially clothed`, `undressed`, `no clothes` + `covered` |
| 液体 | `cum`, `semen`, `sperm`, `squirt` | 不写，或 `fluid`, `liquid`（极含蓄） |

**第三层：加遮挡词（对冲残留风险）**

在 prompt 中加入以下词可显著提高过审率：
```
clothed, covered, no nudity, bulge, clothes lifted, partially dressed, underwear, pants
```

**第四层：角色类型保留规则（防止意图丢失）**

| 用户要的 | 触发词 | 去敏时**必须保留** | ❌ 禁止替换为 |
|---------|--------|-------------------|------------|
| 扶她 | `futanari`, `futa`, `dickgirl` | `futanari` 或 `dickgirl`（保留一个） | `gender ambiguity`（完全丢失意图） |
| 巨根 | `big penis`, `large penis`, `huge` | `large bulge`, `huge package` | 删除不写 |
| 爆乳 | `huge breasts`, `large breasts` | `large breasts`（通常不过滤） | 不需要改 |

> **核心原则**：角色标签（futanari/dickgirl）本身通常不会被拦。被拦的是 `futanari` + `penis` + `erection` 的组合。去敏时保留角色标签，只去掉后面的器官/状态词。

**第五层：靠 pose 和 context 暗示（最高级技巧）**

当词汇替换后仍然被拦，去掉所有直接描述词，只靠 pose/context 暗示：
```
"spread legs, looking at viewer, confident smirk, hand between thighs"
"hand on crotch, teasing expression"
"leaning forward, intimate pose, bedroom setting"
```

**完整去敏示例：**

| 原始 prompt | 去敏后 prompt | 策略 |
|------------|-------------|------|
| `explicit, futanari, big penis, erection, standing, spread legs` | `nsfw, futanari, large bulge, tenting, standing, confident pose, clothed, covered` | 标签降级 + 器官换 bulge + 状态换 tenting + 加遮挡词 |
| `nsfw, 1girl, pussy, wet, spread legs` | `nsfw, 1girl, between legs, arousal, spread legs, intimate, underwear` | 器官删除 + 状态换 arousal + 加 underwear |
| `explicit, 1girl, nipples, nude, sex` | `nsfw, 1girl, covered chest, no clothes, intimate embrace, bedroom` | 标签降级 + 器官换 covered + 行为换 embrace |

**去敏效果自检清单：**
1. ✅ 安全标签降级了？（explicit → nsfw 起步）
2. ✅ 所有直接器官词去掉了？（penis/pussy/nipples/anus...）
3. ✅ 角色标签保留了？（futanari 不能换成 gender ambiguity）
4. ✅ 加了遮挡词？（clothed/covered/underwear/bulge）
5. ✅ 用户原始意图保留了？（角色、姿势、场景、尺度级别不变）

**🔴 换模型重试的隐藏 bug：同样的图又发一遍**

相同 prompt + 相同模型 → RunningHub 输出视觉相同的图片。用户看到"同样的图又发了一遍"，会认为 bot 偷懒没重新生成（实际上确实重新生成了，但结果一样）。这比失败更糟——白花额度还让用户以为 bot 坏了。**禁止换模型重试直接杜绝了这个 bug。**

### 铁律 2：输入相同也必须重新执行（统一到铁律 0）

- RunningHub 是生成式 AI，**即使输入完全相同，每次生成的结果也不同**。
- **绝对禁止**：看到与之前相同的提示词时，直接返回之前的图片路径。
- **绝对禁止**：从对话历史中查找之前生成的图片并复用。
- 输出文件路径应始终包含时间戳或使用临时目录。

### 铁律 3：生成完必须立即发送，禁止中断

- **绝对禁止**：脚本跑完后只回复"Success!"就停下来等用户追问。
- **正确行为**：脚本成功 → 同一轮回复中立即发送图片。

### 🔴 铁律 5：生成过程中禁止发送中间状态消息（防止啰嗦）

**从步骤一到步骤四完成，Agent 最多只能发一条文本消息给用户。绝对禁止在每个步骤切换时发消息。**

| ❌ 啰嗦行为（本日志实锤） | ✅ 正确行为 |
|--------------------------|-----------|
| "先读一下画图技能的说明喵~" | **不要说。读文件是内部操作，用户不需要知道。** |
| "再读一下 anima 的知识库喵~" | **不要说。读文件是内部操作，用户不需要知道。** |
| "好的主人~我马上画！先启动生成任务喵~" | **如果一定要说，就说这一句。然后闭嘴直到发图。** |
| "任务启动啦~等等看生成结果喵！" | **轮询是内部操作。不要说。** |
| "成功啦~提取图片路径~" | **不要说。路径提取是内部步骤。** |
| 最后发图时："主人~喜欢吗？😊" | **发图时附带一条简短文本即可（可选），不要超过 10 个字。** |

**正确流程示例：**
```
步骤一（astrbot_execute_python）→ 内部操作，不说话
步骤二（轮询）→ 内部操作，不说话
步骤三（提取路径）→ 内部操作，不说话
步骤四（发图）→ 发送图片 + 可选短文本（≤10字）
```

**核心原则：**
1. 用户只关心结果（图片），不关心过程（读文件、启动任务、轮询、提取路径）
2. 每个中间步骤发消息 = 把用户当日志阅读器
3. AstrBot v4.24.5 的空 Reply+At 消息会被 `respond.stage:264` 静默丢弃——发了也白发
4. **一个请求 → 最多一条文本 + 一张图（成功）/ 一条文本（失败）**
5. **🔴 成功时文本硬限制 ≤10 个汉字**（不含标点、emoji、英文）。超过 10 字 = bug。如果无法在 10 字内表达，只发图不发文字。
6. **轮询期间绝对禁止发任何消息**（包括 Reply、At、文本、图片）。轮询 = `astrbot_execute_shell` 之间不夹带任何 `send_message_to_user`。

| ❌ 超长消息（本日志实锤） | 字数 | ✅ 正确 |
|--------------------------|------|--------|
| "成功啦主人~大角大翅膀的龙娘出来了喵~🐉✨" | 18字 | "画好啦主人~" (6字) 或只发图 |
| "搞定啦主人~这次稳稳过审！大角大翅膀大鸡吧的龙娘新鲜出炉喵~🐉🔥" | 25字 | 只发图 |

### 铁律 4：必须润色丰富用户提示词

**用户的原始描述通常过于简短，直接送入 API 效果差。Agent 必须在传给脚本之前进行补充润色。**

润色规则**按工作流区分**：

| 工作流 | 润色规则 |
|--------|---------|
| **anima\*, oldanima\*** | **先行 `Read {SKILL_DIR}/animaKnowledge.md`**，按其规范构造 POSITIVE/NEGATIVE 英文 prompt |
| **zimg\*, xl\*, qwen\*, bqb\*, cf1** | **通用润色**：保留原语言，按下方通用公式联想补充 |
| **改图类** (qwen_edit, old_edit, gpt2, ban2, outfit, realistic, hd, chibi, upscale, angle) | **不润色**，原样传入（见下方「改图模式例外」） |

**通用润色公式（zimg/xl/qwen/bqb/cf1 适用）：**
```
[用户核心主题] + [场景/氛围补充] + [画质/风格词] + [光线/色彩] + [视角/构图]
```

**通用润色原则：**
1. **核心不动**：用户原始意图和主题 100% 保留
2. **联想补充**：场景氛围、光线、构图、细节元素
3. **风格加持**：zimg → `电影级光影，胶片质感`；xl/qwen → `动漫风格，高品质`
4. **原语言输出**：中文输入→中文输出，英文输入→英文输出
5. **克制**：50-150 词，不过长

> **anima\* / oldanima\* 工作流不使用上述通用润色。Agent 必须 `Read {SKILL_DIR}/animaKnowledge.md` 按其规范构造 POSITIVE/NEGATIVE 英文 prompt。**

### ⚠️ 改图模式例外：禁止润色用户提示词

**凡是有输入图片的改图工作流（`qwen_edit`、`old_edit`、`gpt2`、`ban2`、`outfit`、`realistic`、`hd`、`chibi`、`upscale` 等），Agent 不得对用户提示词进行联想扩展。原因：改图指令是精确描述（如"把衣服改成黑色"），润色会引入不相关元素，导致改图效果偏离用户意图。**

| 工作流类型 | 润色规则 |
|-----------|---------|
| 文生图（`anima*`, `oldanima*`, `zimg*`, `xl*`, `qwen*`, `bqb*`, `cf1`） | 铁律4 正常润色 |
| 改图（`qwen_edit`, `old_edit`, `gpt2`, `ban2`, `outfit`, `realistic`, `hd`, `chibi`, `upscale`, `angle`） | **保持原语言，不做任何扩展** |

**改图 prompt 处理规则：**
1. 保持用户原语言，不翻译
2. 原样传入，不做任何扩展
3. 不加风格词、不加画质词、不加光线/氛围描述
4. 示例：用户说"改成黑色衣服" → `-p "改成黑色衣服"`（不是 `-p "change to black clothes"` 也不是 `-p "change to elegant black clothes, high quality..."`）

### 执行前自检清单

在动手发任何图片之前，问自己：

1. 这个图片是**刚刚**执行 `node run.js` 生成的吗？→ 不是 → **必须执行脚本**
2. 我是不是因为看到磁盘上有旧文件就想发？→ 是 → **住手，执行脚本**
3. 用户这次请求和上次很像，我能复用上次结果吗？→ **不能，永远不能**
4. 我拿到 BUSY 消息中的 output_path 了，这是属于当前用户的吗？→ 不确定 → **不发送。等锁释放后重新生成。**
5. 我是不是想说"主人~xxx喵~正在生成..."之类的话？→ 是 → **闭嘴。一个请求最多说一句话。**
6. 任务失败了，我是不是想重试？→ 是 → **绝对禁止重试。直接告诉用户失败。**
7. 我看到系统临时目录里的 `runninghub_gen.lock` 了，是不是想删掉？→ 是 → **绝对不能删。那是别人的任务。**

## 使用方法

### ⛔ 执行方式（铁律：必须同步阻塞，绝对禁止后台）

```bash
# ✅ 正确：同步执行，脚本自己退出后从 stdout 取输出路径
cd {SKILL_DIR}
node run.js anima2 -p "提示词"
# 脚本退出后 stdout 最后一行：
#   Success! Output saved to: <absolute-output-path>
# ← 只从这一行取路径，不去磁盘搜文件

# ❌ 绝对禁止：后台执行（background: true, &, nohup 等）
# 一旦后台执行，脚本还在跑，Agent 就去磁盘搜文件，
# 通配符 99% 会匹配到旧文件 → 发给用户的是旧图
```

### 基本命令格式

```bash
cd {SKILL_DIR}
node run.js <工作流键> [-p "提示词"] [-i 输入图片...] [-o 输出路径] [-k API_KEY]
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `<工作流键>` | 必填，工作流类型（见下方列表） |
| `-p "提示词"` | 图片描述/编辑指令 |
| `-i 图片1 图片2` | 输入图片路径（本地文件），可多个 |
| `-o 输出.png` | 输出图片路径（默认输出到临时目录） |
| `-k API_KEY` | RunningHub API Key（可选，优先使用环境变量） |
| `-l` | 列出所有可用工作流 |

### 完整示例

**文生图示例（anima竖图）——按 {SKILL_DIR}/animaKnowledge.md 构造 prompt：**
```
用户说："画一只在窗台上晒太阳的猫娘"

Agent 先 Read {SKILL_DIR}/animaKnowledge.md，按规范构造 POSITIVE + NEGATIVE 英文 prompt，
然后 -p 传入 POSITIVE 字符串执行：
```
```bash
cd {SKILL_DIR}
node run.js anima2 -p "masterpiece, best quality, highres, newest, year 2024, safe, 1girl, cat girl, original, @fkey, @jima, , cat ears, tail, short hair, brown hair, green eyes, petite, sitting, window sill, looking out, gentle smile, cozy bedroom, sunlight streaming in, warm lighting, soft shadows, depth of field"
```
→ 脚本成功后立即发送输出图片。完整构造规则见 {SKILL_DIR}/animaKnowledge.md。

**图生图示例（动漫转真人）：**
```bash
# 1. 先下载用户图片到本地
cd {SKILL_DIR}
node run.js realistic -i path/to/user_image.jpg
```
→ 脚本成功后立即发送输出图片。

**双图模式示例（服装迁移）：**
```bash
cd {SKILL_DIR}
node run.js outfit -i person.jpg outfit_ref.jpg
```
→ 脚本成功后立即发送输出图片。

**列出工作流：**
```bash
cd {SKILL_DIR}
node run.js -l
```

## 🧠 工作流智能选择（Agent 必读）

**当用户未明确指定工作流时，按以下规则自动匹配：**

| 用户意图 | 默认工作流 | 备选 |
|---------|-----------|------|
| 用户**没有明确工作流要求**（如"随便画一张"、"生成一张图"） | `anima2`（竖图优先） | `anima1`（如需横图） |
| 用户**让画猫**（含猫娘、猫耳、猫咪等） | `anima2`（竖图优先） | `anima1`（如需横图） |
| 用户**涉及编辑图片/改图**（修改、融合、调整已有图片） | `qwen_edit` | `ban2` |
| 用户**要求转真人/真实风格**（真人化、写实、photorealistic） | `realistic` | - |
| 用户**要求高清化** | `hd` | - |
| 用户**要求转q版/三头身** | `chibi` | - |
| 用户**要求服装迁移/换装** | `outfit` | - |
| 用户**明确说旧版改图**（如"用旧版"、"old_edit"） | `old_edit` | - |
| 用户消息包含 **gpt2** | `gpt2` | - |
| 用户明确提到特定工作流名 | 直接使用该工作流 | - |
| 用户消息包含 **oldanima** | `oldanima2`（竖图优先） | `oldanima1`（如需横图） |

> ⚠️ **`oldanima` 是显式触发工作流**：仅当用户消息明确包含 "oldanima" 时才使用。不会作为任何场景的默认或备选。

**动画/二次元风格** 的横竖图选择：优先 `anima2`（竖图 1024×1584），若用户明确要横图则用 `anima1`（1584×1024）。

**纯文生图、无任何特殊要求**：一律 `anima2`。

> **anima\*/oldanima\* 工作流**：选择工作流后，Agent 必须先 `Read {SKILL_DIR}/animaKnowledge.md`，按其中的规范构造 POSITIVE/NEGATIVE 英文 prompt。不得跳过此步骤自行发挥。

## 可用工作流

### 单图模式（需要输入图片 + 可能需提示词）

| 工作流键 | 名称 | 需要 |
|---------|------|------|
| `old_edit` | 旧版改图 | 图 + 文 |
| `realistic` | 动漫转真人 | 图（文可选） |
| `angle` | 角度控制 | 图 + 文 |
| `hd` | 高清化 | 图（文可选） |
| `chibi` | 转q版 | 图（文可选） |
| `upscale` | 放大 | 图 + 文 |
| `qwen_edit` | qwen改图 | 图 + 文 |
| `gpt2` | gpt2改图 | 图 + 文 |

### 双图模式（需要两张输入图片）

| 工作流键 | 名称 | 需要 |
|---------|------|------|
| `outfit` | 服装迁移 | 双图（文可选） |
| `ban2` | ban2 | 图（1-2张）+ 文 |

### 文生图模式（只需提示词，无需图片）

| 工作流键 | 名称 | 分辨率 |
|---------|------|--------|
| `zimg1` | z_image 横图 | 1920×1088 |
| `zimg2` | z_image 竖图 | 1088×1920 |
| `xl1` | 动漫横图 | 1280×900 |
| `xl2` | 动漫竖图 | 900×1280 |
| `anima1` | anima横图 | 1584×1024 |
| `anima2` | anima竖图 | 1024×1584 |
| `oldanima1` | oldanima横图 | 1584×1024 |
| `oldanima2` | oldanima竖图 | 1024×1584 |
| `bqb1` | 表情包1 | - |
| `bqb2` | 表情包2 | - |
| `qwen1` | qwen横图 | 1280×900 |
| `qwen2` | qwen竖图 | 900×1280 |
| `cf1` | 喵喵 | - |

## 超时与重试

- 默认任务超时：6 分钟
- 状态轮询间隔：2 秒
- 输出结果重试：最多 8 次（脚本内部自动处理，Agent 无需干预）
- 脚本会阻塞等待直到任务完成或超时
- **Agent 侧禁止重试**：脚本报错后 Agent 不得重新执行（详见铁律 1）

## 错误处理

常见错误及处理：

| 错误信息 | 原因 | 处理 |
|---------|------|------|
| `API Key is required` | 未设置 RUNNINGHUB_API_KEY | 创建 `{SKILL_DIR}/.env` 添加 Key |
| `Unknown workflow` | 工作流键不存在 | 使用 `node run.js -l` 查看可用列表 |
| `requires at least one image` | 工作流需要图片但未提供 | 使用 `-i` 参数提供图片 |
| `requires two images` | 双图模式需要两张图片 | 提供两张图片路径 |
| `requires a prompt` | 该工作流需要提示词 | 使用 `-p` 参数提供描述 |
| `Task timeout` | 任务超时（>6分钟） | 告知用户超时。**禁止重试（铁律 1）** |
| `Task failed` | 工作流执行失败 | 告知用户失败。**禁止重试（铁律 1）** |

## 多平台使用指引

### 所有平台通用协议（必须遵守）

```
1. cd 到 {SKILL_DIR}
2. 同步执行 node run.js（禁止后台/background: true）
3. 阻塞等待脚本退出（最长 4 分钟）
4. 读取 stdout 最后一行提取输出路径 ← 唯一路径来源
5. 发送该路径的图片文件
6. ❌ 期间禁止用 ls/find/glob 搜索磁盘上的图片文件
```

### Claude Code / OpenCode

```bash
cd {SKILL_DIR}
node run.js anima2 -p "提示词"
# stdout: Success! Output saved to: <absolute-output-path>
# ← 发送 stdout 中的输出路径
```

### AstrBot（四步法：Python 启动 + 轮询 + 读路径 + 发图）

> **🔴 多用户并发警告**：RunningHub 同一时刻只允许一个生成任务运行（系统临时目录中的 `runninghub_gen.lock` 全局锁）。当用户 A 正在生成时，用户 B 的请求会触发 BUSY。**绝对禁止把用户 A 的图发给用户 B**。详见下方「BUSY 路径——情况 B」。
>
> **🔴 锁文件是圣物**：系统临时目录中的 `runninghub_gen.lock` 记录当前占用锁的 PID 和输出路径。**绝对禁止删除锁文件**。删除锁不会解决 BUSY，只会让正在运行的任务失去追踪能力。
>
> **⚠️ AstrBot 消息发送规则**：`send_message_to_user` 的消息链**必须包含至少一条文本或图片内容**。纯 `Reply` + `At` 消息段（无实际文本/图片）会被 AstrBot v4.24.2+ 在 `respond.stage:264` 静默跳过——用户完全收不到。**任何时候发送回复都必须附带实际的文本内容。**
>
> ```python
> # ❌ 错误：纯 Reply + At，无实际内容，会被静默丢弃
> send_message_to_user(messages=[{"type": "reply", ...}, {"type": "at", ...}])
> 
> # ✅ 正确：始终附带文本
> send_message_to_user(messages=[{"type": "text", "text": "图片正在生成中，请稍候~"}])
> ```

> **⚠️ 核心问题**：`astrbot_execute_shell` 会等待整个进程组退出后再返回，
> 即使用了 `nohup ... &` 也不生效（已验证）。`node run.js` 需要 2-6 分钟。
> 因此**必须使用 `astrbot_execute_python` + `subprocess.Popen` 来解耦启动**。

**步骤一：用 Python Popen 后台启动（`astrbot_execute_python`）**

```python
import os, subprocess, tempfile, time

skill_dir = "{SKILL_DIR}"
timestamp = int(time.time())
tmp_dir = tempfile.gettempdir()
output_path = os.path.join(tmp_dir, f"rh_{timestamp}.png")
log_path = os.path.join(tmp_dir, f"rh_gen_{timestamp}.log")  # ← 每次调用唯一日志，防止覆盖

prompt = "<润色后的提示词>"
# ↑ anima* 工作流：传入完整 POSITIVE 字符串（英文，逗号连接）
# ↑ 其他文生图工作流：传入通用润色后的描述
# ↑ 改图工作流：原样传入用户指令

process = subprocess.Popen(
    ["node", "run.js", "<workflow>", "-p", prompt, "-o", output_path],
    cwd=skill_dir,
    stdout=open(log_path, "w"),
    stderr=subprocess.STDOUT,
    stdin=subprocess.DEVNULL
)

print(f"PID={process.pid}")
print(f"LOG={log_path}")
```
> 此工具调用立即返回 PID 和 LOG 路径。Agent **必须记住 `log_path` 的值**，后续所有 shell 命令都用这个路径。
> **`subprocess.Popen` 而非 `subprocess.run`**——后者会阻塞等待，触发同样的超时问题。
>
> **⚠️ 重试保护**：如果 stderr 出现 `BUSY: Another generation is already running`，
> **禁止重试步骤一**。进程锁已生效——直接跳到步骤二开始轮询日志（用 Agent 记忆中的 `log_path`）。
>
> **⚠️ 日志隔离**：每次调用使用唯一 log_path（含时间戳），避免多任务日志互相覆盖导致 Agent 误判任务状态。
>
> **🔴 绝对禁止 `silent: True`**：`astrbot_execute_python` 的参数中不得设置 `silent: True`。该参数会吞掉 stdout 输出，导致 Agent 收不到 `PID=xxx` 和 `LOG=<log_path>`，丢失对生成任务的追踪能力。一旦丢失 PID/LOG，Agent 将无法正确轮询——后续 BUSY 重试时只能匹配到旧日志，**必定发旧图**。

**步骤二：轮询日志等待完成（`astrbot_execute_shell`，每 15 秒，最多 12 次）**

> **用步骤一中 `print(f"LOG={log_path}")` 输出的实际路径替换 `<LOG_PATH>`。**

```bash
sleep 15 && grep -E "Success!|Error:|Task failed|Task timeout" <LOG_PATH> || echo "running..."
```
> 重复直到 grep 命中。
>
> **⚠️ 轮询期间禁止发送消息**：步骤二期间，Agent 不得向用户发送任何消息（包括 Reply、At、文本等）。每次 `astrbot_execute_shell` 调用是纯粹的内部轮询——Agent 与工具之间交互即可，用户无需知晓中间状态。空白 Reply+At 消息链会被 AstrBot `respond.stage:264` 静默丢弃，浪费工具配额且毫无意义。
>
> **🔴 轮询期间的唯一操作就是 `astrbot_execute_shell`。不要夹杂 `send_message_to_user`、不要夹带 Reply、不要做任何其他事。轮询 → 等待结果 → 发图或发失败消息。**

**🔴 轮询命令冻结——不可修改（本日志实锤违规）：**

```bash
# 这是唯一合法的轮询命令，一字不改：
sleep 15 && grep -E "Success!|Error:|Task failed|Task timeout" <LOG_PATH> || echo "running..."
```

| ❌ log6 实锤违规 | ✅ 唯一正确 |
|-----------------|-----------|
| `sleep 30 && cat log` / `sleep 40 && cat log` | `sleep 15 && grep ...` |
| grep 加额外 pattern: `progress\|BUSY\|queued` | 只用 `Success!\|Error:\|Task failed\|Task timeout` |
| `cat <LOG_PATH>` 替代 grep | 永远不用 cat |
| `tail -20 log` 替代 grep | 永远不用 tail |
| 轮询期间换 `cat` 或 `tail` 偷看日志 | **只用 grep，100 次轮询也只用 grep。cat/tail 是改图/查日志的工具，不是轮询工具** |
| 跳过步骤三直接用步骤一的 output_path | 步骤三不可跳过（见下方） |
| grep 到 `running...` 后越等越焦躁改命令 | `running...` = 继续用同一命令，禁止换 |

**如果 grep 命中的是 `Task failed` 或 `Task timeout`：**
> → **立即停止。不执行步骤三、四。禁止再次轮询同一个 log。**
> → 用 `send_message_to_user` 发送文本告知用户失败（**必须包含文本内容**）：
>
> ```python
> send_message_to_user(messages=[{"type": "text", "text": "图片生成失败~换个提示词或者稍后再试试吧~"}])
> ```
>
> **🔴 关键：grep 命中 Error/Task failed/Task timeout 后，对该请求的处理立即结束。**
> - 禁止：再次轮询同一个 log 文件（"running..." 只是 grep 没有命中，不代表任务还在跑）
> - 禁止：换 shell 命令去重新读取日志（如 `cat` / `tail`）
> - 禁止：检查锁文件 / 清理锁文件
> - 禁止：重新执行步骤一（铁律 1）
> - **一次 Error → 一次失败消息 → 结束。**

**如果 grep 命中的是 `Success!`：**
→ 继续步骤三。

**步骤三：从日志提取输出路径（`astrbot_execute_shell`，不可跳过）**

```bash
grep -oP 'Success! Output saved to: \K.*' <LOG_PATH>
```
> 得到路径如系统临时目录中的 `rh_1712345678.png` 绝对路径。
>
> **🔴 步骤三不可跳过。绝对禁止用步骤一中构造的 `output_path` 直接发图（本日志实锤：log6 第 1312 行跳过了步骤三，凭记忆发图）。**
>
> **为什么步骤三不可跳过：**
> 1. 步骤一的 `output_path` 是你传给 `node run.js` 的 **预期** 路径，不是 run.js 实际写入的路径
> 2. 如果 run.js 因 BUSY 或其他原因写了不同路径，步骤一的 output_path 就是错的
> 3. 步骤三从日志中提取的路径是**实际**写入的路径，是唯一权威来源
> 4. 跳过步骤三 = 可能发旧文件（该路径上的文件可能是之前用户留下的）
>
> | ❌ log6 实锤 | ✅ 正确 |
> |-------------|--------|
> | grep 到 Success → 凭记忆用步骤一的 output_path → 发图 | grep 到 Success → 步骤三 grep -oP → 用提取的路径发图 |

**步骤四：立即发送图片（`send_message_to_user`）**

```python
send_message_to_user(messages=[{"type": "image", "path": "步骤三提取的路径"}])
```

**完整流程（成功路径）：**
```
astrbot_execute_python: subprocess.Popen(...) → PID 1780188, LOG=<LOG_PATH>
  ↓ 立即返回（0ms）
astrbot_execute_shell: sleep 15 && grep ... <LOG_PATH> → "running..."
  ↓ (第二次轮询)
astrbot_execute_shell: sleep 15 && grep ... <LOG_PATH> → "Success! Output saved to: <OUTPUT_PATH>"
  ↓
astrbot_execute_shell: grep -oP ... <LOG_PATH> → <OUTPUT_PATH>
  ↓
send_message_to_user → 完成。禁止继续任何操作。
```

**完整流程（失败路径——同样高频出现）：**
```
astrbot_execute_python: subprocess.Popen(...) → PID 1780188, LOG=<LOG_PATH>
  ↓ 立即返回（0ms）
... (多次轮询) ...
astrbot_execute_shell: sleep 15 && grep ... <LOG_PATH> → "Error: Task timeout"
  ↓
send_message_to_user({"type": "text", "text": "图片生成超时~换个提示词或者稍后再试试吧~"})
  ↓ 结束。⚠️ 严禁重试步骤一。
```

**完整流程（BUSY 路径——分三种情况）：**

### 🔴 BUSY 核心规则（多用户安全）

**系统临时目录中的 `runninghub_gen.lock` 是全局锁——同一时刻只允许一个 run.js 进程运行。当多个用户同时请求时，只有第一个用户的进程获得锁，后续请求全部 BUSY。**

**BUSY 消息中的 `Output will be at: /path` 是「当前正运行的任务」的输出路径，不一定属于「当前用户」。绝对禁止跨用户发送图片。**

**锁文件绝对禁止删除——删除锁会废弃正在运行的任务，且无助于解决 BUSY（新进程会创建新锁）。**

**情况 A：当前用户的步骤一重试（Agent 已有自己的 log_path）**
```
astrbot_execute_python → stderr: "BUSY: Another generation is already running (PID: XXXX)"
  ↓ 立即停止。不启动新进程，不去读锁文件。
  ↓ 用之前步骤一获取的 log_path 直接跳到步骤二轮询。
astrbot_execute_shell: sleep 15 && grep ... <已知log_path> → "Success! ..." 或 "Error: ..."
  ↓
(按结果走成功或失败路径)
```

**情况 B：全新用户请求遇到 BUSY（Agent 没有自己的 log_path）**
```
用户 A 请求 → 启动 Popen → 获得 PID_X, LOG_A
用户 B 请求 → 启动 Popen → stderr: "BUSY: ... Output will be at: <用户A的output_path>"
  ↓ ⚠️ 这个 output_path 是用户 A 的，不是用户 B 的！
  ↓ 🔴 绝对禁止把用户 A 的图片发给用户 B！
  ↓
  ✅ 正确做法：
  1. 告诉用户 B："前面有人在生成，稍等一下~"（用 send_message_to_user 发文本）
  2. 等待系统临时目录中的 `runninghub_gen.lock` 消失
  3. 锁释放后（lock 文件消失），重新执行步骤一为用户 B 启动生成
  4. 按正常流程完成
```

**情况 C：Agent 丢失了 log_path（silent: True 或调用失败）**
```
astrbot_execute_python: 无有效输出（PID/LOG 丢失）
  ↓
1. 读取系统临时目录中的 `runninghub_gen.lock` → 第一行 PID，第二行 output_path
2. 检查 output_path 的文件修改时间是否在最近 5 分钟内
3. 如果文件新鲜且是当前用户的请求 → 用该 output_path 轮询
4. 如果不确定是否属于当前用户 → 不要发，告诉用户"上一任务已完成，请重新发送请求"
5. 如果文件陈旧（>5分钟）→ 告知用户"上一任务已完成，请重新发送请求"
```

> **⚠️ 绝对禁止**：
> - BUSY 时去 grep 硬编码日志路径（如旧版 `/tmp/rh_gen.log`）——可能包含数天前的旧 Success
> - **删除锁文件**——会废弃正在运行的任务
> - **把 BUSY 消息中的 output_path 直接发给另一个用户**——那是别人的图
> - 只信任 Agent 已知的 log_path 或经过校验的锁文件 output_path
