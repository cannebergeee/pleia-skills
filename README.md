# pleia-skills

个人日常使用的 Agent Skills，让 AI Agent 能更好地完成特定任务。每个 skill 都是自包含的指令集 + 脚本，放到对应平台的 skills 目录下即可生效。

---

## Skills

| Skill | 说明 |
|---|---|
| 🔍 **mimo-web-search** | 基于小米 MiMo 开放平台的联网搜索，支持中文网页、实时信息、引用溯源 |

---

## 安装

将 skill 目录复制到对应平台的 skills 路径下即可：

```bash
# Claude Code
cp -r mimo-web-search-skills ~/.claude/skills/

# Codex
cp -r mimo-web-search-skills ~/.codex/skills/
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

## License

MIT
