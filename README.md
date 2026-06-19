# pleia-skills

个人日常使用的 Agent Skills，让 AI Agent 能更好地完成特定任务。每个 skill 都是自包含的指令集 + 脚本，放到对应平台的 skills 目录下即可生效。

---

## Skills

| Skill | 说明 | 运行方式 |
|-------|------|----------|
| 🔍 **mimo-web-search** | 基于小米 MiMo 开放平台的联网搜索，支持中文网页、实时信息、引用溯源 | Python |
| 🎨 **runninghub-image-gen** | 通过 RunningHub API 调用 AI 图像生成/编辑工作流，支持文生图、图生图、改图等 | Node.js |
| ✍️ **cn-polish** | 中文润色、英译中、UI 字符串本地化，支持 OpenAI / Gemini / Anthropic 多种 LLM | Python |
| 🖼️ **step-image** | 调用阶跃星辰 StepFun API 文生图与图像编辑，基于 step-image-edit-2 模型 | Node.js |
| 👁️ **vision-assist** | MCP 视觉助手，分析图像并回答视觉问题，支持 MCP 协议与纯脚本两种模式 | Python + Node |

---

## 安装

### 🤖 给 Agent 看

> 把下面这段 **直接粘贴给你的 AI Agent**，它会自己完成安装和配置。

````text
请帮我安装以下 Agent Skills，将它们克隆并复制到当前平台的 skills 目录：

仓库地址：https://github.com/cannebergeee/pleia-skills

需要安装的 skills：
- mimo-web-search-skills → 需要配置 MIMO_API_KEY 环境变量
- runninghub-image-gen → 需要复制 .env.example 为 .env，填入 RUNNINGHUB_API_KEY
- cn-polish → 需要复制 scripts/config.example.json 为 scripts/config.json，填入 API Key
- step-image → 需要在 step-image 目录下创建 .env 文件，填入 STEP_IMAGE_API_KEY
- vision-assist → 需要复制 scripts/config.example.json 为 scripts/config.json，填入 API Key；MCP 版本需要按客户端注册 MCP 服务

安装步骤：
1. git clone 仓库到本地临时目录
2. 检测当前平台（Claude Code / Codex / OpenCode 等），找到对应的 skills 路径
3. 将各 skill 目录复制过去
4. 检查各 skill 的配置文件 / 环境变量，缺失则提醒我配置
5. 完成后告诉我安装结果
````

### 👤 给人类看

```bash
git clone https://github.com/cannebergeee/pleia-skills.git
cd pleia-skills

# 安装到各平台
# Claude Code
cp -r mimo-web-search-skills ~/.claude/skills/
cp -r runninghub-image-gen ~/.claude/skills/
cp -r cn-polish ~/.claude/skills/
cp -r step-image ~/.claude/skills/
cp -r vision-assist ~/.claude/skills/

# Codex
cp -r mimo-web-search-skills ~/.codex/skills/
cp -r runninghub-image-gen ~/.codex/skills/
cp -r cn-polish ~/.codex/skills/
cp -r step-image ~/.codex/skills/
cp -r vision-assist ~/.codex/skills/

# 配置 API Key
cp runninghub-image-gen/.env.example runninghub-image-gen/.env  # 编辑填入 RUNNINGHUB_API_KEY
cp cn-polish/scripts/config.example.json cn-polish/scripts/config.json  # 编辑填入 LLM API Key
export MIMO_API_KEY="your-mimo-api-key"
```

---

## 🔍 mimo-web-search

> 调用小米 MiMo `web_search`，获取带引用的实时网络搜索结果。特别适合中文语境下的信息检索。

**适合的场景：**
- 实时新闻、政策更新、市场价格
- 产品可用性、天气、活动信息
- 中文互联网信息查询
- 用户明确要求"搜索一下""查一下"的场景

**快速开始：**

```bash
export MIMO_API_KEY="your-api-key"
python mimo-web-search-skills/scripts/mimo_web_search.py "今天北京天气"
```

**依赖：** Python 3.8+、`MIMO_API_KEY` 环境变量（从小米 MiMo 开放平台获取）

参考 [SKILL.md](mimo-web-search-skills/SKILL.md) 查看完整用法。

---

## 🎨 runninghub-image-gen

> 通过 RunningHub API 调用多种 AI 图像生成与编辑工作流，支持文生图、图生图、改图、风格迁移等。

