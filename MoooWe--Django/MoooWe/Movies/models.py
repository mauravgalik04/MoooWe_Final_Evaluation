from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
# Create your models here.
    
class AppUserManager(BaseUserManager):
    def create_user(self, email, name, phone, address, gender, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field is mandatory')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            phone=phone,
            address=address,
            gender=gender,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, address, gender, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not password:
            raise ValueError("Superusers must have a password.")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, name, phone, address, gender, password, **extra_fields)
class AppUser(AbstractUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    name = models.CharField(max_length=150) 
    image = models.ImageField(default = 'None', upload_to='Movies/static/uploads')
    username = None  


    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'address', 'gender']

    def __str__(self):
        return self.email
class Movie(models.Model):
    name = models.CharField(max_length = 50 )
    release_year = models.IntegerField()
    genre = models.CharField(max_length =20)
    cast = models.TextField()
    story = models.TextField()
    imdb_rating = models.DecimalField(max_digits = 2 , decimal_places = 1)
    your_rating = models.DecimalField(max_digits = 2 , decimal_places = 1 , default = 0)
    watchlist = models.BooleanField(default = False)
    poster = models.ImageField()
    landscape = models.ImageField()
    def __str__(self):
        return self.name
class Comment(models.Model):
    user = models.ForeignKey(AppUser , on_delete=models.RESTRICT)
    comment = models.TextField()
    movie_id = models.ForeignKey(Movie, on_delete=models.RESTRICT)
    likes = models.IntegerField( default=0)
    dislikes = models.IntegerField( default=0)
    time_commented = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id