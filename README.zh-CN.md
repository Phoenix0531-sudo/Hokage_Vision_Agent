# Hokage Vision Agent

<p align="center">
  <img src="docs/screenshots/gui_hero.png" alt="Hokage Vision Agent GUI" width="720">
</p>

**Agent 风格动漫角色检测工作台 — YOLO 后端、PySide6 桌面、FastAPI、Typer CLI、工具调用 Agent。**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-%3E%3D3.12-blue.svg)](pyproject.toml)
[![Code style: ruff](https://img.shields.io/badge/lint-ruff-261230.svg)](https://github.com/astral-sh/ruff)
[![Coverage gate 85%](https://img.shields.io/badge/coverage-gate%2085%25-brightgreen.svg)](.github/workflows/ci.yml)

作品集级 CV 工作台。检测由 **vision backend** 完成（mock / Ultralytics / 旧版 YOLOv5）。**Agent 不编造标签**，只选择安全的项目工具（检测、校验数据集、smoke 训练、评估、对比、注册表更新）。

## 为什么值得看

- **真·LLM Agent，不是封装壳**：函数调用 Agent 驱动 16 个带 JSON Schema 的工具，三种 provider（规则 / OpenAI / LangGraph），客户端可注入所以整个 Agent 循环都能离线单测；安全层在任何 LLM 调用之前拒绝越界任务。
- **纯 ONNX CPU 推理**：12 MB 模型，运行时不需要 PyTorch，笔记本 CPU 约 30 FPS（`hokage-vision model benchmark`）。
- **仓库内训练闭环**：合成数据 → yolov8n 微调 → ONNX 导出 → 真实检测，一条命令、纯 CPU、mAP50 0.995。
- **工程质量即卖点**：160+ 测试、93% 覆盖（CI 门禁 85%）、8 条 CI 流水线、三平台桌面包、GHCR 镜像、MkDocs 文档站。

## 🎮 在线试玩（免安装）

内置的合成形状模型已部署在免费的 Hugging Face Space 上——上传图片、拖动置信度滑杆，直接看真实 ONNX 检测结果：

**→ [打开在线 Demo](https://huggingface.co/spaces/phoenix0531-sudo/hokage-vision-agent)** *（部署中 —— 应用已在 [`hf-space/`](hf-space/) 备好，推上去即生效）*

同一套 Space 代码（`hf-space/app.py`）也可本地运行：`pip install -r hf-space/requirements.txt && python hf-space/app.py`。

## 30 秒上手（fresh clone 即可跑）

以下全部随仓库内置，无需下载：

```bash
python examples/quickstart.py        # mock 全流程：检测 → 校验 → smoke 训练 → agent → 报告
```

想跑真实模型？模型就在仓库里（Ultralytics backend 需要 `train` extra 提供 ONNX Runtime）：

```bash
pip install -e ".[dev,train]"      # 补上 ultralytics + onnxruntime（CPU 轮子）
```

```bash
# 解压内置合成数据集，用内置 ONNX 模型跑真实推理
python -c "
import zipfile; from pathlib import Path
tmp = Path('runs/bundled-demo'); tmp.mkdir(parents=True, exist_ok=True)
zipfile.ZipFile('assets/demo/synthetic-shapes-dataset.zip').extractall(tmp)
"
hokage-vision detect image runs/bundled-demo/dataset/images/val/naruto_000.jpg \
  --backend ultralytics --model-path assets/demo/synthetic-shapes-yolov8n.onnx \
  --conf 0.5 --imgsz 320
# → {"label": "naruto", "confidence": 0.999}
```

<p align="center">
  <img src="examples/videos/demo.gif" alt="真实 ONNX 检测演示" width="480">
</p>

## Agent 实战（工具调用）

Agent 通过带 JSON Schema 的工具做规划，执行与 CLI/API 走同一套 `ToolRegistry`，没有平行代码路径：

```bash
hokage-vision agent run "批量识别 examples/images 文件夹里的目标"
# → tool_calls: detect_folder(examples/images) → status success，扫描 1 张图

hokage-vision agent run "帮我写一篇小说"
# → Agent 拒绝越界任务：只处理本项目的视觉、数据、标注、训练、评估、模型管理类任务
```

加 `--provider openai`（或 `langgraph`）即可把同一套工具暴露给 LLM 做 function calling，见 `docs/usage.md`。

文档站：<https://phoenix0531-sudo.github.io/Hokage_Vision_Agent/>

## 截图（真实 Qt 窗口）

<table>
  <tr>
    <td width="50%">
      <img src="docs/screenshots/gui_hero.png" alt="首页概览">
      <br><strong>首页概览</strong>
    </td>
    <td width="50%">
      <img src="docs/screenshots/gui_detect_hero.png" alt="图片检测">
      <br><strong>图片检测</strong> — mock 框 + 结果表
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="docs/screenshots/closed-loop-detection.png" alt="仓库内真实训练模型的检测效果图">
      <br><strong>闭环真实检测</strong> — 仓库内训练（合成数据 → yolov8n 微调 → ONNX 导出 → UltralyticsBackend 渲染），验证集 24/24 全对
    </td>
    <td width="50%">
      <img src="docs/screenshots/preview.png" alt="架构示意图">
      <br><strong>架构示意图</strong> — CLI / GUI / API → backends
    </td>
  </tr>
</table>

```bash
PYTHONPATH=src python scripts/capture_real_shots.py
PYTHONPATH=src python scripts/generate_evidence.py
```

演示类：`obito` / `naruto` / `gaara`（0.91 / 0.84 / 0.77），无需 GPU / 私有权重。
## 设计边界

- 默认 backend = **`mock`**，CI 与演示零权重
- 共享核心类型服务，CLI / API / GUI / Agent 共用
- 旧版 YOLOv5 独立 backend，不把 legacy 包拷进 `src/hokage_vision`

## 安装与快速用

```bash
git clone https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent.git
cd Hokage_Vision_Agent
python -m pip install -e ".[dev,api]"
pytest -q tests/unit tests/integration
hokage-vision --help
```

一条命令跑通全流程（mock 后端，无需 GPU / 权重 / 网络）：

```bash
python examples/quickstart.py
```

想看真实模型？一条命令在仓库内完成训练 + 推理闭环：

```bash
# 合成数据 → yolov8n CPU 微调 → ONNX 导出 → UltralyticsBackend 检测
python scripts/closed_loop_demo.py --epochs 40
# 输出示例： naruto  conf=1.00 box=(34,55,185,169)  （验证集 24/24 全对）
```

Docker：

```bash
docker compose build
docker compose run --rm test
```

## 包结构

`src/hokage_vision/{vision,agents,api,cli,data,training,config,reports}`。  
控制台入口：`hokage-vision`。

## 测试与 CI

- 产品 CI：Python 3.12 + `pip install -e ".[dev,api]"` + unit/integration
- GUI / Docker / package / docs 为独立 workflow

## 范围

- **做：** 多表面检测工作台、Agent 工具层、数据集/训练脚手架、可复现 mock 证据
- **不做：** 内容审核 SaaS、无自有数据的 SOTA 保证、私有权重入库

## 许可证

Apache-2.0。见 [LICENSE](LICENSE) 与 `THIRD_PARTY_NOTICES.md`。
