#!/usr/bin/env node
/**
* Universal launcher for the Vision Assist MCP server.
*
* Codex, Claude Code, and OpenCode are all Node-based, so `node` is reliably
* available in their MCP runner environments. This script locates a usable
* Python interpreter and then spawns the Python MCP server, proxying stdio
* so the JSON-RPC stream is unchanged.
*/

import { spawn } from "node:child_process";
import { access } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const SERVER_SCRIPT = resolve(ROOT, "mcp", "server.py");

const ENV_PYTHON = process.env.VISION_ASSIST_PYTHON;

async function exists(path) {
 try {
   await access(path);
   return true;
 } catch {
   return false;
 }
}

async function tryPython(cmd, extraArgs = []) {
 return new Promise((resolve) => {
   const child = spawn(cmd, [...extraArgs, "-c", "import sys; print(sys.executable)"], {
     stdio: ["ignore", "pipe", "ignore"],
     windowsHide: true,
   });
   let out = "";
   child.stdout.on("data", (chunk) => {
     out += chunk;
   });
   child.on("error", () => resolve(null));
   child.on("close", (code) => {
     const exe = out.trim();
     resolve(code === 0 && exe ? exe : null);
   });
 });
}

async function searchPathCandidates(names) {
 for (const name of names) {
   const found = await tryPython(name);
   if (found) return found;
 }
 return null;
}

async function searchCommonPaths() {
 if (process.platform === "win32") {
   const home = process.env.USERPROFILE || process.env.HOME || "";
   const localAppData = process.env.LOCALAPPDATA || "";
   const programFiles = process.env.PROGRAMFILES || "C:\\Program Files";
   const candidates = [
     // Bundled Codex runtime
     resolve(home, ".cache", "codex-runtimes", "codex-primary-runtime", "dependencies", "python", "python.exe"),
     // Common Windows install locations
     ...[311, 310, 39, 312, 313].map((v) =>
       resolve(localAppData, "Programs", "Python", `Python${v}`, "python.exe")
     ),
     ...[311, 310, 39, 312, 313].map((v) =>
       resolve(programFiles, `Python${v}`, "python.exe")
     ),
     resolve(programFiles, "Python", "python.exe"),
   ];
   for (const p of candidates) {
     if (await exists(p)) return p;
   }
 } else {
   const unixCandidates = [
     "/usr/bin/python3",
     "/usr/local/bin/python3",
     "/opt/homebrew/bin/python3",
     "/usr/bin/python",
     "/usr/local/bin/python",
   ];
   for (const p of unixCandidates) {
     if (await exists(p)) return p;
   }
 }
 return null;
}

async function findPython() {
 if (ENV_PYTHON) {
   if (await exists(ENV_PYTHON)) return ENV_PYTHON;
   const error = `VISION_ASSIST_PYTHON is set to "${ENV_PYTHON}" but that file does not exist.`;
   console.error(error);
   process.stderr.write(error + "\n");
   process.exit(1);
 }

 const pathNames = process.platform === "win32"
   ? ["python", "python3", "py"]
   : ["python3", "python"];
 const fromPath = await searchPathCandidates(pathNames);
 if (fromPath) return fromPath;

 const fromCommon = await searchCommonPaths();
 if (fromCommon) return fromCommon;

 const error =
   "Vision Assist could not find a Python interpreter. " +
   "Please install Python 3.8+ and make sure `python` or `python3` is on PATH, " +
   "or set the VISION_ASSIST_PYTHON environment variable to the python executable path.";
 process.stderr.write(error + "\n");
 process.exit(1);
}

async function main() {
 const python = await findPython();
 const child = spawn(python, [SERVER_SCRIPT], {
   cwd: ROOT,
   stdio: ["inherit", "inherit", "inherit"],
   windowsHide: true,
 });
 child.on("error", (err) => {
   process.stderr.write(`Failed to start Vision Assist server: ${err.message}\n`);
   process.exit(1);
 });
 child.on("exit", (code) => {
   process.exit(code ?? 0);
 });
}

main();
