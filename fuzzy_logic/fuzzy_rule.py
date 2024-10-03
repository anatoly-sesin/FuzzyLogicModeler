class FuzzyRule:
    def __init__(self, antecedents, consequent, weight=1.0, operation="AND"):
        self.antecedents = antecedents  # List of (variable, term) tuples
        self.consequent = consequent    # (variable, term) tuple
        self.weight = weight
        self.operation = operation

    def __str__(self):
        antecedents_str = f" {self.operation} ".join([f"({var} IS {term})" for var, term in self.antecedents])
        return f"IF {antecedents_str} THEN ({self.consequent[0]} IS {self.consequent[1]})"
