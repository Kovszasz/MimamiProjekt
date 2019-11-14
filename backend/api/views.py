from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.views.decorators.cache import never_cache
from rest_framework import viewsets,status, filters
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from rest_framework import parsers
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from rest_framework.reverse import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from random import randint,randrange
from .algorithms import *
from collections import OrderedDict
import json


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    search_fields=('id',)

class FollowViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    search_fields=('user__username',)
    #search_fields = ['Id']
    def list(self,request):
        queryset=Post.objects.filter(IsAdvert=False,IsActive=True,IsPublic=True).order_by('-date')
        print(isinstance(request.user,User))
        if isinstance(request.user,User):
            postpool=[]
            for post in queryset:
                postlabel=PostLabelling.objects.filter(post=post)
                score=0
                for label in postlabel:
                    if len(PersonalScoringProfile.objects.filter(user=request.user, label=label.label))>0:
                        score=score+PersonalScoringProfile.objects.get(user=request.user,label=label.label).score
                print(post.ID,'\t',score)
                if randrange(0,1)<score:
                    postpool.append(post)
            serializer = PostSerializer(postpool,many=True,context={'request':request})
        else:
            serializer = PostSerializer(queryset,many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        booldict={'false':False,'true':True}
        print(booldict[request.data['IsAdvert']])
        print(request.user)
        if booldict[request.data['IsAdvert']]:
            post = Post.objects.create(user=request.user,
                                            ID=request.data['ID'],
                                            IsInlinePost=booldict[request.data['IsInlinePost']],
                                            AppearenceFrequency=request.data['AppearenceFrequency'],
                                            #date=request.data['date'],
                                            #CampaignTime=request.data['CampaignTime'],
                                            IsAdvert=True,
                                            AdURL=request.data['AdURL']
                                            )
        else:
            post = Post.objects.create(user=request.user,ID=request.data['ID'],description=request.data['description'],IsPublic=booldict[request.data['IsPublic']])
        post.save()
        for i in request.data['labels']:
            if len(Label.objects.filter(name=i))==0:
                l=Label.objects.create(name=i,type='category')
                l.save()
            else:
                l=Label.objects.get(name=i)
            pl=PostLabelling.objects.create(post=post,label=l)
            pl.save()
        for index in range(int(request.data['size'])):
            t=MemeContent.objects.create(post=post,index=index,IMG=request.FILES['meme'+str(index)])
            t.save()
            serializer=PostSerializer(post,context={'request': request})
        serializer=PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        api_result = Post.objects.get(pk=pk)
        serializer=PostSerializer(api_result, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_ad(self,request):
        ads=Post.objects.filter(IsAdvert=True,IsActive=True)
        setting=AdvertSettings.objects.get(admin=User.objects.get(username="kovszasz"))
        AdPool=[]
        #if randrange(0,100)<setting.AdFrequency:
        for i in ads:
            for j in range(i.AppearenceFrequency):
                AdPool.append(i)
            #ad=PostSerializer(AdPool[randrange(0,len(AdPool))],context={'request':request})
        ad=PostSerializer(AdPool,many=True,context={'request':request})
        return Response(ad.data)
        #else:
        #    empty=Post.objects.get(ID='empty')
        #    ad=PostSerializer(empty,context={'request':request})
        #    return Response(ad.data)
    @action(detail=True, methods=['get'])
    def gender_stat(self,pk):
        endpoint={}
        ad=Post.objects.get(ID=pk)
        actions=Action.objects.filter(post=ad)
        male=0
        female=0
        for i in actions:
            if i.user.memeuser.sex:
                male=male+1
            else:
                female=female+1
        return Response({'male':male,'female':female})

    def update(self, request, pk=None):
        api_result = Post.objects.get(pk=pk)
        api_result.update(request.data)
        api_result.save()
        serializer=PostSerializer(api_result, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        api_result = Post.objects.get(pk=pk)
        api=Post.objects.all()
        serializer=PostSerializer(api, context={'request': request})
        return Response(serializer.data)


    @action(detail=True, methods=['get'])
    def like(self,request, pk=None):
        post=Post.objects.get(pk=pk)
        if len(Action.objects.filter(user=request.user,post=post,type='Like'))==0:
            post.NumberOfLikes+=1
            post.save()
            serializer=PostSerializer(post, context={'request': request})
            #action=ActionSerializer(post,context={'request': request})
            Action.objects.create(user=request.user,post=post,type='Like')
        else:
            Action.objects.get(user=request.user,post=post,type='Like').delete()
            post.NumberOfLikes-=1
            post.save()
            serializer=PostSerializer(post, context={'request': request})
        UpdateProfileScores(user=request.user)
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def action(self,request):
        setting=AdvertSettings.objects.get(admin=User.objects.get(username="kovszasz"))
        post=Post.objects.get(ID=request.data['post'])
        postOwner=User.objects.get(username=post.user)
        #action=ActionSerializer(post,data={'type':request.data['type']})
        a=Action.objects.create(post=post,user=request.user,type=request.data["type"])
        a.save()
        if request.data["type"]=='Click':
            if postOwner.balance-setting.MoneyForCick <=0:
                post.IsActive=False
                post.save()
                #notify(owner)
            else:
                postOwner.balance=postOwner.balance-setting.MoneyForClick
        elif request.data["type"]=='View':
            if postOwner.balance-setting.MoneyForSeen <=0:
                post.IsActive=False
                post.save()
            else:
                postOwner.mimeuser.balance=postOwner.mimeuser.balance-setting.MoneyForSeen
        postOwner.mimeuser.save()
        postOwner.save()
        serializer = PostSerializer(post,context={'request': request} )
        return Response(serializer.data)








class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    search_fields=('id',)
    def list(self,request):
        queryset=Comment.objects.all()
        serializer = CommentSerializer(queryset,many=True, context={'request': request})
        print('AllCommentLoaded')
        return Response(serializer.data)

    def create(self, request):
        #request.data.update({'user':request.user})
        api_result = Comment.objects.create(user=request.user, ID=request.data['ID'],content=request.data["content"], post=Post.objects.get(ID=request.data["post"]))
        api_result.save()
        serializer=CommentSerializer(api_result,context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        p=Post.objects.get(ID=pk)
        api_result = Comment.objects.filter(post=p)
        serializer=CommentSerializer(api_result, many=True,context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        api_result = Comment.objects.get(pk=pk)
        api_result.update(request.data)
        api_result.save()
        serializer=PostSerializer(api_result, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        api_result = Comment.objects.get(pk=pk)
        api=Comment.objects.all()
        serializer=PostSerializer(api, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def like(self,request, pk=None):
        com=Comment.objects.get(pk=pk)
            #if it has already been liked.....then minus
        com.NumberOfLikes+=1
        com.save()
        serializer=PostSerializer(com, context={'request': request})
        return Response(serializer.data)




class ModsView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)  # checks if user is authenticated to view the model objects

    def get_queryset(self):
        return Mods.objects.all()  # return all model objects

    def get(self, request, *args, **kwargs):  # GET request handler for the model
        queryset = self.get_queryset()
        serializer = ModSerializer(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.exclude(is_superuser=1)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    search_fields=('username',)
    @action(detail=True, methods=['POST'],serializer_class=ProfilePicSerializer,parser_classes=[parsers.MultiPartParser],)
    def pic(self, request, pk):
        user= User.objects.get(username=pk)
        mimeuser=MimeUser.objects.get(user=user)
        mimeuser.profile_pic= request.FILES['profile_pic']
        mimeuser.save()
        serializer = UserSerializer(user)
#        if serializer.is_valid():
#            serializer.save()
        return Response(serializer.data)
        #return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=['get'])
    def user_login(self, request,pk=None):
        #if request.method == 'POST':
        #    username = request.data['username']
        #    password = request.data['password']
    #        user = authenticate(username=username, password=password)
    #        if user:
    #            if user.is_active:
    #                login(request,user)

#        return reverse_lazy('/api/token/',request=request)
        u=User.objects.get(username=pk)
        serializer = UserSerializer(u)
        return Response(serializer.data)
    @action(detail=True,methods=['POST'])
    def user_logout(self,request,pk=None):
        logout(request)
        return Response()


class ActionViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    

class TemplateViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
#OUT OF SERVICE#################################################################################
class MemeContentViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MemeContent.objects.all()
    serializer_class = MemeContentSerializer

    def create(self, request):
        #post = Post.objects.get(ID=request.data['post'])
        post =Post.objects.get(ID=request.data['post'])
        for index in range(int(request.data['size'])):
            t=MemeContent.objects.create(post=post,index=index,IMG=request.FILES['meme'+str(index)])
            t.save()
        serializer=PostSerializer(post,context={'request': request})
        return Response(serializer.data)
################################################################################################
class StatisticsViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class=StatisticsSerializer

    @action(detail=False, methods=['get'])
    def users(self,request):
        endpoint={}
        endpoint['male']=len(MimeUser.objects.filter(sex=True))
        endpoint['female']=len(MimeUser.objects.filter(sex=False))
        #qs=User.objects.all().values('date_joined','username').annotate(newuser=Count('date_joined')).order_by('-date_joined')
        #serialized=json.dumps([OrderedDict(('user', x['username']),('date_joined', x['date_joinded'])) for x in qs])
        #serialized=json.dumps([OrderedDict(('Female',x['female']),('male',x['male'])) for x in endpoint])
        return Response(endpoint)
#        qs = (User.objects
#      .filter(user=user)
#      .values('show_id', 'show__movie__name', 'show__day__date', 'show__time')
#      .annotate(total_tickets=Count('show'), last_booking=Max('booked_at'))
#      .order_by('-last_booking')
#      )


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    def list(self,request):
        if isinstance(request.user, User):
            qs = Template.objects.all()
            serialized = TemplateSerializer(qs, many=True, context={'request':request})
            return Response(serialized.data)
        else:
            return Response({})

    @action(detail=False, methods=['get'])
    def personal(self,request):
        if isinstance(request.user, User):
            qs = Template.objects.filter(user=request.user)
            serialized = TemplateSerializer(qs, many=True, context={'request':request})
            return Response(serialized.data)
        else:
            return Response({})

    @action(detail=False, methods=['get'])
    def browser(self,request):
        if isinstance(request.user, User):
            qs = Template.objects.filter(IsPublic=True)
            serialized = TemplateSerializer(qs, many=True, context={'request':request})
            return Response(serialized.data)
        else:
            return Response({})
