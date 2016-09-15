from enum import Enum


class MetaTag:
    """Metadata container for test case tagging
    """
    def __init__(self):
        self.product = None
        self.priority = None
        self.categories = set()


class ProductTag(Enum):
    """Product labels used in tag-decorator
    """
    ACE = 'ACE'
    BME = 'BME'
    STL = 'STL'


def tag(*categories: str, product: ProductTag=None, priority: int=None):
    """Specify a configuration tag for organizing test cases

    :param categories: Arbitrary list of category names
    :type: str or list of str
    :param product: Indicate if the test case is product-specific. By default, test cases are assumed as Shared
    :type: ProductTag
    :param priority: Numerical indicator of priority, 1 = Highest
    :type: int
    :return: None
    """
    def wrapper(fn):
        try:
            data = fn.tags
        except AttributeError:
            data = MetaTag()

        data.product = product
        data.priority = priority
        data.categories.update(categories)

        setattr(fn, 'tags', data)
        return fn
    return wrapper
