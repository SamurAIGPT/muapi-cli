"""muapi enhance — image/video enhancement tools."""
from typing import Optional

import typer

from .. import client
from ..utils import console, download_outputs, error_exit, print_result, spinner_status

app = typer.Typer(help="Enhance images and videos (upscale, bg-remove, face-swap, etc.).")


def _run(label: str, endpoint: str, payload: dict, wait: bool, download: Optional[str], output_json: bool):
    try:
        with spinner_status(f"{label}..."):
            result = client.generate(endpoint, payload, wait=wait)
    except client.MuapiError as e:
        error_exit(str(e))
    print_result(result, output_json, label=label)
    if download and result.get("status") == "completed":
        download_outputs(result, download)


@app.command("upscale")
def upscale(
    image_url: str = typer.Argument(..., help="Image URL to upscale"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Upscale an image with AI."""
    _run("Upscaling image", "ai-image-upscale", {"image_url": image_url}, wait, download, output_json)


@app.command("bg-remove")
def bg_remove(
    image_url: str = typer.Argument(..., help="Image URL"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Remove the background from an image."""
    _run("Removing background", "ai-background-remover", {"image_url": image_url}, wait, download, output_json)


@app.command("face-swap")
def face_swap(
    source_url: str = typer.Option(..., "--source", "-s", help="Source face image URL"),
    target_url: str = typer.Option(..., "--target", "-t", help="Target image or video URL"),
    mode: str = typer.Option("image", "--mode", "-m", help="'image' or 'video'"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Swap faces in an image or video."""
    payload = {"source_url": source_url, "target_url": target_url}
    if mode == "video":
        _run("Face swapping in video", "ai-video-face-swap", payload, wait, download, output_json)
    else:
        _run("Face swapping in image", "ai-image-face-swap", payload, wait, download, output_json)


@app.command("skin")
def skin(
    image_url: str = typer.Argument(..., help="Image URL"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Enhance skin quality in a portrait image."""
    _run("Enhancing skin", "ai-skin-enhancer", {"image_url": image_url}, wait, download, output_json)


@app.command("colorize")
def colorize(
    image_url: str = typer.Argument(..., help="Black & white image URL"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Colorize a black and white photo."""
    _run("Colorizing photo", "ai-color-photo", {"image_url": image_url}, wait, download, output_json)


@app.command("ghibli")
def ghibli(
    image_url: str = typer.Argument(..., help="Image URL"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Convert an image to Ghibli anime style."""
    _run("Applying Ghibli style", "ai-ghibli-style", {"image_url": image_url}, wait, download, output_json)


@app.command("anime")
def anime(
    image_url: str = typer.Argument(..., help="Image URL"),
    prompt: str = typer.Option("", "--prompt", "-p", help="Style prompt"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Convert an image to anime style."""
    _run("Generating anime style", "ai-anime-generator", {"image_url": image_url, "prompt": prompt}, wait, download, output_json)


@app.command("extend")
def extend(
    image_url: str = typer.Argument(..., help="Image URL to extend/outpaint"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Extend/outpaint an image."""
    _run("Extending image", "ai-image-extension", {"image_url": image_url}, wait, download, output_json)


@app.command("product-shot")
def product_shot(
    image_url: str = typer.Argument(..., help="Product image URL"),
    background_prompt: str = typer.Option("", "--bg", help="Background description"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Generate professional product photography."""
    payload = {"image_url": image_url, "background_prompt": background_prompt}
    _run("Generating product shot", "ai-product-shot", payload, wait, download, output_json)


@app.command("erase")
def erase(
    image_url: str = typer.Argument(..., help="Image URL"),
    mask_url: str = typer.Option(..., "--mask", "-m", help="Mask image URL (white = erase area)"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
):
    """Erase objects from an image using a mask."""
    payload = {"image_url": image_url, "mask_url": mask_url}
    _run("Erasing object", "ai-object-eraser", payload, wait, download, output_json)
