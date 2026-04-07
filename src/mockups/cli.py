"""Command-line interface for mockups."""

import argparse
import sys

from mockups.core import FRAMES, DEFAULT_FRAME, create_mockup


def main():
    parser = argparse.ArgumentParser(
        prog="mockup",
        description="Create pixel-perfect iPhone mockups",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    mockup screenshot.png
    mockup screenshot.png output.png
    mockup screenshot.png --frame 16_pro_black

Available frames:
    16_pro_max_black (default)
    16_pro_max_natural
    16_pro_max_white
    16_pro_max_desert
    16_pro_black
    16_pro_natural
        """,
    )

    parser.add_argument("screenshot", nargs="?", help="Path to screenshot image")
    parser.add_argument("output", nargs="?", help="Output path (optional)")
    parser.add_argument(
        "--frame", "-f",
        default=DEFAULT_FRAME,
        choices=list(FRAMES.keys()),
        help=f"iPhone frame to use (default: {DEFAULT_FRAME})",
    )
    parser.add_argument(
        "--list-frames",
        action="store_true",
        help="List available frames",
    )
    parser.add_argument(
        "--frames-dir",
        help="Override frames directory",
    )

    args = parser.parse_args()

    if args.list_frames:
        print("Available frames:")
        for key, config in FRAMES.items():
            print(f"  {key}: {config['path']}")
        return

    if not args.screenshot:
        parser.error("the following arguments are required: screenshot")

    try:
        output = create_mockup(args.screenshot, args.output, args.frame, args.frames_dir)
        print(f"Mockup saved: {output}")
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
