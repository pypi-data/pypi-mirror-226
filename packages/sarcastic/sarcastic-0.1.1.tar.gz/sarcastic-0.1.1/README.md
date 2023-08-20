[![PyPI version](https://img.shields.io/pypi/v/sarcastic)](https://pypi.org/project/sarcastic/)
[![Python Versions](https://img.shields.io/pypi/pyversions/sarcastic)](https://pypi.org/project/sarcastic/)
[![License: GPL3+](https://img.shields.io/badge/License-GPL3+-yellow.svg)](https://opensource.org/licenses/gpl-3-0)

# sArCaStIc

mAkEs YoUr tExT SaRcAsTiC.

## Dependencies

* [python3];
* [pip3];

## Instalation

This package is not available on [PyPI] yet.
So the only way to install **sarcastic** is by using our latests [distribution packages] or building your own using the steps shown bellow:

### Building distribution packages

Create a virtual environment with:

```sh
$ virtualenv venv
$ source venv/bin/activate
```

Install python [build]:

```sh
$ python3 -m pip install --upgrade build
```

Now run this command in **sarcastic** root folder:

```sh
$ python3 -m build
```

This command should output a lot of text and once completed should generate two files in the `dist` directory:

```sh
$ ls dist/
sarcastic_*-py3-none-any.whl
sarcastic_*.tar.gz
```

Now to install **sarcastic** use the following command:

```sh
$ pip install dist/sarcastic_*.tar.gz
```

## Usage

You can convert your text to sarcastic mode by passing the string as an argument such as bellow:

``` sh
$ sarcastic "This is a test"
tHiS Is a tEsT
```

Or you can pass the text by piping it:

``` sh
$ echo "All you need is love. But a little chocolate now and then doesn't hurt." | sarcastic
aLl yOu nEeD Is lOvE. bUt a lItTlE ChOcOlAtE NoW AnD ThEn dOeSn't hUrT.
```

This phrase is from [Charles M. Schulz](https://en.wikipedia.org/wiki/Charles_M._Schulz) by the way.

## Team

| <img src="https://github.com/Calebe94.png" width="200px"> |
|:---------------------------------------------------------:|
| [Edimar Calebe Castanho (Calebe94)](https://github.com/Calebe94) |

## License

All software is covered under [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

[python3]: https://python.org
[pip3]: https://pypi.org/project/pip/
[build]: https://pypi.org/project/build/
[PyPI]: https://pypi.org/
[distribution packages]: https://packaging.python.org/glossary/#term-Distribution-Package
