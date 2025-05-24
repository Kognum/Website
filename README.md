# Static Site Generator

A simple, GitHub Pages compatible static site generator written in Python.

## Overview

This static site generator consists of two main files:
- `builder.py` - Builds the static site from source files
- `serve.py` - Serves the built site locally for development

## Directory Structure

The generator expects the following directory structure:

```
project/
├── data/           # CSS, images, and other assets
├── pages/          # HTML pages with TEMPLATE tags
├── templates/      # HTML templates with CONTENT placeholders
├── builder.py      # Build script
├── serve.py        # Development server
└── build/          # Generated output (created by builder)
```

## How It Works

### Templates

Templates are stored in the `templates/` directory and contain a special `<!-- CONTENT -->` placeholder where page content will be inserted.

Example template (`templates/base.html`):
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Site</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>...</nav>
    <main>
        <!-- CONTENT -->
    </main>
    <footer>...</footer>
</body>
</html>
```

### Pages

Pages are stored in the `pages/` directory and must start with a TEMPLATE tag that specifies which template to use.

Example page (`pages/index.html`):
```html
<!-- TEMPLATE: base -->
<h1>Welcome</h1>
<p>This is the homepage content.</p>
```

### Assets

All files in the `data/` directory are copied directly to the root of the build directory. This includes CSS files, images, JavaScript, etc.

## Usage

### Building the Site

```bash
python builder.py
```

This will:
1. Create a `build/` directory
2. Copy all files from `data/` to `build/`
3. Process each page in `pages/`:
   - Extract the TEMPLATE tag
   - Load the specified template
   - Replace `<!-- CONTENT -->` with the page content
   - Save as `build/index.html` (for index.html) or `build/pagename/index.html` (for other pages)

### Serving Locally

```bash
python serve.py
```

This starts a development server at `http://localhost:1313` and automatically opens your browser.

Options:
- `--port 8080` - Use a different port
- `--no-browser` - Don't automatically open browser
- `--build-dir custom-build` - Serve from a different build directory

## Output Structure

The generator creates GitHub Pages compatible URLs:

- `pages/index.html` → `build/index.html` (homepage)
- `pages/about.html` → `build/about/index.html` (accessible at `/about/`)
- `pages/contact.html` → `build/contact/index.html` (accessible at `/contact/`)

## GitHub Pages Deployment

The `build/` directory can be deployed directly to GitHub Pages:

1. Build your site: `python builder.py`
2. Commit the `build/` directory contents to your repository
3. Enable GitHub Pages in your repository settings
4. Point GitHub Pages to the root of your repository (or `docs/` folder if you move the build contents there)

## Example

See the included example files:
- `templates/base.html` - Base template
- `pages/index.html` - Homepage
- `pages/about.html` - About page
- `data/style.css` - Stylesheet

To try the example:
1. `python builder.py` - Build the site
2. `python serve.py` - Start the development server
3. Open `http://localhost:1313` in your browser

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

### Installation

No additional Python packages need to be installed! Both scripts use only Python's built-in standard library modules.

Simply ensure you have Python 3.6+ installed:

```bash
# Check your Python version
python --version
# or
python3 --version

# If you need to install Python, visit: https://python.org/downloads/
```

**Note:** If `python --version` shows Python 2.x, use `python3` instead of `python` for all commands below.

The scripts are ready to run immediately:

```bash
# Build the site (use python3 if your system defaults to Python 2)
python3 builder.py

# Serve the site locally  
python3 serve.py
```

## Features

- ✅ Template-based page generation
- ✅ Automatic SEO-friendly URL structure
- ✅ Asset copying and management
- ✅ Local development server
- ✅ GitHub Pages compatible output
- ✅ Clean, minimal codebase
- ✅ No external dependencies 