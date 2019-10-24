from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.views.decorators.cache import never_cache
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from rest_framework.reverse import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from .AuthMiddleware import *
from random import randint,randrange


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def list(self,request):
        queryset=Post.objects.filter(IsAdvert=False,IsActive=True)
        serializer = PostSerializer(queryset,many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        api_result = Post.objects.create(request.data)
        api_result.save()
        api=Post.objects.all()
        serializer=PostSerializer(api, context={'request': request})
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
        if randrange(0,100)<setting.AdFrequency:
            for i in ads:
                for j in range(i.AppearenceFrequency):
                    AdPool.append(i)
            ad=PostSerializer(AdPool[randrange(0,len(AdPool))],context={'request':request})
            return Response(ad.data)
        else:
            empty=Post.objects.get(ID='empty')
            ad=PostSerializer(empty,context={'request':request})
            return Response(ad.data)

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
            serializer=PostSerializer(post, context={'request': request})
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def action(self,request):
        print('heeeej')
        post=Post.objects.get(ID=request.data['post'])
        print(request.data)
        #action=ActionSerializer(post,data={'type':request.data['type']})
        a=Action.objects.create(post=post,user=request.user,type=request.data["type"])
        a.save()

        serializer = PostSerializer(post,context={'request': request} )
        return Response(serializer.data)






class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self,request):
        queryset=Post.objects.all()
        serializer = PostSerializer(queryset,many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        #request.data.update({'user':request.user})
        api_result = Comment.objects.create(user=request.user, ID=request.data['ID'],content=request.data["content"], post=Post.objects.get(ID=request.data["post"]))
        api_result.save()
        api=Comment.objects.all()
        serializer=CommentSerializer(api, many=True, context={'request': request})
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

    #def create(self,request):
    #    if request.method=='POST':
    #        if (len(User.objects.filter(username=request.POST.get('username')))==0):
    #            u=User.objects.create(username=request.POST.get('username'),first_name=request.POST.get('first_name'))
    #            u.set_password(request.POST.get('password'))
    #            u.set_email(request.POST.get('email'))
    #            u.save()
    #            serializer = ModSerializer(queryset, many=True)
    #            return Response(serializer.data)

    #lookup_field = 'username'



"""
class UserViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset=User.objects.all()
    serializer_class = UserSerializer
    #lookup_field = 'username'
    #lookup_url_kwarg = 'username'
    def list(self,request):
        queryset=User.objects.all()
        serializer = UserSerializer(queryset,many=True, context={'request': request})
        return Response(serializer.data)

    @api_view(['POST'])
    def register(request):
        serialized = UserSerializer(data=request.DATA)
        if serialized.is_valid():
            User.objects.create_user(
                serialized.init_data['email'],
                serialized.init_data['username'],
                serialized.init_data['password']
                )
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

    def detail(self, request, pk=None):
        api=User.objects.get(username=pk)
        serializer=UserSerializer(api, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        api_result = User.objects.get(username=pk)
        api_result.update(request.data)
        api_result.save()
        serializer=UserSerializer(api_result, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        api_result = User.objects.get(username=pk)
        api=User.objects.all()
        serializer=PostSerializer(api, context={'request': request})
        return Response(serializer.data)


"""



"""
class UserViewSet(viewsets.ViewSet):
    ""Userviewset
    Restful Structure:
        | URL style      | HTTP Method | URL Nanme   | Action Function |
        |----------------|-------------|-------------|-----------------|
        | /users         | GET, POST   | user-list   | user_list       |
        | /users/<email> | GET, DELETE | user-detail | user_detail     |
    ""
    # Router class variables
    lookup_field = 'email'
    lookup_value_regex = '[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'

    # Viewsets class variables
    #queryset = User.objects.all()

    def list(self, request):
        ""GET - Show all users""
        print request.version
        api_result = user_list.lists_all_users()
        return Response(api_result)

    def create(self, request):
        ""POST - Add new user""
        api_result = user_list.create_new_user(request.data)
        return Response(api_result)

    def retrieve(self, request, email=None):
        ""GET - Show <email> user""
        api_result = user_detail.retrieve_the_user(email)
        return Response(api_result)

    def partial_update(self, request, email=None):
        return Response()

    def destroy(self, request, email=None):
        ""DETELE - Delete <email> user""
        api_result = user_detail.destroy_the_user(email)
        return Response(api_result)
"""
