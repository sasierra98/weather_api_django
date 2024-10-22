# Weather API Django Project

## Project Description
This project is a weather API built using Django, a high-level Python web framework. The API allows users to retrieve weather information for various locations. It leverages Redis for caching and MongoDB for storing weather data. The project is designed to be easily deployable using Docker, ensuring a consistent environment across different development and production setups.

## Technologies Used
- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Redis**: An in-memory data structure store, used as a database, cache, and message broker.
- **MongoDB**: A source-available cross-platform document-oriented database program.

## Running the Project with Docker
1. Ensure Docker is installed and running on your machine.
2. Navigate to the project directory.
3. Build the Docker images:
    ```sh
    docker-compose build
    ```
4. Start the Docker containers:
    ```sh
    docker-compose up
    ```
5. The application should now be running and accessible at `http://localhost:8000`.

## Running the Project without Docker
1. Ensure Python and virtualenv are installed on your machine.
2. Navigate to the project directory.
3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
5. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
6. Run the Django development server:
    ```sh
    python manage.py runserver
    ```
7. The application should now be running and accessible at `http://localhost:8000`.

## Running Tests with Pytest
1. Ensure the virtual environment is activated.
2. Install pytest if not already installed:
    ```sh
    pip install pytest
    ```
3. Run the tests:
    ```sh
    pytest
    ```
4. The test results will be displayed in the terminal.

### Finding the API URLs

To find these URLs, you can use the developer tools in your web browser. Follow these steps:

1. Open your web browser and navigate to the OpenWeatherMap city page, for example, [Bogota](https://openweathermap.org/city/3688689).
2. Open the developer tools by pressing `F12` or right-clicking on the page and selecting `Inspect`.
3. Go to the `Network` tab in the developer tools.
4. Refresh the page to capture the network requests.
5. Look for requests made to the OpenWeatherMap API endpoints. These requests will contain the URLs you need.

By following these steps, you can easily find the necessary API URLs for different cities.

## Handling API Request Failures

In case the request to the OpenWeather API fails, the application will handle the error gracefully and return an appropriate response to the user. Common reasons for request failures include network issues, invalid API keys, or exceeding the rate limit.

### Adding the API Key to the Request Headers

To authenticate requests to the OpenWeather API, you can include your API key in the headers of the request. Use the following headers to add your API key:

- `X-Open-Weather-Key`: Corresponding the appid of the data endpoint. For instance: https://api.openweathermap.org/data/2.5/weather?id=3688689&appid=5796abbde9106b7da4febfae8c44c232
- `X-Open-Weather-Call-Key`: Corresponding the appid of the onecall endpoint. For instance: https://api.openweathermap.org/data/2.5/onecall?lat=4.6097&lon=-74.0817&units=metric&appid=5796abbde9106b7da4febfae8c44c2324


Example of adding headers in a request:

```python
import requests

url = "https://api.openweathermap.org/data/2.5/weather"
headers = {
    "X-Open-Weather-Key": "your_api_key_here",
    "X-Open-Weather-Call-Key": "your_call_key_here"
}
params = {
    "city": "Bogota",
    "country": "co"
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    weather_data = response.json()
else:
    print("Failed to retrieve data:", response.status_code, response.text)
```

Ensure you replace `"your_api_key_here"` and `"your_call_key_here"` with your actual API keys.

## Live Demo

You can see a demonstration of the app's functionality at the following link: [Weather API Demo](https://weather-api-django.onrender.com/weather/?city=Bogota&country=co)