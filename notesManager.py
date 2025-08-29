import datetime
import calendar
import os
from colorama import Fore, Style, init
from tabulate import tabulate
import pandas as pd

init(autoreset=True)

class Note:
    def __init__(self, title, content, category, date=None):
        if not content.strip():
            raise ValueError("Note content cannot be empty!")
        self.title = title
        self.content = content
        self.category = category
        self.date = date if date else datetime.date.today()

    def __str__(self):
        return f"[{self.date}] {self.title} ({self.category})"


class DiaryManager:
    def __init__(self, filename="notes.txt"):
        self.filename = filename
        self.notes = []
        self.load_notes()

    def add_note(self, title, content, category):
        try:
            note = Note(title, content, category)
            self.notes.append(note)
            self.save_notes()
            print(Fore.GREEN + "✅ Note added successfully!\n")
        except ValueError as e:
            print(Fore.RED + f"❌ Error: {e}")

    def view_notes(self):
        if not self.notes:
            print(Fore.YELLOW + "No notes found!")
            return
        table = [[i+1, n.date, n.title, n.category, n.content[:40]+"..."] 
                 for i, n in enumerate(self.notes)]
        print(Fore.CYAN + "\n--- All Notes ---")
        print(tabulate(table, headers=["ID", "Date", "Title", "Category", "Preview"], tablefmt="fancy_grid"))

    def search_note(self, keyword):
        results = [n for n in self.notes if keyword.lower() in n.title.lower() or keyword.lower() in n.content.lower()]
        if not results:
            print(Fore.YELLOW + f"No notes found with '{keyword}'")
            return
        table = [[n.date, n.title, n.category, n.content[:50]+"..."] for n in results]
        print(Fore.CYAN + f"\n--- Search Results for '{keyword}' ---")
        print(tabulate(table, headers=["Date", "Title", "Category", "Preview"], tablefmt="grid"))

    def delete_note(self, note_id):
        try:
            deleted = self.notes.pop(note_id-1)
            self.save_notes()
            print(Fore.GREEN + f"✅ Deleted note: {deleted.title}")
        except IndexError:
            print(Fore.RED + "❌ Invalid note ID.")

    def note_calendar(self, year, month):
        cal = calendar.month(year, month)
        print(Fore.MAGENTA + f"\n--- Calendar ({month}/{year}) ---")
        print(cal)
        note_dates = [n.date.day for n in self.notes if n.date.year == year and n.date.month == month]
        if note_dates:
            print(Fore.GREEN + "📌 Notes exist on days:", note_dates)

    def analyze_notes(self):
        if not self.notes:
            print(Fore.YELLOW + "No notes to analyze!")
            return
        data = {
            "Title": [n.title for n in self.notes],
            "Category": [n.category for n in self.notes],
            "Date": [n.date for n in self.notes],
        }
        df = pd.DataFrame(data)
        print(Fore.CYAN + "\n--- Notes Analysis ---")
        print("📊 Notes per Category:")
        print(df["Category"].value_counts())
        print("\n📅 Busiest Day:")
        print(df["Date"].value_counts().head(1))

    def save_notes(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            for n in self.notes:
                f.write(f"{n.title}|{n.content}|{n.category}|{n.date}\n")

    def load_notes(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    title, content, category, date = line.strip().split("|")
                    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                    self.notes.append(Note(title, content, category, date))
        except Exception:
            print(Fore.RED + "❌ Error loading notes file!")


def main():
    diary = DiaryManager()

    while True:
        print(Fore.BLUE + Style.BRIGHT + "\n📓 ==== Personal Diary Menu ====")
        print(Fore.YELLOW + "1. Add Note")
        print("2. View Notes")
        print("3. Search Note")
        print("4. Delete Note")
        print("5. Calendar View")
        print("6. Analyze Notes")
        print("7. Exit")

        choice = input(Fore.WHITE + "Choose an option: ")

        if choice == "1":
            title = input("Enter title: ")
            content = input("Enter content: ")
            category = input("Enter category: ")
            diary.add_note(title, content, category)

        elif choice == "2":
            diary.view_notes()

        elif choice == "3":
            keyword = input("Enter keyword to search: ")
            diary.search_note(keyword)

        elif choice == "4":
            try:
                note_id = int(input("Enter note ID to delete: "))
                diary.delete_note(note_id)
            except ValueError:
                print(Fore.RED + "❌ Invalid input. Please enter a number.")

        elif choice == "5":
            try:
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (1-12): "))
                diary.note_calendar(year, month)
            except ValueError:
                print(Fore.RED + "❌ Invalid input for year/month.")

        elif choice == "6":
            diary.analyze_notes()

        elif choice == "7":
            print(Fore.GREEN + "Exiting Diary... Goodbye!")
            break
        else:
            print(Fore.RED + "❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
