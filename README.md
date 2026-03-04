# docu-mizer

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill for generating Excalidraw diagrams and presentations that **argue visually** — shapes mirror concepts, colors encode meaning, and evidence artifacts (real code, JSON, API names) replace generic placeholders.

## What Makes This Different

- **Diagrams that argue, not display.** Every shape mirrors the concept it represents — fan-outs for one-to-many, timelines for sequences, convergence for aggregation. No uniform card grids.
- **Evidence artifacts.** Technical diagrams include real code snippets, actual JSON payloads, and concrete API names — not just labeled boxes.
- **Community library icons.** On-demand access to 100+ Excalidraw community libraries (AWS, Azure, GCP, network topology, UML, system design, etc.) for recognizable product icons and standard notation.
- **Per-slide rendering.** Presentations render each frame as a separate PNG for individual review, catching per-slide issues invisible in a full-canvas render.
- **Built-in visual validation.** A Playwright-based render pipeline lets the agent see its own output, catch layout issues, and fix them in a loop before delivering.
- **Brand-customizable.** All colors live in a single file (`references/color-palette.md`). Swap it out and every diagram follows your palette.

## Installation

```bash
# Clone into your project's skills directory
git clone https://github.com/jneaimi/docu-mizer.git .claude/skills/excalidraw-diagram-skill-main
```

Or copy the `.claude/skills/excalidraw-diagram-skill-main/` directory into any project.

## Setup

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
cd .claude/skills/excalidraw-diagram-skill-main/references
uv sync
uv run playwright install chromium
```

Or just tell Claude Code: *"Set up the Excalidraw diagram skill renderer."*

### Recommended: VS Code + Excalidraw Extension

Install the [Excalidraw extension for VS Code](https://marketplace.visualstudio.com/items?itemName=pomdtr.excalidraw-editor) to open and edit `.excalidraw` files directly in your editor. This lets you visually inspect, tweak, and present diagrams without leaving your IDE.

## Usage

Ask Claude Code to create a diagram:

> "Create an Excalidraw diagram showing our microservices architecture"

> "Make a presentation explaining the CI/CD pipeline"

> "Draw a network topology diagram using community library icons"

The skill handles concept mapping, layout, JSON generation, rendering, and visual validation.

### Rendering

```bash
cd .claude/skills/excalidraw-diagram-skill-main/references

# Render a diagram to PNG
uv run python render_excalidraw.py <path-to-file.excalidraw>

# Render each presentation slide as a separate PNG
uv run python render_excalidraw.py <path-to-file.excalidraw> --slides
```

### Community Library Icons

Access 100+ Excalidraw community icon libraries on demand:

```bash
cd .claude/skills/excalidraw-diagram-skill-main/references

# List items in a library
uv run python library_helper.py list rohanp/system-design.excalidrawlib

# Extract an item repositioned to target coordinates
uv run python library_helper.py fetch "dwelle/network-topology-icons.excalidrawlib" \
  --item "Server" --x 500 --y 300 --seed-base 300000 --id-prefix "srv"

# Search across cached libraries
uv run python library_helper.py search "firewall"
```

See `references/library-catalog.md` for the full curated catalog organized by category (cloud, system design, networking, DevOps, UX, data/ML, diagramming standards).

## How It Works

The skill teaches the agent a structured workflow:

1. **Depth assessment** — determine if the diagram needs simple conceptual shapes or comprehensive technical detail
2. **Concept mapping** — map each concept to a visual pattern (fan-out, convergence, timeline, assembly line, etc.)
3. **Section-by-section JSON building** — construct Excalidraw JSON incrementally with seed namespacing to avoid collisions
4. **Render-validate loop** — render to PNG, visually inspect, fix issues, re-render until it passes quality checks

For presentations, frames (1920x1080) act as slides laid out horizontally. The `--slides` flag renders each frame individually for per-slide review.

## Project Structure

```
docu-mizer/
  CLAUDE.md                                          # Agent instructions
  .claude/skills/excalidraw-diagram-skill-main/
    SKILL.md                                         # Core methodology (design philosophy,
                                                     #   patterns, workflow, quality checklist)
    references/
      color-palette.md                               # Semantic color system (customizable)
      element-templates.md                           # JSON templates for each element type
      json-schema.md                                 # Excalidraw JSON format reference
      library-catalog.md                             # Curated catalog of 50+ community libraries
      library_helper.py                              # Download/extract community library icons
      render_excalidraw.py                           # Render .excalidraw to PNG (+ --slides)
      render_template.html                           # Browser template for Playwright rendering
      pyproject.toml                                 # Python dependencies
```

## Customization

Edit `references/color-palette.md` to match your brand colors. The file defines semantic fill/stroke pairs for shapes, text hierarchy colors, and evidence artifact styling. Everything else in the skill is universal design methodology.

## License

MIT
