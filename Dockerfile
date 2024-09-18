FROM python:3.11-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PATH /home/appuser/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# create and switch to a new user, running as root is insecure!
RUN useradd --create-home appuser
WORKDIR /home/appuser/clarita
USER appuser

COPY requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock

# Install application into container
COPY . ./

ENV CLARITA_DATA_DIR /home/appuser/clarita_data/
ENV DIGIKAM_DB_DIR /home/appuser/digikam_data/
ENV PORT 8000
EXPOSE $PORT

# Run the application
CMD ["uvicorn", "--host", "0.0.0.0", "--app-dir", "src", "clarita.main:app"]
