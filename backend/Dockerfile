FROM python:3.11-slim

WORKDIR /app

# install ffmpeg (and dependencies) before Python packages
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (required by backend/application/spotify_scrapper.py)
RUN python -m playwright install --with-deps

COPY . .

CMD ["python3", "main.py"]