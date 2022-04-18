from .models import Order
from django import forms


class OrderForm(forms.ModelForm):
  # some check
  def clean_quantity(self):
    btc_quantity = self.cleaned_data["quantity"]
    if btc_quantity < 0:
      raise forms.ValidationError("Quantity can not be negative")
    return btc_quantity
  
  def clean_price(self):
    price = self.cleaned_data["price"]
    if price < 0:
      raise forms.ValidationError("Price can not be negative")
    return price
  
  def clean_type(self):
    type = self.cleaned_data["type"]
    if type != "buy" and type != "sell":
      raise forms.ValidationError("Order type must be 'buy or 'sell'")
    return type

  class Meta:
    model = Order
    fields = ("quantity", "price", "type")
