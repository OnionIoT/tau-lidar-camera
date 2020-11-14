# Documentation

Using Sphinx to generate HTML documentation

## Prerequisites

Install [sphinx](https://www.sphinx-doc.org/en/master/usage/installation.html)

## Building the Docs

```
make clean ; make html
```

HTML output will be in `_build/html`

## Locally Hosting Docs for Testing

After build, to host locally on a dev machine:

```
cd _build/html
python3 -m http.server
```

Navigate to `http://localhost:8000/` in a browser
