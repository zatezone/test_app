# Expense Tracker

A small Flask expense tracker with expense and income categories, daily dashboard totals, charts, and transaction history.

## Setup

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the example environment file and fill in your local values:

```bash
cp .env.example .env
```

4. Run the app:

```bash
python app.py
```

## Database Setup

1. Create a MySQL database server locally.
2. Run the schema file:

```bash
mysql -u your_mysql_user -p < database/schema.sql
```

3. Seed demo data:

```bash
mysql -u your_mysql_user -p < database/seed.sql
```

4. Use the demo account if you want sample dashboard data right away:

- Email: `demo@example.com`
- Password: `demo1234`

## Environment Variables

Set these in `.env`:

- `DB_HOST`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`
- `SECRET_KEY`

## Notes Before Publishing

- Do not commit your real `.env` file.
- If your password or secret key were ever committed or shared, rotate them before publishing.
- The project uses MySQL, so make sure the schema and seed scripts are imported before running the app.

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── .env.example
├── database/
│   ├── schema.sql
│   └── seed.sql
└── templates/
```
