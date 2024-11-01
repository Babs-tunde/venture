from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import * 
import datetime
from decimal import Decimal
from django.http import HttpResponse
from .forms import StoreBookForm, StoreBookEntryForm, PaymentForm, UserRegistrationForm
from django.db.models import Sum 


@login_required
def home(request):
    products = Product.objects.all()
    today = datetime.date.today()
    daily_sales = Transaction.objects.filter(date__date=today)

    # Calculate total sales for today
    total_sales = 0
    transaction_data = []
    
    for sale in daily_sales:
        transaction_total = sum(item.product.price * item.quantity for item in sale.items.all())
        transaction_data.append({
            'sale': sale,
            'total_amount': transaction_total
        })
        total_sales += transaction_total

    return render(request, 'inventory/home.html', {
        'products': products,
        'transaction_data': transaction_data,
        'total_sales': total_sales,
    })


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page or dashboard
    return render(request, 'registration/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

def customer_transactions(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    transactions = Transaction.objects.filter(customer=customer)
    return render(request, 'inventory/customer_transactions.html', {'customer': customer, 'transactions': transactions})


# def create_transaction(request):
#     if request.method == 'POST':
#         customer_id = request.POST['customer_id']
#         customer = get_object_or_404(Customer, pk=customer_id)
#         transaction = Transaction.objects.create(customer=customer)

#         # Process products and quantities from the POST request
#         for product in Product.objects.all():
#             product_checkbox = request.POST.get(f'product_id_{product.id}')
#             quantity = request.POST.get(f'quantity_{product.id}')

#             if product_checkbox and quantity and int(quantity) > 0:
#                 # Create transaction item and update product stock
#                 TransactionItem.objects.create(
#                     transaction=transaction,
#                     product=product,
#                     quantity=int(quantity)
#                 )
#                 product.stock -= int(quantity)
#                 product.save()

#         # Redirect to customer detail page after transaction completion
#         return redirect('customer_detail', customer_id=customer.id)

#     customers = Customer.objects.all()
#     products = Product.objects.all()
#     return render(request, 'inventory/create_transaction.html', {'customers': customers, 'products': products})


def create_transaction(request):
    if request.method == 'POST':
        customer_id = request.POST['customer_id']
        customer = get_object_or_404(Customer, pk=customer_id)
        transaction = Transaction.objects.create(customer=customer, user=request.user)

        total_transaction_amount = 0  # Initialize total amount for the transaction

        # Process products and quantities from the POST request
        for product in Product.objects.all():
            product_checkbox = request.POST.get(f'product_id_{product.id}')
            quantity = request.POST.get(f'quantity_{product.id}')

            if product_checkbox and quantity and int(quantity) > 0:
                # Create transaction item and update product stock
                item_total = product.price * int(quantity)  # Calculate total for the current product
                total_transaction_amount += item_total  # Add to total transaction amount

                TransactionItem.objects.create(
                    transaction=transaction,
                    product=product,
                    quantity=int(quantity)
                )
                product.stock -= int(quantity)
                product.save()

        # Update customer's outstanding balance
        customer.outstanding_balance += total_transaction_amount
        customer.save()

        # Redirect to customer detail page after transaction completion
        return redirect('customer_detail', customer_id=customer.id)

    customers = Customer.objects.all()
    products = Product.objects.all()
    return render(request, 'inventory/create_transaction.html', {'customers': customers, 'products': products})




def daily_sales(request):
    # Fetch today's transactions
    sales = Transaction.objects.filter(date__date=datetime.date.today()).order_by('-id')

    # Create a list to store the total amount for each sale
    transaction_data = []
    
    for sale in sales:
        total_amount = 0
        for item in sale.items.all():
            total_amount += item.product.price * item.quantity
        
        # Append the transaction and total amount to the list
        transaction_data.append({
            'sale': sale,
            'total_amount': total_amount,
            'user': sale.user
        })

    return render(request, 'inventory/daily_sales.html', {'transaction_data': transaction_data})





def search(request):
    query = request.GET.get('q', '').strip()  # Get the query from the search form, default to an empty string if not present

    if query:
        # Perform search when query is present
        customers = Customer.objects.filter(name__icontains=query)
        products = Product.objects.filter(name__icontains=query)
        transactions = Transaction.objects.filter(customer__name__icontains=query)
    else:
        # If no query is entered, show all customers, products, and transactions (or customize this as needed)
        customers = Customer.objects.all()
        products = Product.objects.all()
        transactions = Transaction.objects.all()

    context = {
        'customers': customers,
        'products': products,
        'transactions': transactions,
        'query': query,
    }

    return render(request, 'inventory/search_results.html', context)


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'inventory/customer_list.html', {'customers': customers})

def customer_payment_view(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)

    if request.method == 'POST':
        amount_paid = request.POST['amount_paid']

        # Create a payment record
        Payment.objects.create(customer=customer, amount_paid=amount_paid)

        # Update the customer's outstanding balance
        customer.outstanding_balance -= Decimal(amount_paid)
        customer.save()

        return redirect('customer_detail', customer_id=customer.id)

    return render(request, 'inventory/customer_record_payment.html', {'customer': customer})

# Customer Detail View (for showing customer transactions)
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    transactions = Transaction.objects.filter(customer=customer).order_by('-id')
    payments = Payment.objects.filter(customer=customer).order_by('-date_paid')

    # Calculate total for each transaction
    transaction_data = []
    for transaction in transactions:
        total_amount = sum(item.product.price * item.quantity for item in transaction.items.all())
        transaction_data.append({
            'transaction': transaction,
            'total_amount': total_amount
        })

    return render(request, 'inventory/customer_detail.html', {
        'customer': customer,
        'transaction_data': transaction_data,  # Transaction details with totals
        'payments': payments  # Payment details
    })


def receipt_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    # Calculate total amount and subtotals
    items_with_subtotals = []
    total_amount = 0
    for item in transaction.items.all():
        subtotal = item.product.price * item.quantity
        total_amount += subtotal
        items_with_subtotals.append({
            'product': item.product,
            'quantity': item.quantity,
            'price': item.product.price,
            'subtotal': subtotal
        })

    return render(request, 'inventory/receipt.html', {
        'transaction': transaction,
        'items_with_subtotals': items_with_subtotals,
        'total_amount': total_amount,
    })



@staff_member_required
def create_storebook(request):
    if request.method == 'POST':
        manufacturer_id = request.POST['manufacturer']
        total_goods_value = request.POST['total_goods_value']
        amount_paid = request.POST['amount_paid']
        date_received = request.POST['date_received']

        manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)
        storebook = StoreBook.objects.create(
            manufacturer=manufacturer,
            total_goods_value=total_goods_value,
            amount_paid=amount_paid,
            date_received=date_received
        )

        # Create initial payment record
        Payment.objects.create(
            storebook=storebook,
            amount_paid=amount_paid,
            date_paid=date_received
        )

        return redirect('storebook_detail', storebook_id=storebook.id)

    manufacturers = Manufacturer.objects.all()
    return render(request, 'inventory/create_storebook.html', {'manufacturers': manufacturers})


