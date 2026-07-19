# gabriel-sanchezh.github.io

Personal academic website of **Gabriel Sánchez Hernández** — economics,
monetary policy, and financial econometrics.

Live at **[gabriel-sanchezh.github.io](https://gabriel-sanchezh.github.io)**.
Built with [Astro](https://astro.build); deployed to GitHub Pages by the
workflow in `.github/workflows/deploy.yml` on every push to `main`.

## Structure

```
src/pages/            Page templates (About, Research, Teaching)
src/content/research/ One markdown file per research project
src/content/teaching/ One markdown file per course
src/styles/global.css All colors and styling (CSS variables at the top)
public/files/         Papers and slides (PDF)
public/apps/          Interactive WebAssembly demos (marimo exports)
public/notebooks/     Downloadable Jupyter notebooks
apps/                 marimo source for the interactive demos
notebooks/            Notebook sources (also the Colab entry points)
```

## Local development

```bash
npm install
npm run dev        # live preview at http://localhost:4321
npm run build      # production build to dist/
```

## Adding a research project

Create `src/content/research/<slug>.md` with the frontmatter fields
(`title`, `description`, `date`, `abstract`, `keywords`, `conclusions`,
`materials`, `packages`, and optionally `colab`, `notebook`, `app`).
The Research index and project page are generated automatically.

## Regenerating an interactive demo

```bash
.venv/bin/marimo export html-wasm apps/<name>.py -o public/apps/<name> --mode run
```
