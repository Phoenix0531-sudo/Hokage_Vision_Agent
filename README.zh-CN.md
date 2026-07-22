# Hokage Vision Agent

**动漫角色检测工作台（YOLO + PySide6）**

[English](README.md) | [中文](README.zh-CN.md)

![CI](https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

面向**动漫角色检测**的 Agent 工作台：YOLO 系模型、PySide6 桌面流程、`configs/` 配置、`apps/` 应用入口。

## 为什么做这个

粉丝 / 科研 CV 演示需要的不只是 notebook：模型配置、桌面标注/推理 UI、非 GUI 部分的 CI。

## 功能

- `apps/` 多应用布局  
- `configs/` 实验配置  
- `assets/` / `examples/` 演示  
- 多套 requirements（api / desktop-build / docker）  

## 安装

```bash
git clone https://github.com/Phoenix0531-sudo/Hokage_Vision_Agent.git
cd Hokage_Vision_Agent
pip install -r requirements-api.txt
```

## 使用

按 `apps/` 入口与 `docs/` 选择桌面或 API 路径。

## 目录结构

```
apps/ configs/ assets/ examples/ models/ data/
docs/
```

## 许可证

MIT。可在署名前提下商用。见 [LICENSE](LICENSE)。
