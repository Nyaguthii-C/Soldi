# Soldi
Expenses tracking application - Python/Django Backend - Django Rest Framework
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


## Views

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