FROM python:3.10-slim-bullseye

# 使用国内镜像源加速下载
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
    
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements-app.txt ./

RUN pip install --no-cache-dir -r requirements.txt -r requirements-app.txt

COPY . .

EXPOSE 8000
EXPOSE 7860
EXPOSE 8080

# Unified server with SEO pages (/ , /en), API (/api) and Gradio (/tool)
ENV PUBLIC_SITE_URL=""
CMD ["python3", "-u", "serve.py"]
