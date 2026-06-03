from . import client
from .commands.image import (
    T2I_MODELS,
    I2I_MODELS,
    LIST_INPUT_MODELS,
)


class ImagesAPI:
    def generate(
        self,
        prompt: str,
        model: str = "flux-dev",
        wait: bool = True,
        num_images: int = 1,
        width: int = 1024,
        height: int = 1024,
    ):
        if model not in T2I_MODELS:
            raise ValueError(f"Unknown model: {model}")

        endpoint = T2I_MODELS[model]

        payload = {
            "prompt": prompt,
            "num_images": num_images,
            "width": width,
            "height": height,
        }

        return client.generate(
            endpoint,
            payload,
            wait=wait,
        )

    def edit(
        self,
        prompt: str,
        image: str,
        model: str = "flux-kontext-dev",
        wait: bool = True,
        num_images: int = 1,
        aspect_ratio: str = "1:1",
    ):
        if model not in I2I_MODELS:
            raise ValueError(f"Unknown model: {model}")

        endpoint = I2I_MODELS[model]

        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "num_images": num_images,
        }

        if model in LIST_INPUT_MODELS:
            payload["images_list"] = [image]
        else:
            payload["image_url"] = image

        return client.generate(
            endpoint,
            payload,
            wait=wait,
        )