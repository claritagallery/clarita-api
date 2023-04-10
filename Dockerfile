FROM python:3.11-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PATH /home/appuser/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# create and switch to a new user, running as root is insecure!
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser


FROM base AS python-deps

# install Python dependencies in /home/appuser/.local/
ENV PIP_USER 1
ENV PIP_NO_CACHE_DIR 1
ENV PIPENV_SYSTEM 1

# Install pipenv
RUN pip install pipenv

COPY Pipfile Pipfile.lock /tmp/
RUN cd /tmp && pipenv install --deploy


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /home/appuser /home/appuser

# Install application into container
COPY . clarita/

WORKDIR /home/appuser/clarita

ENV DATABASE_MAIN_PATH /home/appuser/digikam_data/digikam4.db
ENV DATABASE_THUMBNAIL_PATH /home/appuser/digikam_data/thumbnails-digikam.db
ENV PORT 8000
EXPOSE $PORT

# Run the application
CMD ["uvicorn", "--host", "0.0.0.0", "--app-dir", "src", "clarita.main:app"]
