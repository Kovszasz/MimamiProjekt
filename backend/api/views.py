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
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from rest_framework.reverse import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from random import randint,randrange
from .algorithms import *
from collections import OrderedDict
import json
from django.http import Http404
from numpy import polyfit
from django.db.models import Count
from django.db.models.functions import TruncDay
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from requests.exceptions import HTTPError
from rest_framework_jwt.utils import jwt_encode_handler,jwt_payload_handler
User = get_user_model()

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

class FollowViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def create(self,request):
        if isinstance(request.user,User):
            if len(Follow.objects.filter(follower=request.user,channel=User.objects.get(username=request.data['user'])))==0:
                f=Follow.objects.create(follower=request.user,channel=User.objects.get(username=request.data['user']))
                f.save()
            else:
                Follow.objects.get(follower=request.user,channel=User.objects.get(username=request.data['user'])).delete()
            return Response(UserSerializer(request.user).data)
        else:
            raise Http404

class PostSearchViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    search_fields=('user__username','description','postlabelling__label__name','comment__content','imgs__template__name')

    def create(self,request):
        term=request.data['term']
        for i in request.data['result']:
            p=Post.objects.get(ID=i['ID'])
            if isinstance(request.user,User):
                sr=SearchResult.objects.create(user=request.user,result=p,term=term)
            else:
                sr=SearchResult.objects.create(result=p,term=term)
        return Response({})


