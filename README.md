# Soldi
An expenses tracking application built in python/Django, Django Rest Framework and postgreSQL database. Supports user registration, authentication, logging and categorization of expenses and budget.

---

## Features 
- User Profile  
- Budget  
- Budget Categories  
- Expense (logging)  
- Expense Categories  
<!-- - AI Parsing Log (optional)  
- AI Chat History (later) -->  


## Models  
User (authentication)  
UserProfile (monthly budget and user-specific settings)  
ExpenseCategory (shared list of categories)  
Expense (the actual spending records)  
BudgetCategory (per-user monthly allocations by category)  

## Tech Stack

- **Backend**: Django, Django REST Framework  
- **Database**: PostgreSQL  
- **Docs**: Swagger / drf-yasg  
- **Testing**: Pytest, pytest-django
- **DevOps**: Docker, Docker Compose  
- [**Frontend**](https://github.com/Nyaguthii-C/soldi-frontend.git): JavaScript, Css, HTML, Vite, React  


## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/Nyaguthii-C/Soldi.git
cd Soldi

```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environmental Variables .env
```
SECRET_KEY=valuehere
POSTGRES_DB=valuehere
POSTGRES_USER=valuehere
POSTGRES_PASSWORD=valuehere
DEBUG=TrueOrFalse
DATABASE_URL=valuehere
ALLOWED_HOSTS=valuehere
```
### 5. Configure Database  
Set up PostgreSQL and update .env (see .env.example).  
Create a PostgreSQL database and user (if not already created).  
#### Log in to PostgreSQL:  
   Open your terminal and log in to the PostgreSQL command line interface:

   ```bash
   psql -U postgres
   ```

   (Replace `postgres` with your username if you use a different PostgreSQL username.)

#### Create a Database:
   To create a new database, run:

   ```sql
   CREATE DATABASE your_db_name;
   ```

#### Create a User:
   Create a user (if it doesn’t exist) with a password:

   ```sql
   CREATE USER your_db_user WITH PASSWORD 'your_db_password';
   ```

#### Grant Privileges:
   Grant all privileges on the database to the user:

   ```sql
   GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
   ```

#### Exit PostgreSQL:

   ```sql
   \q
   ``` -->

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Collect static files
```bash
python manage.py collectstatic
```
### 7. Run Server (supporting wsgi)
<!-- ```bash
python manage.py runserver
``` -->

```bash
gunicorn config.wsgi:application
```

## Running Tests
```bash
pytest
```

## API Documentation
Access Swagger UI at:
```bash
http://localhost:8000/swagger/

```

## Docker Setup (Optional)

0. Installing Docker and Docker Compose
```bash
sudo apt update && sudo apt install docker.io docker-compose -y
sudo systemctl enable docker -->
```

1. Build and Run the Containers

```bash
sudo docker-compose up --build
```

2. Access App
```bash
API: http://localhost:8000

Swagger Docs: http://localhost:8000/swagger/
```

3. Common Docker Commands

### Stop all services
```bash
docker-compose down
```
### View logs from web app
```bash
docker-compose logs -f web
```
### Bash into the web container
```bash
docker-compose exec web bash
```

<!-- 
## SERVICE FLOW
User Prompt
      │
      ▼
parse_expense(prompt)
      │
      ▼
[
    {
      description,
      amount,
      category
    }
]
      │
      ▼
create_expenses(user, parsed_expenses)
      │
      ▼
Expense table
      │
      ▼
get_monthly_summary(user, year, month)
      │
      ▼
JSON Response



# logging expenses
User Prompt
      │
      ▼
ExpensePromptSerializer
      │
      ▼
parse_expense(prompt)
      │
      ▼
[
    {
        "description":"Bread",
        "amount":120,
        "category":"Food"
    },
    {
        "description":"Milk",
        "amount":80,
        "category":"Food"
    },
    {
        "description":"Bus fare",
        "amount":100,
        "category":"Transport"
    }
]
      │
      ▼
create_expenses()
      │
      ▼
Expense.objects.create(...)
      │
      ▼
Database
      │
      ▼
ExpenseSerializer
      │
      ▼
Response

 -->


## Views
```bash
Views
│
├── register()
├── get_profile()
├── update_profile()
├── log_expense()
│        │
│        └── create_expenses()
│                 │
│                 └── create_expense()
│
├── list_expenses()
├── update_expense()
├── delete_expense()
│
├── month_total()
│        │
│        └── get_month_total()
│
├── category_summary()
│        │
│        └── get_category_summary()
│
└── monthly_summary()
         │
         ├── get_month_total()
         └── get_category_summary()
```  

## Author  
[Nyaguthii Carol](https://github.com/Nyaguthii-C)  
