FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (needed for some Python packages)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        build-essential \
        g++ \
        gcc \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . .

# Install Agentics from IBM Research Repository
RUN git clone https://github.com/IBM/agentics.git /tmp/agentics && \
    cd /tmp/agentics && \
    pip install -e . && \
    cd /app && \
    rm -rf /tmp/agentics

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install project in editable mode
RUN pip install -e .

# Create .env file placeholder (should be overridden at runtime)
RUN echo "# Environment variables should be set at runtime" > .env

# Expose Streamlit port
EXPOSE 8501

# IMPORTANT: Replace 'your-project-slug' with YOUR actual slug!
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.baseUrlPath=/smart-contracts"]