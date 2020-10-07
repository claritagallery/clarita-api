# Clarita API backend

## Install

    $ pipenv install

Clarita should work on Python 3.7 or later, but it has been most tested on Python 3.8.

## Development

    $ pipenv install --dev
    $ cd src/clarita
    $ pipenv run uvicorn main:app --reload

## Changelog

See [CHANGELOG](CHANGELOG.md).

## Benchmarks and performance

TODO

The biggest performance impact will come from placing the SQLite databases in an SSD and not an
HDD. If an SSD is not an option then consider copying the database into a ramdisk.
