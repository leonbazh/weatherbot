
# Documentation for Weather Telegram Bot & REST API

## Overview

This project includes two major components:
1. A **Telegram bot** that provides weather information.
2. A **REST API** to view logs of user queries.

### Table of Contents
1. [Telegram Bot](#telegram-bot)
   - [Commands](#commands)
   - [Examples](#examples)
2. [REST API](#rest-api)
   - [Endpoints](#endpoints)
   - [Query Parameters](#query-parameters)
   - [Examples](#examples)
3. [Database Schema](#database-schema)
4. [How to Run](#how-to-run)

---

## Telegram Bot

This bot allows users to fetch current weather information by typing commands in a Telegram chat. It interacts with an external weather API (e.g., OpenWeatherMap) and logs the details of each request in the database.

### Commands

| Command             | Description                                      |
|---------------------|--------------------------------------------------|
| `/start`            | Starts interaction with the bot.                 |
| `/weather <city>`   | Fetches current weather data for the specified city. |
| `/help`             | Provides help information about bot commands.    |

### Examples

#### Example 1: `/weather Kazan`
- **Request**: `/weather Kazan`
- **Response**:
  ```
  Weather in Kazan:
  Temp: 15.6°C
  Feels like: 14.2°C
  Description: Clear sky
  Humidity: 60%
  Wind speed: 3.5 m/s
  ```

#### Error Handling:
- If the user types an invalid city or if the weather API is unavailable:
  ```
  Sorry, I couldn't find the weather for the city you requested. Please check the city name and try again.
  ```

---

## REST API

The REST API allows users to view the history of requests made to the Telegram bot. It supports fetching logs, filtering by user ID, and pagination for easier data management.

### Endpoints

#### `GET /logs`
Returns the list of logs of all user queries. Supports pagination and optional filtering by date.

- **URL**: `/logs`
- **Method**: `GET`
- **Description**: Retrieves logs of all user queries.
- **Query Parameters**:
  - `page` (optional, integer): Specifies which page to retrieve. Default is 1.
  - `page_size` (optional, integer): Number of logs per page. Default is 10.
  - `start_time` (optional, datetime): Start date and time to filter logs.
  - `end_time` (optional, datetime): End date and time to filter logs.

- **Response Example**:
```json
[
  {
    "user_id": 833274610,
    "command": "/weather Kazan",
    "timestamp": "2024-10-11T00:25:30.557953",
    "response": "Weather in London:\nTemp: 15.6°C\nFeels like: 14.2°C\nDescription: Clear sky\nHumidity: 60%\nWind speed: 3.5 m/s"
  },
  {
    "user_id": 123456789,
    "command": "/weather Kazan",
    "timestamp": "2024-10-11T02:12:05.123456",
    "response": "Weather in Paris:\nTemp: 12.5°C\nFeels like: 10.3°C\nDescription: Cloudy\nHumidity: 75%\nWind speed: 5.1 m/s"
  }
]
```

---

#### `GET /logs/{user_id}`
Returns the history of requests made by a specific user.

- **URL**: `/logs/{user_id}`
- **Method**: `GET`
- **Description**: Retrieves logs for a specific user.
- **Path Parameter**:
  - `user_id` (integer): The ID of the user whose logs should be retrieved.

- **Query Parameters**:
  - `page` (optional, integer): Specifies which page to retrieve. Default is 1.
  - `page_size` (optional, integer): Number of logs per page. Default is 10.
  - `start_time` (optional, datetime): Start date and time to filter logs.
  - `end_time` (optional, datetime): End date and time to filter logs.

- **Response Example**:
```json
[
  {
    "user_id": 833274610,
    "command": "/weather Kazan",
    "timestamp": "2024-10-11T00:25:30.557953",
    "response": "Weather in London:\nTemp: 15.6°C\nFeels like: 14.2°C\nDescription: Clear sky\nHumidity: 60%\nWind speed: 3.5 m/s"
  }
]
```

---

### Query Parameters

- **`page`**: Specifies the page number for paginated results.
- **`page_size`**: Specifies how many logs are returned per page.
- **`start_time`**: Filters logs starting from this date and time (format: `YYYY-MM-DDTHH:MM:SS`).
- **`end_time`**: Filters logs up to this date and time (format: `YYYY-MM-DDTHH:MM:SS`).

### Examples

#### Example 1: Fetch logs from a specific time range

**Request**:
```
GET /logs?page=1&page_size=5&start_time=2024-10-10T00:00:00&end_time=2024-10-11T23:59:59
```

**Response**:
```json
[
  {
    "user_id": 833274610,
    "command": "/weather Kazan",
    "timestamp": "2024-10-11T00:25:30.557953",
    "response": "Weather in London:\nTemp: 15.6°C\nFeels like: 14.2°C\nDescription: Clear sky\nHumidity: 60%\nWind speed: 3.5 m/s"
  }
]
```

#### Example 2: Fetch logs for a specific user

**Request**:
```
GET /logs/833274610?page=1&page_size=5
```

**Response**:
```json
[
  {
    "user_id": 833274610,
    "command": "/weather Kazan",
    "timestamp": "2024-10-11T00:25:30.557953",
    "response": "Weather in London:\nTemp: 15.6°C\nFeels like: 14.2°C\nDescription: Clear sky\nHumidity: 60%\nWind speed: 3.5 m/s"
  }
]
```

---

## Database Schema

The project uses a PostgreSQL database to store logs of user requests. Below is the schema for the `logs` table:

### Table: `logs`

| Column Name  | Data Type | Description                              |
|--------------|-----------|------------------------------------------|
| `id`         | `SERIAL`  | Unique identifier for the log entry.     |
| `user_id`    | `BIGINT`  | Telegram user ID who made the request.   |
| `command`    | `TEXT`    | Command that the user sent to the bot.   |
| `timestamp`  | `TIMESTAMP` | Date and time of the request.         |
| `response`   | `TEXT`    | The bot's response to the user.          |

---

## How to Run

### Prerequisites
1. **Python 3.9+**
2. **PostgreSQL**
3. **pip** - Python package manager

### Steps

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up the PostgreSQL database**:
   - Create a PostgreSQL database and update the connection details in your `.env` file.

3. **Run the bot**:
   ```bash
   python bot.py
   ```

4. **Run the FastAPI REST server**:
   ```bash
   uvicorn app:app --reload
   ```

5. **Access the REST API**:
   - Open your browser or use `curl` to access `http://127.0.0.1:8000/logs`.
