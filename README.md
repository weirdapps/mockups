# iPhone Mockup Generator

Pixel-perfect iPhone mockups from any screenshot, in one command. The screenshot is composited inside a bundled Apple device frame PNG using a flood-fill masking algorithm, so content stays strictly inside the curved screen area with no bleeding through the rounded corners.

[![CI](https://github.com/weirdapps/mockups/actions/workflows/ci.yml/badge.svg)](https://github.com/weirdapps/mockups/actions/workflows/ci.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=weirdapps_mockups&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=weirdapps_mockups)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## What it does

You give it a clean screenshot (PNG or JPG, any resolution). It gives you back a full-resolution PNG with a transparent background, showing that screenshot placed inside a real iPhone frame. Ready for presentations, App Store previews, marketing sites, or design hand-offs.

Six device frames ship inside the package, no runtime download or external asset directory required.

## Device frames

<table>
<tr>
  <td align="center"><img src="src/mockups/frames/16%20Pro%20Max%20-%20Black%20Titanium.png" width="140" alt="iPhone 16 Pro Max Black Titanium"><br><sub><code>16_pro_max_black</code><br>(default)</sub></td>
  <td align="center"><img src="src/mockups/frames/16%20Pro%20Max%20-%20Natural%20Titanium.png" width="140" alt="iPhone 16 Pro Max Natural Titanium"><br><sub><code>16_pro_max_natural</code></sub></td>
  <td align="center"><img src="src/mockups/frames/16%20Pro%20Max%20-%20White%20Titanium.png" width="140" alt="iPhone 16 Pro Max White Titanium"><br><sub><code>16_pro_max_white</code></sub></td>
  <td align="center"><img src="src/mockups/frames/16%20Pro%20Max%20-%20Desert%20Titanium.png" width="140" alt="iPhone 16 Pro Max Desert Titanium"><br><sub><code>16_pro_max_desert</code></sub></td>
  <td align="center"><img src="src/mockups/frames/16%20Pro%20-%20Black%20Titanium.png" width="120" alt="iPhone 16 Pro Black Titanium"><br><sub><code>16_pro_black</code></sub></td>
  <td align="center"><img src="src/mockups/frames/16%20Pro%20-%20Natural%20Titanium.png" width="120" alt="iPhone 16 Pro Natural Titanium"><br><sub><code>16_pro_natural</code></sub></td>
</tr>
</table>

Pro Max frames output at 1520 x 3068 px. Pro frames output at 1406 x 2822 px.

## How the masking works

A device frame PNG has two transparent regions: the outer rounded corners (outside the phone body) and the inner screen area. A naive alpha check would let the screenshot bleed through both. Instead, `_flood_fill_screen_mask` in `src/mockups/core.py` seeds a BFS from the center of the frame and expands only through the connected inner transparent region, producing a pixel-accurate screen mask that respects every curve. The screenshot is resized to the frame's content rectangle with LANCZOS resampling, masked, then alpha-composited under the frame overlay.

## Installation

For everyday use, install the CLI in an isolated environment with pipx:

```bash
pipx install git+https://github.com/weirdapps/mockups.git
```

(Install pipx first if needed: `brew install pipx`.)

For use as a library or for development:

```bash
pip install git+https://github.com/weirdapps/mockups.git
```

Requires Python 3.9 or newer. Dependencies (Pillow and NumPy) are pulled in automatically.

## Usage

### Command line

```bash
# Default frame (iPhone 16 Pro Max Black Titanium),
# writes screenshot_mockup.png next to the input.
mockup screenshot.png

# Explicit output path.
mockup screenshot.png out.png

# Pick a specific frame.
mockup screenshot.png --frame 16_pro_black

# List every available frame.
mockup --list-frames

# Point at a custom directory of frame PNGs
# (must contain the filenames listed by --list-frames).
mockup screenshot.png --frames-dir /path/to/frames
```

Full flag reference:

| Flag | Description |
|---|---|
| `screenshot` (positional) | Path to the input screenshot (PNG or JPG). |
| `output` (positional, optional) | Output path. Defaults to `<screenshot-stem>_mockup.png` in the same directory. |
| `--frame`, `-f` | Frame key to use. Choices come from the six bundled frames. Default: `16_pro_max_black`. |
| `--list-frames` | Print the available frame keys and their PNG filenames, then exit. |
| `--frames-dir` | Override the bundled frames directory (advanced). |

### Python API

```python
from mockups import create_mockup, FRAMES, DEFAULT_FRAME

output = create_mockup(
    screenshot_path="screenshot.png",
    output_path="mockup.png",     # optional
    frame_key="16_pro_max_black", # optional, defaults to DEFAULT_FRAME
    frames_dir=None,              # optional override
)
print(f"Saved: {output}")

# Enumerate frames programmatically.
for key, cfg in FRAMES.items():
    print(key, cfg["path"])
```

`create_mockup` raises `ValueError` for an unknown `frame_key` and `FileNotFoundError` for a missing screenshot or missing frame PNG.

## Input and output

| | Details |
|---|---|
| Input formats | PNG, JPG (any resolution, resized with LANCZOS to fit the frame's content rectangle). |
| Best input | Clean screenshots with no existing device chrome or frame artifacts. |
| Output format | PNG with a transparent background (RGBA). |
| Default output name | `<input-stem>_mockup.png`, written next to the input. |
| Pro Max output size | 1520 x 3068 px. |
| Pro output size | 1406 x 2822 px. |

## Architecture

```text
src/mockups/
  __init__.py          Public API: create_mockup, FRAMES, DEFAULT_FRAME.
  core.py              Flood-fill masking, frame registry, image composition.
  cli.py               argparse CLI entry point (mockup).
  frames/              Six bundled iPhone 16 Pro / Pro Max PNGs.
tests/
  test_mockup.py       CLI, frame registry, and end-to-end composition tests.
```

Add a new frame by dropping its PNG into `src/mockups/frames/` and adding an entry to the `FRAMES` dict in `core.py` with the four content-rectangle coordinates (`content_left`, `content_top`, `content_right`, `content_bottom`).

## Development

```bash
git clone https://github.com/weirdapps/mockups.git
cd mockups
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
pip install pytest
pytest
```

The project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting, and [pre-commit](https://pre-commit.com/) hooks that also run mypy, gitleaks, yamllint, and markdownlint. CI (`.github/workflows/ci.yml`) runs `ruff check` and `ruff format --check`, then `pytest`, on every push and PR to `master`.

Install the hooks locally with:

```bash
pip install pre-commit && pre-commit install
```

## License

[MIT](LICENSE). Copyright (c) 2026 Dimitrios Plessas.

## Acknowledgments

Device frame images are based on Apple's publicly available product imagery. iPhone is a trademark of Apple Inc., registered in the U.S. and other countries. This project is not affiliated with or endorsed by Apple.

Built with [Pillow](https://pillow.readthedocs.io/) and [NumPy](https://numpy.org/).
