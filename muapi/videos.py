from . import client
from .commands.video import (
    T2V_MODELS,
    I2V_MODELS,
    LIST_INPUT_I2V,
)


class VideosAPI:
    def generate(
        self,
        prompt: str,
        model: str = "kling-master",
        wait: bool = True,
        duration: int = 5,
        aspect_ratio: str = "16:9",
    ):
        if model not in T2V_MODELS:
            raise ValueError(f"Unknown model: {model}")

        endpoint = T2V_MODELS[model]

        payload = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
        }

        return client.generate(
            endpoint,
            payload,
            wait=wait,
        )

    def from_image(
        self,
        prompt: str,
        image: str,
        model: str = "kling-std",
        wait: bool = True,
        duration: int = 5,
        aspect_ratio: str = "16:9",
    ):
        if model not in I2V_MODELS:
            raise ValueError(f"Unknown model: {model}")

        endpoint = I2V_MODELS[model]

        payload = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
        }

        if model in LIST_INPUT_I2V:
            payload["images_list"] = [image]
        else:
            payload["image_url"] = image

        return client.generate(
            endpoint,
            payload,
            wait=wait,
        )