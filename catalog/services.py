from django.db import transaction

from catalog.models import Stock


def buy_book(book_id, quantity):
    if quantity <= 0:
        raise ValueError('Quantity can not be less then one')

    with transaction.atomic():
        stock = Stock.objects.select_for_update().get(book__pk=book_id)

        if stock.quantity >= quantity:
            stock.quantity -= quantity
            stock.save(update_fields=['quantity'])
        else:
            raise ValueError('Book quantity less than ypu want to buy')

        return stock