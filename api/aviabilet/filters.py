from django_filters import rest_framework as filters

from api.aviabilet.models import Aviabilet


class AviabiletFilter(filters.FilterSet):
    # planes = filters.NumberFilter(field_name='planes', lookup_expr='e')
    price_from = filters.NumberFilter(field_name='price', lookup_expr='gte') # >=
    price_to = filters.NumberFilter(field_name='price', lookup_expr='lte') # <=
     # = filters.CharFilter(field_name='origin', lookup_expr='icontains')
    destination = filters.CharFilter(field_name='planes__destination', lookup_expr='icontains')
    depart_day = filters.CharFilter(field_name='planes__depart_day', lookup_expr='exact')
    flight_from = filters.CharFilter(field_name='planes__origin', lookup_expr='icontains')
    class Meta:
        model = Aviabilet
        # fields = ['price','flight_from','destination', 'depart_day',]
        fields = '__all__'
    #
    # def to_representation(self, instance):
    #         request = self.context.get('request')
    #         destination = request.destination
    #         representation = super().to_representation(instance)
    #         f_ticket = instance.flight_ticket.filter(destination=destination)
    #         print(f_ticket)
    #         representation['planes'] = f_ticket.destination
    #
    #         return representation