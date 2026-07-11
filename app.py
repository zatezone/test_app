import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def insert_user(cursor, name, email, password_hash):
    cursor.execute(
        """
        insert into users (name, email, password_hash)
        values (%s, %s, %s)
        """,
        (name, email, password_hash)
    )

def add_categories(user_id, cursor):
    cursor.execute(
        """
        select 1 from categories
        where user_id = %s limit 1
        """,
        (user_id,)
    )

    if not cursor.fetchone():
        default_expense_categories = ["Food", "Transport", "Home Bills", "Self-Care", "Shopping", "Health"]
        default_income_categories = ["Salary", "Freelance", "Investment"]

        for category in default_expense_categories:
            cursor.execute(
                """
                insert into categories (user_id, category_name, category_type, is_default)
                values (%s, %s, %s, %s)
                """,
                (user_id, category, "expense", True)
            )
        
        for category in default_income_categories:
            cursor.execute(
                """
                insert into categories (user_id, category_name, category_type, is_default)
                values (%s, %s, %s, %s)
                """,
                (user_id, category, "income", True)
            )

def user_category(cursor, category_name, category_type, user):
    cursor.execute(
        """
        select category_id from categories
        where category_name = %s 
        and category_type = %s
        and user_id = %s
        """,
        (category_name, category_type, user)
    )

    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        cursor.execute(
            """
            insert into categories (user_id, category_name, category_type, is_default)
            values (%s, %s, %s, %s)
            """,
            (user, category_name, "expense", False)
        )

        return cursor.lastrowid
    
def insert_transaction(cursor, user, category_id, amount, description, date):
    cursor.execute(
        """
        insert into transactions (user_id, category_id, transaction_type, amount, description, transaction_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user, category_id, "expense", amount, description, date)
    )

def insert_income(cursor, user, category_id, amount, description, date):
    cursor.execute(
        """
        insert into transactions (user_id, category_id, transaction_type, amount, description, transaction_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user, category_id, "income", amount, description, date)
    )

def expense_category_totals(cursor, user, selected_date):
    cursor.execute(
        """
        select categories.category_name, sum(transactions.amount) as total_amount
        from transactions
        join categories on categories.category_id = transactions.category_id
        where transactions.user_id = %s 
        and transactions.transaction_type = 'expense'
        and transactions.transaction_date = %s
        group by categories.category_name
        """,
        (user, selected_date)
    )

    rows = cursor.fetchall()

    return {row[0]: float(row[1]) for row in rows}

def income_category_totals(cursor, user, selected_date):
    cursor.execute(
        """
        select categories.category_name, sum(transactions.amount) as total_amount
        from transactions
        join categories on categories.category_id = transactions.category_id
        where transactions.user_id = %s 
        and transactions.transaction_type = 'income'
        and transactions.transaction_date = %s
        group by categories.category_name
        """,
        (user, selected_date)
    )

    rows = cursor.fetchall()

    return {row[0]: float(row[1]) for row in rows}

def get_summary(cursor,user):
    cursor.execute(
        """
        select transactions.transaction_id, transactions.transaction_type, categories.category_name, transactions.description, transactions.amount, transactions.transaction_date, categories.category_id
        from transactions
        left join categories on transactions.category_id = categories.category_id
        where transactions.user_id = %s
        order by transactions.transaction_date desc, transactions.created_at desc
        limit 20
        """,
        (user,)
    )

    return cursor.fetchall()

def get_categoryId(cursor, user):
    cursor.execute(
        """
        select category_id, category_name
        from categories
        where user_id = %s
        """,
        (user,)
    )

    return cursor.fetchall()

def total_expenses(cursor, user, selected_date):
    cursor.execute(
        """
        select sum(amount)
        from transactions
        where user_id = %s
        and transaction_type = "expense"
        and transaction_date = %s
        """,
        (user, selected_date)
    )

    return cursor.fetchone()[0] or 0

def total_incomee(cursor, user, selected_date):
    cursor.execute(
        """
        select sum(amount)
        from transactions
        where user_id = %s
        and transaction_type = "income"
        and transaction_date = %s
        """,
        (user, selected_date)
    )

    return cursor.fetchone()[0] or 0

def get_date_range(selected_date, summary_range):
    chosen_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

    if summary_range == "monthly":
        start_date = chosen_date.replace(day=1)

        if chosen_date.month == 12:
            next_month = chosen_date.replace(year=chosen_date.year + 1, month=1, day=1)
        else:
            next_month = chosen_date.replace(month=chosen_date.month + 1, day=1)

        end_date = next_month - timedelta(days=1)
    else:
        start_date = chosen_date - timedelta(days=chosen_date.weekday())
        end_date = start_date + timedelta(days=6)

    return start_date, end_date

def get_chart_totals(cursor, user, transaction_type, start_date, end_date):
    cursor.execute(
        """
        select categories.category_name, sum(transactions.amount) as total_amount
        from transactions
        join categories on categories.category_id = transactions.category_id
        where transactions.user_id = %s
        and transactions.transaction_type = %s
        and transactions.transaction_date between %s and %s
        group by categories.category_name
        order by total_amount desc
        """,
        (user, transaction_type, start_date, end_date)
    )

    rows = cursor.fetchall()
    labels = [row[0] for row in rows]
    values = [float(row[1]) for row in rows]

    return labels, values

