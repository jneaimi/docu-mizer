---
name: excalidraw-diagram
description: Create Excalidraw diagram and presentation JSON files that make visual arguments. Use when the user wants to visualize workflows, architectures, concepts, or create visual presentations/slides. Trigger for any mention of diagrams, flowcharts, architecture diagrams, system designs, visual explanations, Excalidraw, or when the user wants presentation slides with a hand-crafted visual style rather than a standard PowerPoint deck.
---

# Excalidraw Diagram Creator

Generate `.excalidraw` JSON files that **argue visually**, not just display information.

**Setup:** If the user asks you to set up this skill (renderer, dependencies, etc.), see `README.md` for instructions. All paths in this file that reference `<skill-directory>` mean the directory containing this SKILL.md file.

## Customization

**All colors and brand-specific styles live in one file:** `references/color-palette.md`. Read it before generating any diagram and use it as the single source of truth for all color choices — shape fills, strokes, text colors, evidence artifact backgrounds, everything.

To make this skill produce diagrams in your own brand style, edit `color-palette.md`. Everything else in this file is universal design methodology and Excalidraw best practices.

---

## Core Philosophy

**Diagrams should ARGUE, not DISPLAY.**

A diagram isn't formatted text. It's a visual argument that shows relationships, causality, and flow that words alone can't express. The shape should BE the meaning.

**The Isomorphism Test**: If you removed all text, would the structure alone communicate the concept? If not, redesign.

**The Education Test**: Could someone learn something concrete from this diagram, or does it just label boxes? A good diagram teaches—it shows actual formats, real event names, concrete examples.

---

## Depth Assessment (Do This First)

Before designing, determine what level of detail this diagram needs:

### Simple/Conceptual Diagrams
Use abstract shapes when:
- Explaining a mental model or philosophy
- The audience doesn't need technical specifics
- The concept IS the abstraction (e.g., "separation of concerns")

### Comprehensive/Technical Diagrams
Use concrete examples when:
- Diagramming a real system, protocol, or architecture
- The diagram will be used to teach or explain (e.g., YouTube video)
- The audience needs to understand what things actually look like
- You're showing how multiple technologies integrate

**For technical diagrams, you MUST include evidence artifacts** (see below).

---

## Research Mandate (For Technical Diagrams)

**Before drawing anything technical, research the actual specifications.**

If you're diagramming a protocol, API, or framework:
1. Look up the actual JSON/data formats
2. Find the real event names, method names, or API endpoints
3. Understand how the pieces actually connect
4. Use real terminology, not generic placeholders

Bad: "Protocol" → "Frontend"
Good: "AG-UI streams events (RUN_STARTED, STATE_DELTA, A2UI_UPDATE)" → "CopilotKit renders via createA2UIMessageRenderer()"

**Research makes diagrams accurate AND educational.**

---

## Evidence Artifacts

Evidence artifacts are concrete examples that prove your diagram is accurate and help viewers learn. Include them in technical diagrams.

