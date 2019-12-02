from rest_framework import serializers
from .models import *
#from backend.settings.dev import AUTH_USER_MODEL as User
from django.contrib.auth import get_user_model
import backend.settings.dev as settings
from rest_framework.validators import UniqueValidator
import jwt
from rest_framework_jwt.utils import jwt_payload_handler
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from numpy import polyfit
User = get_user_model()

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model=PersonalScoringProfile
        exlude=['user']
        fields=('score','label',)


class FollowSerializer(serializers.ModelSerializer):
    #profile=serializers.SerializerMethodField()
    class Meta:
        model = Follow
        fields = ['channel',]#'profile']
        depth=1

    #def get_profile(self,Follow):
    #    profile=Follow.channel
    #    serialized=UserSerializer(profile)
    #    return serialized.data

class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar']
        #owner = serializers.Field(source='user.username')
class UserSerializer(serializers.ModelSerializer):
    score = serializers.RelatedField(many=True, read_only=True)
    avatar=serializers.SerializerMethodField()
    score=ScoreSerializer(many=True,read_only=True)
    channel=serializers.SerializerMethodField()#FollowSerializer(many=True,read_only=True)
    complete_account=serializers.SerializerMethodField()
    IsFollowed=serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username','is_staff','is_superuser','is_authenticated','is_advertiser','score','channel','avatar','complete_account','IsFollowed']

    def get_avatar(self,User):
        request = self.context.get('request')
        try:
            IMG_url = User.avatar.url
        except:
            IMG_url='/media/profile/e2.png'
        return IMG_url


    def get_channel(self,User):
        follows=Follow.objects.filter(follower=User)
        serialized=FollowSerializer(follows,many=True)
        return serialized.data

    def get_complete_account(self,User):
        if len(PersonalScoringProfile.objects.filter(user=User))==0:
            return False
        else:
            return True

    def get_IsFollowed(self,User):
        request=self.context.get('request')
        if request is not None:
            if type(request.user) == type(User):
                if User.username != request.user.username:
                    try:
                        f=Follow.objects.get(channel=User, follower=request.user)
                        return True
                    except:
                        return False
        return False



class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Action
        fields=('post','user','date','type',)

class TemplateSerializer(serializers.ModelSerializer):
    recycler = serializers.SerializerMethodField()
    IMG_url = serializers.SerializerMethodField()
    class Meta:
        model = Template
        fields =['IMG_url','user','id','name','IsPublic','recycler','type']

    def get_recycler(self,Template):
        request=self.context.get('request')
        template = Recycle.objects.filter(user=request.user,template=Template)
        if len(template)==0:
            return False
        else:
            serialized=RecycleSerializer(template)
            return serialized.data

    def get_IMG_url(self,Template):
        return Template.IMG.url


class MemeContentSerializer(serializers.ModelSerializer):
    IMG_url=serializers.SerializerMethodField()
    template=TemplateSerializer()
    class Meta:
        model = MemeContent
        fields = ('IMG_url','index','template')
    def get_IMG_url(self, MemeContent):
        request = self.context.get('request')
        try:
            IMG_url = MemeContent.IMG.url
        except:
            IMG_url= ''
        return IMG_url
class PostLabellingSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostLabelling
        fields='__all__'

