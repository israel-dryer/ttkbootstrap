def combine_style_keywords(color: str = None, variant: str = None):
    return '-'.join({x for x in {color, variant} if x is not None})