**支持的工作流：**

| 类型 | 工作流 |
|------|--------|
| 文生图 | `anima1/2`、`oldanima1/2`、`zimg1/2`、`xl1/2`、`qwen1/2`、`bqb1/2`、`cf1` |
| 图生图 | `realistic`（动漫转真人）、`hd`（高清化）、`chibi`（转Q版）、`angle`（角度控制）、`upscale`（放大） |
| 改图 | `qwen_edit`、`old_edit`、`gpt2`、`ban2` |
| 双图 | `outfit`（服装迁移） |

**快速开始：**

```bash
cp runninghub-image-gen/.env.example runninghub-image-gen/.env
# 编辑 .env 填入 RUNNINGHUB_API_KEY
node runninghub-image-gen/run.js anima2 -p "a cat sitting on a windowsill, warm sunlight"
```

**依赖：** Node.js >= 21、RunningHub API Key（从 [runninghub.cn](https://www.runninghub.cn) 获取）

参考 [SKILL.md](runninghub-image-gen/SKILL.md) 查看完整工作流列表。

---

## ✍️ cn-polish

> 中文润色、英译中、UI 字符串本地化。支持 OpenAI 兼容接口、Gemini、Anthropic 等多种 LLM 后端。

**支持的模式：**

| 模式 | 说明 |
|------|------|
| `polish` | 润色中文文本，优化表达流畅度和地道程度 |
| `translate` | 将英文翻译成自然的中文 |
| `localize` | 本地化 `key=value` 格式的 UI 字符串，保持键不变 |

**快速开始：**

```bash
cp cn-polish/scripts/config.example.json cn-polish/scripts/config.json
# 编辑 config.json 填入 API Key 和模型配置

python cn-polish/scripts/cn_polish.py polish -t "需要润色的中文文本"
python cn-polish/scripts/cn_polish.py translate -t "English text to translate"
python cn-polish/scripts/cn_polish.py localize -t "save=Save"
```

**依赖：** Python 3.8+、配置文件 `scripts/config.json`（填入 LLM API Key）

参考 [SKILL.md](cn-polish/SKILL.md) 查看完整用法和参数说明。

---

## 🖼️ step-image

> 通过阶跃星辰 StepFun API 调用 `step-image-edit-2` 模型，支持文生图与图像编辑。基于 Node.js，无外部依赖。

**支持的操作：**

| 操作 | 说明 |
|------|------|
| `generate` | 文生图，从文本描述生成图像 |
| `edit` | 图像编辑，基于输入图像 + 文本指令修改 |

**快速开始：**

```bash
# 首次使用需在 step-image/ 下创建 .env，填入 STEP_IMAGE_API_KEY
node step-image/run.js generate -p "一只坐在窗台上的猫，温暖的阳光"
node step-image/run.js edit -i input.png -p "把猫换成狗"
```

**依赖：** Node.js 18+

参考 [SKILL.md](step-image/SKILL.md) 查看完整用法和参数说明。

---

## 👁️ vision-assist

> 分析图像并回答视觉问题。提供 MCP 协议版和纯脚本版两种使用方式。

**两种版本：**

| 版本 | 使用方式 | 适用场景 |
|------|----------|----------|
| **MCP 版** | 注册 MCP 服务，Agent 自动调用 | 支持 MCP 的客户端（Claude Code、Codex、OpenCode 等） |
| **纯脚本版** (`pure-skill/`) | 直接执行 Python 脚本 | MCP 不可用的环境 |

**快速开始（纯脚本版）：**

```bash
cp vision-assist/pure-skill/scripts/config.example.json vision-assist/pure-skill/scripts/config.json
# 编辑 config.json 填入 API Key

cd vision-assist/pure-skill
python scripts/vision_assist.py analyze -i /path/to/image.jpg -p "描述这张图片"
```

**MCP 版注册（以 OpenCode / VS Code 为例）：**

```json
{
  "mcpServers": {
    "vision-assist": {
      "command": "node",
      "args": ["path/to/vision-assist/mcp/run.mjs"]
    }
  }
}
```

**依赖：** Python 3.8+、Node.js 18+、配置文件（填入视觉模型 API Key）

参考 [SKILL.md](vision-assist/SKILL.md) 查看完整用法和 MCP 配置说明。

---

## License

MIT
