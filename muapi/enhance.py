from . import client


class EnhanceAPI:
    def upscale(
        self,
        image_url: str,
        wait: bool = True,
    ):
        return client.generate(
            "ai-image-upscale",
            {"image_url": image_url},
            wait=wait,
        )

    def remove_background(
        self,
        image_url: str,
        wait: bool = True,
    ):
        return client.generate(
            "ai-background-remover",
            {"image_url": image_url},
            wait=wait,
        )

    def face_swap(
        self,
        source_url: str,
        target_url: str,
        mode: str = "image",
        wait: bool = True,
    ):
        endpoint = (
            "ai-video-face-swap"
            if mode == "video"
            else "ai-image-face-swap"
        )

        return client.generate(
            endpoint,
            {
                "source_url": source_url,
                "target_url": target_url,
            },
            wait=wait,
        )

    def skin(
        self,
        image_url: str,
        wait: bool = True,
    ):
        return client.generate(
            "ai-skin-enhancer",
            {"image_url": image_url},
            wait=wait,
        )

    def colorize(
        self,
        image_url: str,
        wait: bool = True,
    ):
        return client.generate(
            "ai-color-photo",
            {"image_url": image_url},
            wait=wait,
        )

    def ghibli(
        self,
        image_url: str,
        wait: bool = True,
    ):
        return client.generate(
            "ai-ghibli-style",
            {"image_url": image_url},
            wait=wait,
        )

    def anime(
        self,
        image_url: str,
        prompt: str = "",
        wait: bool = True,
    ):
        return client.generate(
            "ai-anime-generator",
            {
                "image_url": image_url,
                "prompt": prompt,
            },
            wait=wait,
        )

    def extend(
        self,
        image_url: str,
        wait: bool = True,
    ):
        return client.generate(
            "ai-image-extension",
            {"image_url": image_url},
            wait=wait,
        )

    def product_shot(
        self,
        image_url: str,
        background_prompt: str = "",
        wait: bool = True,
    ):
        return client.generate(
            "ai-product-shot",
            {
                "image_url": image_url,
                "scene_description": background_prompt,
            },
            wait=wait,
        )

    def erase(
        self,
        image_url: str,
        mask_url: str,
        wait: bool = True,
    ):
        return client.generate(
            "ai-object-eraser",
            {
                "image_url": image_url,
                "mask_image_url": mask_url,
            },
            wait=wait,
        )