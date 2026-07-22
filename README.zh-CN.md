# Hokage Vision Agent

**Agent 风格动漫角色检测工作台：YOLO、PySide6、Docker、工具工作流。**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

桌面 + API。配置驱动实验。CI 硬化的打包布局。

## 预览

![Hokage Vision Agent](docs/screenshots/preview.png)

## 功能

- 面向动漫角色的 YOLO 系检测管线
- apps/ 下 PySide6 桌面流程
- configs/ 配置驱动运行
- Hatch src/hokage_vision 布局，CI 可编辑安装
- unit + integration；GUI 走独立 workflow

## 快速开始

### 安装

```bash
git clone https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent.git
cd Hokage_Vision_Agent
python -m pip install -e ".[dev,api]"
```

### 使用

```bash
python -c "import hokage_vision; print('ok')"
pytest -q tests/unit tests/integration
```

## 项目结构

```
src/hokage_vision/
apps/  configs/  examples/  models/
tests/{unit,integration,gui,packaging}
```

## 说明

作品集级 CV 工作台，不是生产内容审核系统。

## 许可证

Apache-2.0。在注明出处的前提下可商业使用（以 LICENSE 为准）。详见 [LICENSE](LICENSE)。
