#Given the following string: text = "  Hello, World! Welcome to Python Programming.  "
#Write a program that prints:
    #The string with leading and trailing spaces removed (use strip())
    #The number of words in the string (use split())
    #The string with the first letter of each word capitalized (use title())
    #Whether the stripped string starts with "Hello" (use startswith())
    #Whether the stripped string ends with "ing." (use endswith())
    #The position (index) of the word "Python" in the stripped string (use find())
    #The words joined back together separated by " - " (use split() and " - ".join())

text = "  Hello, World! Welcome to Python Programming.  "
new_text = text.strip()
print("stripped:", text.strip())
print("Word count:", len(new_text))
print("Title case:", new_text.title())
print("Starts with hello", new_text.startswith("Hello"))
print("Ends with ing.", new_text.endswith("ing."))
print("The word python is in position", new_text.find("Python"))
print("Joined", "-".join(new_text))




