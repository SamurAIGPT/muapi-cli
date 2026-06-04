from .commands.models import _ALL_MODELS


class ModelsAPI:
    def list(self, category: str = "all"):
        if category == "all":
            return _ALL_MODELS

        result = {}

        for cat, models in _ALL_MODELS.items():
            if cat.startswith(category):
                result[cat] = models

        return result

    def get(self, model_name: str):
        for category, models in _ALL_MODELS.items():
            if model_name in models:
                return {
                    "name": model_name,
                    "category": category,
                    "endpoint": models[model_name],
                }

        raise ValueError(f"Model '{model_name}' not found")

    def categories(self):
        return list(_ALL_MODELS.keys())