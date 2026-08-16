# Exercise 1: Prompt Classifier
# Fix the bugs and complete the TODOs.
# Goal:
# - repair the code
# - classify prompts as short / medium / long

prompts = [
    "generate image",
    "write a poem about robots",
    "hello there",
    "create a detailed story about a time-traveling scientist"
]

def count_words(text):
    words = text.split()
    return len(words)

def classify_prompt(text):
    count = count_words(text)

    if count < 3:
        return "short"
    elif 3 <= count <= 6:
        return "medium"
    else:
        return "long"
    # TODO:
    # return "short" if count < 3
    # return "medium" if count is 3 to 6
    # return "long" if count > 6
    pass

for prompt in prompts:
    print(prompt, "->", classify_prompt(prompt))
