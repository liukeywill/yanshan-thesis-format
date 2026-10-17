# 燕山学院专科论文格式调整

供 Codex 使用的技能，**仅限山东财经大学燕山学院专科毕业论文（设计）的格式修改**，保留正文内容。不适用于其他院校、本科或研究生论文，也不用于内容撰写、润色或通用论文排版。

支持整页封面替换、题目和个人信息表格、中文班号转阿拉伯数字、中英文摘要分页、关键词标签格式、目录和页码，以及 GB/T 7714—2015 参考文献著录。附匿名化封面模板和只读结构检查脚本。

## 安装

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo liukeywill/yanshan-thesis-format --path . --name yanshan-thesis-format
```

## 使用

附上论文，需要时同时提供学校最新版模板，然后输入：

```text
使用 $yanshan-thesis-format，按学校要求修改这篇论文的格式，保留正文内容。
```

也可以指定只修改封面、摘要、参考文献等部分。用户本次要求和最新版模板优先。技能不代写论文、不自动提交，不保证未核查的文献信息真实完整。

## 文件

- `SKILL.md`：流程和适用范围。
- `references/format-rules.md`：格式约定与适用边界。
- `assets/cover-template.docx`：使用占位符的封面模板，不包含学生身份信息。
- `scripts/thesis_checks.py`：班号转换和只读结构清单；依赖 `lxml`，不能代替逐页渲染检查。
- `agents/openai.yaml`：Codex 调用入口。

文档处理使用当前 Codex 工作区依赖；PDF 预览和字体支持需按执行环境配置。模板包含占位符，填入学生真实信息后须检查封面仍为一页。
