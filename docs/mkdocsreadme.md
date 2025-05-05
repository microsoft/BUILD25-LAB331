# Azure Deep Research Workshop Documentation

This directory contains the documentation for the Azure Deep Research Workshop, built with [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

## Prerequisites

To work with this documentation, you'll need:

- Python 3.10 or higher
- Pip package manager

## Local Setup

1. Install MkDocs and required plugins:

```bash
pip install mkdocs mkdocs-material pymdown-extensions mkdocs-glightbox
```

2. Clone this repository (if you haven't already):

```bash
git clone https://github.com/yourusername/azure-deep-research.git
cd azure-deep-research/docs
```

## Previewing the Documentation Locally

To preview the documentation site locally:

```bash
mkdocs serve
```

This will start a local development server at `http://127.0.0.1:8000/`. The site will automatically reload when you make changes to the markdown files.

## Building the Documentation

To build the static site:

```bash
mkdocs build
```

This will create a `site` directory with the built HTML files.

## Deploying to GitHub Pages

There are two ways to deploy the documentation to GitHub Pages:

### Method 1: MkDocs gh-deploy

The easiest way is to use the built-in deployment command:

```bash
mkdocs gh-deploy
```

This command will:
1. Build the documentation
2. Create (or update) a dedicated `gh-pages` branch
3. Push the built site to that branch
4. GitHub will automatically publish the content

### Method 2: Manual GitHub Pages Setup

Alternatively, you can set up GitHub Pages manually:

1. Build the site:

```bash
mkdocs build
```

2. Push the `site` directory to a `gh-pages` branch or configure GitHub Pages to use your preferred branch.

3. In your repository settings, configure GitHub Pages to use the appropriate branch.

## Documentation Structure

The documentation is organized as follows:

```
docs/
├── docs/                 # Documentation source files
│   ├── index.md          # Home page
│   ├── getting-started.md
│   ├── lab-1-reasoning-thoughts.md
│   ├── lab-2-web-research.md
│   ├── lab-3-reflection.md
│   └── lab-4-launch-researcher.md
├── mkdocs.yml           # MkDocs configuration
```

## Customizing the Documentation

### Site Configuration

Edit the `mkdocs.yml` file to customize:
- Site name, description, and author
- Navigation structure
- Theme colors and features
- Plugins and extensions

### Adding Content

1. Add new Markdown files to the `docs/docs/` directory
2. Update the `nav` section in `mkdocs.yml` to include your new pages

## Troubleshooting

- If you see errors about missing plugins, make sure all required packages are installed
- If images are not displaying, check that file paths are correct (use relative paths from the markdown file location)
- For GitHub Pages deployment issues, ensure your repository has GitHub Pages enabled in settings

## Additional Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs Documentation](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
