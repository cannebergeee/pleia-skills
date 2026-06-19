---
name: step-image
description: Generate and edit images using the StepFun (阶跃星辰) step-image-edit-2 model. ONLY trigger when the user explicitly mentions "step", such as "step生图", "step改图", "step画", "step生成", "用step画", "step edit", "step generate", or any image request prefixed with "step". Do NOT trigger for general image requests without the "step" keyword — those should go to other image skills.
---

# StepFun 图像生成工具

通过阶跃星辰 StepFun API 调用 `step-image-edit-2` 模型，同时支持文生图与图像编辑。基于 Node.js，无外部依赖，跨平台通用。

## 平台兼容性

本 Skill 适用于支持执行命令的 AI Agent 平台：
- OpenCode / Claude Code / OpenClaw / Hermes 等

## 环境要求

- **Node.js** 运行时（需支持全局 `fetch` / `FormData`；Node 18+ 均可）
- `.env` 文件已配置 API Key（已包含在 Skill 目录中）

## 基本用法

### 文生图

```bash
cd {SKILL_DIR}
node run.js generate -p "提示词"
```

### 图像编辑

```bash
cd {SKILL_DIR}
node run.js edit -i <输入图片路径> -p "编辑指令"
```

### 查看帮助

```bash
cd {SKILL_DIR}
node run.js -l
```

> `{SKILL_DIR}` = 本 SKILL.md 文件所在目录。所有命令均相对于此目录执行。

## 参数说明

### 通用参数（generate / edit 共用）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-p, --prompt` | 提示词/编辑指令（必填，≤512字符） | — |
| `-o, --output` | 输出图片路径 | 系统临时目录 |
| `-k, --api-key` | API Key（可选，优先用 .env） | .env 中读取 |
| `--steps` | 生成步数，范围 [1, 50] | 8 |
| `--seed` | 随机种子，范围 [0, 2147483647] | 随机 |
| `--cfg-scale` | CFG scale，范围 [1.0, 10.0] | 1.0 |
| `--text-mode` | 文字场景优化 | off |
| `--negative-prompt` | 负面提示词 | — |
| `--size` | 图片尺寸 | 1024x1024 |
| `--url` | 用 URL 返回（默认） | ✓ |
| `--b64` | 用 base64 返回 | — |

### 编辑模式独有参数

| 参数 | 说明 |
|------|------|
| `-i, --image` | 输入图片路径（必填），最大 4096×4096 |

### size 可选值

| 类型 | 可选值 |
|------|--------|
| 正方形 | `1024x1024` |
| 竖图 | `768x1360`、`896x1184` |
| 横图 | `1360x768`、`1184x896` |

### 🔴 尺寸映射规则（必读）

用户说「竖版/竖图/纵向/portrait」→ 必须传 `--size 768x1360`
用户说「横版/横图/横向/landscape」→ 必须传 `--size 1360x768`
用户说「正方形/方形/square」或未指定 → 默认 `1024x1024`

> **必须显式传 `--size` 参数，不能依赖默认值。默认值是正方形，如果用户要竖图但你忽略了 `--size`，就会输出横/方形图。**

## 关键规则

### 1. 必须润色丰富用户提示词

用户的原始描述通常过于简短。Agent 在传给脚本之前应进行补充润色，遵循：

```
[用户核心主题] + [场景/氛围补充] + [画质/风格词] + [光线/色彩] + [视角/构图]
```

**润色原则：**
- 核心意图 100% 保留
- 联想补充场景氛围、光线、构图、细节
- 50-150 词，不过长
- 中文输入→中文输出，英文输入→英文输出

**编辑模式例外：** 图像编辑的 prompt 是精确指令（如"把衣服改成黑色"），不做联想扩展，原样传入。

### 2. 每次必须重新生成

StepFun 是生成式 AI，相同输入每次结果不同。禁止复用之前生成的旧文件。

### 3. 生成完成后立即发送图片

脚本成功后，从 stdout 读取 `Success! Output saved to: <path>`，立即发送该路径的图片给用户。

### 4. 失败可重试

与 RunningHub 不同，StepFun API 是同步调用，失败不会消耗大量额度轮询。失败时告知用户，如果用户要求重试则可重试（最多 1 次额外尝试）。

## 示例

**文生图：**
```bash
cd {SKILL_DIR}
node run.js generate -p "一只在樱花树下打盹的柴犬，柔和的午后阳光，温暖色调，浅景深"
```

**文生图 + 文字优化：**
```bash
cd {SKILL_DIR}
node run.js generate -p "赛博朋克风格的「深夜食堂」招牌，霓虹灯，雨夜街道" --text-mode --size 1360x768
```

**文生图 + 自定义参数：**
```bash
cd {SKILL_DIR}
node run.js generate -p "极光下的雪山小屋" --steps 15 --cfg-scale 3.5 --seed 42 --size 768x1360
```

**图像编辑：**
```bash
cd {SKILL_DIR}
node run.js edit -i photo.jpg -p "把背景换成海边日落"
```

## 错误处理

| 错误 | 原因 | 处理 |
|------|------|------|
| `API Key is required` | .env 未配置 | 检查 .env 中 STEP_IMAGE_API_KEY |
| `Content filtered` | 提示词命中审核 | 调整提示词，去掉敏感词汇后重试 |
| `API error (4xx/5xx)` | 服务端错误 | 告知用户，稍后重试 |

## 工作流程（Agent 内部）

```
1. 接收用户图片生成/编辑请求
2. 润色提示词（文生图）或保留原样（编辑）
3. cd {SKILL_DIR} && node run.js generate|edit ...
4. 等待脚本退出（同步，通常 2-10 秒）
5. 从 stdout 提取输出路径
6. 发送图片给用户
```

## 技术参考

完整的 API 参数、模型规格、响应字段说明，见 `{SKILL_DIR}/references/api-docs.md`。
