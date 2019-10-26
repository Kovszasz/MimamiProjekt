from .models import *
from django.contrib.auth.models import User


def UpdateProfileScores(user):
    labelpooldict={}
    labelpool=0
    likes=Action.objects.filter(type='Like',user=user)
    posts=[PostLabelling.objects.filter(post=post.post) for post in likes]
    labels=PersonalScoringProfile.objects.all()
    print(likes)
    print(posts)
    for label in labels:
        print(label.label,'\t',label.score)
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
                labels=labels.extend([p])
    for score in labels:
        for s in labelpooldict.keys():
            if score.label==s:
                print(score.label,'\t',labelpooldict[s]/labelpool)
                if labelpool==0:
                    score.score=0
                else:
                    score.score=labelpooldict[s]/labelpool
                score.save()
