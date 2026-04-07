# iPhone Mockup Generator

Create pixel-perfect iPhone mockups by placing screenshots inside Apple device frames.

Uses a **flood-fill masking algorithm** to ensure content only appears within the screen area -- no leaking through rounded corners.

![Python](https://img.shields.io/badge/python-3.9+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## How It Works

The device frame PNGs have **two** transparent regions: the outer rounded corners and the inner screen area. A simple alpha check would bleed content through the corners. Instead, flood-fill starts from the screen center and finds only the connected inner transparent region, creating a precise mask.

## Quick Start

```bash
pip install pillow numpy
python iphone_mockup.py screenshot.png
```

Output: `screenshot_mockup.png` in the same directory.

## Usage

```bash
# Basic (default: iPhone 16 Pro Max Black Titanium)
python iphone_mockup.py screenshot.png

# Custom output path
python iphone_mockup.py screenshot.png mockup.png

# Different frame
python iphone_mockup.py screenshot.png --frame 16_pro_black

# List available frames
python iphone_mockup.py --list-frames
```

### Python API

```python
from iphone_mockup import create_mockup

output = create_mockup(
    screenshot_path="screenshot.png",
    output_path="mockup.png",
    frame_key="16_pro_max_black"
)
```

## Available Frames

| Key | Device |
|-----|--------|
| `16_pro_max_black` | iPhone 16 Pro Max - Black Titanium **(default)** |
| `16_pro_max_natural` | iPhone 16 Pro Max - Natural Titanium |
| `16_pro_max_white` | iPhone 16 Pro Max - White Titanium |
| `16_pro_max_desert` | iPhone 16 Pro Max - Desert Titanium |
| `16_pro_black` | iPhone 16 Pro - Black Titanium |
| `16_pro_natural` | iPhone 16 Pro - Natural Titanium |

## Input Requirements

- **Format**: PNG or JPG (any size, automatically resized)
- **Best results**: Use clean screenshots without existing frame artifacts

## Output

- **Format**: PNG with transparent background
- **Resolution**: Full frame dimensions (1520x3068 for Pro Max, 1406x2822 for Pro)

## Tests

```bash
pip install pytest
pytest test_iphone_mockup.py
```

## License

MIT
