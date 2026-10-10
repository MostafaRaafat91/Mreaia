# ==============================================================================
# Mreaia (مرآيا) - Universal Zero-Token File Engine & Ghost Cryptography
# Dockerfile for Hugging Face Spaces
# 
# Conceived & Directed by: Mostafa Raafat
# Engineered with: Autonomous AI Cyber-Security Swarm (Antigravity Technology)
# License: Mreaia Source-Available Non-Commercial License
# ==============================================================================

FROM python:3.11-slim

# Prevent interactive prompts and buffer outputs
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    GRADIO_SERVER_NAME="0.0.0.0" \
    GRADIO_SERVER_PORT=7860

# Install required system tools (ffmpeg for acoustic analysis, curl, git, compiler)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user matching Hugging Face Spaces requirements (UID 1000)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Install Python dependencies
COPY --chown=user requirements.txt $HOME/app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all application assets and source code
COPY --chown=user . $HOME/app/

# Expose Hugging Face default port
EXPOSE 7860

# Launch Mreaia application
CMD ["python3", "app.py"]
