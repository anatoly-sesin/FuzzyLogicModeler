import numpy as np
import skfuzzy as fuzz

class MembershipFunction:
    @staticmethod
    def triangular(x, params):
        return fuzz.trimf(x, params)

    @staticmethod
    def trapezoidal(x, params):
        return fuzz.trapmf(x, params)

    @staticmethod
    def gaussian(x, params):
        return fuzz.gaussmf(x, params[0], params[1])

    @staticmethod
    def sigmoid(x, params):
        return fuzz.sigmf(x, params[0], params[1])

    @staticmethod
    def get_function(mf_type):
        mf_map = {
            "triangular": MembershipFunction.triangular,
            "trapezoidal": MembershipFunction.trapezoidal,
            "gaussian": MembershipFunction.gaussian,
            "sigmoid": MembershipFunction.sigmoid
        }
        return mf_map.get(mf_type)
