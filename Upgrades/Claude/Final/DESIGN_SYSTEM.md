# Design Intelligence System
## Motion, Typography, Layout — Vocabulary for World-Class Frontend

> This file is loaded as context for all frontend/UI work.
> It encodes design grammar extracted from award-winning agencies and studios.
> Gemini must reference this before building any component with visual output.

---

## Motion Vocabulary

### Easing
- **Entrance (primary):** `cubic-bezier(0.16, 1, 0.3, 1)` — fast acceleration, long deceleration, no bounce
- **Entrance (subtle):** `cubic-bezier(0.25, 0.46, 0.45, 0.94)` — easeOutQuad for secondary elements
- **Exit:** `cubic-bezier(0.4, 0, 1, 1)` — fast exit, never linger
- **Scrub (scroll-driven):** `linear` with `scrub: 1` — never mechanical, use `scrub: 0.8–1.2` for lag feel
- **Never use:** `ease`, `ease-in-out`, `linear` for entrances. These read as default/generic.

### Duration
| Type | Range | Notes |
|------|-------|-------|
| Micro (hover, toggle) | 150–250ms | |
| Standard (element entrance) | 400–600ms | |
| Hero / page reveal | 800–1200ms | Never exceed 1400ms |
| Scroll scrub | Driven by scroll position, not time | |

### Stagger
- Between siblings: **80–120ms** — never uniform, never zero
- Direction: bottom-to-top or left-to-right for reveals. Never top-to-bottom (reads as loading)
- GSAP syntax: `stagger: { amount: 0.4, from: "start" }` not `stagger: 0.1`

### Scroll
- Smooth scroll: **Lenis** (preferred over Locomotive in 2024+, lighter, better Nuxt integration)
- ScrollTrigger start: `"top 85%"` for most reveals (not `"top bottom"` — too early)
- Parallax depth range: `yPercent: -15` to `yPercent: -40` — never exceed ±50

### Principles
- Entrances are fast-out: acceleration is short, deceleration is long
- Nothing moves without purpose. Animation communicates state, not decoration
- Mobile: reduce motion by 30–40%, respect `prefers-reduced-motion`
- Never animate more than 3 independent elements simultaneously
- **Paint Thrashing Prevention:** Set `will-change: transform` on elements that will be animated by GSAP before the animation begins. Remove it after via `clearProps: 'will-change'` on animation complete.

---

## Typography Grammar

### Scale Logic
- Display / hero: large optical size, tight tracking (`-0.02em` to `-0.05em`), high weight contrast
- Body: `1.6–1.75` line-height, medium weight (400–450), generous paragraph spacing
- UI labels: slightly tight tracking (`-0.01em`), consistent weight hierarchy

### Variable Fonts (preferred)
- Use variable font axes for optical size: `font-variation-settings: "opsz" 72` for display
- Weight range: 300 (thin accents) to 800 (display) within one family
- Avoid mixing more than 2 typeface families in a single UI

### Sizing
- Do not use fixed px for body text — use `clamp()` for fluid scaling
  - Example: `font-size: clamp(1rem, 1.5vw + 0.5rem, 1.25rem)`
- Display sizes: `clamp(3rem, 8vw, 8rem)` for hero headings

---

## Color Logic

### Near-Black vs True Black
- Prefer near-blacks: `#0a0a0a`, `#111111`, `#0d0d0d` — not `#000000`
- True black is for text on pure white only; everywhere else it reads as flat/cheap
- Dark backgrounds: use slightly warm near-black (`#0f0e0d`) or cool (`#0b0c10`) based on brand temp

### Accent Strategy
- One primary accent, used sparingly (max 15% of visual surface area)
- Tints: generate from the accent at 10%, 20%, 40% opacity over the near-black
- Never use pure saturated RGB values — always slightly desaturate: `hsl(220, 85%, 55%)` not `hsl(220, 100%, 50%)`

### Gradient Use
- Gradients for depth, not decoration
- Preferred: subtle radial gradient on hero sections for lighting feel
- Avoid linear gradients that go color-to-color — use color-to-transparent
- Mesh gradients: use sparingly, at very low opacity (0.4–0.6)

