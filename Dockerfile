
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    libxrender1 \
    libxext6 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install rdkit

# # Install RDKit from the wheel file
# COPY rdkit-2024.3.5-cp39-cp39-win_amd64.whl /app/
# RUN pip install /app/rdkit-2024.3.5-cp39-cp39-win_amd64.whl
# RUN rm /app/rdkit-2024.3.5-cp39-cp39-win_amd64.whl

# Collect static files
# RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD python manage.py collectstatic --noinput && gunicorn chemapp.wsgi:application --bind 0.0.0.0:$PORT
