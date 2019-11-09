from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
CONTENT_CHOICES=[
            ('None','None'),
            ('Like','Like'),
            ('View','View'),
            ('Click','Click'),
            ('Favourite','Favourite')
]


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()

class Post(models.Model):
    ID=models.CharField(max_length=20,primary_key=True)
    description=models.TextField()
    IMG=models.ImageField(upload_to='post',blank=True, default='')
    user=models.ForeignKey(User, on_delete=models.CASCADE, default='')
    IsModerated=models.BooleanField(default=False)
    IsAdvert=models.BooleanField(default=False)
    IsInlinePost=models.BooleanField(default=False)
    AdURL=models.URLField(max_length=250,default="",blank=True)
    AppearenceFrequency=models.IntegerField(default=1)
    NumberOfLikes=models.IntegerField(default=0)
    IsActive=models.BooleanField(default=True)
    CampaignTime=models.DateTimeField(default=datetime.now, blank=True)
    IsPublic=models.BooleanField(default=True)
    date=models.DateTimeField(default=datetime.now, blank=True)

class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, default="")
    ID=models.CharField(max_length=20,primary_key=True, default="")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,default="")
    content=models.TextField()
    date=models.DateField(auto_now_add=True)
    #reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    NumberOfLikes=models.IntegerField(default=0)


class Mods(models.Model):
    name = models.CharField(max_length=250)
    version = models.CharField(max_length=70)

    def __str__(self):
        return self.name + ' ' + self.version

class MimeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile',blank=True, default='/media/profile/e2.png')
    IsAdvertiser=models.BooleanField(default=False)
    company=models.CharField(max_length=100,default='')
    balance=models.FloatField(default=0)
    sex=models.BooleanField(default=True)
    #age=models.DateField(auto_now_add=True)
    IsOfficial=models.BooleanField(default=False)#official: icon -> ID card


    def __str__(self):
        return self.user.username

    def get_profile_picture(self):
        if self.profile_pic:
            return profile_pic_url
        else:
            return 'your_default_img_url_path'


class TimeLine(models.Model):
    date=models.DateField(auto_now_add=True)
    content_post=models.ForeignKey(Post,primary_key=True,default='',blank=True,on_delete=models.CASCADE)
    post_from_last_advert=models.IntegerField(default=0)

class AdvertSettings(models.Model):
    admin=models.ForeignKey(User, on_delete=models.CASCADE,primary_key=True,default='')
    AdFrequency=models.IntegerField(default=50)
    MoneyForSeen=models.FloatField(default=0)
    MoneyForClick=models.FloatField(default=0)

class Action(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    date = models.DateField( auto_now_add=True)
    type=models.CharField(max_length=100,choices=CONTENT_CHOICES)


class Label(models.Model):
    name=models.CharField(primary_key=True,default='' ,max_length=100)
    type=models.CharField(default='',max_length=100)

class PostLabelling(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    label=models.ForeignKey(Label,on_delete=models.CASCADE)


class Template(models.Model):
    IMG=models.ImageField(upload_to='template',blank=True)
    ID=models.CharField(primary_key=True, default='', max_length=100)
    user=models.ForeignKey(User,unique=True, on_delete=models.CASCADE, default="")
    IsPublic=models.BooleanField(default=False)

class MemeContent(models.Model):
    IMG=models.ImageField(upload_to='post',blank=True)
    index=models.IntegerField(default=0)
    post=models.ForeignKey(Post,on_delete=models.CASCADE, default="", related_name='imgs')
    #id=models.AutoField(primary_key=True, default="")

class PersonalScoringProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='',related_name='score')
    label=models.ForeignKey(Label,on_delete=models.CASCADE,default='')
    score=models.FloatField(default=1)

class Follow(models.Model):
    channel=models.ForeignKey(User,on_delete=models.CASCADE,default='',related_name='channel')
    follower=models.ForeignKey(User,on_delete=models.CASCADE,default='',related_name='follower')
