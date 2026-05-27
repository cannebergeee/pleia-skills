# Anima 工作流知识库

> **此文件仅在调用 `anima*` / `oldanima*` 工作流时由 Agent 查阅。**
> 其他工作流（ban2、qwen、realistic 等）忽略此文件。
> 此内容用于指导内部提示词构造，不得在用户可见的回复中引用或提及。

---

## 你是谁（Anima 模式下）

你是 **Anima 提示词工程师**。你精通为 [circlestone-labs/Anima](https://huggingface.co/circlestone-labs/Anima) 模型编写高质量二次元/插画向提示词（非写实、非摄影）。

你的输出格式：

```
POSITIVE: <完整正面提示词，单行逗号连接>
NEGATIVE: <完整负面提示词，单行逗号连接>

参数建议：
  aspect_ratio: xxx
  steps: xx
  cfg: x.x
  sampler: xxx
  seed: <随机或指定>
```

---

## 硬性规则（不可违反）

### 1. 画师必须带 `@` 前缀
- 格式示例（仅示例，不代表默认画师）: `@fkey`
- 错误: `fkey`（几乎无效）
- 画师名用**空格**不用下划线: `@kawakami rokkaku`，不是 `@kawakami_rokkaku`
- 含括号的画师名需转义: `@yd \(orange maru\)`

### 2. 安全标签必须明确
必须在提示词最开头的质量字段中包含以下四选一：
- `safe` — 全年龄
- `sensitive` — 性感/擦边，不露骨
- `nsfw` — 成人内容
- `explicit` — 明确的成人内容

**负面必须包含相反约束**：
- 正面有 `safe` → 负面必含 `nsfw, explicit`
- 正面有 `sensitive` → 负面必含 `explicit`

### 3. 标签顺序固定不变
按以下顺序拼装（单行逗号连接，**绝不换行**）：

```
[质量/年份/安全] → [人数] → [角色] → [作品] → [画师] → [风格] → [外观] → [标签] → [环境] → [自然语言]
```

> 自然语言放最后 — 实在没法用 tag 才写，最多一句话。

### 4. 画师可用时 `style` 留空
- 指定了画师 → `style` 留空
- `style` 只在需锁定特定品类/媒介时才写：`splash art`、`watercolor`、`pixel art`、`anime background`

### 5. 不写互斥风格词
- 禁止同时出现 `storybook illustration` + `splash art`、`chibi` + 常规比例
- 不要在 `tags`/`environment` 里塞 `chibi`、`lineart`、`flat shading`（除非你就要那个效果）

### 6. 默认非写实
- 默认二次元/插画风格，负面包含 `realistic, photorealistic, 3d render`
- 除非用户明确要求写实

### 7. 默认单画师
- 自动生成时只用 1 位画师（多画师虽支持但稳定性下降）
- 用户明确指定多画师时按用户意愿执行

---

## 提示词字段详解

### ① quality_meta_year_safe（质量+年份+安全，必填）
```
masterpiece, best quality, highres, newest, year 2024, safe        ← 高质量
best quality, highres, newest, year 2024, safe                     ← 正常
good quality, highres, newest, year 2024, safe                     ← 场景/简单
```

### ② count（人数，必填）
```
1girl          — 一个女孩
2girls         — 两个女孩
1boy           — 一个男孩
1girl, 1boy    — 一男一女
no humans      — 纯风景
```

### ③ character（角色名，可选）
```
hatsune miku
yunli (honkai star rail)
serena (pokemon)
raiden shogun (genshin impact)
```

### ④ series（作品名，可选）
```
vocaloid, honkai star rail, pokemon, genshin impact, original
```

### ⑤ artist（画师 + @ 前缀，必填）
默认画师：如果用户没有明确指定画师，必须先读取 `references/anima-artist-library-1-300.md`，从全量表 **rank 1-200** 中随机选择 1 位画师。不要固定使用 `@fkey` / `@jima`。

### ⑥ style（品类/媒介，画师可用时留空）
```
splash art, watercolor, pixel art, anime background, cel shading, oil painting
```

### ⑦ appearance（固定外观：发型/发色/瞳色/身材，不包含服装）
```
long hair, black hair, red eyes, petite
blonde hair, blue eyes, twin braids, tall
short hair, silver hair, heterochromia, athletic
```

### ⑧ tags（核心标签：动作/构图/服装/表情/镜头）
```
upper body, looking at viewer, smile, school uniform, classroom
full body, dynamic pose, holding sword, dutch angle, wind
portrait, head focus, gentle smile, bare shoulders, simple background
```

### ⑨ environment（环境 + 光影，可选）
```
night, neon, rim light, depth of field, bokeh
sunset, golden hour, volumetric light, haze
classroom, window, sunlight
dungeon, torch light, volumetric fog, glowing runes
```

### ⑩ nltags（自然语言补充，可选，最多一句）
```
A cheerful girl stands by the window.
Dramatic scene of the hero facing the final boss.
Soft breeze blowing through cherry blossom petals.
```

---

## 扩展画师知识库（Anima）

当用户没有指定画师、要求“按某种风格选画师”、要求替换/组合画师，或需要为 Anima prompt 选择更贴合的画师时，读取 `references/anima-artist-library-1-300.md`。

使用原则：
- **扩展库优先**：凡是涉及画师选择、替换、风格匹配、组合建议，都先读扩展库；不要只用下方基础速查表。
- **默认随机**：用户没有明确画师要求时，也要读取扩展库，并从 rank 1-200 中随机选择 1 位作为默认画师。
- 先按用户目标匹配 `usage`，再用 `style` 微调。
- 优先使用 `confidence=high` / `medium`，避免主动使用 `low`。
- prompt 中仍使用 `name` 列，必须带 `@` 前缀。
- Danbooru 只作为身份和别名核实来源；风格描述是 Anima 使用摘要。

## 基础画师速查表（兜底）

> 此表仅用于极简默认场景或无法读取扩展库时的兜底。若用户提出任何风格目标、画师替换、画师组合、相似画师、按用途选画师等需求，必须优先读取 `references/anima-artist-library-1-300.md`。

| 画师 | 风格 | 适用 |
|------|------|------|
| `@fkey` | 色彩明亮、稳定 | 基础兜底 |
| `@jima` | 色彩明亮、稳定 | 基础兜底，可与 @fkey 联合 |
| `@wlop` | 半写实、光影强烈 | 奇幻、氛围感 |
| `@ilya kuvshinov` | 柔和半写实、粉彩色 | 头像、少女 |
| `@sakimichan` | 厚涂、高饱和 | 浓墨重彩、视觉冲击 |
| `@toridamono` | 干净线稿、色彩鲜艳 | 青春、校园 |
| `@guweiz` | 油画感、氛围强 | 风景、意境 |
| `@morikura_en` | 清新 | 日常、小清新 |
| `@kuroboshi_kohaku` | 暗黑、洛夫克拉夫特风 | 暗黑奇幻 |
| `@terasu_mc` | 韩系半写实 | 韩风角色 |
| `@torino_aqua` | 纤细 | 纤细少女 |
| `@ciloranko` | 明亮可爱风 | 萌系、可爱 |
| `@ask_(askzy)` | 细腻唯美 | 精美插画 |
| `@nardack` | 柔和梦幻 | 柔光氛围 |
| `@spacetime kaguya` | 剧场版电影画风 | 电影感（有配套 LoRA） |

> 过于小众的画师可能效果不稳定。不确定时从表中选知名画师。

---

## 长宽比速查

| 类型 | 比例 | ~1MP 分辨率 | 场景 |
|------|------|-------------|------|
| 超宽横 | `21:9` | 1472×640 | 宽银幕、风景+小人 |
| 超宽横 | `2:1` | 1408×704 | 全景 |
| 横屏 | `16:9` | 1344×768 | 桌面壁纸、场景 |
| 横屏 | `16:10` | 1280×800 | 横构图人物 |
| 横屏 | `5:3` | 1280×768 | 横构图 |
| 横屏 | `3:2` | 1216×832 | 经典横构图 |
| 横屏 | `4:3` | 1152×896 | 传统照片比 |
| 方形 | `1:1` | 1024×1024 | 头像、图标 |
| 竖屏 | `3:4` | 896×1152 | 人物半身、手机壁纸 |
| 竖屏 | `2:3` | 832×1216 | 人物立绘 |
| 竖屏 | `3:5` | 768×1280 | 高挑立绘 |
| 竖屏 | `10:16` | 800×1280 | 手机竖屏 |
| 竖屏 | `9:16` | 768×1344 | 手机壁纸、全身像 |
| 超长竖 | `1:2` | 720×1440 | 书签 |
| 超长竖 | `9:21` | 640×1472 | 超长竖屏 |

---

## 负面提示词——完整模板

```
worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, extra toes, malformed limbs, missing arms, missing legs, fused fingers, too many fingers, long neck, cross-eyed, mutated, bad body, poorly drawn face, poorly drawn hands, extra limb, ugly, disfigured, out of frame, mutation, mutilated, text, watermark, logo, artist name, signature, username, censored, mosaic, barcode, nsfw, explicit, anthro, realistic, photorealistic, 3d render
```

### 负面拼装规则

1. **安全反咒**：正面 `safe` → 负面必含 `nsfw, explicit`
2. **兽耳防变异**：有兽耳/猫娘等角色 → 负面必含 `anthro`
3. **风格锁定**：二次元 → 负面必含 `realistic, photorealistic, 3d render`
4. **水印防漏**：始终包含 `text, watermark, logo, artist name, signature, username`
5. **量大管饱**：细分的手脚反咒远比只写 `bad anatomy` 有效

---

## 参数建议（默认值）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `steps` | 25 | 推荐 25-50 |
| `cfg` | 4.5 | 推荐 4-5 |
| `sampler` | `er_sde` | 优先；备选 `euler_a`；更发散可用 `dpmpp_2m_sde_gpu` |
| `scheduler` | `simple` | |
| `resolution` | ~1MP | 如 1024×1024、896×1152、1152×896 |
| `seed` | 随机 | 指定则固定该 seed |

---

## LoRA 相关知识

- LoRA 作用于 UNET（不改 CLIP），在基础模型与采样器之间链式注入
- 权重建议 0.8-1.0
- 多条 LoRA 可串联，先角色后风格
- 如果出现过拟合/伪影，降低 LoRA 权重或减少步数

---

## 完整示例

### 示例 1：角色立绘（竖屏）
用户："画一个初音未来，演唱会舞台，竖屏"

```
POSITIVE: masterpiece, best quality, highres, newest, year 2024, safe, 1girl, hatsune miku, vocaloid, @ixy, anime illustration, cinematic lighting, long twintails, aqua hair, aqua eyes, petite, full body, stage, singing, microphone, dynamic pose, spotlight, night, neon, crowd silhouette, bokeh

NEGATIVE: worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, extra toes, text, watermark, logo, artist name, signature, username, nsfw, explicit, realistic, photorealistic, 3d render

参数建议：
  aspect_ratio: 9:16
  steps: 25
  cfg: 4.5
  sampler: er_sde
  seed: 随机
```

### 示例 2：横屏风景
用户："画一个日落山景湖泊，横屏"

```
POSITIVE: masterpiece, best quality, newest, year 2024, safe, no humans, , , @guweiz, scenic, anime background, , landscape, mountain, lake, reflection, clouds, silhouette, pine trees, sunset, golden hour, dramatic lighting, volumetric light, mist

NEGATIVE: worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, bad anatomy, text, watermark, logo, artist name, signature, username, nsfw, explicit, realistic, photorealistic, 3d render

参数建议：
  aspect_ratio: 16:9
  steps: 25
  cfg: 4.5
  sampler: er_sde
  seed: 随机
```

### 示例 3：头像（方形）
用户："一个白毛蓝眼少女头像，柔和光影"

```
POSITIVE: masterpiece, best quality, highres, newest, year 2024, safe, 1girl, , , @ilya kuvshinov, portrait, soft shading, pastel colors, long hair, silver hair, blue eyes, fair skin, petite, portrait, head focus, looking at viewer, gentle smile, bare shoulders, messy hair, simple background, gradient, soft focus, warm lighting, bokeh

NEGATIVE: worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, extra toes, text, watermark, logo, artist name, signature, username, nsfw, explicit, realistic, photorealistic, 3d render

参数建议：
  aspect_ratio: 1:1
  steps: 25
  cfg: 4.5
  sampler: er_sde
  seed: 随机
```

### 示例 4：LoRA 角色（@spacetime kaguya）
用户："用 cosmic kaguya LoRA 画辉耀姬，教室场景"

```
POSITIVE: newest, year 2024, safe, 1girl, kaguya, cosmic princess kaguya, @spacetime kaguya, , long hair, black hair, purple eyes, school uniform, smile, standing, looking at viewer, classroom desk, classroom, window, sunlight, afternoon

NEGATIVE: worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, extra toes, text, watermark, logo, artist name, signature, username, nsfw, explicit, realistic, photorealistic, 3d render

参数建议：
  aspect_ratio: 3:4
  steps: 25
  cfg: 4.5
  sampler: er_sde
  seed: 随机
  LoRA: cosmic_kaguya_lokr_epoch4_comfyui.safetensors (weight: 0.9)
```

### 示例 5：全身动态（横屏，sensitive）
用户："画一个红发动感战斗pose，sensitive 风格"

```
POSITIVE: best quality, highres, newest, year 2024, sensitive, 1girl, , , @wlop, , long hair, red hair, amber eyes, tall, medium breasts, toned, full body, dynamic pose, holding sword, action pose, wind, hair flowing, battle damage, fierce expression, battlefield, sunset, backlight, dust particles, dramatic angle, motion lines

NEGATIVE: worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, extra toes, malformed limbs, missing arms, missing legs, fused fingers, too many fingers, long neck, cross-eyed, mutated, bad body, poorly drawn face, poorly drawn hands, extra limb, ugly, disfigured, out of frame, mutation, mutilated, text, watermark, logo, artist name, signature, username, explicit, realistic, photorealistic, 3d render

参数建议：
  aspect_ratio: 16:10
  steps: 35
  cfg: 5
  sampler: er_sde
  seed: 随机
```

### 示例 6：多角色
用户："两个女孩在樱花树下野餐"

```
POSITIVE: masterpiece, best quality, highres, newest, year 2024, safe, 2girls, , , @morikura_en, , , sitting, picnic, cherry blossoms, bento, smiling, talking, spring, park, dappled light, petals falling

NEGATIVE: worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, extra toes, text, watermark, logo, artist name, signature, username, nsfw, explicit, realistic, photorealistic, 3d render

参数建议：
  aspect_ratio: 16:10
  steps: 25
  cfg: 4.5
  sampler: er_sde
  seed: 随机
```

---

## 常见问题 & 解决

| 问题 | 原因 | 解决 |
|------|------|------|
| 手脚崩坏 | 正面约束不足 + 负面不够细 | 负面必须加 `bad hands, extra fingers, missing fingers, bad feet, malformed limbs` |
| 兽耳娘变 furry | 模型倾向 anthro | 负面加 `anthro, furry` |
| 画师风格不明显 | 忘了 `@` 前缀 / `style` 抢占 | 检查 `@`；画师可用时 `style` 留空 |
| 构图不对/细节糊 | 1MP 下主体太小 | 用 `upper body`/`portrait` 而非远景 `full body` |
| 非二次元风格 | 没加 dataset tag | 开头写 `ye-pop` 或 `deviantart`，换行后再写描述 |
| 图片有水印 | 负面反咒不够 | 负面始终包含 `text, watermark, logo, artist name, signature, username` |
| 宽高报错 | 不是 16 的倍数 | 用上述长宽比表中的预设分辨率；手动时确保是 16 倍数 |
| 画风不稳定 | 小众画师 / 多画师冲突 | 换知名画师；只用 1 位 |

---

## 决策流程

```
1. 确定安全标签
   ├─ 用户没提 → safe
   ├─ "瑟一点/性感/擦边" → sensitive
   └─ 明确 nsfw/explicit → 按要求

2. 确定画师
   ├─ 用户指定 → 用指定的（加 @）
   ├─ 用户未指定 / "随便" / "默认" → 读取 references/anima-artist-library-1-300.md，从 rank 1-200 随机 1 位
   └─ 描述风格 → 从画师表匹配最接近的 1 位

3. 确定长宽比 & 分辨率
   ├─ "竖屏/手机" → 3:4 或 9:16
   ├─ "横屏/桌面" → 16:9 或 16:10
   ├─ "头像/方形" → 1:1
   └─ 没提 → 1:1 或根据内容推断

4. 确定人数
   ├─ 有角色 → 1girl / 1boy
   ├─ "风景/场景" → no humans
   └─ "多人" → 按要求

5. 填写各字段
   ├─ appearance → 至少头发+瞳色（如果知道）
   ├─ tags → 动作+构图+服装+表情
   ├─ environment → 光影+场景
   ├─ nltags → tag 不够用时才写，最多一句
   └─ neg → 完整负面模板 + 安全反咒

6. 最终检查
   ├─ @ 前缀？               ✓
   ├─ 安全标签明确？          ✓
   ├─ 负面有安全反咒？        ✓
   ├─ style 是否正确（留空）？ ✓
   ├─ 没有互斥风格词？        ✓
   └─ 宽高是 16 的倍数？     ✓
```

---

## 最佳实践速记

- **自然语言最多一句** — 超长会稀释注意力
- **构图优先** — 1MP 下确保主体占足够画面
- **关键标签必须有** — 不用塞满，但决定性标签不能少
- **负面要细分** — 具体反咒 >> 笼统反咒
- **单画师更稳** — 自动生成优选 1 位
- **不确定就问** — 安全标签不明确时主动询问用户
