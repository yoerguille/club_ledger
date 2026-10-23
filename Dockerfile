# Stage 1: Build frontend assets
FROM node:22-bookworm-slim AS frontend

WORKDIR /app

# Install root dependencies (Flowbite)
COPY package.json package-lock.json ./
RUN npm ci

# Install Tailwind build dependencies
WORKDIR /app/theme/static_src

COPY theme/static_src/package.json theme/static_src/package-lock.json ./
RUN npm ci

# Copy project files required by Tailwind
WORKDIR /app

COPY theme/ ./theme/
COPY templates/ ./templates/
COPY apps/ ./apps/
COPY static/ ./static/

# Compile Tailwind CSS
WORKDIR /app/theme/static_src

RUN npm run build

# Stage 2: Django application
FROM python:3.12-slim-bookworm AS backend

WORKDIR /app

# System libraries required by WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libharfbuzz-subset0 \
    libffi8 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY . .

# Copy compiled CSS from frontend stage
COPY --from=frontend /app/theme/static/css/dist/styles.css \
    /app/theme/static/css/dist/styles.css

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]