#def retrievePost(self, request,user=None,post=None):
#    IsPublic=post.find('_private') == -1
#    post=pk2.replace('_private','')
#    user= User.objects.get(username=user)
#    post= Post.objects.get(ID=post,user=user)
#    serializer=PostSerializer(post, context={'request': request})
#    if not post.IsPublic and not IsPublic:
#    return Response(serializer.data, status=status.HTTP_200_OK)
#    else:
#        raise Http404

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Post.objects.filter(IsAdult=False)
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    search_fields=('user__username',)
    def list(self,request):
        queryset=Post.objects.filter(IsAdvert=False,IsActive=True,IsPublic=True).order_by('-date')
        serializer = PostSerializer(queryset,many=True, context={'request': request})
        if isinstance(request.user,User):
            if request.user.is_staff:
                postquery=Post.objects.filter(IsAdvert=False,IsModerated=False)
                serializer=PostSerializer(postquery,many=True,context={'request':request})
            elif len(PersonalScoringProfile.objects.filter(user=request.user))==0:
                serializer = PostSerializer(queryset,many=True, context={'request': request})
            else:
                postpool=[]
                for post in queryset:
                    postlabel=PostLabelling.objects.filter(post=post)
                    score=0
                    for label in postlabel:
                        if len(PersonalScoringProfile.objects.filter(user=request.user, label=label.label))>0:
                            score=score+PersonalScoringProfile.objects.get(user=request.user,label=label.label).score
                    if randrange(0,1)<score:
                        postpool.append(post)
                serializer = PostSerializer(postpool,many=True,context={'request':request})
        return Response(serializer.data)

    def create(self, request):
        booldict={'false':False,'true':True}
        if booldict[request.data['IsAdvert']]:
            post = Post.objects.create(user=request.user,
                                            IsInlinePost=booldict[request.data['IsInlinePost']],
                                            AppearenceFrequency=request.data['AppearenceFrequency'],
                                            #date=request.data['date'],
                                            #CampaignTime=request.data['CampaignTime'],
                                            IsAdvert=True,
                                            AdURL=request.data['AdURL']
                                            )
            for index in range(int(request.data['size'])):
                mc=MemeContent.objects.create(post=post,index=index,IMG=request.FILES['meme'+str(index)])
                mc.save()
            serializer=PostSerializer(post,context={'request': request})
        else:
            post = Post.objects.create(user=request.user,description=request.data['description'],IsPublic=booldict[request.data['IsPublic']])
            for i in request.data['labels'].split(','):
                if len(Label.objects.filter(name=i))==0:
                    l=Label.objects.create(name=i,type='category')
                    l.save()
                else:
                    l=Label.objects.get(name=i)
                pl=PostLabelling.objects.create(post=post,label=l)
                pl.save()
            for index in range(int(request.data['size'])):
                if len(request.data['templates'])>0:
                    t=Template.objects.get(name=request.data['templates'])
                    mc=MemeContent.objects.create(post=post,index=index,IMG=request.FILES['meme'+str(index)],template=t)
                else:
                    mc=MemeContent.objects.create(post=post,index=index,IMG=request.FILES['meme'+str(index)])
                mc.save()
            serializer=PostSerializer(post,context={'request': request})
        post.save()
        return Response(serializer.data)

    def update(self,request):
        pass

    @action(detail=False, methods=['get'])
    def get_ad(self,request):
        ads=Post.objects.filter(IsAdvert=True,IsActive=True)
        setting=AdvertSettings.objects.get(admin=User.objects.get(username="admin"))
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


    @action(detail=True, methods=['post'])
    def moderate(self,request, pk=None):
        if request.user.is_staff:
            post=Post.objects.get(pk=pk)
            print(request.data)
            if request.data['decision']:
                post.delete()
                return Response(True)
            else:
                post.IsModerated=True
                post.save()
                Action.objects.filter(post=post,type='Report').delete()
                return Response(False)

        raise Http404


    def destroy(self, request, pk=None):
        api_result = Post.objects.get(pk=pk)
        api=Post.objects.all()
        serializer=PostSerializer(api, context={'request': request})
        return Response(serializer.data)

    @action(detail=False,
        methods=['get'],
        url_path='retrievePost/(?P<user>[^/.]+)/(?P<post>[^/.]+)')
    def retrievePost(self, request,user,post):
        #IsPublic=post.find('_private') == -1
        #post=pk2.replace('_private','')
        user= User.objects.get(username=user)
        post= Post.objects.get(ID=post,user=user)
        serializer=PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




    @action(detail=True, methods=['get'])
    def like(self,request, pk=None):
        post=Post.objects.get(pk=pk)
        if len(Action.objects.filter(user=request.user,post=post,type='Like'))==0:
            post.save()
            serializer=PostSerializer(post, context={'request': request})
            #action=ActionSerializer(post,context={'request': request})
            Action.objects.create(user=request.user,post=post,type='Like')
        else:
            Action.objects.get(user=request.user,post=post,type='Like').delete()
            post.save()
            serializer=PostSerializer(post, context={'request': request})
        UpdateProfileScores(user=request.user)
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def action(self,request):
        if isinstance(request.user,User):
            setting=AdvertSettings.objects.get(admin=User.objects.get(username="admin"))
            post=Post.objects.get(ID=request.data['post'])
            postOwner=User.objects.get(username=post.user)
            #action=ActionSerializer(post,data={'type':request.data['type']})
            a=Action.objects.create(post=post,user=request.user,type=request.data["type"])
            a.save()
            if request.data["type"]=='Click' and post.IsAdvert:
                if postOwner.balance-setting.MoneyForCick <=0:
                    post.IsActive=False
                    post.save()
                #notify(owner)
                else:
                    postOwner.balance=postOwner.balance-setting.MoneyForClick
            elif request.data["type"]=='View' and post.IsAdvert:
                if postOwner.balance-setting.MoneyForSeen <=0:
                    post.IsActive=False
                    post.save()
                else:
                    postOwner.balance=postOwner.balance-setting.MoneyForSeen
            postOwner.save()
            serializer = PostSerializer(post,context={'request': request} )
            return Response(serializer.data)
        else:
            pass
        return Response({})



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    search_fields=('ID',)
    def list(self,request):
        queryset=Comment.objects.all()
        serializer = CommentSerializer(queryset,many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        #request.data.update({'user':request.user})
        api_result = Comment.objects.create(user=request.user, content=request.data["content"], post=Post.objects.get(ID=request.data["post"]))
        api_result.save()
        serializer=CommentSerializer(api_result,context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def reply(self,request):
        print(request.data)
        post=Post.objects.get(ID=request.data['post'])
        comment=Comment.objects.get(ID=request.data['comment'])
        reply=Comment.objects.create(reply_to=comment,post=post,user=request.user,content=request.data['content'])
        serializer=CommentSerializer(reply,context={'request':request})
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
        if len(CommentLike.objects.filter(user=request.user,comment=com))==0:
            serializer=CommentSerializer(com, context={'request': request})
            #action=ActionSerializer(post,context={'request': request})
            CommentLike.objects.create(user=request.user,comment=com)
        else:
            CommentLike.objects.get(user=request.user,comment=com).delete()
            serializer=CommentSerializer(com, context={'request': request})
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.exclude(is_superuser=1)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    search_fields=('username',)
    @action(detail=False,methods=['Post'])
    def complete(self,request):
        user = User.objects.get(username=request.user.username)
        user.last_name=request.data['last_name']
        user.first_name=request.data['first_name']
        user.save()
        for i in Label.objects.all():
            p=PersonalScoringProfile.objects.create(user=user,label=i,score=0)
            p.save()
        for lp in request.data['meme']:
            a=Action.objects.create(user=user,post=Post.objects.get(ID=lp),type="Like")
            a.save()
        UpdateProfileScores(user=request.user)
        serialized=UserSerializer(user)
        return Response(serialized.data)

    @action(detail=False, methods=['POST'],serializer_class=ProfilePicSerializer,parser_classes=[parsers.MultiPartParser],)
    def pic(self, request):


        user= User.objects.get(username=request.user.username)
        user.avatar= request.FILES['profile_pic']
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=True,methods=['get'])
    def user_login(self, request,pk=None):
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
        endpoint['male']=len(User.objects.filter(sex=True))
        endpoint['female']=len(User.objects.filter(sex=False))
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
    @action(detail=False,methods=['post'])
    def estimate(self,request):
        xy=User.objects.annotate(day=TruncDay('date_joined')).values('day').annotate(c=Count('id')).values('day', 'c')
        if request.data['function']=='estimateUsers':
            response=estimateUsers(xy,request.data['startDate'],request.data['endDate'],request.data['budget'])
        elif request.data['function']=='estimateDateRange':
            response=estimateDateRange(xy,request.data['reachedUsers'],request.data['budget'])
        else:
            response=estimateBudget(xy,request.data['startDate'],request.data['endDate'],request.data['reachedUsers'])

        return Response(response)


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


    @action(detail=False, methods=['POST'])#,parser_classes=[parsers.MultiPartParser],)
    def upload(self, request):
        booldict={'false':False,'true':True}
        t=Template.objects.create(user=request.user,IsPublic=booldict[request.data['IsPublic']],name=request.data['name'],type='portrait')
        print(request.FILES)
        t.IMG= request.FILES['img']
        t.save()
        templates=Template.objects.all()
        serializer = TemplateSerializer(templates,many=True,context={'request':request})
        return Response(serializer.data)

class RecycleViewSet(viewsets.ModelViewSet):
    queryset=Recycle.objects.all()
    serializer_class=RecycleSerializer

    def create(self,request):
        for t in request.data['templates']:#(??)

            rc=Recycle.objects.create(user=request.user,template=Template.objects.get(id=t))
            rc.save()
        serialized=RecycleSerializer(rc,context={'request':request})
        return Response(serialized.data)

    def destroy(self,request,pk):
        for temp in request.data['templates']:
            Recycle.objects.get(user=request.user,template=Template.objects.get(id=temp)).delete()
        return Response({})

class SocialLoginView(generics.GenericAPIView):
    """Log in using facebook"""
    serializer_class = SocialSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)

        try:
            backend = load_backend(strategy=strategy, name=provider,
            redirect_uri=None)

        except MissingBackend:
            return Response({'error': 'Please provide a valid provider'},
            status=status.HTTP_400_BAD_REQUEST)
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
                #password = serializer.data.get('password')
                print('here')
                print(type(backend))
            user = backend.do_auth(access_token)#,password)
            print(user)
        except HTTPError as error:
            print('here2')
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthTokenError as error:
            print('here3')
            return Response({
                "error": "Invalid credentials",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            print('here3')
            print(user)
            authenticated_user = backend.do_auth(access_token, user=user)
            print('here4')
        except HTTPError as error:
            print('here5')
            return Response({
                "error":"invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        except AuthForbidden as error:
            return Response({
                "error":"invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        if authenticated_user and authenticated_user.is_active:
			#generate JWT token
            print('here6')
            print(authenticated_user.email)
            print(authenticated_user.username)
            login(request, authenticated_user)
            print('here7')
            data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )}
			#customize the response to your needs
            response = {
                "email": authenticated_user.email,
                "username": authenticated_user.username,
                "token": data.get('token')
            }
            return Response(status=status.HTTP_200_OK, data=response)
