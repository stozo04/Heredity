import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_genes` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set `have_trait` does not have the trait.
    """
    joint_prob = 1

    for person in people:
        # Check if this person has parents
        if people[person]["mother"] is None and people[person]["father"] is None:
            # Determine gene count
            if person in two_genes:
                gene_count = 2
            elif person in one_gene:
                gene_count = 1
            else:
                gene_count = 0

            # Unconditional probability for the gene count
            gene_prob = PROBS["gene"][gene_count]

            # Conditional probability for the trait
            has_trait = person in have_trait
            trait_prob = PROBS["trait"][gene_count][has_trait]

            # Multiply the probabilities
            person_prob = gene_prob * trait_prob
            print(f"{person}: gene_prob={gene_prob}, trait_prob={trait_prob}, person_prob={person_prob}")

        else:
            # For individuals with parents, calculate the probability of inheriting their genes
            mother = people[person]["mother"]
            father = people[person]["father"]

            # Helper function to calculate inheritance probability
            def parent_inheritance_prob(parent):
                if parent in two_genes:
                    return 1 - PROBS["mutation"]
                elif parent in one_gene:
                    return 0.5
                else:
                    return PROBS["mutation"]

            # Probabilities of getting the gene from each parent
            from_mother = parent_inheritance_prob(mother)
            from_father = parent_inheritance_prob(father)

            # Combine probabilities for child's gene count
            if person in two_genes:
                gene_prob = from_mother * from_father
            elif person in one_gene:
                gene_prob = (from_mother * (1 - from_father)) + ((1 - from_mother) * from_father)
            else:
                gene_prob = (1 - from_mother) * (1 - from_father)

            # Conditional probability for the trait
            has_trait = person in have_trait
            trait_prob = PROBS["trait"][2 if person in two_genes else 1 if person in one_gene else 0][has_trait]

            # Multiply the probabilities
            person_prob = gene_prob * trait_prob
            print(f"{person}: from_mother={from_mother}, from_father={from_father}, gene_prob={gene_prob}, trait_prob={trait_prob}, person_prob={person_prob}")

        # Accumulate into the joint probability
        joint_prob *= person_prob

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # Determine the count for this person
        if person in two_genes:
            gene_count = 2
        elif person in one_gene:
            gene_count = 1
        else:
            gene_count = 0

        # Determine the trait for this person
        trait = person in have_trait

        # Update the probabilities
        probabilities[person]["gene"][gene_count] += p
        probabilities[person]["trait"][trait] += p

        # Should not return anything!


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Normalize gene probabilities
        gene_total = sum(probabilities[person]["gene"].values())
        for gene_count in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene_count] /= gene_total

        # Normalize trait probabilities
        trait_total = sum(probabilities[person]["trait"].values())
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= trait_total

    # Should not return anything!


if __name__ == "__main__":
    main()
