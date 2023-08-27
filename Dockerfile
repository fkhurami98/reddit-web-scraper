# Use a base image with Python 3.9
FROM python:3.9

# Set the working directory inside the container
WORKDIR /home/farhadkhurami/reddit-web-scraper

# Copy the application files into the container
COPY . .

# Install dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libnss3 \
    libglib2.0-0 \
    libx11-6 \
    python3-pip


# Install Python dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright and Chromium
RUN pip install playwright
RUN playwright install --with-deps chromium

# Set the entry point for your application
CMD ["python", "main.py"]
