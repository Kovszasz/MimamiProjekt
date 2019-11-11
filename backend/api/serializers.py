from rest_framework import serializers
from .models import *
import backend.settings.dev as settings
from rest_framework.validators import UniqueValidator
import jwt
from rest_framework_jwt.utils import jwt_payload_handler

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model=PersonalScoringProfile
        exlude=['user']
        fields=('score','label',)


class FollowSerializer(serializers.ModelSerializer):
    profile=serializers.SerializerMethodField()
    class Meta:
        model = Follow
        fields = ['channel','profile']
        depth=1

    def get_profile(self,Follow):
        profile=Follow.channel.mimeuser
        serialized=MimeUserSerializer(profile)
        return serialized.data

class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = MimeUser
        fields = ['profile_pic']
        #owner = serializers.Field(source='user.username')

class MimeUserSerializer(serializers.ModelSerializer):
    avatar=serializers.SerializerMethodField()
    class Meta:
        model=MimeUser
        exlude=['user']
        fields=('IsAdvertiser','avatar',)
        read_only_fields = ['profile_pic']
    def get_avatar(self,MimeUser):
        request = self.context.get('request')
        try:
            IMG_url = MimeUser.profile_pic.url
        except:
            IMG_url='/media/profile/e2.png'
        return IMG_url

class UserSerializer(serializers.ModelSerializer):
    mimeuser = MimeUserSerializer()
    #score = serializers.RelatedField(many=True, read_only=True)
    score=ScoreSerializer(many=True,read_only=True)
    channel=serializers.SerializerMethodField()#FollowSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ['username','password','first_name','last_name','mimeuser','is_staff','is_superuser','is_authenticated','score','channel']

    def create(self, validated_data):
        print(validated_data)
        mimeuser = validated_data.pop('mimeuser')
        user = User.objects.create(**validated_data)
        MimeUser.objects.create(user=user, **mimeuser)
        user.set_password(user.password)
        user.save()
        labels=Label.objects.all()
        for i in labels:
            p=PersonalScoringProfile.objects.create(user=user,label=i,score=0)
            p.save()
        return user

    def update(self, instance, validated_data):
        mimeuser = validated_data.pop('mimeuser')
        mimeuser = instance.mimeuser

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        mimeuser.IsAdvertiser = mimuser_data.get(
            'IsAdvertiser',
            mimeuser.IsAdvertiser
        )
        mimeuser.company = mimuser_data.get(
            'company',
            mimeuser.company
         )
        mimeuser.save()

        return instance

    def get_channel(self,User):
        follows=Follow.objects.filter(follower=User)
        serialized=FollowSerializer(follows,many=True)
        return serialized.data


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Action
        fields=('post','user','date','type',)

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Template
        fields='__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')

class MemeContentSerializer(serializers.ModelSerializer):
    IMG_url=serializers.SerializerMethodField()
    class Meta:
        model = MemeContent
        fields = ('IMG_url','index',)
    def get_IMG_url(self, MemeContent):
        request = self.context.get('request')
        try:
            IMG_url = MemeContent.IMG.url
        except:
            IMG_url= ''
        return IMG_url

class PostSerializer(serializers.ModelSerializer):
    ID=serializers.CharField(max_length=20)
    description=serializers.CharField()
    IsLiked = serializers.SerializerMethodField()
    #IMG=serializers.ImageField(allow_empty_file=False)
    imgs=MemeContentSerializer(many=True,read_only=True)
    user=UserSerializer()
    IsModerated=serializers.BooleanField(default=False)
    IsAdvert=serializers.BooleanField(default=False)
    IsInlinePost=serializers.BooleanField(default=False)
    AdURL=serializers.URLField(max_length=250,default="")
    AppearenceFrequency=serializers.IntegerField(default=1)
    NumberOfLikes=serializers.IntegerField(default=0)
    #IMG_url = serializers.SerializerMethodField()

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
        fields = ['user', 'description', 'imgs', 'ID','IsModerated','IsAdvert','IsInlinePost','AdURL','AppearenceFrequency','NumberOfLikes','IsLiked',]
    #def get_IMG_url(self, Post):
    #    request = self.context.get('request')
    #    IMG_url = Post.IMG.url
    #    return request.build_absolute_uri(IMG_url)
    def get_IsLiked(self, Post):
        if self.context.get('request') is not None:
            request=self.context.get('request')
            if request.user.is_authenticated:
                print(Action.objects.filter(user=request.user,post=Post,type='Like'))
                if len(Action.objects.filter(user=request.user,post=Post,type='Like'))>0:
                    return True

        return False



class CommentSerializer(serializers.ModelSerializer):
    ID=serializers.CharField(max_length=20, default="")
    content=serializers.CharField()
    date=models.DateField(auto_now_add=True)
    #reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    NumberOfLikes=models.IntegerField(default=0)
    #user=serializers.SerializerMethodField()
    user=UserSerializer()

    class Meta:
        model = Comment
        fields = ('content','date','NumberOfLikes','ID','post','user')

    #def get_user(self,Comment):
    #    pass

class PostLabellingSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostLabelling
        fields='__all__'
# output serializer class for  'Mods' model
class ModSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mods
        fields='__all__'

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

class TemplateSerializer(serializers.ModelSerializer):
    recycler = serializers.SerializerMethodField()
    IMG_url = serializers.SerializerMethodField()
    class Meta:
        model = Template
        fields =['IMG_url','user','ID','IsPublic','recycler']

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
