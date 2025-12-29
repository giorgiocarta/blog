# My Personal Blog

This repository hosts a simple, low-cost, and automatically published personal blog. 
It's designed to allow you to write content in Markdown (e.g., using Obsidian) and have it automatically 
converted to HTML and deployed to GitHub Pages.

## Features

*   **Markdown-based Content:** Write your blog posts using Markdown.
*   **Automatic Publishing:** Content is automatically published via GitHub Actions when you push to the `main` branch.
*   **GitHub Pages Hosting:** Free hosting directly from your GitHub repository.
*   **Subdirectory Organization:** Each post resides in its own subdirectory within `published/`, allowing for clean management of associated assets.
*   **Local Image Support:** Easily include local images alongside your Markdown files.
*   **Mermaid Diagram Support:** Embed Mermaid diagrams directly in your Markdown for dynamic visualizations.
*   **Pygments Code Highlighting:** Syntax highlighting for code blocks.
*   **Simple, Readable Design:** A clean, minimalist layout focused on readability.
*   **Permanent Navigation Pane:** A left-hand sidebar with links to all your blog posts.
*   **Customizable "About Me" Page:** A landing page with information about yourself.

## Getting Started

Follow these steps to set up and run your blog locally.

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

### 2. Local Setup and Preview

This project uses a `Makefile` to streamline local development.

*   **Install Dependencies:**
    Run this command once to create a Python virtual environment and install all necessary dependencies:
    ```bash
    make setup
    ```

*   **Generate and Serve Locally:**
    To generate the static site and serve it with a local web server (so you can view it in your browser):
    ```bash
    make
    # Or, to run steps separately:
    # make generate
    # make serve
    ```
    Open your web browser and navigate to `http://localhost:8000` to see your blog. Press `Ctrl+C` in your terminal to stop the server.

*   **Clean Up:**
    To remove generated files (`docs/`) and the virtual environment (`.venv/`):
    ```bash
    make clean
    ```

### 3. Adding New Content

To add a new blog post:

1.  **Create a new subdirectory** inside the `published/` folder for your post.
    Example: `published/my-new-post/`

2.  **Create an `index.md` file** inside this new subdirectory. This will be your blog post content.
    Example: `published/my-new-post/index.md`

3.  **Include Front Matter:** At the top of your `index.md` file, add a YAML front matter block for metadata:
    ```markdown
    ---
    title: Your Post Title Here
    date: YYYY-MM-DD
    ---
    ```

4.  **Add Your Content:** Write your blog post in Markdown below the front matter.

5.  **Local Images:** If you have local images for your post, place them in the same subdirectory (e.g., `published/my-new-post/your-image.png`). Reference them in your Markdown like this:
    ```markdown
    ![Alt Text for Image](./your-image.png)
    ```

6.  **Mermaid Diagrams:** Embed Mermaid diagrams using fenced code blocks:
    ```markdown
    ```mermaid
    graph TD;
        A[Start] --> B[End];
    ```
    ```

7.  **Update "About Me" Page:** Edit the `about.md` file in the project root to update your landing page content.

### 4. Publishing to GitHub Pages

Your blog is configured for automatic deployment to GitHub Pages via GitHub Actions.

1.  **Commit and Push:** After making changes, commit all your new content and push it to the `main` branch of your GitHub repository.
    ```bash
    git add .
    git commit -m "Add new blog post"
    git push origin main
    ```

2.  **Initial GitHub Pages Setup (One-time):**
    The first time you push, a GitHub Action will run and create a `gh-pages` branch. Once that action completes successfully:
    *   Go to your GitHub repository's **Settings** tab.
    *   In the left sidebar, click on **Pages**.
    *   Under "Build and deployment", for the **Source**, select **Deploy from a branch**.
    *   For the **Branch**, select `gh-pages` and `/ (root)` for the folder.
    *   Click **Save**.

    Your blog will then be accessible at `https://YOUR_USERNAME.github.io/YOUR_REPOSITORY_NAME`.

## Customization

*   **Styling:** Modify `static/style.css` to change the look and feel of your blog.
*   **Templates:** Edit the HTML templates in the `templates/` directory (`base.html`, `index.html`, `post.html`) to adjust the layout and structure.
*   **Blog Title & Profile Picture:** Update `templates/base.html` for your blog's title and the path to your profile picture (e.g., `static/profile.jpeg`).
*   **About Me Content:** Modify `about.md` for your landing page's content.
