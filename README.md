# ShiftRx MVP

ShiftRx MVP is a minimal viable product for an AI-powered staffing solution designed for healthcare facility managers. It allows managers to quickly post shift details by sending natural language requests. The application processes the input using an LLM (OpenAI GPT-4o) to extract key shift details, which are then stored in a PostgreSQL database.

## Features

- **Natural Language Processing:** Uses OpenAI's GPT-4o to parse shift details from a free-form text input.
- **RESTful API:** A single endpoint (`POST /shifts/create`) accepts user input and returns a confirmation with a unique shift ID.
- **Database Persistence:** Shift details including position, start time, end time, rate, facility name, and location are stored in a PostgreSQL database.
- **Robust Error Handling & Logging:** Comprehensive logging is implemented using Python's logging module.
- **Continuous Integration (CI):** Automated tests are executed on every commit using GitHub Actions.

## Technologies Used

- **Backend Framework:** Python with Flask
- **Database:** PostgreSQL (with schema including columns: `id`, `position`, `start_time`, `end_time`, `rate`, `facility_name`, `location`, `created_at`)
- **NLP/LLM Integration:** OpenAI GPT-4o
- **Environment Management:** python-dotenv
- **Testing:** pytest
- **CI/CD:** GitHub Actions

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/shiftrx-mvp.git
cd shiftrx-mvp
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
# On Windows using Git Bash:
source venv/Scripts/activate
# On macOS/Linux:
# source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example file to create your own configuration:

```bash
cp .env.example .env
```

Edit the `.env` file and set the following values:

- `OPENAI_API_KEY`: Your OpenAI API key (or a dummy key for testing)
- `DB_HOST`: Typically localhost
- `DB_PORT`: Typically 5432
- `DB_USER`: e.g., postgres
- `DB_PASS`: Your PostgreSQL password (for development, you might use postgres)
- `DB_NAME`: e.g., shiftrx

### 5. Set Up the PostgreSQL Database

Install PostgreSQL if not already installed.

Open your terminal and run:

```bash
psql -U postgres
```

Create the database:

```sql
CREATE DATABASE shiftrx;
\q
```

Initialize the schema:

```bash
psql -U postgres -d shiftrx
```

Then run the following SQL command to create the table:

```sql
CREATE TABLE IF NOT EXISTS shifts (
    id SERIAL PRIMARY KEY,
    position VARCHAR(50),
    start_time VARCHAR(50),
    end_time VARCHAR(50),
    rate VARCHAR(50),
    facility_name VARCHAR(100) DEFAULT 'unknown',
    location VARCHAR(100) DEFAULT 'unknown',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
\q
```

### 6. Running the Application

Start the Flask development server:

```bash
python app.py
```

The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## API Documentation

### POST /shifts/create

**Description:**
Accepts a JSON payload with a `user_input` field containing a natural language description of the shift. The system processes the input using an LLM to extract shift details and then stores the data in the database.

**Request:**

- URL: `/shifts/create`
- Method: `POST`
- Headers:
  - `Content-Type: application/json`

**Body Example:**

```json
{
  "user_input": "We need a Pharmacist at City Hospital in Denver from 9AM to 5PM at $50/hr"
}
```

**Response:**

- Success (`201 Created`):

```json
{
  "success": true,
  "shift_id": 1
}
```

- Error (`400 Bad Request`):

```json
{
  "error": "No user_input provided"
}
```

- Error (`500 Internal Server Error`):

```json
{
  "success": false,
  "error": "Database insertion failed"
}
```

## Testing

Automated tests have been written using pytest. To run the tests:

```bash
pytest
```

## Continuous Integration

GitHub Actions is set up to run tests automatically on every push or pull request. See the `.github/workflows/ci.yml` file for details.

## Logging

The application uses Python’s logging module for robust error handling and debugging. Log messages are printed to the console with timestamps and log levels.

## License

This project is licensed under the MIT License.
