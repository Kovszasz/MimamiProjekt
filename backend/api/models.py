from django.db import models
#from django.contrib.auth.models import User
from datetime import datetime,date
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone
CONTENT_CHOICES=[
            ('None','None'),
            ('Like','Like'),
            ('View','View'),
            ('Click','Click'),
            ('Share','Share'),
            ('Report','Report'),
            ('Favourite','Favourite')
]

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, alias=None):
            #raise ValueError("ENTER AN EMAIL BUDDY")
        if not username:
            raise ValueError("I KNOW YOU HAVE A NAME")
            #raise ValueError("PASSWORD?!?!?!? HELLO??")
        if not alias:
            alias = username
        print(self.model)
        user = self.model(
             email = self.normalize_email(email),
             username = username,
             alias = alias)
        if password:
            user.set_password(password)
        user.save()
        return user
    def create_superuser(self, username, password, email,alias=None):
        user=self.create_user(email, username, password, alias)
        user.is_staff=True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=25, unique=True)
    alias = models.CharField(max_length=40)
    aboutme = models.CharField(max_length=140),
    first_name=models.CharField(max_length=200),
    last_name=models.CharField(max_length=200),
    avatar = models.ImageField(upload_to='profile',blank=True, default='/media/profile/e2.png')
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_official=models.BooleanField(default=False)
    is_advertiser=models.BooleanField(default=False)
    company=models.CharField(max_length=100,default='')
    balance=models.FloatField(default=0)
    sex=models.BooleanField(default=True)
    age=models.DateField(default=datetime.now, blank=True)
    IDCard=models.FileField(upload_to='IDcards',blank=True,)

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS=["email", ]


    def __str__(self):
        return "{}".format(self.username)

    def get_short_name(self):
        return self.alias
    def get_long_name(self):
        return "{} {}".format(self.alias, self.username)

    @property
    def is_adult(self):
        today = date.today()
        age=today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        if age>17:
            return True
        else:
            return False


class Post(models.Model):
    ID=models.AutoField(primary_key=True)
    description=models.TextField()
    IMG=models.ImageField(upload_to='post',blank=True, default='')
    user=models.ForeignKey(User, on_delete=models.CASCADE, default='')
    IsModerated=models.BooleanField(default=False)
    IsAdvert=models.BooleanField(default=False)
    IsInlinePost=models.BooleanField(default=False)
    AdURL=models.URLField(max_length=250,default="",blank=True)
    AppearenceFrequency=models.IntegerField(default=1)
    IsActive=models.BooleanField(default=True)
    CampaignTime=models.DateTimeField(default=datetime.now, blank=True)
    IsPublic=models.BooleanField(default=True)
    date=models.DateTimeField(default=datetime.now, blank=True)
    IsAdult=models.BooleanField(default=False)

class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, default="")
    ID=models.AutoField(primary_key=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,default="")
    content=models.TextField()
    date=models.DateField(auto_now_add=True)
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    NumberOfLikes=models.IntegerField(default=0)

class CommentLike(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    date = models.DateField( auto_now_add=True)


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
    name=models.CharField(unique=True,max_length=100,default='meme')
    user=models.ForeignKey(User,on_delete=models.CASCADE, default="")
    IsPublic=models.BooleanField(default=False)
    type=models.CharField(max_length=100,default='portrait')

class MemeContent(models.Model):
    IMG=models.ImageField(upload_to='post',blank=True)
    index=models.IntegerField(default=0)
    post=models.ForeignKey(Post,on_delete=models.CASCADE, default="", related_name='imgs')
    template=models.ForeignKey(Template, on_delete=models.SET_NULL, blank=True,null=True)
    ID=models.AutoField(primary_key=True)

class PersonalScoringProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='',related_name='score')
    label=models.ForeignKey(Label,on_delete=models.CASCADE,default='')
    score=models.FloatField(default=1)

class Follow(models.Model):
    channel=models.ForeignKey(User,on_delete=models.CASCADE,default='',related_name='channel')
    follower=models.ForeignKey(User,on_delete=models.CASCADE,default='',related_name='follower')

class Recycle(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    template=models.ForeignKey(Template, on_delete=models.CASCADE,default='')
    date = models.DateField( auto_now_add=True)
    #IsRemoved=models.BooleanField(default=False)

class SearchResult(models.Model):
    term=models.CharField(max_length=1000,default='')
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    result = models.ForeignKey(Post,on_delete=models.CASCADE,default='')
