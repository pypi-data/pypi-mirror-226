# energy-logger

[![PyPI - Version](https://img.shields.io/pypi/v/energy-logger.svg)](https://pypi.org/project/energy-logger)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/energy-logger.svg)](https://pypi.org/project/energy-logger)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

Energy Logger is a way to log 'energy inputs' to data outputs periodically. The inputs and outputs
are declared in the `config.toml` file. At least one input and one output should be present in the
configuration file.

Energy Logger can be run on its own, or included as a module in other projects.

## Installation

```console
pip install energy-logger
```

### Local installs

```console
pip install .
```

#### Testing

```console
pip install '.[test]'
```

#### Docs

```console
pip install '.[docs]'
```


## License

`energy-logger` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
