from django_filters import rest_framework as filters

class TopMemeFilter(filters.FilterSet):

    finish_on = filters.IntegerFilter(name='', method='PopularityScoreMethod')

    begin_on = filters.BooleanFilter(name='begin_on', method='filter_manifestation')


    def PopularityScoreMethod(self,queryset,name,value):
        if not Post.IsAdvert:
            actiontypes={}
            for i in ['Like','Click','Share','Report']:
                actiontypes[i]=len(Action.objects.filter(post=Post,type=i))
            return actiontypes['Like']+actiontypes['Click']+2*actiontypes['Share']-10*actiontypes['Report']
        else:
            return 0


    def filter_manifestation(self, queryset, name, value):
        if value is False:
            lookup = '__'.join([name, 'gte'])
        else:
            lookup = '__'.join([name, 'lte'])
        qs = queryset.filter(**{lookup: timezone.now()})
        return qs

    class Meta:
        model = Event
        fields = [
            'finished', 'has_begun'
        ]
