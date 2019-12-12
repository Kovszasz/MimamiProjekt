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
from rest_framework import generics
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from rest_framework.reverse import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from random import randint,randrange
from .algorithms import *
from collections import OrderedDict
import json
import jwt
from django.http import Http404
from numpy import polyfit
from django.db.models import Count
from django.db.models.functions import TruncDay
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from requests.exceptions import HTTPError
from rest_framework_jwt.utils import jwt_encode_handler,jwt_payload_handler
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .paginations import *
from rest_framework import pagination
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.serializers import ActivationSerializer
from django.http import QueryDict
from datetime import datetime
User = get_user_model()

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

class FollowViewSet(viewsets.ModelViewSet):
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



class TimelineView(generics.ListCreateAPIView):
    #serializer_class = PostSerializer
    pagination_class = PostPagination
    def get_queryset(self):
        queryset=Post.objects.filter(IsAdvert=False,IsActive=True,IsPublic=True).order_by('-date')
        top = self.request.GET.get('top', None)
        like=self.request.GET.get('like',None)
        user=self.request.GET.get('user',None)
        if top:
            queryset=queryset.order_by('-PopularityScore')
        elif like and user:
            queryset=Action.objects.filter(user__username=user,type='Like').order_by('-post__date')
        elif user:
            queryset=Post.objects.filter(user__username=user,IsAdvert=False).order_by('-date')
        return queryset

    def get_serializer_class(self):
        top = self.request.GET.get('top', None)
        like=self.request.GET.get('like',None)
        user=self.request.GET.get('user',None)
        if top:
            return PostSerializer
        elif like and user:
            return ActionSerializer
        elif user:
            return PostSerializer
        return PostSerializer

class PostSearchViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    search_fields=('user__username','description','postlabelling__label__name','comment__content','imgs__template__name','memetext__text')
    def create(self,request):
#        term=request.data['term']
#        for i in request.data['result']:
#            p=Post.objects.get(ID=int(i['ID'])
#            if isinstance(request.user,User):
#                sr=SearchResult.objects.create(user=request.user,result=p,term=term)
#            else:
#                sr=SearchResult.objects.create(result=p,term=term)
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
    paginator=PostPagination
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    search_fields=('user__username',)
    def list(self,request):
        queryset=Post.objects.filter(IsAdvert=False,IsActive=True,IsPublic=True).order_by('-date')
        serializer = PostSerializer(queryset,many=True, context={'request': request})
        if isinstance(request.user,User):
            if request.user.is_staff:
                postquery=Post.objects.filter(IsAdvert=False,IsModerated=False).order_by('-date')
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
                                            CampaignTimestart=request.data['CampaignTimestart'],
                                            CampaignTimeend=request.data['CampaignTimeend'],
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

    @action(detail=False,methods=['post'])
    def updateAd(self,request):
        print(request.data)
        if request.data['IsAdvert']:
            p=Post.objects.get(ID=request.data['ID'])
            p.ID=request.data['ID']
            p.IsActive=request.data['IsActive']
            p.CampaignTimestart=request.data['CampaignTimestart']
            p.CampaignTimeend=request.data['CampaignTimeend']
            p.save()
            serializer=PostSerializer(p,context={'request':request})
            return Response(serializer.data)
        else:
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
                Action.objects.filter(post=post,type='Report').delete().set_popularityscore(post)
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
            Action.objects.set_popularityscore(post)
            serializer=PostSerializer(post, context={'request': request})
            #action=ActionSerializer(post,context={'request': request})

            Action.objects.create(user=request.user,post=post,type='Like')
        else:
            Action.objects.get(user=request.user,post=post,type='Like').delete()
            Action.objects.set_popularityscore(post)
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
            Action.objects.set_popularityscore(post)
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



class CommentView(generics.ListAPIView):
    pagination_class = PostPagination
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = self.request.GET.get('post', None)
        reply=self.request.GET.get('reply',None)
        if post:
            if reply:
                comments = Comment.objects.filter(post=post,reply_to=reply)
            else:
                comments = Comment.objects.filter(post=post)
        return comments

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
        print(request.data)
        user = User.objects.get(username=request.user.username)
        user.last_name=request.data['last_name']
        user.first_name=request.data['first_name']
        user.age=request.data['birthday']
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

    @action(detail=False,methods=['GET'])
    def changeTheme(self,request):
        print(type(request.user))
        if isinstance(request.user,User):
            u=User.objects.get(username=request.user.username)
            u.DarkMode = not u.DarkMode
            u.save()
            print(u.username,'\t',u.DarkMode)
        return Response(status=status.HTTP_200_OK)

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
            t=MemeText.objects.create(post=post,text=request.data['text'][i])
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
        today=datetime.now().date()
        start=datetime.strptime(request.data['startDate'],'%Y-%m-%d')
        end=datetime.strptime(request.data['endDate'],'%Y-%m-%d')
        range=end-start
        lookback=today-range
        clicks=len(Action.objects.filter(date__range=[lookback.isoformat(),today.isoformat()]),type='Click')
        views=len(Action.objects.filter(date__range=[lookback.isoformat(),today.isoformat()]),type='Seen')
        if request.data['function']=='estimateUsers':
            settings=AdvertSettings.objects.get(admin=admin)
            normalized_budget=settings.MoneyForSeen*views+settings.MoneyForClick*click
            frequency=request.data['budget']/normalized_budget
            users=len(Action.objects.filter(date__range=[lookback.isoformat(),today.isoformat()],type=['Click','View']))*frequency
            response={'users':users,'AdFrequency':frequency}
        return Response(response)


class TemplateViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateSerializer
    pagination_class = TemplatePagination
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    search_fields=('user__username','name',)

    def get_queryset(self):
        my = self.request.GET.get('my', None)
        recycle=self.request.GET.get('recycle',None)
        user=self.request.GET.get('user',None)
        if my:
            return Template.objects.filter(user__username=user).order_by('-date')
        elif recycle:
            return Recycle.objects.filter(user__username=user).order_by('-date')
        else:
            return Template.objects.filter(IsPublic=True).order_by('-date')

    def get_serializer_class(self):
        my = self.request.GET.get('my', None)
        recycle=self.request.GET.get('like',None)
        if recycle:
            return RecycleSerializer
        else:
            return TemplateSerializer

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
                print(serializer.data)
                access_token = serializer.data.get('access_token')
                #password = serializer.data.get('password')
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
            login(request, authenticated_user)
            data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )}
			#customize the response to your needs
            response = {
                "email": authenticated_user.email,
                "username": authenticated_user.username,
                #"gender": authenticated_user.gender,
                #"birthday": authenticated_user.birthday,
                #"profile": authenticated_user.profile,
                "token": data.get('token')
            }
#            try:
            #self.user_activate(authenticated_user)
#            except:
#                pass
            authenticated_user.is_active=True
            authenticated_user.save()
            password = jwt.encode({'username':authenticated_user.username}, 'secret', algorithm='HS256')
            d={'username':authenticated_user.username,'password':password.decode("utf-8")}#,'csrfmiddlewaretoken':request.data['csrfmiddlewaretoken']}
            query_dict = QueryDict('', mutable=True)
            query_dict.update(d)
            response=TokenObtainPairSerializer(data=query_dict)
            response.is_valid()
            serialized_user=UserSerializer(authenticated_user)
            serialized={'token':response.validated_data,'user':serialized_user.data}
            print(serialized)
            return Response(status=status.HTTP_200_OK, data=serialized)

    def user_activate(self,user):
        uid=utils.encode_uid(user.pk)
        token=default_token_generator.make_token(user)
        ActivationSerializer({'uid':uid,'token':token})
