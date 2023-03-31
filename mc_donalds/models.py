from django.db import models
from mc_donalds.resurses import POSITIONS, cashier
from datetime import datetime


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)


class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    full_name = models.CharField(max_length=255, default='FIO')
    position = models.CharField(max_length=2, choices=POSITIONS, default=cashier)
    labor_contract = models.IntegerField(default=0)

    def get_last_name(self):
        surnames = self.full_name.split()[0]
        return surnames


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds() // 60
        else:
            return (datetime.now() - self.time_in).total_seconds() // 60


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    def product_sum(self):
        return self.product.price * self.amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()


# product_1 = Product(name="Витая пара (3 м)", price=993)
# product_1.save()
#
# product_2 = Product.objects.create(name="Клавиатура", price=1060)


# cashier1 = Staff.objects.create(full_name = "Иванов Иван Иванович",
#                                 position = cashier,
#                                 labor_contract = 1754)
# cashier2 = Staff.objects.create(full_name = "Петров Петр Петрович",
#                                 position = cashier,
#                                 labor_contract = 4355)
# direct = Staff.objects.create(full_name = "Максимов Максим Максимович",
#                                 position = director,
#                                 labor_contract = 1254)
