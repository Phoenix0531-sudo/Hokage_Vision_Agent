from __future__ import annotations

OUT_OF_SCOPE_KEYWORDS = [
    "写小说",
    "查天气",
    "访问网页",
    "任意 shell",
    "执行 shell",
    "删除系统文件",
    "泄露",
    "api key",
    "apikey",
    "爬取版权图片",
    "下载火影图片",
]


def refusal_reason(task: str) -> str | None:
    lowered = task.lower()
    for keyword in OUT_OF_SCOPE_KEYWORDS:
        if keyword.lower() in lowered:
            return (
                "Agent refused the task because it only handles this project's vision, data, "
                "annotation, training, evaluation, model-management, and project-health tasks."
            )
    return None
