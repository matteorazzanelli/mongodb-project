from django.http import JsonResponse
from datetime import datetime
from .models import Order, Profile, Wallet
from .forms import OrderForm
from django.shortcuts import  render, redirect
from django.contrib import messages

"""
  Utility functions
"""
def canBuy(wallet, price, quantity):
  if wallet.usd_balance < price * quantity:
    return False
  wallet.usd_balance -= price * quantity # to avoid short selling (vendite allo scoperto)
  return True

def canSell(wallet, quantity):
  if wallet.btc_balance < quantity:
    return False
  wallet.btc_balance -= quantity # to avoid short selling (vendite allo scoperto)
  return True

###############
def findSeller(user, price, quantity):
  # find the oldest, fifo approach
  seller = Order.objects.exclude(profile=user).filter(status="pending", type="sell", price__lte=price, quantity__gte=quantity).order_by('datetime').first()
  if seller is None:
    return None, None, None
  else:
    return seller.profile, seller.price, seller.quantity

def findBuyer(user, price, quantity):
  # find the oldest, fifo approach
  buyer = Order.objects.exclude(profile=user).filter(status="pending", type="buy", price__gte=price, quantity__lte=quantity).order_by('datetime').first()
  if buyer is None:
    return None, None, None
  else:
    return buyer.profile, buyer.price, buyer.quantity

###############
def updateWallet(buyer_wallet, seller_wallet, buyer_price, buyer_quantity, seller_price, seller_quantity):
  buyer_wallet.btc_balance += buyer_quantity
  buyer_wallet.usd_balance += buyer_quantity*(seller_price-buyer_price)
  buyer_wallet.profit += buyer_quantity*(seller_price-buyer_price)
  seller_wallet.btc_balance += (seller_quantity - buyer_quantity)
  seller_wallet.usd_balance += seller_price*seller_quantity
  seller_wallet.profit += seller_price*seller_quantity
  buyer_wallet.save()
  seller_wallet.save()

###############
def processOrder(form, request):
  type = form.cleaned_data["type"]
  price = form.cleaned_data["price"]
  quantity = form.cleaned_data["quantity"]
  
  wallet = Wallet.objects.filter(user=request.user).first()
  # Can buy ?
  if type == "buy" and canBuy(wallet, price, quantity):
    [seller, seller_price, seller_quantity] = findSeller(request.user, price, quantity)
    # if a seller is found execute transaction and update wallet
    if seller is not None:
      print(request.user, ' buy to ', seller)
      status = "executed"
      updateWallet(wallet, Wallet.objects.filter(user=seller).first(), price, quantity, seller_price, seller_quantity)
    else:
      status = "pending"
  # Can Sell ?
  elif type == "sell" and canSell(wallet, quantity):
    print('sell')
    [buyer, buyer_price, buyer_quantity] = findBuyer(request.user, price, quantity)
    # if a buyer is found execute transaction and update wallet
    if buyer is not None:
      print(request.user, ' sell to ', buyer)
      status = "executed"
      updateWallet(Wallet.objects.filter(user=buyer).first(), wallet, buyer_price, buyer_quantity, price, quantity)
    else:
      status = "pending"
  else:
    messages.error(request, "Operation not allowed.")
    return redirect("app:homepage")
  
  order = form.save(commit=False)
  order.profile = request.user
  order.type = type
  order.status = status
  order.price = price
  order.quantity = quantity
  order.datetime = datetime.now()
  order.save()
  

"""
  End of utility functions
"""

def all_orders(request):
  response = []
  posts = Order.objects.filter(status='pending').order_by('-datetime')
  for post in posts:
    response.append(
      {
        'profile': str(post.profile),
        'datetime': post.datetime,
        'type': post.type,
        'price': post.price,
        'quantity': post.quantity
      }
    )
  return JsonResponse(response, safe=False)

def homepage(request):
  form = OrderForm()
  #if there is an incoming submitted form
  if request.method == "POST":
    form = OrderForm(request.POST)
    if form.is_valid():
      processOrder(form, request)
      return redirect('app:homepage')

  wallet = Wallet.objects.filter(user=request.user).first()
  context = {
    "user": request.user,
    "open_orders": Order.objects.filter(profile=request.user, status="pending").order_by('datetime'),
    "closed_orders": Order.objects.filter(profile=request.user, status="executed").order_by('-datetime'),
    "btc_balance":  wallet.btc_balance,
    "usd_balance": wallet.usd_balance,
    "profit": wallet.profit,
    "form": form
  }
  return render(request=request, template_name='app/home.html', context=context)