class LinguisticVariable:
    def __init__(self, name, range_min, range_max, variable_type):
        self.name = name
        self.range_min = range_min
        self.range_max = range_max
        self.variable_type = variable_type
        self.terms = {}

    def add_term(self, term_name, mf_type, mf_params):
        self.terms[term_name] = (mf_type, mf_params)

    def remove_term(self, term_name):
        if term_name in self.terms:
            del self.terms[term_name]

    def get_terms(self):
        return self.terms

    def __str__(self):
        return f"LinguisticVariable(name={self.name}, type={self.variable_type}, range=[{self.range_min}, {self.range_max}], terms={len(self.terms)})"
