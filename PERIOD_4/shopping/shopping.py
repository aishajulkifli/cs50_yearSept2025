import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):    # Load shopping data from CSV and return (evidence, labels)

    evidence = []           # List of lists, where each list contains the features for a single data point
    labels = []             # List of labels corresponding to each data point in evidence

    # Convert month abbreviations to numbers
    months = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "June": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11
    }

    with open(filename, "r") as file:   # Open the CSV file for reading
        reader = csv.DictReader(file)   # Create a CSV reader that maps the information in each row to a dictionary

        for row in reader:              # Iterate over each row in the CSV file

            evidence.append([
                int(row["Administrative"]),
                float(row["Administrative_Duration"]),
                int(row["Informational"]),
                float(row["Informational_Duration"]),
                int(row["ProductRelated"]),
                float(row["ProductRelated_Duration"]),
                float(row["BounceRates"]),
                float(row["ExitRates"]),
                float(row["PageValues"]),
                float(row["SpecialDay"]),
                months[row["Month"]],
                int(row["OperatingSystems"]),
                int(row["Browser"]),
                int(row["Region"]),
                int(row["TrafficType"]),
                1 if row["VisitorType"] == "Returning_Visitor" else 0,
                1 if row["Weekend"] == "TRUE" else 0
            ])

            labels.append(
                1 if row["Revenue"] == "TRUE" else 0
            )

    return evidence, labels


def train_model(evidence, labels):      # Train and return a k-NN model with k=1

    model = KNeighborsClassifier(n_neighbors=1) # Create a k-NN classifier with k=1
    model.fit(evidence, labels)                 # Fit the model to the training data (evidence and labels)

    return model


def evaluate(labels, predictions):      # Calculate sensitivity and specificity

    positive_total = 0
    positive_correct = 0

    negative_total = 0
    negative_correct = 0

    for actual, predicted in zip(labels, predictions):      # Iterate over the actual labels and predicted labels

        # Positive cases (Revenue = TRUE)
        if actual == 1:
            positive_total += 1

            if predicted == actual:                         # If the predicted label matches the actual label, increment the count of correct positive predictions
                positive_correct += 1

        # Negative cases (Revenue = FALSE)
        else:
            negative_total += 1

            if predicted == actual:
                negative_correct += 1

    sensitivity = positive_correct / positive_total
    specificity = negative_correct / negative_total

    return sensitivity, specificity


if __name__ == "__main__":
    main()
