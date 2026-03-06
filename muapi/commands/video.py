"""muapi video — text-to-video and image-to-video generation."""
from typing import Optional

import typer

from .. import client, exitcodes
from ..utils import (
    console, download_outputs, error_exit, print_result,
    print_dry_run, read_stdin_if_dash, spinner_status,
)

app = typer.Typer(help="Generate videos from text or images.")

T2V_MODELS = {
    "veo3":         "veo3-text-to-video",
    "veo3-fast":    "veo3-fast-text-to-video",
    "kling-master": "kling-master-text-to-video",
    "wan2.1":       "wan2.1-text-to-video",
    "wan2.2":       "wan2.2-text-to-video",
    "seedance-pro": "seedance-pro-text-to-video",
    "seedance-lite":"seedance-lite-text-to-video",
    "hunyuan":      "hunyuan-text-to-video",
    "runway":       "runway-text-to-video",
    "pixverse":     "pixverse-text-to-video",
    "vidu":         "vidu-text-to-video",
    "minimax-std":  "minimax-hailuo-02-std-text-to-video",
    "minimax-pro":  "minimax-hailuo-02-pro-text-to-video",
}

I2V_MODELS = {
    "veo3":         "veo3-image-to-video",
    "veo3-fast":    "veo3-fast-image-to-video",
    "kling-std":    "kling-std-image-to-video",
    "kling-pro":    "kling-pro-image-to-video",
    "kling-master": "kling-master-image-to-video",
    "wan2.1":       "wan2.1-image-to-video",
    "wan2.2":       "wan2.2-image-to-video",
    "seedance-pro": "seedance-pro-image-to-video",
    "seedance-lite":"seedance-lite-image-to-video",
    "hunyuan":      "hunyuan-image-to-video",
    "runway":       "runway-image-to-video",
    "pixverse":     "pixverse-image-to-video",
    "vidu":         "vidu-image-to-video",
    "midjourney":   "midjourney-image-to-video",
    "minimax-std":  "minimax-hailuo-02-std-image-to-video",
    "minimax-pro":  "minimax-hailuo-02-pro-image-to-video",
}


@app.command("generate")
def generate(
    prompt: str = typer.Argument(..., help="Text prompt. Pass '-' to read from stdin."),
    model: str  = typer.Option("kling-master", "--model", "-m",
                               help=f"Model. Choices: {', '.join(T2V_MODELS)}"),
    duration: int     = typer.Option(5, "--duration", "-D", help="Duration in seconds"),
    aspect_ratio: str = typer.Option("16:9", "--aspect-ratio", "-a"),
    webhook: Optional[str] = typer.Option(None, "--webhook"),
    wait: bool    = typer.Option(True, "--wait/--no-wait"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
    jq: Optional[str] = typer.Option(None, "--jq"),
):
    """Generate a video from a text prompt.

    \b
    Examples:
      muapi video generate "a dog running on a beach" --model kling-master
      muapi video generate "ocean waves" --no-wait --output-json --jq '.request_id'
    """
    prompt = read_stdin_if_dash(prompt)
    if model not in T2V_MODELS:
        error_exit(f"Unknown model '{model}'. Choices: {', '.join(T2V_MODELS)}", exitcodes.VALIDATION)
    endpoint = T2V_MODELS[model]

    payload: dict = {"prompt": prompt, "duration": duration, "aspect_ratio": aspect_ratio}
    if webhook:
        payload["webhook_url"] = webhook

    if dry_run:
        print_dry_run(endpoint, payload)
        return

    try:
        with spinner_status(f"Generating video with {model}... (may take a while)"):
            result = client.generate(endpoint, payload, wait=wait)
    except client.MuapiError as e:
        error_exit(str(e), e.exit_code)

    print_result(result, output_json, label=f"Video ({model})", jq=jq)
    if download and result.get("status") == "completed":
        download_outputs(result, download)


@app.command("from-image")
def from_image(
    prompt: str = typer.Argument(..., help="Motion/animation prompt. Pass '-' for stdin."),
    image: str  = typer.Option(..., "--image", "-i", help="Source image URL"),
    model: str  = typer.Option("kling-std", "--model", "-m",
                               help=f"Model. Choices: {', '.join(I2V_MODELS)}"),
    duration: int     = typer.Option(5, "--duration", "-D"),
    aspect_ratio: str = typer.Option("16:9", "--aspect-ratio", "-a"),
    webhook: Optional[str] = typer.Option(None, "--webhook"),
    wait: bool    = typer.Option(True, "--wait/--no-wait"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
    jq: Optional[str] = typer.Option(None, "--jq"),
):
    """Animate an image into a video."""
    prompt = read_stdin_if_dash(prompt)
    if model not in I2V_MODELS:
        error_exit(f"Unknown model '{model}'. Choices: {', '.join(I2V_MODELS)}", exitcodes.VALIDATION)
    endpoint = I2V_MODELS[model]

    payload: dict = {
        "prompt": prompt, "image_url": image,
        "duration": duration, "aspect_ratio": aspect_ratio,
    }
    if webhook:
        payload["webhook_url"] = webhook

    if dry_run:
        print_dry_run(endpoint, payload)
        return

    try:
        with spinner_status(f"Animating image with {model}..."):
            result = client.generate(endpoint, payload, wait=wait)
    except client.MuapiError as e:
        error_exit(str(e), e.exit_code)

    print_result(result, output_json, label=f"Image-to-Video ({model})", jq=jq)
    if download and result.get("status") == "completed":
        download_outputs(result, download)


@app.command("models")
def list_models():
    """List all available video generation models."""
    from rich.table import Table
    from ..utils import out

    t = Table(title="Video Models", show_header=True, header_style="bold magenta")
    t.add_column("Name", style="cyan")
    t.add_column("Type")
    t.add_column("Endpoint")
    for name, ep in T2V_MODELS.items():
        t.add_row(name, "text-to-video", ep)
    for name, ep in I2V_MODELS.items():
        t.add_row(name, "image-to-video", ep)
    out.print(t)
