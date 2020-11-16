# Documentation

Using [Sphinx](https://www.sphinx-doc.org/en/master/) to generate HTML documentation and the following Sphinx extensions:

* [AutoDoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) for pulling in documentation from docstrings in a semi-automatic way.
* [Napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) to support NumPy and Google style docstrings

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
