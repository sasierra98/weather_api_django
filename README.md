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
