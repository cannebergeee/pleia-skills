#!/usr/bin/env node
/**
 * RunningHub 图像生成工具 (Node.js CLI)
 * 支持多种 AI 图像处理工作流
 *
 * Usage: node run.js <workflow> [-p "prompt"] [-i img1 img2...] [-o output.png] [-l]
 *
 * 要求: Node.js >= 21 (需要全局 fetch/FormData/File)
 *       Node 18-20 需额外: npm install undici
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { Blob } = require('node:buffer');

// ─── 加载 .env ────────────────────────────────────────────────
const SCRIPT_DIR = __dirname;
// 优先当前目录（脚本在 skill 根），回退上级（脚本在 scripts/ 子目录）
const ENV_FILE = (
  fs.existsSync(path.join(SCRIPT_DIR, '.env'))
    ? path.join(SCRIPT_DIR, '.env')
    : path.join(path.resolve(SCRIPT_DIR, '..'), '.env')
);
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

// ─── 默认配置 ──────────────────────────────────────────────────
const DEFAULT_BASE_URL = 'https://www.runninghub.cn';
const DEFAULT_TIMEOUT = 360;      // 6分钟硬超时
const DEFAULT_POLL_INTERVAL = 2;  // 轮询间隔（秒）

// ─── 进程锁（防止 Agent 重试导致多实例同时跑） ──────────────────
const LOCK_FILE = path.join(os.tmpdir(), 'runninghub_gen.lock');
const LOCK_MAX_AGE_MS = 10 * 60 * 1000;  // 锁超过 10 分钟视为僵尸锁

function isProcessAlive(pid) {
  try { process.kill(pid, 0); return true; } catch { return false; }
}
function readLockFile() {
  try {
    return fs.readFileSync(LOCK_FILE, 'utf-8').trim().split('\n');
  } catch { return []; }
}

function acquireLock(outputPath) {
  if (fs.existsSync(LOCK_FILE)) {
    let lockStale = false;
    try {
      const stat = fs.statSync(LOCK_FILE);
      if (Date.now() - stat.mtimeMs > LOCK_MAX_AGE_MS) {
        lockStale = true;
      }
    } catch {}

    if (lockStale) {
      try { fs.unlinkSync(LOCK_FILE); } catch {}
    } else {
      const lines = readLockFile();
      const oldPid = parseInt(lines[0], 10);
      const oldOutput = lines[1] || null;
      if (oldPid && isProcessAlive(oldPid)) {
        console.error(`BUSY: Another generation is already running (PID: ${oldPid}).`);
        if (oldOutput) {
          console.error(`Output will be at: ${oldOutput}`);
        }
        console.error(`Wait for the lock to clear or the output file to appear.`);
        process.exit(1);
      }
      try { fs.unlinkSync(LOCK_FILE); } catch {}
    }
  }
  const content = outputPath ? `${process.pid}\n${outputPath}` : String(process.pid);
  ensureDir(path.dirname(LOCK_FILE));
  fs.writeFileSync(LOCK_FILE, content);
}
function releaseLock() {
  try {
    const lines = readLockFile();
    if (lines[0] === String(process.pid)) fs.unlinkSync(LOCK_FILE);
  } catch {}
}

// ─── 工作流配置 ────────────────────────────────────────────────
const WORKFLOWS = {
  old_edit: {
    name: '旧版改图',
    workflow_id: '1985066364090142721',
    node_image: '78',
    node_prompt: '111',
    text_field_name: 'prompt',
    need_image: true,
    need_prompt: true,
    prefix: '',
    mode: 'single',
  },
  realistic: {
    name: '动漫转真人',
    workflow_id: '1987074571213975553',
    node_image: '78',
    node_prompt: '111',
    text_field_name: 'prompt',
    need_image: true,
    need_prompt: false,
    prefix: 'transform the image to realistic photograph,',
    mode: 'single',
  },
  angle: {
    name: '角度控制',
    workflow_id: '1987149953069944834',
    node_image: '78',
    node_prompt: '111',
    text_field_name: 'prompt',
    need_image: true,
    need_prompt: true,
    prefix: '',
    mode: 'single',
  },
  outfit: {
    name: '服装迁移',
    workflow_id: '1987234864036515841',
    node_image1: '78',
    node_image2: '106',
    node_prompt: '111',
    text_field_name: 'prompt',
    need_image: true,
    need_prompt: false,
    prefix:
      '图一人物去掉所有衣服，把图2中动漫人物中的发型，服饰和装扮道具迁移到图1的真实人物，图1真实人物保持高度的动作和人脸一致性，图一人物融入背景光影，',
    mode: 'double',
  },
  hd: {
    name: '高清化',
    workflow_id: '1988351754267967489',
    node_image: '78',
    node_prompt: '111',
    text_field_name: 'prompt',
    need_image: true,
    need_prompt: false,
    prefix: 'regenerate this image,',
    mode: 'single',
  },
  chibi: {
    name: '转q版',
    workflow_id: '1991331721488740354',
    node_image: '78',
    node_prompt: '111',
    text_field_name: 'prompt',
    need_image: true,
    need_prompt: false,
    prefix: '生成这个角色的q版图，三头身比例，其他细节不变，miratsu style, chibi,',
    mode: 'single',
  },
  zimg1: {
    name: 'z_image 横图',
    workflow_id: '1994071897593806849',
    need_image: false,
    need_prompt: true,
    prefix: '震撼光影，胶片质感，',
    mode: 'text_only',
    node_text: '6',
    node_latent: '13',
    width: 1920,
    height: 1088,
  },
  zimg2: {
    name: 'z_image 竖图',
    workflow_id: '1994071897593806849',
    need_image: false,
    need_prompt: true,
    prefix: '震撼光影，胶片质感，',
    mode: 'text_only',
    node_text: '6',
    node_latent: '13',
    width: 1088,
    height: 1920,
  },
  xl1: {
    name: '动漫横图',
    workflow_id: '1994424716280598529',
    need_image: false,
    need_prompt: true,
    prefix: '',
    mode: 'text_only',
    node_text: '15',
    node_latent: '6',
    width: 1280,
    height: 900,
  },
  xl2: {
    name: '动漫竖图',
    workflow_id: '1994424716280598529',
    need_image: false,
    need_prompt: true,
    prefix: '',
    mode: 'text_only',
    node_text: '15',
    node_latent: '6',
    width: 900,
    height: 1280,
  },
  anima1: {
    name: 'anima横图',
    workflow_id: '2056025847756271618',
    need_image: false,
    need_prompt: true,
    prefix: '',
    mode: 'text_only',
    node_text: '6',
    node_latent: '8',
    width: 1584,
    height: 1024,
  },
  anima2: {
    name: 'anima竖图',
    workflow_id: '2056025847756271618',
    need_image: false,
    need_prompt: true,
    prefix: '',
    mode: 'text_only',
    node_text: '6',
    node_latent: '8',
    width: 1024,
    height: 1584,
  },
  oldanima1: {
    name: 'oldanima横图',
    workflow_id: '2028101389511041025',
    need_image: false,
    need_prompt: true,
    prefix: '',
    mode: 'text_only',
    node_text: '13',
    node_latent: '5',
    width: 1584,
    height: 1024,
  },
  oldanima2: {
    name: 'oldanima竖图',
    workflow_id: '2028101389511041025',
    need_image: false,
    need_prompt: true,
    prefix: '',
    mode: 'text_only',
    node_text: '13',
    node_latent: '5',
    width: 1024,
    height: 1584,
  },
  bqb1: {
    name: '表情包1',
    workflow_id: '2023435759520325634',
    need_image: false,
    need_prompt: true,
    prefix: '',
    mode: 'text_only',
    node_text: '15',
  },
  bqb2: {
    name: '表情包2',
    workflow_id: '2023449731439009793',
    need_image: false,
    need_prompt: true,
    prefix: '',
    mode: 'text_only',
    node_text: '15',
  },
  qwen1: {
    name: 'qwen横图',
    workflow_id: '2007137004617736194',
    need_image: false,
    need_prompt: true,
    prefix: '',
    mode: 'text_only',
    node_text: '6',
    node_latent: '8',
    width: 1280,
    height: 900,
  },
  qwen2: {
    name: 'qwen竖图',
    workflow_id: '2007137004617736194',
    need_image: false,
    need_prompt: true,
    prefix: '',
    mode: 'text_only',
    node_text: '6',
    node_latent: '8',
    width: 900,
    height: 1280,
  },
  cf1: {
    name: '喵喵',
    workflow_id: '2023873024457445378',
    need_image: false,
    need_prompt: true,
    prefix: '',
    mode: 'text_only',
    node_text: '15',
  },
  upscale: {
    name: '放大',
    workflow_id: '2003097984990609409',
    node_image: '295',
    node_prompt: '297',
    text_field_name: 'prompt',
    need_image: true,
    need_prompt: true,
    prefix: '',
    mode: 'single',
  },
  qwen_edit: {
    name: 'qwen改图',
    workflow_id: '2029594780891619330',
    node_image: '74',
    node_prompt: '266',
    text_field_name: 'prompt',
    need_image: true,
    need_prompt: true,
    prefix: '',
    mode: 'single',
  },
  gpt2: {
    name: 'gpt2改图',
    workflow_id: '2053137753000423425',
    node_image: '3',
    node_prompt: '6',
    text_field_name: 'text',
    need_image: true,
    need_prompt: true,
    prefix: '',
    mode: 'single',
  },
  ban2: {
    name: 'ban2',
    workflow_id: '2028779336123293697',
    node_image1: '2',
    node_image2: '3',
    node_text: '11',
    text_field_name: 'text',
    need_image: true,
    need_prompt: true,
    prefix: '',
    mode: 'flexible',
  },
};

// ─── 工具函数 ──────────────────────────────────────────────────
function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function tmpName(prefix, ext) {
  const dir = process.env.RUNNINGHUB_TMP_DIR || os.tmpdir();
  ensureDir(dir);
  const stamp = Date.now() + '_' + Math.random().toString(16).slice(2, 8);
  return path.join(dir, `${prefix}_${stamp}.${ext}`);
}

// ─── RunningHub API 客户端 ─────────────────────────────────────
class RunningHubClient {
  constructor(apiKey, baseUrl = DEFAULT_BASE_URL) {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/+$/, '');
  }

  /** 带重试的 fetch：5xx 和网络错误自动重试（最多 3 次） */
  async _fetchWithRetry(url, options, maxRetries = 3) {
    let lastError;
    for (let i = 0; i <= maxRetries; i++) {
      try {
        const res = await fetch(url, options);
        if (res.status < 500) return res;  // 2xx/3xx/4xx — 不重试
        lastError = new Error(`HTTP ${res.status}`);
      } catch (e) {
        lastError = e;  // 网络错误 / DNS 失败
      }
      if (i < maxRetries) await sleep(2000);
    }
    throw lastError || new Error('Fetch failed after retries');
  }

  /** 上传图片到 RunningHub，返回 fileName */
  async uploadImage(imagePath) {
    const buf = await fs.promises.readFile(imagePath);
    const blob = new Blob([buf]);
    const fd = new FormData();
    fd.append('apiKey', this.apiKey);
    fd.append('file', blob, path.basename(imagePath));

    const res = await this._fetchWithRetry(
      `${this.baseUrl}/task/openapi/upload`,
      { method: 'POST', body: fd }
    );
    if (!res.ok) throw new Error(`Upload HTTP ${res.status}`);
    const json = await res.json();
    if (json.code !== 0 || !json.data?.fileName) {
      throw new Error(`Upload failed: ${JSON.stringify(json)}`);
    }
    return json.data.fileName;
  }

  /** 创建任务，返回 taskId */
  async createTask(workflowId, nodeInfoList) {
    const body = { apiKey: this.apiKey, workflowId, nodeInfoList };
    const res = await this._fetchWithRetry(
      `${this.baseUrl}/task/openapi/create`,
      { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }
    );
    if (!res.ok) throw new Error(`Create HTTP ${res.status}`);
    const json = await res.json();
    if (json.code !== 0 || !json.data?.taskId) {
      throw new Error(`Create failed: ${JSON.stringify(json)}`);
    }
    return json.data.taskId;
  }

  /** 轮询等待任务完成（含 5xx/网络重试） */
  async waitForTask(taskId, timeout = DEFAULT_TIMEOUT) {
    const body = { apiKey: this.apiKey, taskId };
    const start = Date.now();
    while (Date.now() - start < timeout * 1000) {
      const res = await this._fetchWithRetry(
        `${this.baseUrl}/task/openapi/status`,
        { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }
      );
      if (!res.ok) throw new Error(`Status HTTP ${res.status}`);
      const json = await res.json();
      if (json.code !== 0) throw new Error(`Status fail: ${JSON.stringify(json)}`);
      const raw = json.data;
      const st = String((raw && raw.status) ? raw.status : (raw || '')).toUpperCase();
      if (['SUCCESS', 'COMPLETED', 'FINISHED'].includes(st)) return;
      if (['FAILED', 'ERROR'].includes(st)) throw new Error('Task failed');
      await sleep(DEFAULT_POLL_INTERVAL * 1000);
    }
    throw new Error('Task timeout');
  }

  /** 获取结果 URL（带重试，处理输出未就绪的竞态 + 5xx/网络重试） */
  async getOutputs(taskId, retries = 8) {
    const body = { apiKey: this.apiKey, taskId };
    for (let i = 0; i <= retries; i++) {
      const res = await this._fetchWithRetry(
        `${this.baseUrl}/task/openapi/outputs`,
        { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }
      );
      if (!res.ok) throw new Error(`Outputs HTTP ${res.status}`);
      const json = await res.json();

      if (json.code === 0) {
        const arr = Array.isArray(json.data) ? json.data : [];
        const first = arr[0] || {};
        const out = first.fileUrl || first.url || first.resultUrl || null;
        if (out) return out;
        // 输出尚未就绪，等待后重试
        if (i < retries) { await sleep(2000); continue; }
      }
      // 非成功响应，等待后重试
      if (i < retries) { await sleep(2000); continue; }
      throw new Error(`Get outputs failed after ${retries} retries: ${JSON.stringify(json)}`);
    }
    throw new Error('Result not ready after retries');
  }

  /** 下载图片到本地 */
  async downloadImage(imageUrl, outputPath) {
    const res = await this._fetchWithRetry(imageUrl, {});
    if (!res.ok) throw new Error(`Download HTTP ${res.status}`);
    const buf = Buffer.from(await res.arrayBuffer());
    ensureDir(path.dirname(path.resolve(outputPath)) || '.');
    await fs.promises.writeFile(outputPath, buf);
    return path.resolve(outputPath);
  }
}

