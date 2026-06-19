#!/usr/bin/env node
/**
 * StepFun Image CLI — 调用阶跃星辰 step-image-edit-2 模型
 *
 * Usage:
 *   node run.js generate -p "提示词" [选项]
 *   node run.js edit -p "编辑指令" -i <图片路径> [选项]
 *   node run.js -l
 *
 * 文生图: POST /step_plan/v1/images/generations (JSON)
 * 图像编辑: POST /step_plan/v1/images/edits (multipart/form-data)
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// ─── 加载 .env ────────────────────────────────────────────────
const SCRIPT_DIR = __dirname;
const ENV_FILE = path.join(SCRIPT_DIR, '.env');
if (fs.existsSync(ENV_FILE)) {
  const lines = fs.readFileSync(ENV_FILE, 'utf-8').split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eq = trimmed.indexOf('=');
    if (eq === -1) continue;
    const key = trimmed.slice(0, eq).trim();
    const value = trimmed.slice(eq + 1).trim();
    if (!(key in process.env)) process.env[key] = value;
  }
}

// ─── 配置 ─────────────────────────────────────────────────────
const BASE_URL = 'https://api.stepfun.com/step_plan/v1';
const MODEL = 'step-image-edit-2';

// 支持的 size（注意：step-image-edit-2 格式为 高度x宽度）
const VALID_SIZES = ['1024x1024', '768x1360', '896x1184', '1360x768', '1184x896'];

// ─── 工具函数 ─────────────────────────────────────────────────
function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function tmpName(prefix, ext) {
  const dir = os.tmpdir();
  ensureDir(dir);
  const stamp = Date.now() + '_' + Math.random().toString(16).slice(2, 8);
  return path.join(dir, `${prefix}_${stamp}.${ext}`);
}

/** 下载 URL 到本地文件 */
async function downloadFile(url, outputPath) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Download HTTP ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  ensureDir(path.dirname(path.resolve(outputPath)));
  await fs.promises.writeFile(outputPath, buf);
  return path.resolve(outputPath);
}

// ─── API 调用 ─────────────────────────────────────────────────
/**
 * 文生图
 * POST /step_plan/v1/images/generations
 */
