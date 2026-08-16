import pandas

data = {
    'Nationality': ['Malaysian', 'Indian', 'Iranian', 'Czech', 'Pakistani', 'Turkish', 'Turkish'],
    'Name': ['Aisha', 'Vyshna', 'Sana', 'Ondrej', 'Uraib', 'Ener', 'Ener'],
    'Age': [35, 27, 23, None, 20, 20, 20]
}

df = pandas.DataFrame(data)

print(df.head(6))            # Display the first few rows of the DataFrame

df.drop_duplicates(inplace = True)      # Remove duplicate rows from the DataFrame

df = df.fillna(0)           # Fill any missing values with 0

print("Mode Age:", df["Age"].mode())    # Calculate and print the mode age

