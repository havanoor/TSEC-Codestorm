from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.urls import reverse


class AccountManager(BaseUserManager):
    def create_user(self,username,password=None,**extra_fields):
        if not username:
            raise ValueError("Username is required")


        user=self.model(
            username=username,

            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, password, **extra_fields):
        # Creating superuser having all the rights


        user=self.create_user(

                    username,
                     password,
                      **extra_fields)

        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)


        return user


class Account(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=100,blank=True,null=True)
    dob=models.DateField(null=True,blank=True)

    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)

    is_farmer=models.BooleanField(default=False)
    is_buyer=models.BooleanField(default=False)




    USERNAME_FIELD='username'
    REQUIRED_FIELDS=[]
    objects=AccountManager()


class Farmer(Account):

    pan_no = models.CharField(max_length=10,blank=True,null=True)
    aadhar_no = models.IntegerField(null=True,blank=True)


class Buyer(Account):
    aadhar_no = models.IntegerField(blank=True, null=True)
    pan_no = models.CharField(max_length= 10,blank=True, null=True)



class Category(models.Model):
	name = models.CharField(max_length=200,
				db_index=True)
	slug = models.SlugField(max_length=200,
				unique=True)
	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def _str_(self):
		return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    #buyer =  models.ForeignKey(Farmer, related_name='Farmer_buy',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
    	ordering = ('name',)
    	index_together = (('id', 'slug'),)

    def _str_(self):
    	return self.name



class CropFilter(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'filter'
        verbose_name_plural = 'filters'

    def _str_(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])




class Crops(models.Model):
    name=models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, db_index=True)
    farmer=models.ForeignKey(Farmer,related_name='Farmer',on_delete=models.CASCADE)
    category = models.ForeignKey(CropFilter,related_name='Crop_Filter',on_delete=models.CASCADE)
    c_type=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.IntegerField(default =0)
    available = models.BooleanField(default=True)
    photo=models.ImageField(upload_to='cropImage/',blank=True)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])


class CropSeeds(models.Model):
    name=models.CharField(max_length=100)
    s_type=models.CharField(max_length=100)
    price=models.IntegerField()
    photo=models.ImageField(upload_to='cropImage/',blank=True)
    quality = models.IntegerField()


class fertilizer(models.Model):
    name = models.CharField(max_length = 100)
    f_type = models.CharField(max_length=100,null=True,blank=True)
    quality = models.IntegerField()
    price =models.IntegerField()
    image = models.ImageField(upload_to='cropImage/',blank=True)


class pesticide(models.Model):
    name = models.CharField(max_length = 100)
    quality = models.IntegerField()
    p_type=models.CharField(max_length=100,null=True,blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='cropImage/',blank=True)

<<<<<<< HEAD

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Crops, related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
=======
>>>>>>> e0097b4b9c618fd29f500de87f4fbe77b062d91b
