# iPhone Mockup Generator

Create pixel-perfect iPhone mockups by placing screenshots inside Apple device frames.

[![CI](https://github.com/weirdapps/mockups/actions/workflows/ci.yml/badge.svg)](https://github.com/weirdapps/mockups/actions/workflows/ci.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=weirdapps_mockups&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=weirdapps_mockups)
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## What It Does

Drop a screenshot in, get a polished device mockup out — in one command.

The generator places your screenshot precisely inside a high-resolution iPhone frame PNG and applies a **flood-fill masking algorithm** so the content stays strictly within the curved screen area. No bleeding through rounded corners, no manual cropping.

**Input:** any PNG or JPG screenshot
**Output:** full-resolution PNG with a transparent background, ready for presentations, App Store previews, or design hand-offs

## How the Masking Works

Device frame PNGs have **two** transparent regions: the outer rounded corners and the inner screen area. A naive alpha check would bleed content through both. The flood-fill algorithm starts from the screen center and expands only through the connected inner transparent region — producing a pixel-accurate screen mask that respects every curve.

## Installation

### CLI (recommended)

```bash
pipx install git+https://github.com/weirdapps/mockups.git
```

Install `pipx` first if needed: `brew install pipx`

### Library / development

```bash
pip install git+https://github.com/weirdapps/mockups.git
```

## Usage

### Command line

```bash
# Default frame (iPhone 16 Pro Max Black Titanium)
mockup screenshot.png

# Custom output path
mockup screenshot.png mockup.png

# Choose a specific frame
mockup screenshot.png --frame 16_pro_black

# List all available frames
mockup --list-frames
```

### Python API

```python
from mockups import create_mockup

output = create_mockup(
    screenshot_path="screenshot.png",
    output_path="mockup.png",
    frame_key="16_pro_max_black",  # default
)
print(f"Saved to: {output}")
```

## Available Frames

| Key | Device |
|-----|--------|
| `16_pro_max_black` | iPhone 16 Pro Max — Black Titanium **(default)** |
| `16_pro_max_natural` | iPhone 16 Pro Max — Natural Titanium |
| `16_pro_max_white` | iPhone 16 Pro Max — White Titanium |
| `16_pro_max_desert` | iPhone 16 Pro Max — Desert Titanium |
| `16_pro_black` | iPhone 16 Pro — Black Titanium |
| `16_pro_natural` | iPhone 16 Pro — Natural Titanium |

## Input & Output

| | Details |
|---|---|
| **Input formats** | PNG, JPG (any resolution — auto-resized with LANCZOS) |
| **Best input** | Clean screenshots without existing frame artifacts |
| **Output format** | PNG with transparent background |
| **Pro Max resolution** | 1520 × 3068 px |
| **Pro resolution** | 1406 × 2822 px |

## Development

```bash
git clone https://github.com/weirdapps/mockups.git
cd mockups
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
pytest
```

The project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting, [mypy](https://mypy.readthedocs.io/) for type-checking, and [pre-commit](https://pre-commit.com/) hooks to keep everything consistent. CI runs lint then tests on every push and PR.

## Acknowledgments

Device frame images are based on Apple's publicly available product imagery. iPhone is a trademark of Apple Inc., registered in the U.S. and other countries. This project is not affiliated with or endorsed by Apple.

Built with [Pillow](https://pillow.readthedocs.io/) and [NumPy](https://numpy.org/).

## License

[MIT](LICENSE)