class PostSerializer(serializers.ModelSerializer):
    ID=serializers.CharField(max_length=20)
    description=serializers.CharField()
    IsLiked = serializers.SerializerMethodField()
    IsRecycled=serializers.SerializerMethodField()
    imgs=MemeContentSerializer(many=True,read_only=True)
    user=UserSerializer()
    IsModerated=serializers.BooleanField(default=False)
    IsAdvert=serializers.BooleanField(default=False)
    IsInlinePost=serializers.BooleanField(default=False)
    AdURL=serializers.URLField(max_length=250,default="")
    AppearenceFrequency=serializers.IntegerField(default=1)
    NumberOfLikes=serializers.SerializerMethodField()
    PopularityScore=serializers.SerializerMethodField()
    ReportScore=serializers.SerializerMethodField()
    NumberOfComments=serializers.SerializerMethodField()
    labels=serializers.SerializerMethodField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.description = validated_data.get('description', description.title)
        #instance.IMG = validated_data.get('IMG', instance.IMG)
        instance.IsModerated = validated_data.get('IsModerated', instance.IsModerated)
        instance.IsAdvert = validated_data.get('IsAdvert', instance.IsAdvert)
        instance.IsInlinePost = validated_data.get('IsInlinePost', instance.IsInlinePost)
        instance.AdURL = validated_data.get('AdURL', instance.AdURL)
        instance.AppearenceFrequency = validated_data.get('AppearenceFrequency', instance.AppearenceFrequency)
        instance.NumberOfLikes = validated_data.get('NumberOfLikes', instance.NumberOfLikes)
        instance.save()
        return instance

    class Meta:
        model = Post
        fields = ['user',
                'description',
                'imgs',
                'ID',
                'IsModerated',
                'IsAdvert',
                'IsInlinePost',
                'AdURL',
                'AppearenceFrequency',
                'NumberOfLikes',
                'IsLiked',
                'IsRecycled',
                'PopularityScore',
                'ReportScore',
                'NumberOfComments',
                'labels',
                ]

    def get_IsLiked(self, Post):
        request=self.context.get('request')
        if isinstance(request.user,User):
            if len(Action.objects.filter(user=request.user,post=Post,type='Like'))>0:
                return True
        return False

    def get_IsRecycled(self,Post):
        request=self.context.get('request')
        if isinstance(request.user,User):
            if len(Action.objects.filter(user=request.user,post=Post,type='Recycle'))>0:
                return True
        return False

    def get_NumberOfLikes(self,Post):
        return len(Action.objects.filter(post=Post,type='Like'))

    def get_PopularityScore(self,Post):
        if not Post.IsAdvert:
            actiontypes={}
            for i in ['Like','Click','Share','Report']:
                actiontypes[i]=len(Action.objects.filter(post=Post,type=i))
            return actiontypes['Like']+actiontypes['Click']+2*actiontypes['Share']-10*actiontypes['Report']
        else:
            return 0

    def get_ReportScore(self,Post):
        return len(Action.objects.filter(post=Post,type='Report'))

    def get_NumberOfComments(self,Post):
        return len(Comment.objects.filter(post=Post))

    def get_labels(self,Post):
        labels = PostLabelling.objects.filter(post=Post)
        #serialized= PostLabellingSerializer(labels,many=True)
        #return serialized.data
        data=[]
        for i in labels:
            data.append(i.label.name)
        return data

class CommentSerializer(serializers.ModelSerializer):
    ID=serializers.CharField(max_length=20, default="")
    content=serializers.CharField()
    user=UserSerializer()
    NumberOfLikes=serializers.SerializerMethodField()
    IsLiked=serializers.SerializerMethodField()
    #replies=serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('content','date','ID','post','user','reply_to','IsLiked','NumberOfLikes')

    def get_IsLiked(self, Comment):
        request=self.context.get('request')
        if isinstance(request.user,User):
            if len(CommentLike.objects.filter(user=request.user,comment=Comment))>0:
                return True
        return False

    def get_NumberOfLikes(self,Comment):
        return len(CommentLike.objects.filter(comment=Comment))


class LabelSerializer(serializers.ModelSerializer):
    posts=serializers.SerializerMethodField()
    users=serializers.SerializerMethodField()
    class Meta:
        model= Label
        fields=['name','type','posts','users',]

    def get_posts(self,Label):
        post=PostLabelling.objects.filter(label=Label)
        serialized=PostLabellingSerializer(post,many=True)
        return serialized.data
    def get_users(self,Label):
        user=PersonalScoringProfile.objects.filter(label=Label)
        serialized=ScoreSerializer(user,many=True)
        return serialized.data


class StatisticsSerializer(serializers.ModelSerializer):
    #all_post=serializers.SerializerMethodField()
    #all_user=serializers.SerializerMethodField()
    #all_label=serializers.SerializerMethodField()
    class Meta:
        model =Action
        fields = ['post','date','type',]

    def get_all_post(self,Action):
        post=Post.objects.all()
        serialized=PostSerializer(post,many=True)
        return serialized.data

    def get_all_user(self,Action):
        user=User.objects.filter(is_staff=False,is_superuser=False)
        serialized=UserSerializer(user,many=True)
        return serialized.data

    def get_all_label(self,Action):
        label=Label.objects.all()
        serialized=LabelSerializer(label,many=True)
        return serialized.data

class RecycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recycle
        fields = '__all__'


#AUTH SERIALIZERS OF djoser


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = ( 'username', 'email', 'password', )
        extra_kwargs = {'password' : {'write_only': True}}

class SocialSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)
    password=serializers.CharField(max_length=1000,required=True)
