# NYC DSA Healthcare Website

A Pelican-powered static site for the NYC DSA Healthcare Working Group, deployed automatically to GitHub Pages.

## Local Development

### Prerequisites

- Python 3.12+
- [Pipenv](https://pipenv.pypa.io/en/latest/)

Install pipenv if you haven't:
```bash
pip install pipenv
```

### Setup

1. Clone the repository:
```bash
git clone https://github.com/nyc-dsa-healthcare/nyc-dsa-healthcare.github.io.git
cd nyc-dsa-healthcare.github.io
```

2. Install dependencies with Pipenv:
```bash
make install
# Or directly: pipenv install
```

This creates a virtual environment and installs Pelican with Markdown support.

### Running the development server

```bash
make devserver
```

Then visit http://localhost:8000 to see your site.

To stop the server, press `Ctrl+C`.

### Running Pelican commands

Use `pipenv run` to execute Pelican commands:

```bash
# Build the site
pipenv run pelican content -o output -s pelicanconf.py

# List all available commands
pipenv run pelican --help
```

Or use the Makefile shortcuts:

```bash
make html        # Build once
make clean       # Remove output/
make regenerate  # Auto-regenerate on changes
make serve       # Serve only (no regeneration)
```

### Using the virtual environment directly

```bash
# Enter the virtual environment
pipenv shell

# Now you can run pelican directly
pelican content -o output -s pelicanconf.py
pelican -lr content -o output -s pelicanconf.py  # dev server

# Exit the virtual environment
exit
```

## Adding Content

Create new content in the `content/` directory:

- **Pages**: Add to `content/pages/` for static pages
- **Blog posts**: Add to `content/` directly or organize by category

Example:
```markdown
Title: My Post Title
Date: 2024-02-24
Category: General
Tags: tag1, tag2
Slug: my-post
Author: Your Name

Your content here...
```

## Deployment

The site is automatically deployed to GitHub Pages via GitHub Actions when you push to the `main` branch. No manual steps needed!

### GitHub Pages Settings

Ensure your repository is configured:
1. Go to **Settings → Pages**
2. Set **Source** to "GitHub Actions"
3. (Optional) Enable **Enforce HTTPS**

## Managing Dependencies

### Add new packages

```bash
pipenv install <package>
```

For development dependencies:
```bash
pipenv install --dev <package>
```

### Update dependencies

```bash
pipenv update
```

### Generate lock file

```bash
pipenv lock
```

## Project Structure

```
.
├── .github/workflows/pelican.yml  # GitHub Actions workflow
├── content/                       # Website content (Markdown files)
├── output/                        # Generated site (not in git)
├── pelicanconf.py                 # Development settings
├── publishconf.py                 # Production settings
├── Pipfile                        # Pipenv dependencies
├── Pipfile.lock                   # Locked dependency versions
└── Makefile                       # Convenience commands
```

### Why both Pipfile and requirements.txt?

- **Pipfile/Pipfile.lock**: Used for local development with Pipenv
- **requirements.txt**: Generated for GitHub Actions compatibility

The `Pipfile` is the source of truth. You can regenerate `requirements.txt` if needed:
```bash
pipenv requirements > requirements.txt
```

## Theme

By default, Pelican uses a simple theme. To use a custom theme, add to `pelicanconf.py`:

```python
THEME = "path/to/theme"
```

Or specify a GitHub repo in the GitHub Actions workflow (see `.github/workflows/pelican.yml`).

## License

[Your license here]
