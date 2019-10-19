from rest_framework import serializers
from .models import *
import backend.settings.dev as settings
from rest_framework.validators import UniqueValidator
import jwt
from rest_framework_jwt.utils import jwt_payload_handler



class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'
    def create(self,validated_data):
        return Action.objects.create(post=Post,user=request.user,**validated_data)




class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')

class PostSerializer(serializers.ModelSerializer):
    ID=serializers.CharField(max_length=20)
    description=serializers.CharField()
    IsLiked = serializers.SerializerMethodField()
    #IMG=serializers.ImageField(allow_empty_file=False)
    #user=models.ForeignKey(User, on_delete=models.CASCADE)
    IsModerated=serializers.BooleanField(default=False)
    IsAdvert=serializers.BooleanField(default=False)
    IsInlinePost=serializers.BooleanField(default=False)
    AdURL=serializers.URLField(max_length=250,default="")
    AppearenceFrequency=serializers.IntegerField(default=1)
    NumberOfLikes=serializers.IntegerField(default=0)
    IMG_url = serializers.SerializerMethodField()

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
        fields = ('url', 'description', 'IMG_url', 'ID','IsModerated','IsAdvert','IsInlinePost','AdURL','AppearenceFrequency','NumberOfLikes','IsLiked')
    def get_IMG_url(self, Post):
        request = self.context.get('request')
        IMG_url = Post.IMG.url
        return request.build_absolute_uri(IMG_url)
    def get_IsLiked(self, Post):
        request=self.context.get('request')
        if request.user.is_authenticated:
            if len(Action.objects.filter(user=request.user,post=Post,type='Like'))>0:
                return True

        return False


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    ID=serializers.CharField(max_length=20, default="")
    content=serializers.CharField()
    date=models.DateField(auto_now_add=True)
    #reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    NumberOfLikes=models.IntegerField(default=0)
    class Meta:
        model = Comment
        fields = ('url', 'content', 'post','date','NumberOfLikes')

# output serializer class for  'Mods' model
class ModSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mods
        fields = '__all__'


class MimeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=MimeUser
        exlude=['user']
        fields=('IsAdvertiser',)

class UserSerializer(serializers.ModelSerializer):
    mimeuser = MimeUserSerializer()

    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','mimeuser')

    def create(self, validated_data):
        mimeuser = validated_data.pop('mimeuser')
        user = User.objects.create(**validated_data)
        MimeUser.objects.create(user=user, **mimeuser)
        user.set_password(user.password)
        user.save()
        return user

    def update(self, instance, validated_data):
        mimeuser = validated_data.pop('mimeuser')
        # Unless the application properly enforces that this field is
        # always set, the follow could raise a `DoesNotExist`, which
        # would need to be handled.
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