def get_total(cursor, user, transaction_type, start_date, end_date):
    cursor.execute(
        """
        select sum(transactions.amount) as total_amount
        from transactions
        join categories on categories.category_id = transactions.category_id
        where transactions.transaction_type = %s
        and transactions.user_id = %s
        and transactions.transaction_date between %s and %s
        """,
        (transaction_type, user, start_date, end_date)
    )

    return cursor.fetchone()[0] or 0

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()

        email = request.form["email"].strip()
        name = request.form["name"].strip()
        password = request.form["password"]

        cursor.execute(
            """
            select * from users where email = %s
            """,
            (email,)
        )
        existing_email = cursor.fetchone()

        if existing_email:
            conn.close()
            return("Email already exists")

        password_hash = generate_password_hash(password, method="pbkdf2:sha256")
        insert_user(cursor, name, email, password_hash)

        conn.commit()
        conn.close()

        flash("Signup successful.", "success")

        return redirect("/login")

    return render_template("signup.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()

        login_email = request.form["email"].strip()
        login_password = request.form["password"]

        cursor.execute(
            """
            SELECT * from users
            where email = %s
            """,
            (login_email,)
        )
        user = cursor.fetchone()

        if not user:
            flash("Account not found.", "error")
        elif user and check_password_hash(user[3], login_password):
            session["user_id"] = user[0]
            session["name"] = user[1]

            add_categories(user[0], cursor)

            conn.commit()
            conn.close()

            flash("Login successful.", "success")
            return redirect("/add_expense")
        else:
            flash("Invalid email or password.", "error")
    
    return render_template("index.html")

@app.route("/add_expense", methods=["POST", "GET"])
def add_expense():
    user = session.get("user_id")
    if not user:
        return redirect("/login")
    
    selected_date = request.args.get("selected_date")
    if not selected_date:
        selected_date = datetime.today().strftime("%Y-%m-%d")

    summary_range = request.args.get("summary_range", "weekly")
    if summary_range not in ["weekly", "monthly"]:
        summary_range = "weekly"
    
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()

        amount = request.form["amount"]
        description = request.form["description"]
        date = request.form["date"]
        category_name = request.form["category"]
        type_category = request.form["category_type"]

        category_id = user_category(cursor, category_name, type_category, user)
        insert_transaction(cursor, user, category_id, amount, description, date)

        conn.commit()
        cursor.close()
        conn.close()

        flash("Added successfully.", "success")
        return redirect("/add_expense")
    
    conn = get_connection()
    cursor = conn.cursor()

    expense_totals = expense_category_totals(cursor, user, selected_date)
    income_totals = income_category_totals(cursor, user, selected_date)
    summary_transactions = get_summary(cursor, user)
    categories_id = get_categoryId(cursor, user)
    total_expense = total_expenses(cursor, user, selected_date)
    total_income = total_incomee(cursor, user, selected_date)
    start_date, end_date = get_date_range(selected_date, summary_range)
    expense_chart_labels, expense_chart_values = get_chart_totals(cursor, user, "expense", start_date, end_date)
    income_chart_labels, income_chart_values = get_chart_totals(cursor, user, "income", start_date, end_date)
    overall_total_expense = get_total(cursor, user, "expense", start_date, end_date)
    overall_total_income = get_total(cursor, user, "income", start_date, end_date)

    cursor.close()
    conn.close()
        
    return render_template(
        "home.html", expense_totals=expense_totals, income_totals=income_totals, summary_transactions=summary_transactions, categories_id=categories_id, total_expense=total_expense, 
        total_income=total_income, selected_date=selected_date, summary_range=summary_range, expense_chart_labels=expense_chart_labels, expense_chart_values=expense_chart_values, 
        income_chart_labels=income_chart_labels, income_chart_values=income_chart_values, overall_total_expense=overall_total_expense, overall_total_income=overall_total_income
    )
    
@app.route("/add_income", methods=["POST"])
def add_income():
    user = session.get("user_id")
    if not user:
        return redirect("/login")
    
    conn = get_connection()
    cursor = conn.cursor()

    amount = request.form["amount"]
    description = request.form["description"]
    date = request.form["date"]
    category_name = request.form["category"]
    type_category = request.form["category_type"]

    category_id = user_category(cursor, category_name, type_category, user)
    insert_income(cursor, user, category_id, amount, description, date)

    conn.commit()
    cursor.close()
    conn.close()

    flash("Added successfully.", "success")

    return redirect("/add_expense")


@app.route("/delete_transaction", methods=["POST"])
def delete_expense():
    conn = get_connection()
    cursor = conn.cursor()

    transaction_id = request.form["transaction_id"]

    cursor.execute(
        """
        delete from transactions where transaction_id = %s
        """,
        (transaction_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Successfully deleted transaction.", "success")

    return redirect("/add_expense")

@app.route("/update_transaction", methods=["POST"])
def update_transaction():
    user = session.get("user_id")
    if not user:
        return redirect("/login")
    
    conn = get_connection()
    cursor = conn.cursor()

    transaction_id = request.form["transaction_id"]
    category_id = request.form["category"].strip()
    description = request.form["description"].strip()
    amount = request.form["amount"]

    cursor.execute(
        """
        update transactions
        set category_id = %s, description = %s, amount = %s
        where transaction_id = %s
        and user_id = %s
        """,
        (category_id, description, amount, transaction_id, user)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Transaction updated successfully.", "success")

    return redirect("/add_expense")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)