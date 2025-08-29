import datetime
import pandas as pd

class Expense:
    def __init__(self, name, amount, category, date=None):
        if amount < 0:
            raise ValueError("Expense amount cannot be negative!")
        self.name = name
        self.amount = amount
        self.category = category
        self.date = date if date else datetime.date.today()

    def __str__(self):
        return f"{self.date} | {self.category:<10} | {self.name:<15} | ${self.amount:.2f}"


class ExpenseTracker:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self.expenses = []
        self.load_expenses()

    def add_expense(self, name, amount, category, date=None):
        try:
            expense = Expense(name, float(amount), category, date)
            self.expenses.append(expense)
            self.save_expenses()
            print("✅ Expense added successfully!")
        except ValueError as e:
            print("❌ Error:", e)

    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        print("\n--- All Expenses ---")
        for exp in self.expenses:
            print(exp)

    def monthly_summary(self, year, month):
        if not self.expenses:
            print("No expenses available for summary.")
            return

        data = {
            "Name": [e.name for e in self.expenses],
            "Amount": [e.amount for e in self.expenses],
            "Category": [e.category for e in self.expenses],
            "Date": [e.date for e in self.expenses],
        }

        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])

        monthly_df = df[(df["Date"].dt.year == year) & (df["Date"].dt.month == month)]

        if monthly_df.empty:
            print(f"No expenses for {month}/{year}.")
            return

        total = monthly_df["Amount"].sum()
        category_summary = monthly_df.groupby("Category")["Amount"].sum()

        print(f"\n--- Monthly Summary ({month}/{year}) ---")
        print("Total Spending: $", total)
        print("\nSpending by Category:")
        print(category_summary)

    def save_expenses(self):
        with open(self.filename, "w") as f:
            for exp in self.expenses:
                f.write(f"{exp.name},{exp.amount},{exp.category},{exp.date}\n")

    def load_expenses(self):
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    name, amount, category, date = line.strip().split(",")
                    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                    self.expenses.append(Expense(name, float(amount), category, date))
        except FileNotFoundError:
            pass


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n==== Expense Tracker ====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter expense name: ")
            try:
                amount = float(input("Enter amount: "))
            except ValueError:
                print("❌ Invalid amount. Try again.")
                continue
            category = input("Enter category: ")
            tracker.add_expense(name, amount, category)

        elif choice == "2":
            tracker.view_expenses()

        elif choice == "3":
            try:
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (1-12): "))
                tracker.monthly_summary(year, month)
            except ValueError:
                print("❌ Invalid input for year/month.")

        elif choice == "4":
            print("Exiting Expense Tracker... Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")


if __name__ == "__main__":
    main()
