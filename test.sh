#!/bin/sh
export DATABASE_MAIN_PATH=tests/digikam_db/digikam4.db
export DATABASE_THUMBNAIL_PATH=tests/digikam_db/thumbnails.db
export CORS_ORIGINS='["*"]'
pytest $*
