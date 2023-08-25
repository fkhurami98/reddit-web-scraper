# Use a base image with Python 3.9
FROM python:3.9

# Set the working directory inside the container
WORKDIR /home/farhadkhurami/reddit-web-scraper

# Copy the application files into the container
COPY . .

# Install Playwright dependencies and Chromium
RUN apt-get update && apt-get install -y \
    libnss3 \
    libglib2.0-0 \
    libx11-6 \
    chromium

# Set locale
ENV LANG C.UTF-8


# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

RUN playwright install --with-deps chromium


CMD ["python3.9", "main.py"]
