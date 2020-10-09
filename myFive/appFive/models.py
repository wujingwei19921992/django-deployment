from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #sentence above is the 1to1 relationship with user in bracket

    # additional class

    portfolio_site = models.URLField(blank=True)
    # it  is okay to keep it blank
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username
  #username is the default User atrribute
