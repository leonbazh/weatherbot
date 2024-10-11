# Weather Bot API Documentation

## Overview
This is a Telegram bot that provides weather information for a specified city. The bot logs all requests to a PostgreSQL database.

## Telegram Bot
- **API Token**: Replace `API_TOKEN` with your own Telegram bot token.
- **Commands**:
  - `/start`: Initializes the bot and gives a welcome message.
  - `/weather <city>`: Retrieves the current weather for the specified city.

### Example Usage
1. Start the bot by sending `/start`.
2. Request weather information by sending `/weather London`.

## Weather Data
The bot retrieves weather data from an external weather API. The response includes:
- Temperature
- Feels Like Temperature
- Weather Description
- Humidity
- Wind Speed

## Database Logging
All user requests and bot responses are logged in a PostgreSQL database.

### Table Structure
```sql
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    command TEXT,
    timestamp TIMESTAMP,
    response TEXT
);
```

## REST API for Viewing Logs
The bot provides a REST API for retrieving the history of requests.

### Endpoints
- **GET /logs**: Returns a list of all requests.
- **GET /logs/{user_id}**: Returns requests from a specific user.

### Example Requests
1. To get all logs: `GET /logs?page=1&page_size=10`
2. To get logs for a specific user: `GET /logs/123456?page=1&page_size=10`

## Pagination
Both endpoints support pagination using `page` and `page_size` query parameters.

## Tests
The project includes unit tests to verify the functionality of the bot and the REST API.

### Test Cases
1. **Test for getting all logs**: Checks if all logs are returned correctly.
2. **Test for getting logs for a specific user**: Validates that logs for a specific user are retrieved.
3. **Test for pagination**: Ensures pagination works correctly by checking the number of returned logs based on page size.
4. **Test for invalid user ID**: Verifies that an appropriate error message is returned for a user ID that doesn't exist.

### Running Tests
To run the tests, use the following command:
```bash
pytest api_test.py
```

## Conclusion
This documentation outlines how to use the Weather Bot and its REST API. Ensure that you have the required permissions and tokens set up before using the bot.
