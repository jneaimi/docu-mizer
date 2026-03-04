"""Render Excalidraw JSON to PNG using Playwright + headless Chromium.

Usage:
    cd <skill-directory>/references
    uv run python render_excalidraw.py <path-to-file.excalidraw> [--output path.png] [--scale 2] [--width 1920]

    # Render each presentation frame as a separate slide PNG
    uv run python render_excalidraw.py <path-to-file.excalidraw> --slides

First-time setup:
    cd <skill-directory>/references
    uv sync
    uv run playwright install chromium
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate_excalidraw(data: dict) -> list[str]:
    """Validate Excalidraw JSON structure. Returns list of errors (empty = valid)."""
    errors: list[str] = []

    if data.get("type") != "excalidraw":
        errors.append(f"Expected type 'excalidraw', got '{data.get('type')}'")

    if "elements" not in data:
        errors.append("Missing 'elements' array")
    elif not isinstance(data["elements"], list):
        errors.append("'elements' must be an array")
    elif len(data["elements"]) == 0:
        errors.append("'elements' array is empty — nothing to render")

    return errors


def compute_bounding_box(elements: list[dict]) -> tuple[float, float, float, float]:
    """Compute bounding box (min_x, min_y, max_x, max_y) across all elements."""
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")

    for el in elements:
        if el.get("isDeleted"):
            continue
        x = el.get("x", 0)
        y = el.get("y", 0)
        w = el.get("width", 0)
        h = el.get("height", 0)

        # For arrows/lines, points array defines the shape relative to x,y
        if el.get("type") in ("arrow", "line") and "points" in el:
            for px, py in el["points"]:
                min_x = min(min_x, x + px)
                min_y = min(min_y, y + py)
                max_x = max(max_x, x + px)
                max_y = max(max_y, y + py)
        else:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + abs(w))
            max_y = max(max_y, y + abs(h))

    if min_x == float("inf"):
        return (0, 0, 800, 600)

    return (min_x, min_y, max_x, max_y)


def render(
    excalidraw_path: Path,
    output_path: Path | None = None,
    scale: int = 2,
    max_width: int = 1920,
) -> dict:
    """Render an .excalidraw file to PNG.

    Returns a dict with:
      - success: bool
      - path: str (output PNG path, if successful)
      - error: str (error message, if failed)
    """
    # Import playwright here so validation errors show before import errors
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            "success": False,
            "error": "playwright not installed. Run: cd <skill-directory>/references && uv sync && uv run playwright install chromium",
        }

    # Read and validate
    if not excalidraw_path.exists():
        return {"success": False, "error": f"File not found: {excalidraw_path}"}

    raw = excalidraw_path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON in {excalidraw_path}: {e}"}

    errors = validate_excalidraw(data)
    if errors:
        return {"success": False, "error": f"Invalid Excalidraw file: {'; '.join(errors)}"}

    # Compute viewport size from element bounding box
    elements = [e for e in data["elements"] if not e.get("isDeleted")]
    min_x, min_y, max_x, max_y = compute_bounding_box(elements)
    padding = 80
    diagram_w = max_x - min_x + padding * 2
    diagram_h = max_y - min_y + padding * 2

    # Cap viewport width, let height be natural
    vp_width = min(int(diagram_w), max_width)
    vp_height = max(int(diagram_h), 600)

    # Output path
    if output_path is None:
        output_path = excalidraw_path.with_suffix(".png")

    # Template path (same directory as this script)
    template_path = Path(__file__).parent / "render_template.html"
    if not template_path.exists():
        return {"success": False, "error": f"Template not found at {template_path}"}

    template_url = template_path.as_uri()

    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception as e:
                if "Executable doesn't exist" in str(e) or "browserType.launch" in str(e):
                    return {
                        "success": False,
                        "error": "Chromium not installed for Playwright. Run: cd <skill-directory>/references && uv run playwright install chromium",
                    }
                return {"success": False, "error": f"Browser launch failed: {e}"}

            page = browser.new_page(
                viewport={"width": vp_width, "height": vp_height},
                device_scale_factor=scale,
            )

            # Load the template
            page.goto(template_url)

            # Wait for the ES module to load (imports from esm.sh)
            page.wait_for_function("window.__moduleReady === true", timeout=30000)

            # Inject the diagram data and render
            json_str = json.dumps(data)
            result = page.evaluate(f"window.renderDiagram({json_str})")

            if not result or not result.get("success"):
                error_msg = result.get("error", "Unknown render error") if result else "renderDiagram returned null"
                browser.close()
                return {"success": False, "error": f"Render failed: {error_msg}"}

            # Wait for render completion signal
            page.wait_for_function("window.__renderComplete === true", timeout=15000)

            # Screenshot the SVG element
            svg_el = page.query_selector("#root svg")
            if svg_el is None:
                browser.close()
                return {"success": False, "error": "No SVG element found after render"}

            svg_el.screenshot(path=str(output_path))
            browser.close()

    except Exception as e:
        return {"success": False, "error": f"Unexpected error during rendering: {e}"}

    return {"success": True, "path": str(output_path)}


def find_frames(elements: list[dict]) -> list[dict]:
    """Find all frame elements, sorted by name then x position."""
    frames = [e for e in elements if e.get("type") == "frame" and not e.get("isDeleted")]
    frames.sort(key=lambda f: (f.get("name", ""), f.get("x", 0)))
    return frames


def elements_in_frame(elements: list[dict], frame: dict) -> list[dict]:
    """Return elements whose center falls within the frame bounds (excluding the frame itself)."""
    fx = frame.get("x", 0)
    fy = frame.get("y", 0)
    fw = frame.get("width", 1920)
    fh = frame.get("height", 1080)
    frame_id = frame.get("id")

    result = []
    for el in elements:
        if el.get("isDeleted") or el.get("id") == frame_id:
            continue
        # Skip other frames
        if el.get("type") == "frame":
            continue

        ex = el.get("x", 0)
        ey = el.get("y", 0)
        ew = el.get("width", 0)
        eh = el.get("height", 0)

        # Use center point for containment check
        if el.get("type") in ("arrow", "line") and "points" in el:
            # Use midpoint of first and last point
            pts = el["points"]
            cx = ex + (pts[0][0] + pts[-1][0]) / 2
            cy = ey + (pts[0][1] + pts[-1][1]) / 2
        else:
            cx = ex + abs(ew) / 2
            cy = ey + abs(eh) / 2

        if fx <= cx <= fx + fw and fy <= cy <= fy + fh:
            result.append(el)

    return result


def render_slides(
    excalidraw_path: Path,
    output_dir: Path | None = None,
    scale: int = 2,
) -> dict:
    """Render each frame in a presentation as a separate slide PNG.

    Returns a dict with:
      - success: bool
      - slides: list[dict] with {name, path, index} for each slide
      - error: str (if failed)
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            "success": False,
            "error": "playwright not installed. Run: cd <skill-directory>/references && uv sync && uv run playwright install chromium",
        }

    if not excalidraw_path.exists():
        return {"success": False, "error": f"File not found: {excalidraw_path}"}

    raw = excalidraw_path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON in {excalidraw_path}: {e}"}

    errors = validate_excalidraw(data)
    if errors:
        return {"success": False, "error": f"Invalid Excalidraw file: {'; '.join(errors)}"}

    all_elements = data.get("elements", [])
    frames = find_frames(all_elements)

    if not frames:
        return {"success": False, "error": "No frame elements found — use --slides only with presentations that have frames"}

    # Output directory defaults to same location as the input file
    if output_dir is None:
        output_dir = excalidraw_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    base_name = excalidraw_path.stem

    template_path = Path(__file__).parent / "render_template.html"
    if not template_path.exists():
        return {"success": False, "error": f"Template not found at {template_path}"}

    template_url = template_path.as_uri()
    slides_info: list[dict] = []

    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception as e:
                if "Executable doesn't exist" in str(e) or "browserType.launch" in str(e):
                    return {
                        "success": False,
                        "error": "Chromium not installed for Playwright. Run: cd <skill-directory>/references && uv run playwright install chromium",
                    }
                return {"success": False, "error": f"Browser launch failed: {e}"}

            page = browser.new_page(
                viewport={"width": 1920, "height": 1080},
                device_scale_factor=scale,
            )

            page.goto(template_url)
            page.wait_for_function("window.__moduleReady === true", timeout=30000)

            for idx, frame in enumerate(frames):
                frame_name = frame.get("name", f"Slide {idx + 1}")
                slide_elements = elements_in_frame(all_elements, frame)

                if not slide_elements:
                    continue

                # Build a per-slide diagram with the same appState
                slide_data = {
                    "type": "excalidraw",
                    "version": 2,
                    "source": data.get("source", "https://excalidraw.com"),
                    "elements": slide_elements,
                    "appState": data.get("appState", {"viewBackgroundColor": "#ffffff"}),
                    "files": data.get("files", {}),
                }

                # Reset render state and render the slide
                page.evaluate("window.__renderComplete = false")
                json_str = json.dumps(slide_data)
                result = page.evaluate(f"window.renderDiagram({json_str})")

                if not result or not result.get("success"):
                    error_msg = result.get("error", "Unknown") if result else "null"
                    browser.close()
                    return {"success": False, "error": f"Render failed for '{frame_name}': {error_msg}"}

                page.wait_for_function("window.__renderComplete === true", timeout=15000)

                svg_el = page.query_selector("#root svg")
                if svg_el is None:
                    browser.close()
                    return {"success": False, "error": f"No SVG found for '{frame_name}'"}

                # Filename: basename-slide-01-framename.png
                safe_name = "".join(c if c.isalnum() or c in "-_ " else "" for c in frame_name).strip().replace(" ", "-")
                slide_filename = f"{base_name}-slide-{idx + 1:02d}-{safe_name}.png"
                slide_path = output_dir / slide_filename

                svg_el.screenshot(path=str(slide_path))
                slides_info.append({
                    "index": idx + 1,
                    "name": frame_name,
                    "path": str(slide_path),
                })

            browser.close()

    except Exception as e:
        return {"success": False, "error": f"Unexpected error during slide rendering: {e}"}

    return {"success": True, "slides": slides_info}


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Excalidraw JSON to PNG")
    parser.add_argument("input", type=Path, help="Path to .excalidraw JSON file")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output PNG path (default: same name with .png)")
    parser.add_argument("--scale", "-s", type=int, default=2, help="Device scale factor (default: 2)")
    parser.add_argument("--width", "-w", type=int, default=1920, help="Max viewport width (default: 1920)")
    parser.add_argument("--slides", action="store_true", help="Render each frame as a separate slide PNG")
    args = parser.parse_args()

    if args.slides:
        result = render_slides(args.input, args.output, args.scale)
        if result["success"]:
            for slide in result["slides"]:
                print(f"Slide {slide['index']:02d} ({slide['name']}): {slide['path']}")
        else:
            print(f"ERROR: {result['error']}", file=sys.stderr)
            sys.exit(1)
    else:
        result = render(args.input, args.output, args.scale, args.width)
        if result["success"]:
            print(result["path"])
        else:
            print(f"ERROR: {result['error']}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
