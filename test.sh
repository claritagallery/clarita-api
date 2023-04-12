#!/bin/sh
export DATABASE_MAIN_PATH=tests/test-digikam4.db
export DATABASE_THUMBNAIL_PATH=tests/test-thumbnails.db
export CORS_ORIGINS='["*"]'
pytest $*
