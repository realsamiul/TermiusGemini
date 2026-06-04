# 🌟 Exo Ape Portfolio Site — Customization & Deployment Guidelines

Welcome to your final portfolio website! This repository contains a fully automated, high-fidelity rebuild of the award-winning **Exo Ape** website. 

To prevent manual coding and parsing errors, your repository is equipped with a custom **GitHub CMS** that allows you to easily edit site texts and media files directly in GitHub's web interface. 

---

## 🛠️ How It Works (GitHub CMS)

You do **not** need to install Node.js, run local commands, or write code.

1. **You Edit:** Change any JSON file under `portfolio-content/pages/` (for page texts/media) or `portfolio-content/global/` (for site-wide settings like email, phone, social links) directly on GitHub.
2. **GitHub Actions Compiles:** A pre-configured background workflow (`.github/workflows/rebuild.yml`) detects your change, executes the compiler (`node compile.cjs`), and pushes the compiled static payloads back to the repository.
3. **Vercel Deploys:** Vercel automatically detects the compiled push and updates your live portfolio in seconds!

---

## 📂 Content Folder Structure

*   📁 **`portfolio-content/pages/`** (Individual Page Contents)
    *   `home.json` — Homepage hero text, featured projects list, play showreel settings, and news layout.
    *   `studio.json` — "The Studio" page text, list of design/culture philosophies, partners list, and studio details.
    *   `contact.json` — Contact details, hero image, and background details.
    *   `news.json` — News & Recognition grids.
    *   `work_list.json` — The main "/work" project collection list.
    *   `work_ottografie.json` — Project Detail page: Ottografie.
    *   `work_amaterasu.json` — Project Detail page: Amaterasu.
    *   `work_columbia_pictures.json` — Project Detail page: Columbia Pictures.
    *   `work_cambium.json` — Project Detail page: Cambium.
    *   `work_reno_pelle.json` — Project Detail page: Rino & Pelle (A new active page!).
    *   `work_the_st_regis_venice.json` — Project Detail page: The St. Regis Venice (A new active page!).
*   📁 **`portfolio-content/global/`** (Global branding and layout)
    *   `state.json` — Company brand email, phone number, physical address, and social links (Instagram, LinkedIn, Twitter, etc.).

---

## 📐 Editorial Design Specs & Guidelines

To maintain the sophisticated, high-fashion aesthetic, follow these precise guidelines on copy length and image dimensions:

### 1. Typography & Copy Lengths
| Location | Field / Key | Recommended Length | Description / Example |
| :--- | :--- | :--- | :--- |
| **Homepage Hero** | `intro` | 150 – 200 chars | *"We help experience-driven companies thrive by making their audience feel..."* |
| **Work Hero Title** | `title` | 1 – 3 words | *"Ottografie"*, *"Columbia Pictures"*, *"Amaterasu"* |
| **Work Hero Subtitle** | `subtitle` | 2 – 4 words | *"Pioneering Sustainable Solutions"*, *"Celebrated Entertainment History"* |
| **Work Case Intro** | `intro` | 180 – 280 chars | Describe the client brief and your direct contribution in a poetic, sensory-rich tone. |
| **Work Details** | `client` | 1 – 3 words | The client's brand name. |
| **Work Details** | `services` | 1 – 3 items | Array of services performed: `["Digital Design", "Web Development"]` |

### 2. Media Dimensions & Formats
All media files should be placed inside a folder in your repository (e.g., `video/` or a new folder), and referenced as relative paths starting with `/` (e.g., `/video/my-project.mp4`).

*   🖼️ **Vertical Hero Images (Work Details & Grid):**
    *   **Ideal Dimensions:** `2400 x 2990` pixels (Aspect Ratio: **4:5**)
    *   **Alternative:** `1200 x 1500` pixels
    *   **Format:** `.jpg` or `.webp` (optimized under 500KB)
*   🖼️ **Square Images (Studio / Collage):**
    *   **Ideal Dimensions:** `2500 x 2626` pixels (or solid square `2000 x 2000`)
    *   **Aspect Ratio:** **1:1**
*   🖼️ **Landscape Video Thumbnails (Home Showreel):**
    *   **Ideal Dimensions:** `1920 x 1080` (Aspect Ratio: **16:9**)
*   🎥 **Cinematic Loop Videos:**
    *   **Ideal Dimensions:** Same aspect ratio as their target card (usually **4:5** vertical or **16:9** landscape).
    *   **Format:** Optimized `.mp4` video (compressed using H.264/AAC, target bitrate under 2Mbps, file size under 5MB for smooth, lag-free autoplay loops).

---

## 🔄 Step-by-Step: Changing a Project's Text and Image

Suppose you want to edit **Ottografie** to showcase **"Your Brand Project"**:

1.  Open your browser to your GitHub repository: `https://github.com/realsamiul/final-portfolio-website`.
2.  Navigate to `portfolio-content/pages/work_ottografie.json`.
3.  Click the **✏️ Pencil Icon (Edit this file)** in GitHub's top-right toolbar.
4.  Find the `hero` section in the JSON file. Change the text parameters:
    ```json
    "title": "Your Project Name",
    "subtitle": "Poetic One Line Subtitle",
    "intro": "Write a compelling, sensory-rich intro text describing your project in 2 sentences...",
    "client": "Your Client Name",
    "services": [
      "Brand Strategy",
      "UI/UX Design",
      "3D Interactions"
    ]
    ```
5.  If you want to use your own image or video:
    *   Upload your optimized image (e.g. `my-project-hero.jpg`, size `2400x2990`) to your repository (e.g. inside `video/` or `storyblok/`).
    *   In the JSON, change the image and video file paths:
        ```json
        "image": {
          "filename": "/video/my-project-hero.jpg"
        },
        "video": {
          "filename": "/video/my-project-hover.mp4"
        }
        ```
6.  Scroll to the bottom of the page, add a commit message (e.g. `Update my-project content`), and click **Commit changes**.
7.  **That's it!** GitHub Actions will automatically re-compile the site's static payload and trigger Vercel to update your live website.
