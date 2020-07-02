from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


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
	category = models.ForeignKey(Category,
					related_name='products',
					on_delete=models.CASCADE)
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True)
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



class Crops(models.Model):
    name=models.CharField(max_length=100)
    c_type=models.CharField(max_length=100)
    price=models.IntegerField()
    photo=models.ImageField(upload_to='cropImage/',blank=True)

class CropSeeds(models.Model):
    name=models.CharField(max_length=100)
    s_type=models.CharField(max_length=100)
    price=models.IntegerField()
    photo=models.ImageField(upload_to='cropImage/',blank=True)
    quality = models.IntegerField()
class fertilizer(models.Model):
    name = models.CharField(max_length = 100)
    quality = models.IntegerField()
    price =models.IntegerField()
    image = models.ImageField(upload_to='cropImage/',blank=True)
class pesticide(models.Model):
    name = models.CharField(max_length = 100)
    quality = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='cropImage/',blank=True) 