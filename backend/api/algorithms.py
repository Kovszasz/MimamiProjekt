from .models import *
#from django.contrib.auth.models import User
#from backend.settings.dev import AUTH_USER_MODEL as User
from django.contrib.auth import get_user_model
User = get_user_model()

def UpdateProfileScores(user):
    labelpooldict={}
    labelpool=0
    likes=Action.objects.filter(type='Like',user=user).order_by('-date')
    if len(likes)>150:
        posts=[PostLabelling.objects.filter(post=post.post) for post in likes[:150]]
    else:
        posts=[PostLabelling.objects.filter(post=post.post) for post in likes]
    labels=PersonalScoringProfile.objects.all()
    for label in labels:
        labelpooldict[label.label]=0

    for post in posts:
        labelpool=labelpool+len(post)
        for l in post:
            if l.label in labelpooldict.keys():
                labelpooldict[l.label]+=1
            else:
                labelpooldict[l.label]=1
                p=PersonalScoringProfile.objects.create(user=user,label=l.label,score=0)
                p.save()
                #labels=labels.extend([p])

                labels |= PersonalScoringProfile.objects.filter(p)
    for score in labels:
        for s in labelpooldict.keys():
            if score.label==s:
                if labelpool==0:
                    score.score=0
                else:
                    score.score=labelpooldict[s]/labelpool
                score.save()


def estimateUsers(dataset,x0,x1,area):
    return 

def estimateBudget(dataset,areaObj,areaHave):
    return 10000

def estimateDateRange(dataset,x0,x1,area):
    return 50

def Personalization(UserObject,PostObject):
    postlabel=PostLabelling.objects.filter(post=PostObject)
    score=0
    for label in postlabel:
            if len(PersonalScoringProfile.objects.filter(user=UserObject, label=label.label))>0:
                score=score+PersonalScoringProfile.objects.get(user=UserObject,label=label.label).score
    return score
