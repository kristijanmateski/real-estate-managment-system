from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class RealState(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    area = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    characteristic = models.CharField(max_length=255, default='', blank=True, null=True)
    reserved = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Agent(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    profile_url = models.URLField()
    contact_phone = models.CharField(max_length=50)
    total_sales = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AgentRealEstate(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    real_state = models.ForeignKey(RealState, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.agent.name} - {self.real_state.name}"


class Characteristic(models.Model):
    name = models.CharField(max_length=255)
    value = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name


class CharacteristicRealEstate(models.Model):
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE)
    real_state = models.ForeignKey(RealState, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.characteristic.name} - {self.real_state.name}"
