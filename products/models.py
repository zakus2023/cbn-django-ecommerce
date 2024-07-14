from django.db import models

from django.contrib.auth.models import User

from django.core.files import File

from io import BytesIO
from PIL import Image




# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
    
class Product(models.Model):

    DRAFT = 'draft'
    WAITING_APPROVAL = 'waitingapproval'
    ACTIVE = 'active'
    DELETED = 'deleted'

    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (WAITING_APPROVAL, 'Waiting approval'),
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
    )

    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    photo = models.ImageField(upload_to='photos/', default='photos/default_photo.jpg')
    # thumbnail = models.ImageField(upload_to='photos/thumbnail/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-created_at',)
    
    def display_price(self):
        return self.price / 100
    
    # def get_thumbnail(self):
    #     if self.thumbnail:
    #         return self.thumbnail
    #     else:
    #         if self.image:
    #             self.thumbnail = self.make_thumbnail(self.image)
    #             self.save()
    #             return self.thumbnail.url
    #         else:
    #             return 'https://placehold.co/600x400/png'
    
    # def make_thumbnail(self, image, size=(300, 300)):
    #     img = Image.open(image)
    #     img.convert('RGB')
    #     img.thumbnail(size)

    #     thumb_io = BytesIO()
    #     img.save(thumb_io, 'JPEG', quality=85)

    #     thumbnail = File(thumb_io, name=image.name)

    #     return thumbnail

from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
  ORDERED = 'ordered'
  SHIPPED = 'shipped'

  STATUS_CHOICES = (
    (ORDERED, 'Ordered'),
    (SHIPPED, 'Shipped'),
  )

  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  postalcode = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  phone = models.CharField(max_length=255)
  paid_amount = models.IntegerField(blank=True, null=True)
  is_paid = models.BooleanField(default=False)
  payment_intent = models.CharField(max_length=255, null=True)  # Allow null values
  created_by = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

  def __str__(self):
    return f"{self.id} - {self.first_name} {self.last_name}"

class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
  product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
  price = models.IntegerField()
  quantity = models.IntegerField(default=1)

  def display_price(self):
    return self.price / 100

