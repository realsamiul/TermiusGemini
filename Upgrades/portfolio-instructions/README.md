# 🚀 Vercel-Ready Portfolio Website — Setup & Customization Instructions

The high-fidelity rebuild of your portfolio website is complete, fully committed, and published on your GitHub account!

*   **Repository URL:** `https://github.com/realsamiul/final-portfolio-website`
*   **Target Hosting Platform:** **Vercel** (Pre-configured via `vercel.json` for clean URLs, static headers, and routing fallbacks).

---

## 📂 Instructions & Guidelines

All detailed instructions for customizing texts, uploading and resizing images, configuring loop videos, and updating global social/contact info are located in the companion file:

👉 **[GUIDELINES.md](./GUIDELINES.md)**

---

## 🛠️ CMS Automation Overview

This portfolio site features a **completely serverless, code-free GitHub CMS**. You can edit texts and media files directly on the GitHub website, and the system automatically compiles and updates your live portfolio website on Vercel:

```text
[You edit a JSON file on GitHub]
           │
           ▼
[GitHub Actions triggers on push]
           │
           ▼
[Runner runs: node compile.cjs] ──► (Regenerates Nuxt dynamic payloads & routing manifest)
           │
           ▼
[Action pushes compiled files back to main]
           │
           ▼
[Vercel detects push & builds live deployment] ──► (Your site updates instantly!)
```

Feel free to open and refer to `GUIDELINES.md` for complete dimensions and character limits matching the Exo Ape editorial layout!
