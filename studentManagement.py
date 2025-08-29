import datetime
import os
import pandas as pd
import calendar

class Student:
    def __init__(self, name, age, grade, city, admission_date=None):
        if age <= 0:
            raise ValueError("Age must be positive!")
        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100!")
        if not name.strip():
            raise ValueError("Name cannot be blank!")
        if not city.strip():
            raise ValueError("City cannot be blank!")

        self.name = name.strip()
        self.age = age
        self.grade = grade
        self.city = city.strip()
        self.admission_date = admission_date if admission_date else datetime.date.today()

    def __str__(self):
        status = "Pass" if self.grade >= 40 else "Fail"
        return f"{self.name:<15} | Age: {self.age:<2} | Grade: {self.grade:<3} ({status}) | City: {self.city:<10} | Admission: {self.admission_date}"


class StudentManager:
    def __init__(self, filename="students.txt"):
        self.filename = filename
        self.students = []
        self.load_students()

    def add_student(self, name, age, grade, city):
        try:
            student = Student(name, int(age), int(grade), city)
            self.students.append(student)
            self.save_students()
            print("✅ Student added successfully!")
        except ValueError as e:
            print("❌ Error:", e)

    def view_students(self):
        if not self.students:
            print("No students available.")
            return
        print("\n--- Student Records ---")
        for i, s in enumerate(self.students, start=1):
            print(f"{i}. {s}")

    def update_student(self, student_id, name=None, age=None, grade=None, city=None):
        try:
            student = self.students[student_id - 1]

            if name and name.strip():
                student.name = name.strip()
            if age:
                student.age = int(age)
                if student.age <= 0:
                    raise ValueError("Age must be positive!")
            if grade:
                student.grade = int(grade)
                if student.grade < 0 or student.grade > 100:
                    raise ValueError("Grade must be between 0 and 100!")
            if city and city.strip():
                student.city = city.strip()

            self.save_students()
            print("✅ Student updated successfully!")
        except (IndexError, ValueError) as e:
            print("❌ Error:", e)

    def delete_student(self, student_id):
        try:
            deleted = self.students.pop(student_id - 1)
            self.save_students()
            print(f"✅ Deleted student: {deleted.name}")
        except IndexError:
            print("❌ Invalid student ID.")

    def analyze_students(self):
        if not self.students:
            print("No students to analyze.")
            return
        data = {
            "Name": [s.name for s in self.students],
            "Age": [s.age for s in self.students],
            "Grade": [s.grade for s in self.students],
            "City": [s.city for s in self.students],
            "Admission Date": [s.admission_date for s in self.students],
        }
        df = pd.DataFrame(data)

        print("\n--- Student Analysis ---")
        print("📊 Average Age:", round(df["Age"].mean(), 2))
        print("📊 Average Grade:", round(df["Grade"].mean(), 2))
        print("\n📊 Students by City:")
        print(df["City"].value_counts())
        print("\n📊 Students Pass vs Fail:")
        print((df["Grade"] >= 40).value_counts().rename({True: "Pass", False: "Fail"}))

    def show_calendar(self, year, month):
        print(f"\n--- Calendar ({month}/{year}) ---")
        print(calendar.month(year, month))

    def save_students(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            for s in self.students:
                f.write(f"{s.name}|{s.age}|{s.grade}|{s.city}|{s.admission_date}\n")

    def load_students(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    name, age, grade, city, admission_date = line.strip().split("|")
                    admission_date = datetime.datetime.strptime(admission_date, "%Y-%m-%d").date()
                    self.students.append(Student(name, int(age), int(grade), city, admission_date))
        except Exception as e:
            print("❌ Error loading student file:", e)


def main():
    manager = StudentManager()

    while True:
        print("\n🎓 ==== Student Management System ====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Analyze Students")
        print("6. Calendar View")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter name: ")
            try:
                age = int(input("Enter age: "))
                grade = int(input("Enter grade (0-100): "))
            except ValueError:
                print("❌ Invalid number input.")
                continue
            city = input("Enter city: ")
            manager.add_student(name, age, grade, city)

        elif choice == "2":
            manager.view_students()

        elif choice == "3":
            try:
                student_id = int(input("Enter student ID to update: "))
                name = input("Enter new name (leave blank to skip): ") or None
                age = input("Enter new age (leave blank to skip): ") or None
                grade = input("Enter new grade (leave blank to skip): ") or None
                city = input("Enter new city (leave blank to skip): ") or None
                manager.update_student(student_id, name, age, grade, city)
            except ValueError:
                print("❌ Invalid input.")

        elif choice == "4":
            try:
                student_id = int(input("Enter student ID to delete: "))
                manager.delete_student(student_id)
            except ValueError:
                print("❌ Invalid input.")

        elif choice == "5":
            manager.analyze_students()

        elif choice == "6":
            try:
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (1-12): "))
                manager.show_calendar(year, month)
            except ValueError:
                print("❌ Invalid input for year/month.")

        elif choice == "7":
            print("👋 Exiting Student Management System. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
