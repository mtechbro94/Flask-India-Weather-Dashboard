# Use official Python image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Expose Flask port
EXPOSE 5000

# Set environment variable for production
ENV FLASK_ENV=production

# Optionally set OpenWeatherMap API key at runtime
# ENV OPENWEATHER_API_KEY=your_api_key_here

# Run the app
CMD ["python", "app.py"]
