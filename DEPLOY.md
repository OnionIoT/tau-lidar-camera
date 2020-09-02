## Building and Publishing the Package

Prereqs:

```
python3 -m pip install --user --upgrade setuptools wheel
python3 -m pip install --user --upgrade twine
```

To build the package:

```
python3 setup.py sdist bdist_wheel
```

To deploy to test pypi:

```
python3 -m twine upload --repository testpypi dist/*
```
