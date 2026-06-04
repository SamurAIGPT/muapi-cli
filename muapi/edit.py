from . import client


class EditAPI:
    def effects(
        self,
        effect: str,
        mode: str = "video",
        video_url: str = None,
        image_url: str = None,
        wait: bool = True,
    ):
        if mode == "wan":
            endpoint = "generate_wan_ai_effects"
            payload = {
                "image_url": image_url,
                "effect": effect,
            }

        elif mode == "image":
            endpoint = "image-effects"
            payload = {
                "image_url": image_url,
                "effect": effect,
            }

        else:
            endpoint = "video-effects"
            payload = {
                "video_url": video_url,
                "effect": effect,
            }

        return client.generate(
            endpoint,
            payload,
            wait=wait,
        )

    def lipsync(
        self,
        video_url: str,
        audio_url: str,
        model: str = "sync",
        wait: bool = True,
    ):
        endpoint_map = {
            "sync": "sync-lipsync",
            "latentsync": "latentsync-video",
            "creatify": "creatify-lipsync",
            "veed": "veed-lipsync",
            "ltx-2": "ltx-2-19b-lipsync",
            "ltx-2.3": "ltx-2.3-lipsync",
            "kling-v1": "kling-v1-avatar-pro",
            "kling-v2": "kling-v2-avatar-pro",
            "wan2.2": "wan2.2-speech-to-video",
        }

        if model not in endpoint_map:
            raise ValueError(f"Unknown model: {model}")

        return client.generate(
            endpoint_map[model],
            {
                "video_url": video_url,
                "audio_url": audio_url,
            },
            wait=wait,
        )

    def dance(
        self,
        image_url: str,
        video_url: str,
        wait: bool = True,
    ):
        return client.generate(
            "ai-dance-effects",
            {
                "image_url": image_url,
                "video_url": video_url,
            },
            wait=wait,
        )

    def dress(
        self,
        image_url: str,
        dress_url: str,
        wait: bool = True,
    ):
        return client.generate(
            "ai-dress-change",
            {
                "model_image_url": image_url,
                "garment_image_url": dress_url,
            },
            wait=wait,
        )

    def clipping(
        self,
        video_url: str,
        num_highlights: int = 3,
        aspect_ratio: str = "9:16",
        wait: bool = True,
    ):
        return client.generate(
            "ai-clipping",
            {
                "video_url": video_url,
                "num_highlights": num_highlights,
                "aspect_ratio": aspect_ratio,
            },
            wait=wait,
        )