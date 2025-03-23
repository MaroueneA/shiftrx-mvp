# ShiftRx MVP

This project is a minimal viable product (MVP) for the ShiftRx AI application, which helps healthcare facility managers post shift requirements quickly. The MVP includes a single endpoint that accepts shift details in natural language, processes them using an LLM, and stores the parsed information in a PostgreSQL database.

## Features

- **Single API Endpoint:** `POST /shifts/create`
- **LLM Integration:** Uses the OpenAI API (or a local LLM) to extract key shift details from natural language input.
- **Database Persistence:** Stores shift details (position, start time, end time, rate) in a PostgreSQL database.

## Technologies Used

- **Python 3** and **Flask** for the REST API
- **PostgreSQL** for database management
- **OpenAI API**  for natural language processing
- **psycopg2** for PostgreSQL connectivity
- **python-dotenv** for environment variable management

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/shiftrx-mvp.git
cd shiftrx-mvp
```
