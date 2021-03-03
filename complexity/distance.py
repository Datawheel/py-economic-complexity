from .relatedness import relatedness

def distance(rcas, proximities):
    """ 
    Args:
        rcas ([type]): [description]
        proximities ([type]): [description]

    Returns:
        [type]: [description]
    """
    return 1 - relatedness(rcas, proximities)