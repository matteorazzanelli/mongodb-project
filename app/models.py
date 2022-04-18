# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from djongo.models.fields import ObjectIdField, Field



class Profile(models.Model):
  _id = ObjectIdField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  ips = models.Field(default=['127.0.0.1'])

class Wallet(models.Model):
  _id = ObjectIdField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  btc_balance = models.FloatField(default=0)
  usd_balance = models.FloatField(default=0)
  profit = models.FloatField(default=0)

  def __str__(self):
    text = f"Id: {self._id} - User: {self.user}"
    return text
  
class Order(models.Model):
  _id = ObjectIdField()
  profile = models.ForeignKey(User, on_delete=models.CASCADE)
  TYPE = [
    ('buy', 'buy'),
    ('sell', 'sell'),
  ]
  STATUS = [
    ('pending', 'pending'),
    ('executed', 'executed'),
  ]
  status = models.CharField(max_length=10, choices=STATUS, default='pending')
  type = models.CharField(max_length=10, choices=TYPE)
  datetime = models.DateTimeField(auto_now_add=True)
  price = models.FloatField()
  quantity = models.FloatField()
