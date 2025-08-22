# Weather Forecasting App

This is an end-to-end Weather Forecasting web application built with Python and Streamlit. The app allows users to get weather forecasts for Indian cities, featuring a user-friendly interface and automated CI/CD deployment using GitHub Actions and Streamlit Cloud.

## Features

- Real-time weather forecasting for Indian cities
- Simple and interactive UI
- Automated deployment with CI/CD pipeline
- Docker support for containerized deployment

## Project Structure

```
app.py                # Main application file
Dockerfile            # Docker configuration
JenkinsFile           # Jenkins pipeline (optional)
requirements.txt      # Python dependencies
static/               # Static files (CSS, JSON)
templates/            # HTML templates
```

### Prerequisites

- Python 3.8+
- pip
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mtechbro94/Flask-India-Weather-Dashboard
   cd Flask-India-Weather-Dashboard
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app locally:
   ```bash
   streamlit run app.py
   ```

### Docker (Optional)

To run the app in a Docker container:

```bash
docker build -t weather-forecasting-app .
docker run -p 8501:8501 weather-forecasting-app
```

## CI/CD & Deployment

This project uses GitHub Actions for CI/CD and is deployed automatically to Streamlit Cloud on every push to the `main` branch.

### Setting up CI/CD

1. Push your code to GitHub.
2. Configure a GitHub Actions workflow (see `.github/workflows/streamlit-deploy.yml`).
3. Connect your GitHub repo to Streamlit Cloud and set the main file as `app.py`.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [OpenWeatherMap API](https://openweathermap.org/api) (if used)
