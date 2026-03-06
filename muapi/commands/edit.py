"""muapi edit — video editing effects, lipsync, dance, dress-change."""
from typing import Optional

import typer

from .. import client
from ..utils import console, download_outputs, error_exit, print_result, spinner_status

app = typer.Typer(help="Edit videos with effects, lipsync, dance, dress-change, and more.")


def _run(label: str, endpoint: str, payload: dict, wait: bool, download: Optional[str], output_json: bool):
    try:
        with spinner_status(f"{label}..."):
            result = client.generate(endpoint, payload, wait=wait)
    except client.MuapiError as e:
        error_exit(str(e))
    print_result(result, output_json, label=label)
    if download and result.get("status") == "completed":
        download_outputs(result, download)


@app.command("effects")
def effects(
    video_url: str = typer.Option(None, "--video", "-v", help="Source video URL (for video effects)"),
    image_url: str = typer.Option(None, "--image", "-i", help="Source image URL (for image/wan effects)"),
    effect: str = typer.Option(..., "--effect", "-e", help="Effect name/prompt"),
    mode: str = typer.Option("video", "--mode", "-m", help="'video', 'image', or 'wan'"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Apply AI effects to a video or image."""
    if mode == "wan":
        if not image_url:
            error_exit("--image required for wan effects mode")
        payload = {"image_url": image_url, "effect": effect}
        _run("Applying WAN effects", "generate_wan_ai_effects", payload, wait, download, output_json)
    elif mode == "image":
        if not image_url:
            error_exit("--image required for image effects mode")
        payload = {"image_url": image_url, "effect": effect}
        _run("Applying image effects", "image-effects", payload, wait, download, output_json)
    else:
        if not video_url:
            error_exit("--video required for video effects mode")
        payload = {"video_url": video_url, "effect": effect}
        _run("Applying video effects", "video-effects", payload, wait, download, output_json)


@app.command("lipsync")
def lipsync(
    video_url: str = typer.Option(..., "--video", "-v", help="Source video URL"),
    audio_url: str = typer.Option(..., "--audio", "-a", help="Audio file URL"),
    model: str = typer.Option("sync", "--model", "-m", help="Model: sync, latentsync, creatify, veed"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Sync lip movements to audio."""
    endpoint_map = {
        "sync":       "lipsync",
        "latentsync": "latentsync",
        "creatify":   "creatify-lipsync",
        "veed":       "veed-lipsync",
    }
    if model not in endpoint_map:
        error_exit(f"Unknown lipsync model '{model}'. Choices: {', '.join(endpoint_map)}")
    payload = {"video_url": video_url, "audio_url": audio_url}
    _run(f"Lipsync ({model})", endpoint_map[model], payload, wait, download, output_json)


@app.command("dance")
def dance(
    image_url: str = typer.Option(..., "--image", "-i", help="Person image URL"),
    video_url: str = typer.Option(..., "--video", "-v", help="Dance reference video URL"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Make a person dance by referencing a dance video."""
    payload = {"image_url": image_url, "video_url": video_url}
    _run("Generating dance", "dance", payload, wait, download, output_json)


@app.command("dress")
def dress(
    image_url: str = typer.Option(..., "--image", "-i", help="Person image URL"),
    dress_url: str = typer.Option(None, "--dress", "-D", help="Dress/clothing image URL"),
    prompt: str = typer.Option("", "--prompt", "-p", help="Dress description prompt"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Change clothing/dress in an image."""
    payload: dict = {"image_url": image_url, "prompt": prompt}
    if dress_url:
        payload["dress_url"] = dress_url
    _run("Changing dress", "ai-dress-change", payload, wait, download, output_json)


@app.command("clipping")
def clipping(
    video_url: str = typer.Argument(..., help="Source video URL"),
    num_highlights: int = typer.Option(3, "--highlights", "-n", help="Number of highlight clips"),
    aspect_ratio: str = typer.Option("9:16", "--aspect-ratio", "-a"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """AI-powered video clipping — extract the best highlights."""
    payload = {
        "video_url": video_url,
        "num_highlights": num_highlights,
        "aspect_ratio": aspect_ratio,
    }
    _run("AI clipping", "ai-clipping", payload, wait, download, output_json)
