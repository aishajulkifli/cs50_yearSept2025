family_tree = {
    "Alice": ["Bob", "Charlie"],
    "Bob": ["David"],
    "Charlie": ["Eve", "Frank"],
    "David": ["George"],
    "Eve": ["Hannah"],
    "Frank": ["Isaac"]
}

# 1.0 = normal genes, >1.0 = stronger genes, <1.0 = weaker genes
dominance = {
    "Alice": 1.5,
    "Bob": 1.0,
    "Charlie": 0.8,
    "David": 1.2,
    "Eve": 1.0,
    "Frank": 1.0,
    "George": 1.0,
    "Hannah": 1.0,
    "Isaac": 1.0
}

def get_all_people(tree):

    people = set()

    for parent, children in tree.items():       # Add parent to set

        people.add(parent)

        for child in children:                  # Add child to set
            people.add(child)

    return people

def calculate_girank_plus(tree, dominance, iterations=10):

    people = get_all_people(tree)

    # Everyone starts with the same influence
    ranks = {}

    for person in people:
        ranks[person] = 1.0

    # Genetic dilution factor, Only 80% influence is passed on
    DILUTION_FACTOR = 0.8

    # Similar to PageRank damping
    BASE_INFLUENCE = 0.15

    # Repeat several times
    for i in range(iterations):

        # Start everyone with base influence
        new_ranks = {}

        for person in people:
            new_ranks[person] = BASE_INFLUENCE

        # Distribute influence
        for parent, children in tree.items():

            # Skip if no children
            if len(children) == 0:
                continue

            share = (
                ranks[parent]           # Current influence
                * DILUTION_FACTOR
                * dominance[parent]     # Dominance factor
            ) / len(children)           # Number of children

            # Give influence to each child
            for child in children:
                new_ranks[child] += share

        # Update ranks
        ranks = new_ranks

    return ranks

def display_results(ranks):

    print("\nGIRANK+ RESULTS")
    print("-" * 40)

    # Sort from highest to lowest
    sorted_ranks = sorted(
        ranks.items(),
        key=lambda item: item[1],  # Sort by rank value, lambda item: item[1] is a function that takes an item (a tuple of (person, rank)) and returns the rank value for sorting
        reverse=True               # Sort in descending order
    )

    for person, rank in sorted_ranks:
        print(f"{person:<10} : {rank:.4f}")     # Print the person's name left-aligned in a field of width 10, followed by the rank formatted to 4 decimal places

def main():

    print("GENETIC INFLUENCE RANK PLUS (GIRANK+)")
    print("=" * 40)

    ranks = calculate_girank_plus(          # Call the calculate_girank_plus function with the family tree, dominance factors, and number of iterations to compute the GIRank+ scores
        family_tree,
        dominance,
        iterations=10
    )

    display_results(ranks)

main()
