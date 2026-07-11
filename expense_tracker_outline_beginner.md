# Expense Tracker Project Outline for Beginners

## 1. Project Title
Personal Expense Tracker Web App

## 2. Project Goal
Build a simple Flask web application where a user can:
- create an account
- log in securely
- add income and expense transactions
- organize transactions using categories
- view their total income, total expenses, and current balance

This project is good for beginners because it practices:
- Flask routing
- HTML forms
- MySQL database connection
- CRUD operations
- basic authentication
- simple reporting

## 3. Simple Project Description
The Expense Tracker helps users manage their money by recording daily income and expenses. Each transaction belongs to a category, such as Salary, Food, Transportation, or Bills. The app will also show a summary so the user can understand where their money goes.

## 4. Main Features
### Core Features
1. User registration
2. User login and logout
3. Add income transaction
4. Add expense transaction
5. View all transactions
6. Edit a transaction
7. Delete a transaction
8. View dashboard summary
9. Add custom categories
10. Filter transactions by date or type

### Optional Features
1. Monthly report
2. Pie chart or bar chart
3. Export transactions to CSV
4. Search by description

## 5. Database Overview
Your database has 3 main tables:

### `users`
Stores account information for each user.

Fields:
- `user_id` - unique ID for each user
- `name` - user's full name
- `email` - unique email address
- `password_hash` - encrypted password
- `date_created` - date and time the account was created

### `categories`
Stores transaction categories created by the user.

Fields:
- `category_id` - unique ID for each category
- `user_id` - owner of the category
- `category_name` - name of the category
- `category_type` - either `income` or `expense`
- `is_default` - tells whether the category is a default category

### `transactions`
Stores every income and expense entry.

Fields:
- `transaction_id` - unique ID for each transaction
- `user_id` - owner of the transaction
- `category_id` - category used for the transaction
- `transaction_type` - either `income` or `expense`
- `amount` - money value
- `description` - short note about the transaction
- `transaction_date` - date of the transaction
- `created_at` - record creation timestamp
- `updated_at` - record update timestamp

## 6. Database Relationships
1. One user can have many categories.
2. One user can have many transactions.
3. One category can be used in many transactions.

## 7. Suggested Default Categories
These can be inserted when a user registers.

### Income
- Salary
- Allowance
- Business
- Gifts

### Expense
- Food
- Transportation
- Bills
- School
- Entertainment

## 8. Pages to Build
### Public Pages
1. `/` - landing page
2. `/signup` - registration page
3. `/login` - login page

### Logged-in Pages
1. `/dashboard` - summary of income, expenses, and balance
2. `/transactions` - list of all transactions
3. `/transactions/add` - form to add transaction
4. `/transactions/edit/<id>` - form to edit transaction
5. `/transactions/delete/<id>` - delete transaction
6. `/categories` - list and add categories
7. `/logout` - log out user

### Optional Pages
1. `/reports` - monthly report
2. `/export/csv` - download CSV file

## 9. Beginner-Friendly Build Order
Follow this order so the project feels easier.

### Step 1. Set up the Flask project
- create `app.py`
- create `templates/`
- connect Bootstrap for styling
- test that the homepage loads

### Step 2. Set up the MySQL database
- create the database
- create the 3 tables
- test the connection from Flask

### Step 3. Build user registration
- create signup form
- validate email uniqueness
- hash the password before saving
- insert the new user into the `users` table

### Step 4. Build user login
- create login form
- check if email exists
- verify password using the saved hash
- save `user_id` in session

### Step 5. Add logout
- clear session
- redirect to login page

### Step 6. Create categories feature
- show existing categories
- add custom category
- separate income and expense categories

### Step 7. Add transactions
- create a form with:
  - category
  - type
  - amount
  - description
  - date
- save the transaction in the database

### Step 8. Show transaction history
- display all transactions of the logged-in user
- order by latest transaction date
- show amount, category, type, and description

### Step 9. Edit and delete transactions
- allow user to update amount, category, description, or date
- allow user to delete incorrect transactions

### Step 10. Build dashboard summary
- total income
- total expenses
- remaining balance
- latest transactions

### Step 11. Add filters
- filter by category
- filter by transaction type
- filter by date range

### Step 12. Add optional reports
- monthly totals
- charts
- CSV export

## 10. Important Beginner Logic
### Registration
- user enters name, email, and password
- password should be hashed before saving
- app checks if email already exists

### Login
- user enters email and password
- app checks the email
- app compares password with stored hash
- if correct, user starts a session

### Add Transaction
- user selects income or expense
- user selects a category that matches the type
- app saves amount and date

### Dashboard Formula
- `balance = total income - total expenses`

## 11. Recommended Tech Stack
- Frontend: HTML, CSS, Bootstrap
- Backend: Python Flask
- Database: MySQL
- Connector: `mysql-connector-python`
- Authentication helper: `werkzeug.security`

## 12. Folder Structure Example
```text
test_app/
|-- app.py
|-- templates/
|   |-- index.html
|   |-- signup.html
|   |-- login.html
|   |-- dashboard.html
|   |-- transactions.html
|   |-- add_transaction.html
|   |-- edit_transaction.html
|   |-- categories.html
|-- static/
|   |-- css/
|   |-- js/
```

## 13. Beginner Checklist
- database connection works
- signup works
- login works
- session works
- add transaction works
- view transactions works
- edit works
- delete works
- dashboard totals are correct
- categories are separated into income and expense

## 14. Common Mistakes to Avoid
1. Saving plain text passwords instead of hashed passwords
2. Forgetting to filter data by `user_id`
3. Allowing an expense category to be used for an income transaction
4. Forgetting to commit after `INSERT`, `UPDATE`, or `DELETE`
5. Not checking if the user is logged in before showing private pages

## 15. Simple Portfolio Description
Expense Tracker is a beginner-friendly Flask and MySQL web application that allows users to register, log in, record income and expenses, organize transactions by category, and view a financial summary through a personal dashboard.

## 16. Recommended First Version
If you want to keep version 1 simple, build only these features first:
1. Signup
2. Login/logout
3. Add transaction
4. View transaction list
5. Dashboard totals

After that, add:
1. Categories
2. Edit/delete
3. Filters
4. Reports
