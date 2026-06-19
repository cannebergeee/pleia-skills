# StepFun Image API 参数速查

## 接口

| 能力 | 方法 | 路径 |
|------|------|------|
| 文生图 | POST | `https://api.stepfun.com/step_plan/v1/images/generations` |
| 图像编辑 | POST | `https://api.stepfun.com/step_plan/v1/images/edits` |

认证：`Authorization: Bearer <API_KEY>`

## 模型：`step-image-edit-2`

单模型同时支持文生图与图像编辑。输入图最大 4096×4096 分辨率，单次编辑 1-2 秒。

## 通用参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `model` | string | — | 固定为 `step-image-edit-2` |
| `prompt` | string | — | 文本描述，最大 512 字符 |
| `response_format` | string | `url` | `url` 或 `b64_json` |
| `cfg_scale` | float | `1.0` | classifier-free guidance，范围 [1.0, 10.0] |
| `steps` | int | `8` | 生成步数，范围 [1, 50] |
| `seed` | int | 随机 | 范围 [0, 2147483647]，相同 seed 生成相似图片 |
| `text_mode` | bool | `false` | 文字场景优化 |
| `negative_prompt` | string | `""` | 负面提示词，最大 512 字符。`cfg_scale=1.0` 时不生效 |

## size 参数（文生图）

格式为 `高度x宽度`（注意顺序与其他模型相反）：

| 类型 | 可选值 |
|------|--------|
| 正方形 | `1024x1024` |
| 竖图 | `768x1360`、`896x1184` |
| 横图 | `1360x768`、`1184x896` |

## 图像编辑特有说明

- 请求格式：`multipart/form-data`
- `image`：图片文件（必填），最大 4096×4096
- `size` 参数在编辑场景下不生效（返回输入图同尺寸）
- 不支持 mask（与 OpenAI 差异）

## 响应

```json
{
  "created": 1589478378,
  "data": [
    {
      "b64_json": "AAAA...",
      "finish_reason": "success",
      "seed": 123838
    }
  ]
}
```

- `response_format=url` → `data[].url`（有效期 30 天）
- `response_format=b64_json` → `data[].b64_json`
- `finish_reason`: `success` 或 `content_filtered`

## 计费

按 Step Plan 总额度消耗，与开放平台计费一致。详见 [定价与限速](https://platform.stepfun.com/docs/zh/guides/pricing/details)。
