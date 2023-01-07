from django.db import models
from django.contrib.auth.models import User

class User_info(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True)
    GENDER_CHOICE= (('M','Male'),('F','Female'),('OG','Other'))
    profile_pic = models.ImageField(upload_to='profilepic',blank=False)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICE,blank=True)
    address = models.CharField(max_length=100,blank=True)
    phone = models.CharField(max_length=15,blank=True)
    USER_TYPE= (('S','Saller'),('B','Buyer'))
    user_type = models.CharField(max_length=10,choices=USER_TYPE,blank=False)

    def __str__(self):
        return "User: {},Genger: {}".format(self.user.first_name, self.gender)