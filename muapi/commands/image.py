"""muapi image — text-to-image and image-to-image generation."""
from typing import Optional

import typer

from .. import client
from .. import exitcodes
from ..utils import (
    console, download_outputs, error_exit, print_result,
    print_dry_run, read_stdin_if_dash, spinner_status,
)

app = typer.Typer(help="Generate and edit images.")

# ── Model registries ───────────────────────────────────────────────────────────

T2I_MODELS = {
    "flux-dev":           "flux-dev-image",
    "flux-schnell":       "flux-schnell-image",
    "flux-kontext-dev":   "flux-kontext-dev-t2i",
    "flux-kontext-pro":   "flux-kontext-pro-t2i",
    "flux-kontext-max":   "flux-kontext-max-t2i",
    "hidream-fast":       "hidream_i1_fast_image",
    "hidream-dev":        "hidream_i1_dev_image",
    "hidream-full":       "hidream_i1_full_image",
    "wan2.1":             "wan2.1-text-to-image",
    "reve":               "reve-text-to-image",
    "gpt4o":              "gpt4o-text-to-image",
    "midjourney":         "midjourney-text-to-image",
    "seedream":           "seedream-text-to-image",
    "qwen":               "qwen-text-to-image",
}

I2I_MODELS = {
    "flux-kontext-dev":     "flux-kontext-dev-i2i",
    "flux-kontext-pro":     "flux-kontext-pro-i2i",
    "flux-kontext-max":     "flux-kontext-max-i2i",
    "flux-kontext-effects": "flux-kontext-effects",
    "gpt4o":                "gpt4o-image-to-image",
    "reve":                 "reve-image-edit",
    "seededit":             "seededit-image-edit",
    "midjourney":           "midjourney-image-to-image",
    "midjourney-style":     "midjourney-style-reference",
    "midjourney-omni":      "midjourney-omni-reference",
    "qwen":                 "qwen-image-to-image",
}


@app.command("generate")
def generate(
    prompt: str = typer.Argument(..., help="Text prompt. Pass '-' to read from stdin."),
    model: str = typer.Option("flux-dev", "--model", "-m",
                              help=f"Model. Choices: {', '.join(T2I_MODELS)}"),
    width: int       = typer.Option(1024, "--width", "-W"),
    height: int      = typer.Option(1024, "--height", "-H"),
    num_images: int  = typer.Option(1, "--num-images", "-n", min=1, max=4),
    aspect_ratio: str = typer.Option("1:1", "--aspect-ratio", "-a"),
    webhook: Optional[str] = typer.Option(None, "--webhook", help="Webhook URL for async notification"),
    wait: bool       = typer.Option(True, "--wait/--no-wait", help="Poll until done"),
    dry_run: bool    = typer.Option(False, "--dry-run", help="Show request without executing"),
    download: Optional[str] = typer.Option(None, "--download", "-d", help="Download outputs to directory"),
    output_json: bool = typer.Option(False, "--output-json", "-j", help="Print raw JSON"),
    jq: Optional[str] = typer.Option(None, "--jq", help="jq-style filter on JSON output (e.g. '.outputs[0]')"),
):
    """Generate an image from a text prompt.

    Pipe-friendly: pass '-' as PROMPT to read from stdin.

    \b
    Examples:
      muapi image generate "a cyberpunk city" --model flux-dev
      echo "a cat" | muapi image generate -
      muapi image generate "sunset" --model hidream-fast --download ./out
      muapi image generate "logo" --output-json --jq '.outputs[0]'
    """
    prompt = read_stdin_if_dash(prompt)
    if model not in T2I_MODELS:
        error_exit(f"Unknown model '{model}'. Choices: {', '.join(T2I_MODELS)}", exitcodes.VALIDATION)
    endpoint = T2I_MODELS[model]

    payload: dict = {"prompt": prompt, "num_images": num_images}
    if model.startswith("flux-kontext") or model in ("midjourney", "seedream", "qwen", "reve"):
        payload["aspect_ratio"] = aspect_ratio
    else:
        payload["width"] = width
        payload["height"] = height
    if webhook:
        payload["webhook_url"] = webhook

    if dry_run:
        print_dry_run(endpoint, payload)
        return

    try:
        with spinner_status(f"Generating image with {model}..."):
            result = client.generate(endpoint, payload, wait=wait)
    except client.MuapiError as e:
        error_exit(str(e), e.exit_code)

    print_result(result, output_json, label=f"Image ({model})", jq=jq)
    if download and result.get("status") == "completed":
        download_outputs(result, download)


@app.command("edit")
def edit(
    prompt: str = typer.Argument(..., help="Edit instruction. Pass '-' to read from stdin."),
    image: str  = typer.Option(..., "--image", "-i", help="Source image URL"),
    model: str  = typer.Option("flux-kontext-dev", "--model", "-m",
                               help=f"Model. Choices: {', '.join(I2I_MODELS)}"),
    aspect_ratio: str = typer.Option("1:1", "--aspect-ratio", "-a"),
    num_images: int   = typer.Option(1, "--num-images", "-n", min=1, max=4),
    webhook: Optional[str] = typer.Option(None, "--webhook"),
    wait: bool            = typer.Option(True, "--wait/--no-wait"),
    dry_run: bool         = typer.Option(False, "--dry-run"),
    download: Optional[str] = typer.Option(None, "--download", "-d"),
    output_json: bool = typer.Option(False, "--output-json", "-j"),
    jq: Optional[str] = typer.Option(None, "--jq"),
):
    """Edit an image using a prompt and reference image URL."""
    prompt = read_stdin_if_dash(prompt)
    if model not in I2I_MODELS:
        error_exit(f"Unknown model '{model}'. Choices: {', '.join(I2I_MODELS)}", exitcodes.VALIDATION)
    endpoint = I2I_MODELS[model]

    payload: dict = {"prompt": prompt, "aspect_ratio": aspect_ratio, "num_images": num_images}
    if model.startswith("flux-kontext"):
        payload["images_list"] = [image]
    else:
        payload["image_url"] = image
    if webhook:
        payload["webhook_url"] = webhook

    if dry_run:
        print_dry_run(endpoint, payload)
        return

    try:
        with spinner_status(f"Editing image with {model}..."):
            result = client.generate(endpoint, payload, wait=wait)
    except client.MuapiError as e:
        error_exit(str(e), e.exit_code)

    print_result(result, output_json, label=f"Image Edit ({model})", jq=jq)
    if download and result.get("status") == "completed":
        download_outputs(result, download)


@app.command("models")
def list_models():
    """List all available image generation and editing models."""
    from rich.table import Table
    from ..utils import out

    t = Table(title="Image Models", show_header=True, header_style="bold magenta")
    t.add_column("Name", style="cyan")
    t.add_column("Type")
    t.add_column("Endpoint")
    for name, ep in T2I_MODELS.items():
        t.add_row(name, "text-to-image", ep)
    for name, ep in I2I_MODELS.items():
        t.add_row(name, "image-to-image", ep)
    out.print(t)
