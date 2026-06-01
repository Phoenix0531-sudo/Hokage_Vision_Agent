# Agent

The default agent is rule-based and runs without API keys. It routes project-scoped requests to an allowlisted tool registry.

```bash
hokage-vision agent run "检测 examples/images 里的图片"
hokage-vision agent run "检查数据集并给出训练建议"
```

The agent refuses out-of-scope requests such as arbitrary shell execution, weather lookup, unrelated writing tasks, API key disclosure, and copyrighted image scraping.

`generate_report` is only selected when the user explicitly asks to generate a report.
