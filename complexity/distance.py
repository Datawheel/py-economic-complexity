from .relatedness import relatedness

def distance(rcas, proximities):
    return 1 - relatedness(rcas, proximities)