---

## Layout Grammar

### Grid Philosophy
- Mobile-first, but designed desktop-first in intention
- Base grid: 12-column, 24px gutter on desktop, 16px mobile
- Asymmetry is intentional: avoid perfectly centered layouts for editorial content
- Golden sections: place key focal point at ~38% or ~62% from edge, not center

### Spacing System
- Use an 8px base unit. All spacing values are multiples: 8, 16, 24, 32, 48, 64, 96, 128
- Breathing room between sections: minimum 96px on desktop, 64px mobile
- Never use arbitrary spacing values — if it's not on the scale, question whether it belongs

### Breakpoints
```
xs: 375px   (small mobile)
sm: 640px   (mobile landscape / large mobile)  
md: 768px   (tablet)
lg: 1024px  (small desktop)
xl: 1280px  (standard desktop)
2xl: 1536px (large desktop)
```
- Design at 1440px as primary desktop canvas
- Mobile: 390px (iPhone 14 Pro as reference)

### Section Rhythm
- Alternate visual weight between sections (light → dark → light or full-bleed → contained)
- First section (hero): always full viewport height or intentionally overflows
- Last section (CTA/footer): should feel like a landing, not an abrupt stop

---

## Interaction Vocabulary

### Cursor
- Custom cursor: 12–16px dot + 40–60px outer ring, with lag (`lerp: 0.1–0.15`)
- On hover over interactive elements: outer ring expands 1.5–2x, fills partially
- On click: brief scale-down (0.85) on outer ring
- **Touch Fallback:** All cursor composables must gate on `window.matchMedia('(pointer: fine)').matches` before initializing. Touch devices get no custom cursor behavior.

### Hover States
- Text links: underline that draws in from left, not color change alone
- Buttons: subtle y-translate (-2px to -4px) + shadow increase — not just color change
- Cards: slight scale (1.02–1.03) with shadow. Never scale more than 1.05

### Page Transitions
- Preferred: cover/reveal with a colored panel (`clip-path` or transform)
- Duration: 600–800ms out, 400–600ms in — exit is always slower than entrance
- Avoid: fade-only transitions (read as early 2010s), slide-in from side (too app-like for editorial)

---

## GSAP Pattern Library
*Reference these composable names when building; implement if not yet existing*

| Composable / Component | Behavior |
|---|---|
| `useScrollReveal(el, options)` | GSAP ScrollTrigger entrance with vocabulary easing |
| `useMagneticButton(el, strength?)` | Cursor magnetism — `strength: 0.3` default |
| `useParallaxLayer(el, depth)` | Depth-aware vertical parallax, Lenis-integrated |
| `useSplitTextReveal(el)` | SplitText character/word reveal with stagger |
| `usePageTransition()` | Cover-reveal page transition composable |
| `LenisProvider.vue` | Smooth scroll wrapper, must be app root |
| `MagneticButton.vue` | Button with cursor magnetism |
| `SplitHeading.vue` | Heading with split-text entrance |
| `ScrollReveal.vue` | Wrapper component for scroll-triggered entrance |

### GSAP Lifecycle Cleanup
All GSAP animations must be wrapped in gsap.context() scoped to the component 
root element. Call context.revert() in onUnmounted(). No exceptions.

```javascript
// Required pattern in every component using GSAP:
const ctx = gsap.context(() => { /* all animations here */ }, rootEl)
onUnmounted(() => ctx.revert())
```

---

## Reference Sites — Grammar Extracted From
*(Do not copy. Understand the decisions.)*

| Site Type | Key Pattern to Study |
|---|---|
| Agency / motion-heavy | Scrub scroll, cursor behavior, page transitions |
| SaaS / product | Typography scale, micro-interactions, section rhythm |
| Portfolio | Asymmetry, color restraint, white space as design element |
| Editorial | Reading rhythm, typographic hierarchy, image/text interplay |

---

*Load this file when: building any component with visual output, designing layouts, implementing animations*
*Do NOT load this file when: working on API routes, ML pipelines, data processing, backend logic*
