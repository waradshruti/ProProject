from django.db import models

# Create your models here.
class Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	message=models.TextField()

	def __str__(self):
		return self.name

class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	address=models.TextField()
	password=models.CharField(max_length=100)
	cpassword=models.CharField(max_length=100)
	image=models.ImageField(upload_to="user_image/",default="",blank="True",null="True")
	usertype=models.CharField(max_length=100,default="user")
	status=models.CharField(max_length=100,default="inactive")

	def __str__(self):
		return self.fname


class Product(models.Model):
	CHOICE=(
			('blackberry','blackberry'),
			('blueberry','blueberry'),
			('apple','apple'),
			('samsung','samsung'),
			('oppo','oppo'),
			('vivo','vivo'),
		)

	seller=models.ForeignKey(User,on_delete=models.CASCADE)
	product_category=models.CharField(max_length=100,choices=CHOICE)
	product_model=models.CharField(max_length=100)
	product_price=models.CharField(max_length=100)
	product_color=models.CharField(max_length=100)
	product_dec=models.TextField()
	product_image=models.ImageField(upload_to="ProductImage/")

	def __str__(self):
		return self.product_model


class Wishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.fname+" - "+self.product.product_model



class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(auto_now_add=True)
	qty=models.IntegerField(default=1)
	price=models.IntegerField(default=0)
	total_price=models.IntegerField(default=0)
	payment_status=models.CharField(max_length=100,default="pending")

	def __str__(self):
		return self.user.fname+" - "+self.product.product_model


class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    cart=models.CharField(max_length=100,default="")
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)