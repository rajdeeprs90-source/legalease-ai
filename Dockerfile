# 1. Base image: lightweight Linux + Python 3.11
FROM python:3.11-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Install system-level dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy dependency list first (for caching)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy application source code
COPY app ./app
COPY prompts ./prompts

# 7. Expose Streamlit port
EXPOSE 8501

# 8. Command to start the app
CMD ["streamlit", "run", "app/app.py", "--server.address=0.0.0.0"]
