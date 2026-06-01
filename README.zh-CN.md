# Hokage Vision Agent

一个基于 YOLO、PySide6、Docker 与 Agent 工具编排的动漫角色检测工作台。

本项目是个人学习、研究与作品集展示项目，与《火影忍者》、集英社、Pierrot 或相关版权方无官方关联。

## 当前状态

仓库正在从早期 YOLOv5 + PySide6 项目迁移为工程化、可演示、可持续维护的开源作品集项目。

## Docker-first 快速开始

```bash
docker compose build
docker compose run --rm test
```

## 本地可选安装

```bash
python -m venv .venv
pip install -e ".[dev,gui,api,train]"
```

## 许可证

新写项目源码计划采用 Apache-2.0，但需要在 legacy YOLOv5 代码隔离和许可证审计完成后最终确认。旧 YOLOv5 代码遵循其上游许可证。
