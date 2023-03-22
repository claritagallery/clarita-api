# Clarita API backend

This is an API for the Clarita Web Gallery.

See the Clarita React Frontend for a consumer of this API.

## Install

Clarita uses [pipenv](https://pipenv.pypa.io/) for dependency management.

This project supports [direnv](https://direnv.net/).
If you use it just run `direnv allow`.

To install dependencies manually run:

    $ pipenv install --deploy

Clarita should work on Python 3.10 or later, but it has been most tested on Python 3.10.

## Development

Copy *.env.example* file as *.env*.
Default values should work for local development.

```
$ pipenv install --dev
$ cd src
$ pipenv run uvicorn clarita.main:app --reload
```

## Changelog

See [CHANGELOG](CHANGELOG.md).

## Benchmarks and performance

TODO

The biggest performance impact will come from placing the SQLite databases in an SSD and not an HDD.
If an SSD is not an option then consider copying the database into a ramdisk.
