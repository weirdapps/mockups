"""Tests for mockups package."""

import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

from mockups import FRAMES, DEFAULT_FRAME, create_mockup
from mockups.core import get_frames_dir


def test_frames_dict_has_expected_keys():
    expected = {
        "16_pro_max_black",
        "16_pro_max_natural",
        "16_pro_max_white",
        "16_pro_max_desert",
        "16_pro_black",
        "16_pro_natural",
    }
    assert set(FRAMES.keys()) == expected


def test_frames_have_required_fields():
    required_fields = {
        "path",
        "content_left",
        "content_top",
        "content_right",
        "content_bottom",
    }
    for key, config in FRAMES.items():
        assert required_fields.issubset(config.keys()), f"Frame {key} missing fields"


def test_get_frames_dir_returns_path():
    result = get_frames_dir()
    assert isinstance(result, Path)
    assert result.name == "frames"


def test_default_frame_exists_in_frames():
    assert DEFAULT_FRAME in FRAMES


def test_bundled_frames_exist():
    frames_dir = get_frames_dir()
    for key, config in FRAMES.items():
        frame_path = frames_dir / config["path"]
        assert frame_path.exists(), f"Frame file missing: {frame_path}"


def test_list_frames_cli():
    result = subprocess.run(
        [sys.executable, "-m", "mockups.cli", "--list-frames"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Available frames:" in result.stdout


def test_missing_screenshot_raises():
    with pytest.raises(FileNotFoundError):
        create_mockup("/nonexistent/screenshot.png")


def test_invalid_frame_raises():
    with pytest.raises(ValueError, match="Unknown frame"):
        create_mockup("dummy.png", frame_key="nonexistent")


def test_create_mockup_produces_output(tmp_path):
    # Create a minimal test screenshot
    screenshot = Image.new("RGBA", (375, 812), (30, 100, 200, 255))
    screenshot_path = tmp_path / "test_screenshot.png"
    screenshot.save(str(screenshot_path))

    output_path = tmp_path / "test_mockup.png"
    result = create_mockup(str(screenshot_path), str(output_path))

    assert Path(result).exists()
    mockup = Image.open(result)
    assert mockup.mode == "RGBA"
    assert mockup.size == (1520, 3068)  # Pro Max dimensions


def test_create_mockup_default_output_name(tmp_path):
    screenshot = Image.new("RGBA", (375, 812), (30, 100, 200, 255))
    screenshot_path = tmp_path / "my_app.png"
    screenshot.save(str(screenshot_path))

    result = create_mockup(str(screenshot_path))
    assert Path(result).name == "my_app_mockup.png"
    assert Path(result).exists()


def test_create_mockup_pro_frame(tmp_path):
    screenshot = Image.new("RGBA", (375, 812), (30, 100, 200, 255))
    screenshot_path = tmp_path / "test.png"
    screenshot.save(str(screenshot_path))

    output_path = tmp_path / "pro_mockup.png"
    result = create_mockup(
        str(screenshot_path), str(output_path), frame_key="16_pro_black"
    )

    mockup = Image.open(result)
    assert mockup.size == (1406, 2822)  # Pro dimensions
