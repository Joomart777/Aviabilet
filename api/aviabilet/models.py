from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
# Create your models here.

User = get_user_model()

places = (
			('Bishkek', 'Bishkek'),
			('Almaty', 'Almaty'),
			('New York', 'New York'),
			('Paris', 'Paris'),
            ('Istanbul', 'Istanbul'),
            ('Berlin', 'Berlin'),
			('Singapore', 'Singapore'),
			('Moscow', 'Moscow'),
            ('Tbilisi', 'Tbilisi'),
		)

status_str = (
			('A', 'Available'),
			('F', 'Full'),
			('N', 'Not Open'),
		)

class_ticket_str = (
    ('B', 'Business'),
    ('E', 'Economy'),
)


class Airlines(models.Model):
    # title = models.TextField(max_length=100)
    slug = models.SlugField(max_length=30,
                            primary_key=True,
                            blank=True,
                            unique=True)
    def __str__(self):
        return self.slug



class Planes(models.Model):
    plane = models.CharField(max_length=24)
    airlines = models.ForeignKey(Airlines, on_delete = models.CASCADE, null = True)
    origin = models.CharField(max_length = 20, choices = places, default = 'Bishkek')
    destination = models.CharField(max_length = 20, choices = places, default = 'New York')
    depart_time = models.TimeField(auto_now=False, auto_now_add=False)
    depart_day = models.DateField(blank=True, null=True)
    duration = models.DurationField(null=True)
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False)
    capacity = models.PositiveIntegerField()
    economy_fare = models.PositiveIntegerField(null=True)
    business_fare = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.plane}: {self.airlines}; From: {self.origin}, To: {self.destination}"


class Passenger(models.Model):
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    mobile = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Aviabilet(models.Model):

    planes = models.ForeignKey(Planes, on_delete=models.CASCADE, related_name="planess")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="flight_ticket", blank=True, null=True)
    passenger = models.ManyToManyField(Passenger, related_name="flight_ticket")

    status = models.CharField(max_length = 1, choices = status_str, default = 'A', )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    class_ticket = models.CharField(max_length=1, choices=class_ticket_str, default='E', )
    # date_depart = models.DateField(blank=True, null=True)
    # date_arrive = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Flight: {self.planes}, Depart day: {self.planes.depart_day}, depart time: {self.planes.depart_time}, Arrival time: {self.planes.arrival_time}, class_ticket: {self.class_ticket}'




class Image(models.Model):
    image = models.ImageField(upload_to='images')
    airlines = models.ForeignKey(Airlines, on_delete=models.CASCADE, related_name='images')


class Rating(models.Model):
    airlines = models.ForeignKey(Airlines,
                                  on_delete=models.CASCADE,
                                  related_name='rating'
                                  )
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='rating'
                              )
    rating = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])


class Like(models.Model):
    """
    Модель лайков
    """
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='like',
                              verbose_name='Владелец лайка'
                              )
    airlines = models.ForeignKey(Airlines,
                                  on_delete=models.CASCADE,
                                  related_name='like',
                                  verbose_name='Aviaticket'
                                  )
    like = models.BooleanField('likess', default=False)

    def __str__(self):
        return f'{self.owner}, {self.like}'


##Отзывы
class Review(models.Model):
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    airlines = models.ForeignKey(Airlines, related_name='comments', on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} --> {self.airlines}'


class Favorite(models.Model):
    owner = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE,related_name='favorites')
    airlines = models.ForeignKey(Airlines,null=True,blank=True, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=True)

    def str(self):
        return f'{self.owner} --> {self.airlines}'