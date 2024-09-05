# Clarita API backend

This is an API for the Clarita Web Gallery, which exposes a [Digikam](https://www.digikam.org/) photo collection through a nice web interface.

See the [Clarita React Frontend](https://github.com/claritagallery/clarita-react-frontend) for a consumer of this API.

## Run with Docker

Build the image:

    docker build . -t clarita:latest

Run it with:

    docker run --env CORS_ORIGINS='["*"]' -v /path/to/digikam_data:/home/appuser/digikam_data:ro --rm clarita:latest

On a real deployment you should set `CORS_ORIGINS` to the list of hostnames where Clarita is hosted.

`/path/to/digikam_data` should be the local path to where Digikam SQLite databases are stored.

See [.env.example](.env.example) for all possible environment values.

## Install manually

Clarita uses [rye](https://rye.astral.sh/) for dependency management.

This project supports [direnv](https://direnv.net/).
If you use it you need to [add support for the rye layout](https://github.com/direnv/direnv/wiki/Python#rye), then just run `direnv allow`.

To install dependencies manually run:

    rye sync

Clarita should work on Python 3.10 or later, but it has been most tested on Python 3.12.

## Development

Copy *.env.example* file as *.env*.
Default values should work for local development.

    rye sync
    rye run dev

To run ruff linters:

    rye lint

To run tests:

    rye test

Install the pre-commit hooks to lint code before every commit:

    pre-commit install

## Changelog

See [CHANGELOG](CHANGELOG.md).

## Benchmarks and performance

TODO

The biggest performance impact will come from placing the SQLite databases in an SSD and not an HDD.
If an SSD is not an option then consider copying the database into a ramdisk.
