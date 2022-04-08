import random
from datetime import datetime, date

"""Classes for melon orders."""
class TooManyMelonsError(ValueError):
    def __init__(self, message='No more than 100 melons.'):
        super().__init__(message)
        

class AbstractMelonOrder:
    """An abstract base class that other Melon Orders inherit from."""

    def __init__(self, species, qty, tax, order_type):
        """Initialize melon order attributes."""

        #https://stackoverflow.com/questions/20059766/handle-exception-in-init
        if qty > 100:
            raise TooManyMelonsError

        self.species = species
        self.qty = qty
        self.shipped = False
        self.order_type = order_type
        self.tax = tax
       


    def get_total(self):
        """Calculate price, including tax."""
        base_price = self.get_base_price()

        total = (1 + self.tax) * self.qty * base_price

        return total

    def mark_shipped(self):
        """Record the fact than an order has been shipped."""

        self.shipped = True

    def get_base_price(self):
        #add extra $4/each melon during 8-11am Mon- Fri
        base_price = random.randint(5,9)
        now = datetime.now()
        weekday = datetime.today().weekday()
        if 0 <= weekday < 5 and 8 <= now.hour <= 11:
            base_price += 4

        # print(now, weekday)
        return base_price



class DomesticMelonOrder(AbstractMelonOrder):
    """A melon order within the USA."""

    def __init__(self, species, qty, tax=0.08):
        """Initialize melon order attributes."""
        super().__init__(species, qty, tax, order_type='domestic')


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""

    def __init__(self, species, qty, country_code, tax=0.17):
        """Initialize melon order attributes."""

        super().__init__(species, qty, tax, order_type='international')
        self.country_code = country_code

    def get_total(self, fee=3):

        if self.qty < 10:
            return round(super().get_total(), 2) + fee
        return round(super().get_total(), 2)

    def get_country_code(self):
        """Return the country code."""

        return self.country_code


class GovernmentMelonOrder(AbstractMelonOrder):
    def __init__(self, species, qty):
        """Initialize melon order attributes."""

        super().__init__(species, qty, 0, order_type='government')
        self.passed_inspection = False

    def mark_inspection(self, passed):
        self.passed_inspection = passed

try:
    domestic = DomesticMelonOrder("watermelon", 10)
    print(f'This is the domestic_order object {domestic}')
    print(f'domestic_order total is: ${domestic.get_total()}')

    international = InternationalMelonOrder("Casaba", 5, "111")
    print(f'This is the international_order object {international}')
    print(f'international_order total is: ${international.get_total()}')

    gov_order = GovernmentMelonOrder(species="Muskmelon", qty=9)
    print(f'This is the gov_order object {gov_order}')
    print(f'gov_order total is: ${gov_order.get_total()}')

    domestic = DomesticMelonOrder("watermelon", 101)
    print(f'This is the domestic_order object {domestic}')
    print(f'domestic_order total is: ${domestic.get_total()}')
except TooManyMelonsError as e:
    print(e.args[0])

