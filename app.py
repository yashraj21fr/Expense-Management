from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"


# Load expenses from JSON file
def load_expenses():
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r") as f:
            return json.load(f)
    return []


# Save expenses to JSON file
def save_expenses(expenses):
    with open("expenses.json", "w") as f:
        json.dump(expenses, f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_expense", methods=["GET", "POST"])
def add_expense():
    expenses = load_expenses()
    if request.method == "POST":
        expense = request.form.get("expense")
        category = request.form.get("category")
        amount = request.form.get("amount")
        date = request.form.get("date")
        time = request.form.get("time")

        if not (expense and category and amount and date and time):
            flash("Please fill in all fields.", "warning")
            return redirect(url_for("add_expense"))

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash("Please enter a valid amount.", "warning")
            return redirect(url_for("add_expense"))

        expenses.append({"expense": expense, "category": category, "amount": amount, "date": date, "time": time})
        save_expenses(expenses)
        flash("Expense added successfully.", "success")
        return redirect(url_for("add_expense"))

    return render_template("add_expense.html", datetime=datetime)


@app.route("/view_expenses")
def view_expenses():
    expenses = load_expenses()
    if not expenses:
        flash("No expenses recorded yet.", "info")
    return render_template("view_expenses.html", expenses=expenses)


if __name__ == "__main__":
    app.run(debug=True)
