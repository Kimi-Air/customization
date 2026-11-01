# Design QA — architectural folio

final result: passed

## Visual evidence
- Source: /Users/ziyanzou/.codex/generated_images/01a191d7-2b33-7f43-b340-0fa37c08c72c/exec-64d7de4c-e70d-4580-ae1e-c9f920847ef6.png
- Source pixels: 1487 × 1058; normalized to 1440 × 1024 for comparison.
- Implementation: http://localhost:8765/
- Final desktop: ../design/desktop-final.jpg, 1440 × 1024 CSS and screenshot pixels.
- Same state: full home, daytime cutaway, D02 selected, dining guide, display menu closed.
- Full comparison: ../design/comparison-final.jpg (source left, implementation right).
- Focused comparison: ../design/inspector-final.jpg (same normalized inspector region).
- Mobile: ../design/mobile.jpg and ../design/mobile-guide.jpg; 390 × 844 CSS pixels. No page-level horizontal overflow.

## Findings and iteration history
1. P1 — initial model occupied too little of the main drawing surface. Camera framing revised and model enlarged; checked desktop-refined.jpg and desktop-final.jpg.
2. P2 — narrow view could crop the model using the desktop camera zoom. Zoom now derives from canvas aspect ratio, with distinct room-focus framing. Checked full-home mobile capture and a direct dining-point click at 390px.
3. P2 — point identifier typography was heavier and used old-style numerals. Changed to Times New Roman with lining numerals, and increased detail body copy to 14px. Checked inspector-final.jpg.
4. P2 — room and category combination with no matching points kept a stale inspector. Added explicit empty state and disabled the guide action; tested dining + water.
5. P2 — existing copy exposed conversation and video history. Removed those passages from the shell, stories, data, and CSV. DOM inspection found no video/user-confirmation/screenshot references.

No open P0/P1/P2 defects after the final comparison and interaction checks.

## Five fidelity surfaces
- Typography: Songti SC serif title hierarchy, neutral system sans for body, Times point identifiers. Reference's book-like contrast is retained. Operational text remains readable; mobile header condenses the project subtitle.
- Spacing: open canvas and one side inspector, thin separators, inline room sequence, plain rows for point lists. Two main sections remain visible in the desktop composition. Functional view controls and installation disclosure add modest vertical space relative to the concept.
- Color: warm white #faf9f6, charcoal #272d30, burnt orange #ae5732, restrained semantic point colors. No dashboard card grid or decorative badges.
- Images: generated island-outlet close-up and oak-floor texture installed as real local assets, sharp and correctly cropped. The floor plan and Three.js scene remain interactive source-driven diagrams, not raster placeholders. The selected concept's photorealistic scene is intentionally not used as geometry: its entrance and furniture differ from the user's confirmed plan. Actual layout and outward entry arrow take priority. This is a design/installation discussion model, not a photorealistic BIM deliverable.
- Content: functions described through location, quantity, usage, installation conditions. No process narrative. Four seats, smaller island without water, outward entry with left-hand control, robot beside washer/dryer, and original room assignments retained.

## Functional verification
- 3D direct click: dining D01 -> D02 sphere selected and inspector changed.
- Room selection, category selection, all/reset, previous/next point, no-results state.
- Cutaway, point labels, night toggle, return to daytime.
- D02 guide action selects dining; 2D D03 click updates map detail and inspector.
- Kitchen search “洗碗机” yields 2 groups; water filter yields 1; unmatched query shows empty state.
- Whole-home map toggle changes viewBox; dining and balcony guide navigation works.
- CSV action triggers download and visible completion status.
- Full desktop and mobile: no document overflow, image loaded.
- Browser console: no errors in final inspection.

## Follow-up polish
- P3: furniture can gain more material and construction detail if a photorealistic model becomes a separate requirement. Existing room geometry is schematic and intentionally retained.
- P3: typography uses native Songti SC on this Mac; other platforms fall back to their Chinese serif font.

## Implementation checklist
- [x] Reference and implementation compared together, including detail crop.
- [x] Source copy sanitized and 102 functional point groups retained.
- [x] Main interactions verified in the browser.
- [x] Narrow layout verified and clipping corrected.
- [x] Offline HTML and CSV regenerated with current data.
