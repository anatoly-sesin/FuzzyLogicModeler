class FuzzyRule:
    def __init__(self, antecedents, consequent, weight=1.0, operation="AND"):
        self.antecedents = antecedents  # List of (variable, term) tuples
        self.consequent = consequent    # (variable, term) tuple
        self.weight = weight
        self.operation = operation

    def __str__(self, sugeno=False):
        if not sugeno:
            antecedents_str = f" {self.operation} ".join([f"({var} IS {term})" for var, term in self.antecedents])
            return f"IF {antecedents_str} THEN ({self.consequent[0]} IS {self.consequent[1]})"
        else:
            antecedents_str = f" {self.operation} ".join([f"({'_'.join(var.split())} IS {'_'.join(term.split())})" for var, term in self.antecedents])
            return f"IF {antecedents_str} THEN ({'_'.join(self.consequent[0].split())} IS {'_'.join(self.consequent[1].split())})"
        
