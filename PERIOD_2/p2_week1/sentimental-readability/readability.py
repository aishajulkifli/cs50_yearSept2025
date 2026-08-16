
text = input("Text: ")                          # promt input from user

letters = 0                                     # count letter from 0
words = 1                                       # start count 1 for each word
sentences = 0                                   # count sentences from 0

for char in text:
    if char.isalpha():
        letters += 1
    if char == " ":
        words += 1
    if char in [".", "!", "?"]:
        sentences += 1

L = (letters / words) * 100
S = (sentences / words) * 100

index = 0.0588 * L - 0.296 * S - 15.8
grade = round(index)

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
