# Heredity

## Overview
This project implements an AI to assess the likelihood that a person will have a particular genetic trait. Using a Bayesian network, the program models gene inheritance and calculates probabilities based on the traits of individuals and their family relationships. The focus is on understanding how genes and traits are passed from one generation to the next and their corresponding probabilities.

## Features
- Compute joint probabilities for gene and trait configurations.
- Update cumulative probabilities for all individuals based on new evidence.
- Normalize probabilities to ensure proper distributions.
- Unit tests to validate functionality.

## Files
### Main Program
- **`heredity.py`**: The primary implementation file containing functions to compute probabilities, update distributions, and normalize values.

### Data Files
Under the `data` folder, you’ll find three test files used for calculations and testing:
- **`family0.csv`**
- **`family1.csv`**
- **`family2.csv`**

Each file contains information about individuals, their parents, and whether they exhibit a particular trait. This data is used by the program to infer probabilities.

### Unit Tests
- **`heredity_test.py`**: Contains unit tests to validate the functionality of the `joint_probability`, `update`, and `normalize` functions. The tests ensure the correctness of calculations and edge cases.

## How to Run
1. Clone the repository or download the project files.
2. Ensure Python is installed on your system.
3. Run the program with a data file as input:
   ```bash
   python heredity.py data/family0.csv
   ```

   The output will display the computed probabilities for each individual in the family.

4. Run the unit tests to validate functionality:
   ```bash
   python -m unittest heredity_test.py
   ```

## How It Works
The program uses a Bayesian network to calculate probabilities:
1. **Gene Inheritance**: Each child inherits genes from their parents, influenced by probabilities of mutation.
2. **Trait Calculation**: Traits depend on the number of genes a person has and their associated probabilities.
3. **Joint Probabilities**: These probabilities are combined across all individuals for a specific scenario.
4. **Normalization**: Ensures all probabilities in a distribution sum to 1.

## Contributions
Feel free to contribute to this project by submitting pull requests or opening issues for bugs and enhancements.

## License
This project is licensed under the MIT License.

