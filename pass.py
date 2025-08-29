import re

dictionary_words = ["password", "admin", "welcome", "qwerty", "user", "login", "abc123", 
                    "anisha", "anish", "maharjan"]

common_passwords = [
    "123456", "123456789", "qwerty", "password", "111111", "123123", "12345678",
    "abc123", "password1", "iloveyou", "000000", "admin"
]

def check_password_strength(password):
    errors = []

    if len(password) < 12:
        errors.append("Password must be at least 12 characters long.")


    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")
    if not re.search(r"[0-9]", password):
        errors.append("Password must contain at least one digit.")
    if not re.search(r"[^A-Za-z0-9]", password):
        errors.append("Password must contain at least one special character.")


    for word in dictionary_words:
        if word.lower() in password.lower():
            errors.append(f"Password contains dictionary word: '{word}'")
            break

  
    if password.lower() in common_passwords:
        errors.append("Password is too common and guessable.")

    if errors:
        return False, errors
    else:
        return True, ["Password is strong!"]

if __name__ == "__main__":
   
    while True:
        pwd = input("\nEnter your password: ")
        valid, messages = check_password_strength(pwd)

        print("\nPassword Check Results:")
        for msg in messages:
            print(" -", msg)

        if valid:
            print("\n✅ Password accepted!")
            break 
        else:
            print("\n❌ Please try again and fix the above issues.")
