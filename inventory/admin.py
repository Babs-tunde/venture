from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Manufacturer)
admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
admin.site.register(StoreBook)
admin.site.register(StoreBookEntry)
admin.site.register(Payment)
admin.site.register(PostingLedger)