// ─── 核心处理函数 ──────────────────────────────────────────────
async function processImage(workflowKey, { prompt = '', imagePaths = [], outputPath = null, apiKey = null } = {}) {
  // 获取 API Key
  apiKey = apiKey || process.env.RUNNINGHUB_API_KEY || '';
  if (!apiKey) {
    throw new Error('API Key is required. Set RUNNINGHUB_API_KEY in .env or pass --api-key.');
  }

  // 获取工作流配置
  const workflow = WORKFLOWS[workflowKey];
  if (!workflow) {
    throw new Error(`Unknown workflow: ${workflowKey}. Available: ${Object.keys(WORKFLOWS).join(', ')}`);
  }

  const client = new RunningHubClient(apiKey);

  // 构建最终提示词
  let finalPrompt = (prompt || '').trim();
  const prefix = workflow.prefix || '';
  if (prefix && finalPrompt && !finalPrompt.toLowerCase().startsWith(prefix.toLowerCase())) {
    finalPrompt = `${prefix} ${finalPrompt}`.trim();
  } else if (prefix && !finalPrompt) {
    finalPrompt = prefix;
  }

  // 验证输入
  if (workflow.need_image && imagePaths.length === 0) {
    throw new Error(`Workflow '${workflow.name}' requires at least one image.`);
  }
  if (workflow.need_prompt && !finalPrompt) {
    throw new Error(`Workflow '${workflow.name}' requires a prompt.`);
  }

  // 验证图片数量
  const mode = workflow.mode;
  if (mode === 'double' && imagePaths.length < 2) {
    throw new Error(`Workflow '${workflow.name}' requires exactly two images.`);
  }
  if (mode === 'flexible' && imagePaths.length > 2) {
    throw new Error(`Workflow '${workflow.name}' accepts at most two images.`);
  }

  // 上传图片
  const uploadedFiles = [];
  for (const imgPath of imagePaths) {
    if (!fs.existsSync(imgPath)) {
      throw new Error(`Image not found: ${imgPath}`);
    }
    const fileName = await client.uploadImage(imgPath);
    uploadedFiles.push(fileName);
  }

  // 构建节点信息
  const nodeInfoList = [];

  // 处理提示词节点 (兼容 node_text 和 node_prompt)
  const textNodeId = workflow.node_text || workflow.node_prompt;
  if (textNodeId) {
    nodeInfoList.push({
      nodeId: String(textNodeId),
      fieldName: workflow.text_field_name || 'text',
      fieldValue: finalPrompt,
    });
  }

  // 处理图片节点
  if (uploadedFiles.length > 0) {
    // 第一张图: node_image1 或 node_image
    const img1NodeId = workflow.node_image1 || workflow.node_image;
    if (img1NodeId) {
      nodeInfoList.push({
        nodeId: String(img1NodeId),
        fieldName: 'image',
        fieldValue: uploadedFiles[0],
      });
    }
    // 第二张图: node_image2
    if (uploadedFiles.length >= 2 && workflow.node_image2) {
      nodeInfoList.push({
        nodeId: String(workflow.node_image2),
        fieldName: 'image',
        fieldValue: uploadedFiles[1],
      });
    }
  }

  // 处理文生图分辨率节点
  if (workflow.node_latent && workflow.width && workflow.height) {
    nodeInfoList.push({
      nodeId: String(workflow.node_latent),
      fieldName: 'width',
      fieldValue: Number(workflow.width),
    });
    nodeInfoList.push({
      nodeId: String(workflow.node_latent),
      fieldName: 'height',
      fieldValue: Number(workflow.height),
    });
  }

  // 创建任务
  const taskId = await client.createTask(workflow.workflow_id, nodeInfoList);
  console.log(`Task created (ID: ${taskId}), waiting for completion...`);

  // 等待任务完成
  await client.waitForTask(taskId);

  // 短暂等待确保输出就绪（减少竞态）
  await sleep(1000);

  // 获取结果
  const outputUrl = await client.getOutputs(taskId);

  // 下载结果
  const finalOutputPath = outputPath || tmpName('rh_out', 'png');
  const resultPath = await client.downloadImage(outputUrl, finalOutputPath);

  return resultPath;
}

