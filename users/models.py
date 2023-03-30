from django.db import models


class users(models.Model):
    UserId=models.AutoField(primary_key=True)
    FirstName=models.CharField(max_length=100)
    LastName=models.CharField(max_length=100)
    EmailId=models.CharField(max_length=100)
    MobileNumber=models.CharField(max_length=100)
    Password = models.CharField(max_length=50,default="")
    ifLogged = models.BooleanField(default=False)
    token = models.CharField(max_length=500, null=True, default="")

    def __str__(self):
        return "{} -{}".format(self.UserId, self.EmailId)