async function generateImage({ apiKey, prompt, size, steps, seed, cfgScale, textMode, negativePrompt, responseFormat, outputPath }) {
  const body = {
    model: MODEL,
    prompt,
    response_format: responseFormat,
  };

  if (size) body.size = size;
  if (steps != null) body.steps = steps;
  if (seed != null) body.seed = seed;
  if (cfgScale != null) body.cfg_scale = cfgScale;
  if (textMode) body.text_mode = true;
  if (negativePrompt) body.negative_prompt = negativePrompt;

  const res = await fetch(`${BASE_URL}/images/generations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errText = await res.text().catch(() => '');
    throw new Error(`API error (${res.status}): ${errText}`);
  }

  const json = await res.json();
  const data = json.data?.[0];
  if (!data) throw new Error('API returned empty data');

  if (data.finish_reason === 'content_filtered') {
    throw new Error('Content filtered — 提示词命中内容审核，请调整后重试');
  }

  return saveResult(data, responseFormat, outputPath);
}

/**
 * 图像编辑
 * POST /step_plan/v1/images/edits (multipart/form-data)
 */
async function editImage({ apiKey, prompt, imagePath, steps, seed, cfgScale, textMode, negativePrompt, responseFormat, outputPath }) {
  if (!imagePath || !fs.existsSync(imagePath)) {
    throw new Error(`Image not found: ${imagePath}`);
  }

  const fd = new FormData();
  fd.append('model', MODEL);
  fd.append('prompt', prompt);
  fd.append('response_format', responseFormat);

  // 读取图片文件并附加到 FormData
  const imgBuf = await fs.promises.readFile(imagePath);
  const imgExt = path.extname(imagePath).toLowerCase();
  const mimeMap = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.bmp': 'image/bmp' };
  const mimeType = mimeMap[imgExt] || 'image/png';
  const blob = new Blob([imgBuf], { type: mimeType });
  fd.append('image', blob, path.basename(imagePath));

  if (steps != null) fd.append('steps', String(steps));
  if (seed != null) fd.append('seed', String(seed));
  if (cfgScale != null) fd.append('cfg_scale', String(cfgScale));
  if (textMode) fd.append('text_mode', 'true');
  if (negativePrompt) fd.append('negative_prompt', negativePrompt);

  const res = await fetch(`${BASE_URL}/images/edits`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      // Content-Type 由 FormData + boundary 自动设置
    },
    body: fd,
  });

  if (!res.ok) {
    const errText = await res.text().catch(() => '');
    throw new Error(`API error (${res.status}): ${errText}`);
  }

  const json = await res.json();
  const data = json.data?.[0];
  if (!data) throw new Error('API returned empty data');

  if (data.finish_reason === 'content_filtered') {
    throw new Error('Content filtered — 提示词命中内容审核，请调整后重试');
  }

  return saveResult(data, responseFormat, outputPath);
}

/** 保存结果：URL 下载 或 base64 解码 */
async function saveResult(data, responseFormat, outputPath) {
  const finalPath = outputPath || tmpName('step_img', 'png');

  if (responseFormat === 'b64_json' && data.b64_json) {
    const buf = Buffer.from(data.b64_json, 'base64');
    ensureDir(path.dirname(path.resolve(finalPath)));
    await fs.promises.writeFile(finalPath, buf);
  } else if (data.url) {
    await downloadFile(data.url, finalPath);
  } else {
    throw new Error('No image data in response (no url and no b64_json)');
  }

  return finalPath;
}

// ─── CLI 参数解析 ──────────────────────────────────────────────

function showHelp() {
  console.log([
    'StepFun Image CLI — 阶跃星辰 step-image-edit-2 图像生成/编辑',
    '',
    'Usage:',
    '  node run.js generate -p "提示词" [选项]   文生图',
    '  node run.js edit -p "编辑指令" -i <图> [选项]  图像编辑',
    '  node run.js -l                             显示此帮助',
    '',
    '通用选项:',
    '  -p, --prompt <text>       提示词（必填，≤512字符）',
    '  -o, --output <path>        输出路径（默认临时目录）',
    '  -k, --api-key <key>        API Key（优先用.env）',
    '  --size <WxH>               尺寸: 1024x1024, 768x1360, 896x1184, 1360x768, 1184x896',
    '  --steps <1-50>             生成步数（默认 8）',
    '  --seed <0-2147483647>      随机种子（默认随机）',
    '  --cfg-scale <1.0-10.0>     CFG scale（默认 1.0）',
    '  --text-mode                文字优化模式',
    '  --negative-prompt <text>   负面提示词',
    '  --response-format <fmt>    url 或 b64_json（默认 url）',
    '  --url                      用 url 返回（默认）',
    '  --b64                      用 b64_json 返回',
    '',
    '编辑模式额外选项:',
    '  -i, --image <path>         输入图片路径（必填）',
    '',
    'Examples:',
    '  node run.js generate -p "一只有翅膀的猫在月球上漫步"',
    '  node run.js generate -p "山水画风格的小镇" --text-mode --size 1024x1024',
    '  node run.js edit -i input.png -p "让这只猫戴上墨镜"',
    '  node run.js generate -p "赛博朋克夜景" --steps 15 --cfg-scale 3.5 --seed 42',
  ].join('\n'));
}

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {
    command: null,
    prompt: '',
    image: null,
    output: null,
    apiKey: null,
    size: null,
    steps: null,
    seed: null,
    cfgScale: null,
    textMode: false,
    negativePrompt: null,
    responseFormat: 'url',
    help: false,
  };

  let i = 0;
  while (i < args.length) {
    const a = args[i];
    if (a === 'generate' || a === 'edit') {
      result.command = a;
    } else if (a === '-p' || a === '--prompt') {
      result.prompt = args[++i] || '';
    } else if (a === '-i' || a === '--image') {
      result.image = args[++i] || null;
    } else if (a === '-o' || a === '--output') {
      result.output = args[++i] || null;
    } else if (a === '-k' || a === '--api-key') {
      result.apiKey = args[++i] || null;
    } else if (a === '--size') {
      result.size = args[++i] || null;
    } else if (a === '--steps') {
      result.steps = parseInt(args[++i], 10);
    } else if (a === '--seed') {
      result.seed = parseInt(args[++i], 10);
    } else if (a === '--cfg-scale') {
      result.cfgScale = parseFloat(args[++i]);
    } else if (a === '--text-mode') {
      result.textMode = true;
    } else if (a === '--negative-prompt') {
      result.negativePrompt = args[++i] || null;
    } else if (a === '--response-format') {
      result.responseFormat = args[++i] || 'url';
    } else if (a === '--url') {
      result.responseFormat = 'url';
    } else if (a === '--b64') {
      result.responseFormat = 'b64_json';
    } else if (a === '-l' || a === '--help') {
      result.help = true;
    }
    i++;
  }
  return result;
}

// ─── 主入口 ───────────────────────────────────────────────────
async function main() {
  const opts = parseArgs();

  if (opts.help || (!opts.command && !opts.help)) {
    showHelp();
    process.exit(0);
  }

  // API Key
  const apiKey = opts.apiKey || process.env.STEP_IMAGE_API_KEY || '';
  if (!apiKey) {
    console.error('Error: API Key is required. Set STEP_IMAGE_API_KEY in .env or pass -k.');
    process.exit(1);
  }

  // 验证命令
  if (!['generate', 'edit'].includes(opts.command)) {
    console.error('Error: Unknown command. Use "generate" or "edit".');
    process.exit(1);
  }

  // 验证 prompt
  if (!opts.prompt) {
    console.error('Error: Prompt is required. Use -p "your description".');
    process.exit(1);
  }

  // 验证 size
  if (opts.size && !VALID_SIZES.includes(opts.size)) {
    console.error(`Error: Invalid size "${opts.size}". Valid: ${VALID_SIZES.join(', ')}`);
    process.exit(1);
  }

  try {
    let resultPath;

    if (opts.command === 'generate') {
      resultPath = await generateImage({
        apiKey,
        prompt: opts.prompt,
        size: opts.size,
        steps: opts.steps,
        seed: opts.seed,
        cfgScale: opts.cfgScale,
        textMode: opts.textMode,
        negativePrompt: opts.negativePrompt,
        responseFormat: opts.responseFormat,
        outputPath: opts.output,
      });
    } else {
      resultPath = await editImage({
        apiKey,
        prompt: opts.prompt,
        imagePath: opts.image,
        steps: opts.steps,
        seed: opts.seed,
        cfgScale: opts.cfgScale,
        textMode: opts.textMode,
        negativePrompt: opts.negativePrompt,
        responseFormat: opts.responseFormat,
        outputPath: opts.output,
      });
    }

    console.log(`Success! Output saved to: ${resultPath}`);
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }
}

main();
