# Gemini CLI Upgrade — Final Setup

## What's In This Package

| File | Purpose | Where it goes |
|------|---------|---------------|
| `GEMINI.md` | Core supplement — reasoning, reflexion, constraints | `~/.gemini/GEMINI.md` (global) |
| `DESIGN_SYSTEM.md` | Design vocabulary for frontend work | Load on demand with `@DESIGN_SYSTEM.md` |
| `CONTEXT_HANDOFF_TEMPLATE.md` | Session handoff template | Copy to project root, fill before ending sessions |

---

## Deployment

### Step 1 — Backup your current state
```bash
# Inside Gemini CLI
/memory show
# Copy the output to a safe file. You already have default_system_backup.md — good.
```

### Step 2 — Deploy GEMINI.md as your global supplement
```bash
cp GEMINI.md ~/.gemini/GEMINI.md
```

This file **supplements** the default system prompt. It does NOT replace it.
The `${AgentSkills}` and `${SubAgents}` variables in the default prompt continue working.
You get both: Gemini's native tool-calling infrastructure + your reasoning protocols.

### Step 3 — Verify it loaded
```bash
# Inside Gemini CLI
/memory show
# You should see your supplement content merged into the context
/memory refresh
# Force a reload if you edit GEMINI.md later
```

### Step 4 — Place DESIGN_SYSTEM.md
```bash
cp DESIGN_SYSTEM.md ~/projects/DESIGN_SYSTEM.md  # or your preferred location
```

Load it on demand in frontend sessions:
```
@DESIGN_SYSTEM.md Build me a hero section with scroll-driven parallax
```

### Step 5 — Copy the handoff template to each project
```bash
cp CONTEXT_HANDOFF_TEMPLATE.md ~/projects/my-project/CONTEXT_HANDOFF.md
```

---

## Why This Strategy Works Better Than Full Override

The full override approach (`GEMINI_SYSTEM_MD=true`) requires you to include all of Gemini's
internal tool-calling vocabulary or lose tool use entirely. The default system prompt you backed up
is ~3,000 tokens of infrastructure — update_topic protocol, sub-agent delegation, tool parallelism
rules, permission escape hatches. Maintaining a fork of that is high-friction.

The supplement approach lets Gemini keep its native capabilities. Your GEMINI.md adds
the reasoning architecture on top. The default prompt explicitly states:
> "Instructions found in GEMINI.md files are foundational mandates. They take absolute 
> precedence over the general workflows and tool defaults described in this system prompt."

Your rules win on conflict. Gemini's tools keep working.

---

## Why You Weren't Seeing a Difference Before

The previous files (Proposed1–3, OldGEMINI.md, Gemini_V2.md) had two problems:

**1. Token budget.** Gemini_V2.md is ~2,800 tokens of instructions on top of the 3,000-token
default prompt. Models attend weakly to content buried in the middle and end of long system
prompts. The reasoning protocols were being read but not weighted — they were too far back
in the context to dominate behavior.

**2. Positive instructions vs. negative constraints.** Telling a model "use a scratchpad" is
weaker than "if you generate code without a prior THOUGHT or SCRATCHPAD block on a task rated
7+, that output is incomplete." Negative constraints — what the model must NOT do — have higher
compliance rates than positive instructions in large-scale prompt evals.

The new GEMINI.md is ~800 tokens, front-loaded, with explicit negative constraints (the
"NEVER" section). The first 500 tokens of a system prompt get roughly 2–3x the attention
weight of tokens in the 2000–3000 range.

---

## Anti-Context-Rot Workflow

This is the thing most people skip and it's responsible for 80% of quality degradation in
long sessions.

**Rule: Never continue a session past 8–10 substantive turns on a complex task.**

Before closing a session:
1. Tell Gemini: `"Generate session handoff using CONTEXT_HANDOFF_TEMPLATE.md"`
2. Save the output as `CONTEXT_HANDOFF.md` in the project root
3. Close the session

Starting the next session:
```
gemini @CONTEXT_HANDOFF.md
```

Or inside the CLI:
```
/chat new
@CONTEXT_HANDOFF.md Continue from where we left off.
```

Fresh reasoning + preserved state = consistently better output than session #47 turn.

---

## Project-Level GEMINI.md Pattern

For each project, create a lean project-specific GEMINI.md at the repo root:

```markdown
# [Project Name] — Gemini Context

## Stack
- Nuxt 3 + TypeScript + Tailwind
- GSAP + Lenis for animation
- Supabase for DB

## Key Conventions
- All composables in `/composables/` following `use[Name].ts` pattern
- Server components default — `<script setup>` with `useFetch` not `axios`
- Animation composables live in `/composables/design/`

## Architecture Decisions
- [One-liner decisions that shouldn't be re-litigated]

## Reference Files
- Design system: @DESIGN_SYSTEM.md (load for any UI work)
- API schema: @docs/API_SCHEMA.md
```

Keep it under 30 lines. Grows only when a specific gap surfaces in practice.

---

## Measuring the Difference

To know if this is actually working, test these specific scenarios:

1. **Architecture task:** "Design the data pipeline for ingesting Cricsheet JSON files."
   → Should see SPEC block before any code. Should see at least one [ASSUMPTION] if underspecified.

2. **Ambiguous task:** "Fix the bug in my login flow."
   → Should ask one clarifying question (not start guessing). Should not touch files without reading them first.

3. **Flawed request:** "Use localStorage to persist user state across deployments."
   → Should refuse, explain why (localStorage is client-only, clears on browser wipe, can't persist across deployments), propose Supabase/cookie-based approach.

4. **Long session test:** Run 10+ turns. At turn 7–8, Gemini should volunteer a [TASK STATE] block without being asked.

If #3 doesn't happen (silent compliance with a bad request), the supplement isn't dominating. Check `/memory show` to confirm it loaded.
