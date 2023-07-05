#!/bin/sh
export DATABASE_MAIN_PATH=tests/digikam_db/digikam4.db
export DATABASE_THUMBNAIL_PATH=tests/digikam_db/thumbnails-digikam.db
export CORS_ORIGINS='["*"]'
export ROOT_MAP="{\"1\": \"$(pwd)/tests/images/\"}"
pytest $*
