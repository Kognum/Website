<div align="center">
    <img src="https://github.com/user-attachments/assets/a179e0ff-6f25-4623-a20c-19ac8f68f02f"">
    <h3>KOGNUM's World Wide Web page</h3>
    <h4>Powered by a static site generator written in Python and hosted by Github Pages.</h4>
</div>

## Directory Structure

```
project/
├── data/           # CSS, images, and other assets
├── pages/          # HTML pages with TEMPLATE tags
├── templates/      # HTML templates with CONTENT placeholders
├── builder.py      # Build script
├── server.py       # Development server (doesn't support hot reloading)
└── build/          # Generated output (created by builder.py)
```

## Scripts

`builder.py`
- Builds the static site from source files in the /pages directory and parsing them acording to their choosen template.
  
`server.py`
- Serves the built site from the generated source locally in a simple HTTP server for development (doesn't have hot reload).

## Requirements

- Python 3.6 or higher
