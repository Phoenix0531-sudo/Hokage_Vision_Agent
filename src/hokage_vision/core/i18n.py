TRANSLATIONS: dict[str, dict[str, str]] = {
    "en-US": {
        "app.title": "Hokage Vision Agent",
        "backend.mock": "Mock backend",
    },
    "zh-CN": {
        "app.title": "Hokage Vision Agent",
        "backend.mock": "Mock 后端",
    },
}


def translate(key: str, language: str = "zh-CN") -> str:
    return TRANSLATIONS.get(language, {}).get(key, key)
