from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator

length = 100

class Restaurant(models.Model):
    name = models.CharField(max_length=length)
    address = models.TextField(max_length=512)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def get_rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg']

    def get_fields(self):
        fields = [ field for field in self._meta.get_fields() if field.name not in [ "id", "review" ]]

        for f in fields:
            yield f.name, getattr(self, f.name)
    
    def __str__(self):
        return self.name

class Review(models.Model):
    title = models.CharField(max_length=length)
    author = models.CharField(max_length=length)
    content = models.TextField(max_length=1024)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    rating = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(0),
    ])

    def __str__(self):
        return self.title