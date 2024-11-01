from django.db import models
from django.contrib.auth.models import User


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total_purchases = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Store the user who made the transaction
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.customer.name} - {self.date}"

class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


# StoreBook model to track deliveries based on waybill
class StoreBook(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    total_goods_value = models.DecimalField(max_digits=15, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    outstanding_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    other_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    date_received = models.DateField()


    def calculate_balance(self):
        total_payments = sum(payment.amount_paid for payment in self.payments.all())
        self.outstanding_balance = self.total_goods_value - total_payments
        return self.outstanding_balance

    def __str__(self):
        return f"StoreBook for {self.manufacturer.name} on {self.date_received}"

# StoreBookEntry model to track individual items in a storebook (products received)
class StoreBookEntry(models.Model):
    storebook = models.ForeignKey(StoreBook, related_name="entries", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    company_price = models.DecimalField(max_digits=15, decimal_places=2)
    retail_price = models.DecimalField(max_digits=15, decimal_places=2)
    selling_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.IntegerField()

    profit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def calculate_profit(self):
        self.profit = (self.selling_price * self.quantity) - (self.company_price)
        return self.profit

    def __str__(self):
        return self.product_name

# Payment model to track payments towards the outstanding debt
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    storebook = models.ForeignKey(StoreBook, null=True, blank=True, related_name="payments", on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.customer:
            return f"Payment of {self.amount_paid} for {self.customer.name}"
        elif self.storebook:
            return f"Payment of {self.amount_paid} for StoreBook {self.storebook.id}"
        return "Payment"


# Posting Ledger Model
class PostingLedger(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    goods_in = models.IntegerField(default=0)  # From StoreBook
    goods_out = models.IntegerField(default=0)  # From Sales (Daily)
    balance = models.IntegerField(default=0)  # In - Out
    last_updated = models.DateField(auto_now=True)

    def calculate_balance(self):
        self.balance = self.goods_in - self.goods_out
        return self.balance

    def __str__(self):
        return f"Posting Ledger for {self.product.name}"
