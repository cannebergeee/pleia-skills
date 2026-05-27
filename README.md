# pleia-skills

个人日常使用的 Agent Skills，让 AI Agent 能更好地完成特定任务。每个 skill 都是自包含的指令集 + 脚本，放到对应平台的 skills 目录下即可生效。

---

## Skills

| Skill | 说明 |
|---|---|
| 🔍 **mimo-web-search** | 基于小米 MiMo 开放平台的联网搜索，支持中文网页、实时信息、引用溯源 |
| 🎨 **runninghub-image-gen** | 通过 RunningHub API 调用 AI 图像生成/编辑工作流，支持文生图、图生图、改图等 |

---

## 安装

### 🤖 给 Agent 看

> 把下面这段 **直接粘贴给你的 AI Agent**，它会自己完成安装和配置。

````text
请帮我安装以下 Agent Skills，将它们克隆并复制到当前平台的 skills 目录：

仓库地址：https://github.com/pleia-zone/pleia-skills

需要安装的 skills：
- mimo-web-search-skills → 需要配置 MIMO_API_KEY 环境变量
- runninghub-image-gen → 需要复制 .env.example 为 .env，填入 RUNNINGHUB_API_KEY

安装步骤：
1. git clone 仓库到本地临时目录
2. 检测当前平台（Claude Code / Codex / OpenCode 等），找到对应的 skills 路径
3. 将两个 skill 目录复制过去
4. 检查是否已有对应的 API Key 环境变量，没有则提醒我配置
5. 完成后告诉我安装结果
````

### 👤 给人类看

```bash
git clone https://github.com/pleia-zone/pleia-skills.git
cd pleia-skills

# Claude Code
cp -r mimo-web-search-skills ~/.claude/skills/
cp -r runninghub-image-gen ~/.claude/skills/

# Codex
cp -r mimo-web-search-skills ~/.codex/skills/
cp -r runninghub-image-gen ~/.codex/skills/

# 配置 API Key
cp runninghub-image-gen/.env.example runninghub-image-gen/.env
# 编辑 .env 填入 RUNNINGHUB_API_KEY
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

**不适合的场景：**

- 本地代码分析、文件操作
- 无需验证的稳定常识
- 需要登录的私密数据

**快速开始：**

```bash
export MIMO_API_KEY="your-api-key"
python mimo-web-search-skills/scripts/mimo_web_search.py "今天北京天气"
```

**依赖：**

- Python 3.8+
- `MIMO_API_KEY` 环境变量（从小米 MiMo 开放平台获取）

参考 [SKILL.md](mimo-web-search-skills/SKILL.md) 查看完整用法和参数说明。

---

## 🎨 runninghub-image-gen

> 通过 RunningHub API 调用多种 AI 图像生成与编辑工作流，支持文生图、图生图、改图、风格迁移等。

**支持的工作流：**

| 类型 | 工作流 |
|---|---|
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

**依赖：**

- Node.js >= 21
- RunningHub API Key（从 [runninghub.cn](https://www.runninghub.cn) 获取）

参考 [SKILL.md](runninghub-image-gen/SKILL.md) 查看完整的工作流列表和参数说明。

---

## License

MIT
