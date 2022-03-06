class Order:
    def __init__(self, country_origin, count):
        self.country_origin = country_origin
        self.count = count

    def __eq__(self, other):
        if isinstance(other, Order):
            return self.country_origin == other.country_origin and self.count == other.count
        return False
