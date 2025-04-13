# Use a base image with Flutter and Python
FROM ubuntu:22.04

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies directly without virtual environment
# This is a simpler approach for Docker containers
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Set Google Cloud Project environment variable
ENV GOOGLE_CLOUD_PROJECT="resume-chatbot-generator"
ENV GOOGLE_CLOUD_REGION="us-central1"

# Expose the port your server runs on (adjust if needed)
EXPOSE 8080

# Run the server
CMD ["mesop", "main.py", "--port", "8080"]