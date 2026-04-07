"""
iPhone Mockup Generator - Core Logic

Creates pixel-perfect iPhone mockups using Apple device frames.
Uses flood-fill masking to ensure content only appears within the screen area.
"""

from collections import deque
from importlib.resources import files
from pathlib import Path

from PIL import Image
import numpy as np


# Frame configurations
# content_* defines where the screenshot content should be placed
FRAMES = {
    "16_pro_max_black": {
        "path": "16 Pro Max - Black Titanium.png",
        "content_left": 100,
        "content_top": 100,
        "content_right": 1419,
        "content_bottom": 2967,
    },
    "16_pro_max_natural": {
        "path": "16 Pro Max - Natural Titanium.png",
        "content_left": 100,
        "content_top": 100,
        "content_right": 1419,
        "content_bottom": 2967,
    },
    "16_pro_max_white": {
        "path": "16 Pro Max - White Titanium.png",
        "content_left": 100,
        "content_top": 100,
        "content_right": 1419,
        "content_bottom": 2967,
    },
    "16_pro_max_desert": {
        "path": "16 Pro Max - Desert Titanium.png",
        "content_left": 100,
        "content_top": 100,
        "content_right": 1419,
        "content_bottom": 2967,
    },
    "16_pro_black": {
        "path": "16 Pro - Black Titanium.png",
        "content_left": 75,
        "content_top": 100,
        "content_right": 1244,
        "content_bottom": 2693,
    },
    "16_pro_natural": {
        "path": "16 Pro - Natural Titanium.png",
        "content_left": 75,
        "content_top": 100,
        "content_right": 1244,
        "content_bottom": 2693,
    },
}

DEFAULT_FRAME = "16_pro_max_black"


def _flood_fill_screen_mask(alpha, start_x, start_y, threshold=50):
    """
    Create a screen mask by flood-filling from a starting point.

    This finds only the INNER transparent region (screen area) and
    excludes the OUTER transparent region (corners outside the phone).
    """
    h, w = alpha.shape
    mask = np.zeros((h, w), dtype=np.uint8)
    visited = np.zeros((h, w), dtype=bool)

    queue = deque([(start_x, start_y)])
    visited[start_y, start_x] = True

    while queue:
        x, y = queue.popleft()

        if alpha[y, x] < threshold:
            mask[y, x] = 255

            for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
                    visited[ny, nx] = True
                    if alpha[ny, nx] < threshold:
                        queue.append((nx, ny))

    return mask


def get_frames_dir():
    """Get the bundled frames directory."""
    return Path(str(files("mockups").joinpath("frames")))


def create_mockup(screenshot_path, output_path=None, frame_key=DEFAULT_FRAME, frames_dir=None):
    """
    Create a pixel-perfect iPhone mockup.

    Args:
        screenshot_path: Path to clean screenshot (no frame artifacts).
        output_path: Output path (optional, defaults to <name>_mockup.png).
        frame_key: Which frame to use (see FRAMES dict for options).
        frames_dir: Override directory containing frame PNG files.

    Returns:
        Path to the created mockup file.

    Raises:
        ValueError: If frame_key is not recognized.
        FileNotFoundError: If frame PNG or screenshot is missing.
    """
    if frames_dir is None:
        frames_dir = get_frames_dir()
    else:
        frames_dir = Path(frames_dir)

    if frame_key not in FRAMES:
        raise ValueError(
            f"Unknown frame: {frame_key}. "
            f"Available: {list(FRAMES.keys())}"
        )

    config = FRAMES[frame_key]
    frame_path = frames_dir / config["path"]

    if not frame_path.exists():
        raise FileNotFoundError(
            f"Frame not found: {frame_path}. "
            f"Make sure device frame PNGs are installed."
        )

    screenshot_path = Path(screenshot_path)
    if not screenshot_path.exists():
        raise FileNotFoundError(f"Screenshot not found: {screenshot_path}")

    # Load images
    screenshot = Image.open(screenshot_path).convert("RGBA")
    frame = Image.open(frame_path).convert("RGBA")

    # Calculate content dimensions
    content_left = config["content_left"]
    content_top = config["content_top"]
    content_right = config["content_right"]
    content_bottom = config["content_bottom"]
    content_width = content_right - content_left + 1
    content_height = content_bottom - content_top + 1

    # Resize screenshot to fit content area
    screenshot_resized = screenshot.resize(
        (content_width, content_height),
        Image.Resampling.LANCZOS,
    )

    # Create result canvas
    result = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    result.paste(screenshot_resized, (content_left, content_top))

    # Create screen mask using flood-fill from center.
    # This ensures we only include the INNER transparent area (screen)
    # and exclude the OUTER transparent area (corners outside phone).
    frame_array = np.array(frame)
    alpha = frame_array[:, :, 3]
    fw, fh = frame.size

    screen_mask_array = _flood_fill_screen_mask(alpha, fw // 2, fh // 2)
    screen_mask = Image.fromarray(screen_mask_array, mode="L")

    # Apply mask to screenshot
    result_masked = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    result_masked.paste(result, (0, 0), screen_mask)

    # Composite: masked screenshot + frame overlay
    final = Image.alpha_composite(result_masked, frame)

    # Determine output path
    if output_path is None:
        output_path = screenshot_path.parent / f"{screenshot_path.stem}_mockup.png"
    else:
        output_path = Path(output_path)

    final.save(str(output_path), "PNG")
    return output_path
