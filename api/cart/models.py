from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from api.aviabilet.models import Aviabilet, Planes, Passenger
from api.telebot.sendmessage import sendTelegram

User = get_user_model()

class Cart(models.Model): # корзина
    CART_STATUS = (
        ('IN_PROCESSING', 'in_processing'),
        ('COMPLETED', 'completed'), # ЗАВЕРШЕННЫЙ
        ('DECLINED', 'declined') # ОТКЛОНЕННЫЙ
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    status = models.CharField(max_length=30, choices=CART_STATUS, default='in_processing')

    def __str__(self):
        return self.user.email



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    aviabilet = models.ForeignKey(Aviabilet, on_delete=models.CASCADE, related_name='cart_item')
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    # passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='cart_item')

    def __str__(self):
        return f'{self.aviabilet} in {self.cart.id} cart'

    def save(self, *args, **kwargs):
        self.total_cost = self.aviabilet.price * self.quantity

        av = Aviabilet.objects.get(id = self.aviabilet.id)
        pl = Planes.objects.get(id = self.aviabilet.planes.id)

        if av.class_ticket == 'E' and pl.economy_fare == 0 and pl.capacity < self.quantity:
            av.status = 'F'
            raise ValueError(f"Mest net v etom klasse biletov! Ostalos Vsego: {pl.capacity} mest")
        elif av.class_ticket == 'E' and pl.economy_fare > self.quantity:
            pl.economy_fare -= self.quantity
            self.aviabilet.planes.capacity -= self.quantity
        elif av.class_ticket == 'B' and pl.business_fare > self.quantity:
            pl.business_fare -= self.quantity
            self.aviabilet.planes.capacity -= self.quantity
        else:
            raise ValueError(f"Mest net v etom klasse biletov! Ostalos Vsego: {pl.capacity} mest, Business: {pl.business_fare} mest")
        av.save()
        pl.save()
        tg_q = str(self.quantity)
        tg_av = str(self.aviabilet)


        ##TeleBot
        sendTelegram(tg_prod=tg_av, tg_qty=tg_q)

        super(CartItem, self).save(*args, **kwargs)

