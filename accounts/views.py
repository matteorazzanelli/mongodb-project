from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

from app.models import Wallet, Profile
import random
from django.contrib import messages


def get_ip_address(request):
	try:
		x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
		if x_forward:
			ip = x_forward.split(",")[0]
		else:
			ip = request.META.get("REMOTE_ADDR")
	except:
		ip = ""
	return ip

# AuthenticationForm is the pre-built Django form logging in a user

def register_request(request):
  if request.method == "POST":
    form = NewUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      
      # Profile creation
      new_profile = Profile(user=user)
      new_profile.save()
      
      # Wallet creation
      new_wallet = Wallet(user=user,btc_balance=random.randrange(1, 11))
      new_wallet.usd_balance = new_wallet.btc_balance * 50000 #TODO: take BTC price from coinmarketcap using API
      new_wallet.save()
      
      login(request, user)
      messages.success(request, "Registration successful. You can now login." )
      return redirect("/login")
    messages.error(request, "Unsuccessful registration. Invalid information.")
  form = NewUserForm()
  return render (request=request, template_name="accounts/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				
				# check user ip, if not in list, add it!
				try:
					selected_user = Profile.objects.get(user=user)
				except:
					selected_user = Profile.objects.create(user=user)
				ip_address = get_ip_address(request)
				if ip_address not in selected_user.ips:
					selected_user.ips.append(ip_address)

				# ok
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("app:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="accounts/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('/login')