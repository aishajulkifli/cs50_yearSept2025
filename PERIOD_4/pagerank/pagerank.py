from importlib.metadata import distribution
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    num_pages = len(corpus)     # Total number of pages in the corpus
    links = corpus[page]        # Get all pages linked from the current page

    if len(links) == 0:         # If the current page has no outgoing links
        return {                # treat it as linking to every page in the corpus
            p: 1 / num_pages    
            for p in corpus
     }

    distribution = {
        p: (1 - damping_factor) / num_pages         # Start by assigning the random-jump probability to every page in the corpus
        for p in corpus
    }

    for linked_page in links:
        distribution[linked_page] += damping_factor / len(links)        # Distribute the damping-factor probability among pages linked by the current page

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())     # Convert all page names into a list

    counts = {                      # Create a dictionary to count how many times, each page is visited during sampling
        page: 0
        for page in corpus
    }

    current_page = random.choice(pages)         # Choose the first page randomly
    counts[current_page] += 1                   # Count the first visit

    for _ in range(1, n):                       # Generate the remaining samples, start from 1 until n - 1

        distribution = transition_model(         # Get the probability distribution for, next page based on the current page
            corpus,
            current_page,
            damping_factor
        )

        current_page = random.choices(              # Choose the next page according to the probability distribution by transition_model()
            population=list(distribution.keys()),
            weights=list(distribution.values()),
            k=1
        )[0]

        counts[current_page] += 1                   # Count the visit to the next page

    pagerank = {
        page: counts[page] / n
        for page in corpus
    }

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)     # Total number of pages in the corpus

    pagerank = {                # Start by assigning equal PageRank to every page
        page: 1 / num_pages
        for page in corpus
    }

    while True:             # Continue recalculating PageRank values until convergence

        new_pagerank = {}   # Store newly calculated PageRank values

        for page in corpus: # Calculate PageRank for every page

            total = 0         # Sum of contributions from incoming pages

            for possible_page in corpus:     # Check every page in the corpus

                links = corpus[possible_page]

                # Page with no links counts as linking to every page
                if len(links) == 0:
                    total += pagerank[possible_page] / num_pages

                 # If possible_page links to current page, add its contribution to the total
                elif page in links: 
                    total += pagerank[possible_page] / len(links)

            new_pagerank[page] = (                  # Apply the PageRank formula
                (1 - damping_factor) / num_pages
                + damping_factor * total
            )

        # Check convergence
        converged = True

        for page in corpus:              # Compare old and new PageRank values
            if abs(new_pagerank[page] - pagerank[page]) > 0.001:    # If any page changes by more than 0.001, keep iterating
                converged = False
                break

        pagerank = new_pagerank         # Update PageRank values

        if converged:               
            break                       # Stop when all pages have converged

    return pagerank

if __name__ == "__main__":
    main()
