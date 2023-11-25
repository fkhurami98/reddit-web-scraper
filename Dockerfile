FROM python:3.9

# Set the working directory inside the container
WORKDIR /reddit-web-scraper/

# Copy the application files into the container
COPY . .

# Install dependencies 
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

CMD ["python", "main.py"]
