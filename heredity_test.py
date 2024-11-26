import unittest
from heredity import joint_probability, normalize, update

class TestHeredity(unittest.TestCase):

    def test_joint_probability(self):
        people = {
            "Harry": {"mother": None, "father": None, "trait": None},
            "James": {"mother": None, "father": None, "trait": True},
            "Lily": {"mother": None, "father": None, "trait": False},
        }
        one_gene = {"Harry"}
        two_genes = {"James"}
        have_trait = {"James"}

        # Call joint_probability and compare with expected output
        result = joint_probability(people, one_gene, two_genes, have_trait)
        expected = 8.154432e-05
        self.assertAlmostEqual(result, expected, places=6)

    def test_all_zero_genes(self): 
        people = {
            "Harry": {"mother": None, "father": None, "trait": None}
        }
        one_gene = set()
        two_genes = set()
        have_trait = set()

        result = joint_probability(people, one_gene, two_genes, have_trait)
        expected = 0.9504  # PROBS["gene"][0] * PROBS["trait"][0][False]
        self.assertAlmostEqual(result, expected, places=6)

    def test_inheritance_scenario(self):
        people = {
            "Harry": {"mother": "Lily", "father": "James", "trait": None},
            "James": {"mother": None, "father": None, "trait": True},
            "Lily": {"mother": None, "father": None, "trait": False},
        }
        one_gene = {"Harry"}
        two_genes = {"James"}
        have_trait = {"James"}
        
        result = joint_probability(people, one_gene, two_genes, have_trait)
        expected = 0.0026643247488
        self.assertAlmostEqual(result, expected, places=6)

    def test_update(self):
        # Initial probabilities dictionary
        probabilities = {
            "Harry": {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}},
            "James": {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        }
        
        # Example configuration
        one_gene = {"Harry"}       # Harry has one gene
        two_genes = {"James"}      # James has two genes
        have_trait = {"James"}     # Only James has the trait
        p = 0.01                   # Joint probability

        # Call the update function
        update(probabilities, one_gene, two_genes, have_trait, p)

        # Assertions
        self.assertAlmostEqual(probabilities["Harry"]["gene"][1], 0.01)
        self.assertAlmostEqual(probabilities["Harry"]["trait"][False], 0.01)
        self.assertAlmostEqual(probabilities["James"]["gene"][2], 0.01)
        self.assertAlmostEqual(probabilities["James"]["trait"][True], 0.01)

        # Ensure other probabilities remain 0
        self.assertAlmostEqual(probabilities["Harry"]["gene"][0], 0)
        self.assertAlmostEqual(probabilities["Harry"]["gene"][2], 0)
        self.assertAlmostEqual(probabilities["Harry"]["trait"][True], 0)
        self.assertAlmostEqual(probabilities["James"]["gene"][0], 0)
        self.assertAlmostEqual(probabilities["James"]["gene"][1], 0)
        self.assertAlmostEqual(probabilities["James"]["trait"][False], 0)

    def test_normalize(self):
        # Initial unnormalized probabilities
        probabilities = {
            "Harry": {
                "gene": {2: 0.2, 1: 0.5, 0: 0.3},
                "trait": {True: 0.4, False: 0.6}
            },
            "James": {
                "gene": {2: 0.1, 1: 0.1, 0: 0.8},
                "trait": {True: 0.7, False: 0.3}
            }
        }

        # Call normalize
        normalize(probabilities)

        # Assertions
        for person in probabilities:
            # Gene probabilities should sum to 1
            self.assertAlmostEqual(sum(probabilities[person]["gene"].values()), 1, places=6)
            # Trait probabilities should sum to 1
            self.assertAlmostEqual(sum(probabilities[person]["trait"].values()), 1, places=6)

        # Check specific normalized values
        self.assertAlmostEqual(probabilities["Harry"]["gene"][2], 0.2 / 1.0, places=6)
        self.assertAlmostEqual(probabilities["Harry"]["trait"][True], 0.4 / 1.0, places=6)


if __name__ == "__main__":
    unittest.main()
