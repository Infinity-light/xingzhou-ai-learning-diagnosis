# 星舟 AI 学习诊断

这是一个可独立安装的 Agent Skill。它从用户最近一次真实使用 AI 的经历出发，每轮只问一个容易回答的具体事实，用最多三个自适应问题判断 0–100 学习坐标，并给出下一步行动。取得访问密码后，它会直接读取飞书知识库文件夹的当前目录和相关文章，为建议附上原文链接。

评分由安装该 Skill 的 Agent 完成。项目不包含 MCP Server、评分网站、远程模型接口、知识库正文、访问密码或用户报告。

## 安装

让支持 Skills 的 Agent 执行：

```bash
npx -y skills add Infinity-light/xingzhou-ai-learning-diagnosis -g --skill xingzhou-ai-learning-diagnosis
```

这条命令只选择本仓库中的一个 Skill，并让安装器选择当前使用的 Agent。自动安装时，Agent 可以再补上 `--agent <自身平台 ID> -y`。`--all` 会尝试把同一个 Skill 安装到所有受支持的 Agent 平台，普通用户不需要使用；Eve、PromptScript 等名称来自安装器的目标平台列表，不是本项目额外创建的 Skill。

也可以下载仓库，把 `skills/xingzhou-ai-learning-diagnosis` 放入 Agent 的 Skills 目录。

## 使用

可以直接说：

> 帮我判断一下现在的 AI 学习阶段，并给我下一步。

新手只需讲一次最近的真实任务。进阶用户可以额外给出一个项目或文件夹路径，让 Agent 在只读范围内检查现有成果。完整规则见 Skill 内的评分、访谈和飞书知识库说明。

飞书知识库文件夹是内容真源。里面使用原生飞书文档，显示标题不保留 `.md`；文章可以随时新增、改名、移动或重排。Skill 每次需要引用知识时重新发现当前文件夹，不依赖文章编号，也不把文章数量当作用户分数。

## 隐私与运行边界

- 密码只用于当前飞书会话，不写入文件、报告、日志或项目。
- 只有实际打开并读取过的文章才能作为依据引用。
- 无法访问飞书时仍可完成公开诊断，但必须说明本次没有使用知识库。
- 本项目使用宿主 Agent 已有的推理、网页和文件能力，不要求额外模型 API。

## 开发校验

仓库只公开 Skill 行为规则与匿名评测规范。私密运行记录和用户答案不进入版本库。

```bash
python tools/validate_distribution.py
```

## License

MIT