// ─── CLI ───────────────────────────────────────────────────────
function listWorkflows() {
  console.log('Available workflows:');
  console.log('-'.repeat(60));
  for (const [key, cfg] of Object.entries(WORKFLOWS)) {
    const modeMap = { single: '单图', double: '双图', text_only: '文生图', flexible: '单/双图' };
    const modeDesc = modeMap[cfg.mode] || cfg.mode;
    const needs = [];
    if (cfg.need_image) needs.push('图');
    if (cfg.need_prompt) needs.push('文');
    const dim = cfg.width ? ` ${cfg.width}x${cfg.height}` : '';
    console.log(`  ${key.padEnd(12)} ${cfg.name.padEnd(14)} (${modeDesc})${dim}`);
    console.log(`               需要: ${needs.join(', ') || '无'}`);
  }
  console.log('-'.repeat(60));
}

function parseArgs() {
  const args = process.argv.slice(2);
  const result = { workflow: null, prompt: '', images: [], output: null, apiKey: null, list: false };

  let i = 0;
  while (i < args.length) {
    const a = args[i];
    if (a === '-p' || a === '--prompt') {
      result.prompt = args[++i] || '';
    } else if (a === '-i' || a === '--images') {
      while (i + 1 < args.length && !args[i + 1].startsWith('-')) {
        result.images.push(args[++i]);
      }
    } else if (a === '-o' || a === '--output') {
      result.output = args[++i] || null;
    } else if (a === '-k' || a === '--api-key') {
      result.apiKey = args[++i] || null;
    } else if (a === '-l' || a === '--list') {
      result.list = true;
    } else if (!a.startsWith('-') && !result.workflow) {
      result.workflow = a;
    }
    i++;
  }
  return result;
}

async function main() {
  const opts = parseArgs();

  if (opts.list) {
    listWorkflows();
    process.exit(0);
  }

  if (!opts.workflow) {
    console.error('Usage: node run.js <workflow> [-p "prompt"] [-i img1 img2...] [-o output.png]');
    console.error('Use -l to list available workflows.');
    process.exit(1);
  }

  try {
    acquireLock(opts.output);
    const resultPath = await processImage(opts.workflow, {
      prompt: opts.prompt,
      imagePaths: opts.images,
      outputPath: opts.output,
      apiKey: opts.apiKey,
    });
    console.log(`Success! Output saved to: ${resultPath}`);
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  } finally {
    releaseLock();
  }
}

main();
