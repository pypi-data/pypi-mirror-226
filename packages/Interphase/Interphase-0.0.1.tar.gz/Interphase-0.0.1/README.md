# Interphase

# interface is not supported yet

defualt is export On
default is type = 
need file name
need type name
need any data

base directory can be empty string
d.ts is supported & it is defualt


# dev

```bash
pip install --upgrade setuptools
pip install --upgrade build #python -m build
```

```bash
$ pip install -q build
$ python -m build
```

pyproject.toml `https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html`

```
dist/
    meowpkg-0.0.1.whl
    meowpkg-0.0.1.tar.gz
```

```bash
$ pip install dist/meowpkg-0.0.1.whl
$ pip install dist/meowpkg-0.0.1.tar.gz
```

upload to pypi
```bash
$ python -m twine upload --repository pypi dist/*
```