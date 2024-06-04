# TrainAPIService

TrainAPIService is a robust API service designed to provide real-time 
information and functionalities related to train schedules, routes, 
and ticket bookings. The service aggregates data from various train operators 
and offers a unified interface for accessing train-related information.

## Requirements

List of main dependencies required to run the project:

- Python 3.x
- Django 4.x (or other version)
- DRF Spectacular
- Django Extensions 3.x
- Django RestFramework 3.x


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Dmitriy-Poplinski/TrainAPI_Service
    ```

2. Navigate to the project directory:
    ```sh
    cd TrainAPIService
    ```

3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On MacOS/Linux:
        ```sh
        source venv/bin/activate
        ```

5. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

6. Create a `.env` file based on the `.env.example` and fill in the necessary environment variables.

7. Run database migrations:
    ```sh
    python manage.py migrate
    ```

8. Start the development server:
    ```sh
    python manage.py runserver
    ```

## Testing

How to run the tests for the project:
```sh
python manage.py test
