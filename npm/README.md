# muapi CLI

Official command-line interface for [muapi.ai](https://muapi.ai) — generate images, videos, and audio directly from your terminal.

## Install

```bash
pip install muapi-cli
# or with pipx (recommended)
pipx install muapi-cli
```

## Quick Start

```bash
# 1. Set your API key (stored securely in OS keychain)
muapi auth configure

# 2. Generate an image
muapi image generate "a cyberpunk city at night" --model flux-dev

# 3. Generate a video
muapi video generate "a dog running on a beach" --model kling-master

# 4. Create music
muapi audio create "upbeat lo-fi hip hop for studying"

# 5. Wait for an existing job
muapi predict wait <request_id>
```

## Commands

### `muapi auth`
| Command | Description |
|---------|-------------|
| `muapi auth configure` | Save your API key |
| `muapi auth whoami` | Show current API key (masked) |
| `muapi auth logout` | Remove stored API key |

### `muapi image`
| Command | Description |
|---------|-------------|
| `muapi image generate <prompt>` | Text-to-image generation |
| `muapi image edit <prompt> --image <url>` | Image-to-image editing |
| `muapi image models` | List available models |

**Models:** `flux-dev`, `flux-schnell`, `flux-kontext-dev/pro/max`, `hidream-fast/dev/full`, `wan2.1`, `reve`, `gpt4o`, `midjourney`, `seedream`, `qwen`

### `muapi video`
| Command | Description |
|---------|-------------|
| `muapi video generate <prompt>` | Text-to-video generation |
| `muapi video from-image <prompt> --image <url>` | Image-to-video animation |
| `muapi video models` | List available models |

**Models:** `veo3`, `veo3-fast`, `kling-master`, `kling-std`, `kling-pro`, `wan2.1/2.2`, `seedance-pro/lite`, `hunyuan`, `runway`, `pixverse`, `vidu`, `minimax-std/pro`

### `muapi audio`
| Command | Description |
|---------|-------------|
| `muapi audio create <prompt>` | Create music with Suno |
| `muapi audio remix <song-id>` | Remix an existing Suno song |
| `muapi audio extend <song-id>` | Extend a Suno song |
| `muapi audio from-text <prompt>` | Generate audio with MMAudio |
| `muapi audio from-video <video-url>` | Add AI audio to a video |

### `muapi enhance`
| Command | Description |
|---------|-------------|
| `muapi enhance upscale <url>` | AI image upscaling |
| `muapi enhance bg-remove <url>` | Remove background |
| `muapi enhance face-swap --source <url> --target <url>` | Face swap image/video |
| `muapi enhance skin <url>` | Skin enhancement |
| `muapi enhance colorize <url>` | Colorize B&W photo |
| `muapi enhance ghibli <url>` | Ghibli anime style |
| `muapi enhance anime <url>` | Anime style conversion |
| `muapi enhance extend <url>` | Outpaint/extend image |
| `muapi enhance product-shot <url>` | Professional product photo |
| `muapi enhance erase <url> --mask <url>` | Object removal |

### `muapi edit`
| Command | Description |
|---------|-------------|
| `muapi edit effects --video <url> --effect <name>` | AI video/image effects |
| `muapi edit lipsync --video <url> --audio <url>` | Lip sync to audio |
| `muapi edit dance --image <url> --video <url>` | Make person dance |
| `muapi edit dress --image <url>` | Change clothing |
| `muapi edit clipping <video-url>` | AI highlight extraction |

### `muapi predict`
| Command | Description |
|---------|-------------|
| `muapi predict result <id>` | Fetch current status (no polling) |
| `muapi predict wait <id>` | Wait until complete |

### `muapi upload`
| Command | Description |
|---------|-------------|
| `muapi upload file <path>` | Upload a local file → get hosted URL |

## Global Options

| Flag | Description |
|------|-------------|
| `--wait / --no-wait` | Poll until done (default: `--wait`) |
| `--output-json` / `-j` | Print raw JSON response |
| `--download <dir>` / `-d` | Auto-download outputs to directory |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `MUAPI_API_KEY` | API key (overrides keychain/config) |
| `MUAPI_BASE_URL` | Override API base URL |

## Examples

```bash
# Generate with specific size and download result
muapi image generate "sunset over mountains" \
  --model hidream-fast --width 1280 --height 720 \
  --download ./outputs

# Animate an image, no wait (get request_id immediately)
muapi video from-image "camera slowly zooms in" \
  --image https://example.com/photo.jpg \
  --model kling-pro --no-wait

# Check status later
muapi predict result <request_id>

# Upload a local file then use it
URL=$(muapi upload file ./my-photo.jpg --output-json | jq -r '.url')
muapi enhance face-swap --source "$URL" --target https://example.com/target.jpg

# CI/CD: use JSON output + jq
muapi image generate "product on white background" \
  --model flux-dev --output-json | jq '.outputs[0]'
```

## Shell Completions

```bash
# bash
muapi --install-completion bash

# zsh
muapi --install-completion zsh

# fish
muapi --install-completion fish
```