**Types of evidence artifacts** (choose what's relevant to your diagram):

| Artifact Type | When to Use | How to Render |
|---------------|-------------|---------------|
| **Code snippets** | APIs, integrations, implementation details | Dark rectangle + syntax-colored text (see color palette for evidence artifact colors) |
| **Data/JSON examples** | Data formats, schemas, payloads | Dark rectangle + colored text (see color palette) |
| **Event/step sequences** | Protocols, workflows, lifecycles | Timeline pattern (line + dots + labels) |
| **UI mockups** | Showing actual output/results | Nested rectangles mimicking real UI |
| **Real input content** | Showing what goes IN to a system | Rectangle with sample content visible |
| **API/method names** | Real function calls, endpoints | Use actual names from docs, not placeholders |

**Example**: For a diagram about a streaming protocol, you might show:
- The actual event names from the spec (not just "Event 1", "Event 2")
- A code snippet showing how to connect
- What the streamed data actually looks like

**Example**: For a diagram about a data transformation pipeline:
- Show sample input data (actual format, not "Input")
- Show sample output data (actual format, not "Output")
- Show intermediate states if relevant

The key principle: **show what things actually look like**, not just what they're called.

---

## Multi-Zoom Architecture

Comprehensive diagrams operate at multiple zoom levels simultaneously. Think of it like a map that shows both the country borders AND the street names.

### Level 1: Summary Flow
A simplified overview showing the full pipeline or process at a glance. Often placed at the top or bottom of the diagram.

*Example*: `Input → Processing → Output` or `Client → Server → Database`

### Level 2: Section Boundaries
Labeled regions that group related components. These create visual "rooms" that help viewers understand what belongs together.

*Example*: Grouping by responsibility (Backend / Frontend), by phase (Setup / Execution / Cleanup), or by team (User / System / External)

### Level 3: Detail Inside Sections
Evidence artifacts, code snippets, and concrete examples within each section. This is where the educational value lives.

*Example*: Inside a "Backend" section, you might show the actual API response format, not just a box labeled "API Response"

**For comprehensive diagrams, aim to include all three levels.** The summary gives context, the sections organize, and the details teach.

### Bad vs Good

| Bad (Displaying) | Good (Arguing) |
|------------------|----------------|
| 5 equal boxes with labels | Each concept has a shape that mirrors its behavior |
| Card grid layout | Visual structure matches conceptual structure |
| Icons decorating text | Shapes that ARE the meaning |
| Same container for everything | Distinct visual vocabulary per concept |
| Everything in a box | Free-floating text with selective containers |

### Simple vs Comprehensive (Know Which You Need)

| Simple Diagram | Comprehensive Diagram |
|----------------|----------------------|
| Generic labels: "Input" → "Process" → "Output" | Specific: shows what the input/output actually looks like |
| Named boxes: "API", "Database", "Client" | Named boxes + examples of actual requests/responses |
| "Events" or "Messages" label | Timeline with real event/message names from the spec |
| "UI" or "Dashboard" rectangle | Mockup showing actual UI elements and content |
| ~30 seconds to explain | ~2-3 minutes of teaching content |
| Viewer learns the structure | Viewer learns the structure AND the details |

**Simple diagrams** are fine for abstract concepts, quick overviews, or when the audience already knows the details. **Comprehensive diagrams** are needed for technical architectures, tutorials, educational content, or when you want the diagram itself to teach.

---

## Container vs. Free-Floating Text

**Not every piece of text needs a shape around it.** Default to free-floating text. Add containers only when they serve a purpose.

| Use a Container When... | Use Free-Floating Text When... |
|------------------------|-------------------------------|
| It's the focal point of a section | It's a label or description |
| It needs visual grouping with other elements | It's supporting detail or metadata |
| Arrows need to connect to it | It describes something nearby |
| The shape itself carries meaning (decision diamond, etc.) | Typography alone creates sufficient hierarchy |
| It represents a distinct "thing" in the system | It's a section title, subtitle, or annotation |

**Typography as hierarchy**: Use font size, weight, and color to create visual hierarchy without boxes. A 28px title doesn't need a rectangle around it.

**The container test**: For each boxed element, ask "Would this work as free-floating text?" If yes, remove the container.

---

## Design Process (Do This BEFORE Generating JSON)

### Step 0: Assess Depth Required
Before anything else, determine if this needs to be:
- **Simple/Conceptual**: Abstract shapes, labels, relationships (mental models, philosophies)
- **Comprehensive/Technical**: Concrete examples, code snippets, real data (systems, architectures, tutorials)

**If comprehensive**: Do research first. Look up actual specs, formats, event names, APIs.

### Step 1: Understand Deeply
Read the content. For each concept, ask:
- What does this concept **DO**? (not what IS it)
- What relationships exist between concepts?
- What's the core transformation or flow?
- **What would someone need to SEE to understand this?** (not just read about)

### Step 2: Map Concepts to Patterns
For each concept, find the visual pattern that mirrors its behavior:

| If the concept... | Use this pattern |
|-------------------|------------------|
| Spawns multiple outputs | **Fan-out** (radial arrows from center) |
| Combines inputs into one | **Convergence** (funnel, arrows merging) |
| Has hierarchy/nesting | **Tree** (lines + free-floating text) |
| Is a sequence of steps | **Timeline** (line + dots + free-floating labels) |
| Loops or improves continuously | **Spiral/Cycle** (arrow returning to start) |
| Is an abstract state or context | **Cloud** (overlapping ellipses) |
| Transforms input to output | **Assembly line** (before → process → after) |
| Compares two things | **Side-by-side** (parallel with contrast) |
| Separates into phases | **Gap/Break** (visual separation between sections) |

### Step 3: Ensure Variety
For multi-concept diagrams: **each major concept must use a different visual pattern**. No uniform cards or grids.

### Step 4: Sketch the Flow
Before JSON, mentally trace how the eye moves through the diagram. There should be a clear visual story.

### Step 5: Generate JSON
Only now create the Excalidraw elements. **See below for how to handle large diagrams.**

### Step 6: Render & Validate (MANDATORY)
After generating the JSON, you MUST run the render-view-fix loop until the diagram looks right. This is not optional — see the **Render & Validate** section below for the full process.

---

## Output File Location

Save `.excalidraw` files based on context:
- If the user specifies a path, use that.
- If the project has a `diagrams/`, `docs/`, or `assets/` directory, save there.
- Otherwise, save to the project root with a descriptive filename (e.g., `auth-flow.excalidraw`, `system-architecture.excalidraw`).
- For presentations, use a name that reflects the topic (e.g., `api-overview-presentation.excalidraw`).

Always tell the user where you saved the file.

---

## Large / Comprehensive Diagram Strategy

**For comprehensive or technical diagrams, you MUST build the JSON one section at a time.** Do NOT attempt to generate the entire file in a single pass. This is a hard constraint — Claude Code has a ~32,000 token output limit per response, and a comprehensive diagram easily exceeds that in one shot. Even if it didn't, generating everything at once leads to worse quality. Section-by-section is better in every way.

### The Section-by-Section Workflow

**Phase 1: Build each section**

1. **Create the base file** with the JSON wrapper (`type`, `version`, `appState`, `files`) and the first section of elements.
2. **Add one section per edit.** Each section gets its own dedicated pass — take your time with it. Think carefully about the layout, spacing, and how this section connects to what's already there.
3. **Use descriptive string IDs** (e.g., `"trigger_rect"`, `"arrow_fan_left"`) so cross-section references are readable.
4. **Namespace seeds by section** to avoid collisions: section 1 uses 100000–199999, section 2 uses 200000–299999, etc. Each element needs a unique `seed` and a unique `versionNonce` — pick two different values from the section's range. See `references/json-schema.md` for details.
5. **Update cross-section bindings** as you go. When a new section's element needs to bind to an element from a previous section (e.g., an arrow connecting sections), edit the earlier element's `boundElements` array at the same time.

**Phase 2: Review the whole**

After all sections are in place, read through the complete JSON and check:
- Are cross-section arrows bound correctly on both ends?
- Is the overall spacing balanced, or are some sections cramped while others have too much whitespace?
- Do IDs and bindings all reference elements that actually exist?

Fix any alignment or binding issues before rendering.

**Phase 3: Render & validate**

Now run the render-view-fix loop from the Render & Validate section. This is where you'll catch visual issues that aren't obvious from JSON — overlaps, clipping, imbalanced composition.

### Section Boundaries

Plan your sections around natural visual groupings from the diagram plan. A typical large diagram might split into:

- **Section 1**: Entry point / trigger
- **Section 2**: First decision or routing
- **Section 3**: Main content (hero section — may be the largest single section)
- **Section 4-N**: Remaining phases, outputs, etc.

Each section should be independently understandable: its elements, internal arrows, and any cross-references to adjacent sections.

### What NOT to Do

- **Don't generate the entire diagram in one response.** You will hit the output token limit and produce truncated, broken JSON. Even if the diagram is small enough to fit, splitting into sections produces better results.
- **Don't use a coding agent** to generate the JSON. The agent won't have sufficient context about the skill's rules, and the coordination overhead negates any benefit.
- **Don't write a Python generator script.** The templating and coordinate math seem helpful but introduce a layer of indirection that makes debugging harder. Hand-crafted JSON with descriptive IDs is more maintainable.

---

## Visual Pattern Library

### Fan-Out (One-to-Many)
Central element with arrows radiating to multiple targets. Use for: sources, PRDs, root causes, central hubs.
```
        ○
       ↗
  □ → ○
       ↘
        ○
```

### Convergence (Many-to-One)
Multiple inputs merging through arrows to single output. Use for: aggregation, funnels, synthesis.
```
  ○ ↘
  ○ → □
  ○ ↗
```

### Tree (Hierarchy)
Parent-child branching with connecting lines and free-floating text (no boxes needed). Use for: file systems, org charts, taxonomies.
```
  label
  ├── label
  │   ├── label
  │   └── label
  └── label
```
Use `line` elements for the trunk and branches, free-floating text for labels.

### Spiral/Cycle (Continuous Loop)
Elements in sequence with arrow returning to start. Use for: feedback loops, iterative processes, evolution.
```
  □ → □
  ↑     ↓
  □ ← □
```

### Cloud (Abstract State)
Overlapping ellipses with varied sizes. Use for: context, memory, conversations, mental states.

### Assembly Line (Transformation)
Input → Process Box → Output with clear before/after. Use for: transformations, processing, conversion.
```
  ○○○ → [PROCESS] → □□□
  chaos              order
```

### Side-by-Side (Comparison)
Two parallel structures with visual contrast. Use for: before/after, options, trade-offs.

### Gap/Break (Separation)
Visual whitespace or barrier between sections. Use for: phase changes, context resets, boundaries.

### Lines as Structure
Use lines (type: `line`, not arrows) as primary structural elements instead of boxes:
- **Timelines**: Vertical or horizontal line with small dots (10-20px ellipses) at intervals, free-floating labels beside each dot
- **Tree structures**: Vertical trunk line + horizontal branch lines, with free-floating text labels (no boxes needed)
- **Dividers**: Thin dashed lines to separate sections
- **Flow spines**: A central line that elements relate to, rather than connecting boxes

```
Timeline:           Tree:
  ●─── Label 1        │
  │                   ├── item
  ●─── Label 2        │   ├── sub
  │                   │   └── sub
  ●─── Label 3        └── item
```

Lines + free-floating text often creates a cleaner result than boxes + contained text.

---

## Community Library Icons

The Excalidraw community maintains 100+ reusable icon libraries (AWS, Azure, GCP, network topology, UML, system design, etc.). Use these when recognizable product icons or standard notation symbols would strengthen the diagram.

**When to use**: Cloud architecture diagrams, system design with specific technologies, network topology, UML/BPMN notation, wireframes with standard UI components.

**When NOT to use**: Simple conceptual diagrams where hand-drawn shapes carry meaning, items that would be too small to recognize, or when the diagram's argument is about relationships rather than specific products.

### Workflow

1. **Identify** which elements would benefit from library icons (e.g., "AWS Lambda", "Kubernetes Pod", "Firewall")
2. **Consult** `<skill-directory>/references/library-catalog.md` to find the right library and item name
3. **Fetch** with the helper — the output is a JSON array of elements ready to insert:
   ```bash
   cd <skill-directory>/references
   uv run python library_helper.py fetch "dwelle/network-topology-icons.excalidrawlib" \
     --item "Server" --x 500 --y 300 --seed-base 300000 --id-prefix "srv"
   ```
4. **Insert** the returned JSON elements into your diagram's `elements` array
5. **Add labels and arrows** connecting library icons to the rest of your diagram — library items are visual only, they need your text and arrows for context

### Notes

- Library items are pre-styled — do not modify their fill/stroke colors (keeps icons recognizable)
- Use `--seed-base` matching the current section's seed range (e.g., 300000 for section 3)
- Use `--id-prefix` to namespace IDs (e.g., "lambda", "srv", "fw") and avoid collisions
- Run `library_helper.py list <source>` to see all available items in a library
- Run `library_helper.py search "keyword"` to search across all cached libraries
- Complex library items (30+ elements) need more space — give them at least 200×200px in your layout

---

## Shape Meaning

Choose shape based on what it represents—or use no shape at all:

| Concept Type | Shape | Why |
|--------------|-------|-----|
| Labels, descriptions, details | **none** (free-floating text) | Typography creates hierarchy |
| Section titles, annotations | **none** (free-floating text) | Font size/weight is enough |
| Markers on a timeline | small `ellipse` (10-20px) | Visual anchor, not container |
| Start, trigger, input | `ellipse` | Soft, origin-like |
| End, output, result | `ellipse` | Completion, destination |
| Decision, condition | `diamond` | Classic decision symbol |
| Process, action, step | `rectangle` | Contained action |
| Abstract state, context | overlapping `ellipse` | Fuzzy, cloud-like |
| Hierarchy node | lines + text (no boxes) | Structure through lines |

**Rule**: Default to no container. Add shapes only when they carry meaning. Aim for <30% of text elements to be inside containers.

---

## Color as Meaning

Colors encode information, not decoration. Every color choice should come from `references/color-palette.md` — the semantic shape colors, text hierarchy colors, and evidence artifact colors are all defined there.

**Key principles:**
- Each semantic purpose (start, end, decision, AI, error, etc.) has a specific fill/stroke pair
- Free-floating text uses color for hierarchy (titles, subtitles, details — each at a different level)
- Evidence artifacts (code snippets, JSON examples) use their own dark background + colored text scheme
- Always pair a darker stroke with a lighter fill for contrast

**Do not invent new colors.** If a concept doesn't fit an existing semantic category, use Primary/Neutral or Secondary.

---

## Modern Aesthetics

For clean, professional diagrams:

### Roughness
- `roughness: 0` — Clean, crisp edges. Use for modern/technical diagrams.
- `roughness: 1` — Hand-drawn, organic feel. Use for brainstorming/informal diagrams.

**Default to 0** for most professional use cases.

### Stroke Width
- `strokeWidth: 1` — Thin, elegant. Good for lines, dividers, subtle connections.
- `strokeWidth: 2` — Standard. Good for shapes and primary arrows.
- `strokeWidth: 3` — Bold. Use sparingly for emphasis (main flow line, key connections).

### Opacity
**Always use `opacity: 100` for all elements.** Use color, size, and stroke width to create hierarchy instead of transparency.

### Small Markers Instead of Shapes
Instead of full shapes, use small dots (10-20px ellipses) as:
- Timeline markers
- Bullet points
- Connection nodes
- Visual anchors for free-floating text

---

## Layout Principles

### Hierarchy Through Scale
- **Hero**: 300×150 - visual anchor, most important
- **Primary**: 180×90
- **Secondary**: 120×60
- **Small**: 60×40

### Whitespace = Importance
The most important element has the most empty space around it (200px+).

### Flow Direction
Guide the eye: typically left→right or top→bottom for sequences, radial for hub-and-spoke.

### Connections Required
Position alone doesn't show relationships. If A relates to B, there must be an arrow.

---

## Text Rules

**CRITICAL**: The JSON `text` property contains ONLY readable words.

```json
{
  "id": "myElement1",
  "text": "Start",
  "originalText": "Start"
}
```

Settings: `fontSize: 16`, `textAlign: "center"`, `verticalAlign: "middle"`

**Font families:**
- `fontFamily: 1` — Hand-drawn (Virgil). Use for informal, brainstorming-style diagrams.
- `fontFamily: 2` — Sans-serif (Helvetica). Use for presentations and business-facing content.
- `fontFamily: 3` — Monospace (Cascadia). Use for technical diagrams, code-related content. **This is the default.**

---

## JSON Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [...],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

## Element Templates

See `references/element-templates.md` for copy-paste JSON templates for each element type (text, line, dot, rectangle, arrow). Pull colors from `references/color-palette.md` based on each element's semantic purpose.

---

## Render & Validate (MANDATORY)

You cannot judge a diagram from JSON alone. After generating or editing the Excalidraw JSON, you MUST render it to PNG, view the image, and fix what you see — in a loop until it's right. This is a core part of the workflow, not a final check.

### How to Render

```bash
cd <skill-directory>/references && uv run python render_excalidraw.py <path-to-file.excalidraw>
```

For presentations, render each slide as a separate image:
```bash
cd <skill-directory>/references && uv run python render_excalidraw.py <path-to-file.excalidraw> --slides
```

Replace `<skill-directory>` with the actual path to this skill's directory (the folder containing this SKILL.md file).

The default mode outputs a single PNG next to the `.excalidraw` file. The `--slides` mode outputs one PNG per frame (e.g., `name-slide-01-Title.png`, `name-slide-02-Overview.png`). Then use the **Read tool** on each PNG to actually view it.

### The Loop

After generating the initial JSON, run this cycle:

**1. Render & View** — Run the render script, then Read the PNG.

**2. Audit against your original vision** — Before looking for bugs, compare the rendered result to what you designed in Steps 1-4. Ask:
- Does the visual structure match the conceptual structure you planned?
- Does each section use the pattern you intended (fan-out, convergence, timeline, etc.)?
- Does the eye flow through the diagram in the order you designed?
- Is the visual hierarchy correct — hero elements dominant, supporting elements smaller?
- For technical diagrams: are the evidence artifacts (code snippets, data examples) readable and properly placed?

**3. Check for visual defects:**
- Text clipped by or overflowing its container
- Text or shapes overlapping other elements
- Arrows crossing through elements instead of routing around them
- Arrows landing on the wrong element or pointing into empty space
- Labels floating ambiguously (not clearly anchored to what they describe)
- Uneven spacing between elements that should be evenly spaced
- Sections with too much whitespace next to sections that are too cramped
- Text too small to read at the rendered size
- Overall composition feels lopsided or unbalanced

**4. Fix** — Edit the JSON to address everything you found. Common fixes:
- Widen containers when text is clipped
- Adjust `x`/`y` coordinates to fix spacing and alignment
- Add intermediate waypoints to arrow `points` arrays to route around elements
- Reposition labels closer to the element they describe
- Resize elements to rebalance visual weight across sections

**5. Re-render & re-view** — Run the render script again and Read the new PNG.

**6. Repeat** — Keep cycling until the diagram passes both the vision check (Step 2) and the defect check (Step 3). Typically takes 2-4 iterations. Don't stop after one pass just because there are no critical bugs — if the composition could be better, improve it.

### When to Stop

The loop is done when:
- The rendered diagram matches the conceptual design from your planning steps
- No text is clipped, overlapping, or unreadable
- Arrows route cleanly and connect to the right elements
- Spacing is consistent and the composition is balanced
- You'd be comfortable showing it to someone without caveats

### First-Time Setup
If the render script hasn't been set up yet:
```bash
cd <skill-directory>/references
uv sync
uv run playwright install chromium
```

---

## Presentation Mode (Frame-Based Slides)

Excalidraw supports presentations through **frames** — each frame acts as a slide. The viewer zooms into each frame sequentially during presentation mode.

### When to Use Presentation Mode
- The user asks for "slides", "presentation", "deck", or "walkthrough"
- The content has a natural sequence (intro → details → conclusion)
- You want to progressively reveal parts of a larger diagram

### How Frames Work
- Each `frame` element defines a rectangular viewport (one slide)
- Elements inside a frame's bounds are part of that slide
- Frames are presented in order of their position (left-to-right, top-to-bottom) or by naming convention (`01 - Title`, `02 - Overview`, etc.)
- Standard slide dimensions: **1920×1080** (16:9)

### Presentation Design Guidelines

| Principle | Guidance |
|-----------|----------|
| **Content density** | Less than a diagram — aim for 1-2 key ideas per slide |
| **Font sizes** | Minimum 24px for body, 36px+ for titles (readability at projection scale) |
| **Visual consistency** | Reuse the same color palette and shape vocabulary across slides |
| **Slide structure** | Title slide → content slides → summary/conclusion |
| **Transitions** | Place related slides adjacent on the canvas so the zoom transition feels natural |

### Slide Layout Template
```
Frame 1 (0, 0)          Frame 2 (2100, 0)        Frame 3 (4200, 0)
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│  Title Slide │        │   Content 1  │        │   Content 2  │
│              │  180px  │              │  180px  │              │
│  Subtitle    │  gap   │  Diagram +   │  gap   │  Key Points  │
│              │        │  Evidence    │        │              │
└──────────────┘        └──────────────┘        └──────────────┘
   1920×1080               1920×1080               1920×1080
```

Place frames in a horizontal row with ~180px gaps. Name each frame descriptively so the presentation order is clear.

### Building a Presentation
1. Plan the slide sequence first (what story are you telling?)
2. Create frames first, then populate each one
3. Use the same section-by-section workflow as large diagrams
4. Each frame can contain any Excalidraw elements — shapes, text, arrows, evidence artifacts
5. Elements can span frames if you want a "zooming into detail" effect

See `references/element-templates.md` for the frame JSON template.

### Rendering & Validating Slides

Use `--slides` to render each frame as a separate PNG for individual review:

```bash
cd <skill-directory>/references && uv run python render_excalidraw.py <path-to-file.excalidraw> --slides
```

This produces one PNG per frame (e.g., `name-slide-01-Title.png`, `name-slide-02-Overview.png`). Review each slide image individually using the Read tool — this catches per-slide issues (text overflow, crowded layouts, font sizes too small) that are invisible in a full-canvas render.

The validate loop for presentations:
1. Render with `--slides`
2. Read each slide PNG and audit content density, font readability, and visual balance
3. Fix issues in the JSON (per-frame, since each frame's content is independent)
4. Re-render with `--slides` and re-check
5. Optionally also render without `--slides` for a full-canvas overview

---

## Quality Checklist

### Must-Pass (blocking — fix before delivering)

1. **Rendered to PNG**: Diagram has been rendered and visually inspected
2. **No text overflow**: All text fits within its container
3. **No overlapping elements**: Shapes and text don't overlap unintentionally
4. **Arrows land correctly**: Arrows connect to intended elements without crossing others
5. **Text clean**: `text` property contains only readable words (no format codes)
6. **Valid JSON**: All `boundElements`, `containerId`, and binding references point to elements that exist
7. **Readable at export size**: Text is legible in the rendered PNG

### Should-Pass (important for quality — fix if time allows)

8. **Isomorphism**: Each visual structure mirrors its concept's behavior
9. **Argument**: The diagram shows something text alone couldn't express
10. **Connections**: Every relationship has an arrow or line
11. **Flow**: Clear visual path for the eye to follow
12. **Hierarchy**: Important elements are larger and have more whitespace
13. **Even spacing**: Similar elements have consistent spacing
14. **Balanced composition**: No large empty voids or overcrowded regions
15. **Font choice**: `fontFamily: 3` (monospace) for technical diagrams, `fontFamily: 2` (sans-serif) for presentations, `fontFamily: 1` (hand-drawn) for informal/brainstorm style
16. **Roughness**: `roughness: 0` for clean/modern, `roughness: 1` for hand-drawn feel
17. **Opacity**: `opacity: 100` for all elements

### Advisory (nice-to-have for comprehensive diagrams)

18. **Research done**: Looked up actual specs, formats, event names
19. **Evidence artifacts**: Code snippets, JSON examples, or real data included
20. **Multi-zoom**: Has summary flow + section boundaries + detail
21. **Concrete over abstract**: Real content shown, not just labeled boxes
22. **Variety**: Each major concept uses a different visual pattern
23. **Minimal containers**: <30% of text inside containers; prefer free-floating text
24. **Lines as structure**: Tree/timeline patterns use lines + text rather than boxes

### Presentation-Specific Checks (when using frames)

25. **Frame dimensions**: All slides are 1920×1080
26. **Frame naming**: Frames have descriptive names with ordering prefix (e.g., "01 - Title")
27. **Font size**: Minimum 24px body text, 36px+ titles for projection readability
28. **Content density**: 1-2 key ideas per slide, not overcrowded
