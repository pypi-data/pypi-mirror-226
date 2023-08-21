# arghelper

[![PyPi Version][pypi ver image]][pypi ver link]
[![Build Status][travis image]][travis link]
[![Coverage Status][coveralls image]][coveralls link]
[![License Badge][license image]][LICENSE.txt]

[arghelper][] is a Python 3.8+ module providing functions to help with argparse.

## Requirements

- `argparse` module from the [Python Standard Library][]
- `sys` module from the [Python Standard Library][]
- `os` module from the [Python Standard Library][]

## Usage

`arghelper` provides functions to determine if a file or directory
exists:

- `extant_file`
- `extant_dir`

These can be used as follows:

```python
if __name__ == "__main__":
    # Process the arguments
    import argparse
    import arghelper
    parser = argparse.ArgumentParser(
        description='Process the TAFFmat CET files')
    parser.add_argument(
        'config_file',
        help='CSV configuration file.',
        metavar='FILE', type=arghelper.extant_file)
    parser.add_argument(
        'input_dir',
        help='Directory containing input files.',
        metvar='DIR', type=arghelper.extant_dir)
    args = parser.parse_args()
```

A common pattern, for me at least, is to have three positional arguments
consisting of:

1. `config_file` --- A configuration file
2. `input_dir` --- A directory containing input files to be read
3. `output_dir` --- A directory where the output files should be saved

This pattern has been abstracted to a Facade function called
`parse_config_input_output`, which can be used as follows:

```python
if __name__ == "__main__":
    # Process the arguments
    import arghelper
    args = arghelper.parse_config_input_output(sys.argv)
```

Another common pattern is to just parse the name of a config file:

```python
if __name__ == "__main__":
    # Process the arguments
    import arghelper
    args = arghelper.parse_config(sys.argv)
```

## Contributing

Contributions are welcome! To contribute please:

1. Fork the repository
2. Create a feature branch
3. Add code and tests
4. Pass lint and tests
5. Submit a [pull request][]

## Development Setup

### Development Setup Using pyenv

Use the following commands to create a Python 3.9.9 virtualenv using [pyenv][]
and [pyenv-virtualenv][], install the requirements in the virtualenv named
`arghelper`, and list the available [Invoke][] tasks.

```bash
$ pyenv virtualenv 3.11 arghelper
$ pyenv activate arghelper
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ inv -l
```

# License

[arghelper][] is released under the MIT license. Please see the
[LICENSE.txt][] file for more information.

[arghelper]: https://github.com/questrail/arghelper
[coveralls image]: http://img.shields.io/coveralls/questrail/arghelper/master.svg
[coveralls link]: https://coveralls.io/r/questrail/arghelper
[github flow]: http://scottchacon.com/2011/08/31/github-flow.html
[LICENSE.txt]: https://github.com/questrail/arghelper/blob/master/LICENSE.txt
[license image]: http://img.shields.io/pypi/l/arghelper.svg
[pull request]: https://help.github.com/articles/using-pull-requests
[pyenv]: https://github.com/pyenv/pyenv
[pyenv-install]: https://github.com/pyenv/pyenv#installation
[pyenv-virtualenv]: https://github.com/pyenv/pyenv-virtualenv
[pypi ver image]: http://img.shields.io/pypi/v/arghelper.svg
[pypi ver link]: https://pypi.python.org/pypi/arghelper
[python standard library]: https://docs.python.org/2/library/
[travis image]: http://img.shields.io/travis/questrail/arghelper/master.svg
[travis link]: https://travis-ci.org/questrail/arghelper
