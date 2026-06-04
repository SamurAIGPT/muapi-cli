from . import client


class AudioAPI:
    def create(
        self,
        prompt: str,
        title: str = "",
        tags: str = "",
        instrumental: bool = False,
        wait: bool = True,
    ):
        payload = {
            "prompt": prompt,
            "title": title,
            "tags": tags,
            "make_instrumental": instrumental,
        }

        return client.generate(
            "suno-create-music",
            payload,
            wait=wait,
        )

    def remix(
        self,
        song_id: str,
        prompt: str = "",
        title: str = "",
        tags: str = "",
        wait: bool = True,
    ):
        payload = {
            "song_id": song_id,
            "prompt": prompt,
            "title": title,
            "tags": tags,
        }

        return client.generate(
            "suno-remix-music",
            payload,
            wait=wait,
        )

    def extend(
        self,
        song_id: str,
        prompt: str = "",
        continue_at: float = 0,
        wait: bool = True,
    ):
        payload = {
            "song_id": song_id,
            "prompt": prompt,
            "continue_at": continue_at,
        }

        return client.generate(
            "suno-extend-music",
            payload,
            wait=wait,
        )

    def from_text(
        self,
        prompt: str,
        duration: float = 10.0,
        wait: bool = True,
    ):
        payload = {
            "prompt": prompt,
            "duration": duration,
        }

        return client.generate(
            "mmaudio-v2/text-to-audio",
            payload,
            wait=wait,
        )

    def from_video(
        self,
        video_url: str,
        prompt: str = "",
        wait: bool = True,
    ):
        payload = {
            "video_url": video_url,
            "prompt": prompt,
        }

        return client.generate(
            "mmaudio-v2/video-to-video",
            payload,
            wait=wait,
        )