# View to add an entry for products in the storebook
@staff_member_required
def add_storebook_entry(request, storebook_id):
    storebook = get_object_or_404(StoreBook, pk=storebook_id)
    if request.method == 'POST':
        form = StoreBookEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.storebook = storebook
            entry.calculate_profit()  # Calculate profit
            entry.save()
            return redirect('storebook_detail', storebook_id=storebook.id)
    else:
        form = StoreBookEntryForm()

    return render(request, 'inventory/add_storebook_entry.html', {'form': form, 'storebook': storebook})


# View to record payments toward debt
def record_payment(request, storebook_id):
    storebook = get_object_or_404(StoreBook, pk=storebook_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.storebook = storebook
            payment.save()
            return redirect('storebook_detail', storebook_id=storebook.id)
    else:
        form = PaymentForm()

    return render(request, 'inventory/record_payment.html', {'form': form, 'storebook': storebook})



# View to display details of the storebook and transactions
@staff_member_required
def storebook_detail(request, storebook_id):
    storebook = get_object_or_404(StoreBook, pk=storebook_id)
    entries = storebook.entries.all()
    payments = storebook.payments.filter().order_by('-date_paid')
    
    total_profit = sum(entry.profit for entry in entries) - storebook.other_expenses
    storebook.calculate_balance()  # Recalculate balance after showing payments

    return render(request, 'inventory/storebook_detail.html', {
        'storebook': storebook,
        'entries': entries,
        'payments': payments,
        'total_profit': total_profit,
    })

@staff_member_required
def storebook_list(request):
    storebooks = StoreBook.objects.all()  # Retrieve all storebook entries
    for storebook in storebooks:
        storebook.calculate_balance()
    return render(request, 'inventory/storebook_list.html', {'storebooks': storebooks})


def posting_ledger(request):
    # Get all products
    products = Product.objects.all()
    
    # For each product, calculate goods in (from StoreBook) and goods out (from transactions)
    ledgers = []
    for product in products:
        # Calculate goods in from StoreBookEntry
        goods_in = StoreBookEntry.objects.filter(product_name=product.name).aggregate(Sum('quantity'))['quantity__sum'] or 0
        
        # Calculate goods out from Transactions (Daily Sales)
        goods_out = TransactionItem.objects.filter(product=product).aggregate(Sum('quantity'))['quantity__sum'] or 0
        
        # Calculate balance
        balance = goods_in - goods_out
        
        # Create Posting Ledger entry
        ledger = {
            'product': product,
            'goods_in': goods_in,
            'goods_out': goods_out,
            'balance': balance
        }
        ledgers.append(ledger)
    
    return render(request, 'inventory/posting_ledger.html', {'ledgers': ledgers})
