family_tree = {
    "Alice": ["Bob", "Charlie"],
    "Bob": ["David"],
    "Charlie": ["Eve", "Frank"],
    "David": ["George"],
    "Eve": ["Hannah"],
    "Frank": ["Isaac"]
}


# Function to collect all people in the family tree
def get_all_people(tree):

    people = set()

    for parent, children in tree.items():
        people.add(parent)

        for child in children:
            people.add(child)

    return people


# Function to calculate GIRank
def calculate_girank(tree, iterations=10):

    people = get_all_people(tree)

    ranks = {}

    # Everyone starts with rank 1
    for person in people:
        ranks[person] = 1.0

    for i in range(iterations):

        new_ranks = {}

        # Give everyone a small base value
        for person in people:
            new_ranks[person] = 0.15

        # Distribute influence
        for parent, children in tree.items():

            if len(children) == 0:
                continue

            share = (ranks[parent] * 0.85) / len(children)

            for child in children:
                new_ranks[child] += share

        ranks = new_ranks

    return ranks

def main():

    print("GENETIC INFLUENCE RANK (GIRANK)")
    print("-" * 35)

    ranks = calculate_girank(family_tree)

    # Sort from highest influence to lowest
    sorted_ranks = sorted(
        ranks.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print("\nFinal GIRank Results:\n")

    for person, rank in sorted_ranks:
        print(f"{person}: {rank:.4f}")

main()

