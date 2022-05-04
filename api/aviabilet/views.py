from django.shortcuts import render

# Create your views here.

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import *
from rest_framework.mixins import *
from api.aviabilet.filters import AviabiletFilter
from api.aviabilet.models import *
from api.aviabilet.serializers import AviabiletSerializer, RatingSerializers, AirlinesSerializers, PlanesSerializers, \
    PassengerSerializers, FavoriteSerializers, ReviewSerializers


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100000



class AviabiletViewSet(ModelViewSet):
    queryset = Aviabilet.objects.all()
    serializer_class = AviabiletSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filter_fields = ['category', 'owner']
    filterset_class = AviabiletFilter
    ordering_fields = ['price', 'id']
    search_fields = ['price','flight_from','destination','depart_day']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'rating':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # .../rating/2/



class AirlinesViewSet(ModelViewSet):
    queryset = Airlines.objects.all()
    serializer_class = AirlinesSerializers
    permission_classes = [IsAuthenticated]

##like
    @action(methods=['POST'], detail=True)
    def like(self, request, *args, **kwargs):
        airline = self.get_object()
        like_obj, _ = Like.objects.get_or_create(airlines=airline, owner=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unlike'
        return Response({'status': status})

##rating
    @action(methods=['POST'], detail=True)
    def rating(self, request, slug):       # http://localhost:8000/product/id_product/rating/
        serializer = RatingSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj = Rating.objects.get(airlines=self.get_object(),
                                     owner=request.user)
            obj.rating = request.data['rating']
        except Rating.DoesNotExist:
            obj = Rating(owner=request.user,
                         aviabilet=self.get_object(),
                         rating= request.data['rating']
                        )
        obj.save()
        return Response(request.data,
                        status=status.HTTP_201_CREATED)

#review
    @action(methods=['POST'], detail=True)
    def review(self, request, slug):
        serializer = ReviewSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj = Review.objects.get(product=self.get_object(),
                                      owner=request.user)
            obj.review = request.data['review']
        except Review.DoesNotExist:
            obj = Review(owner=request.user,
                          product=self.get_object(),
                          )
        obj.save()
        return Response(request.data,
                        status=status.HTTP_201_CREATED)


##Favorites
    @action(methods=['POST'], detail=True)
    def favorite(self, request, slug):
        serializer = FavoriteSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            object = Favorite.objects.get(product=self.get_object(),owner=request.user)
        except Favorite.DoesNotExist:
            object = Favorite(owner=request.user,product=self.get_object())
        object.save()
        return Response('-- Favorite added', status=status.HTTP_200_OK)




class PassengerViewSet(ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializers
    permission_classes = [IsAuthenticated]



class PlanesListCreateView(ListCreateAPIView):
    queryset = Planes.objects.all()
    serializer_class = PlanesSerializers
    permission_classes = [IsAuthenticated]





class PlanesRetriveDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Planes.objects.all()
    serializer_class = AirlinesSerializers
    permission_classes = [IsAuthenticated]





class AirlinesListCreateView(ListCreateAPIView):
    queryset = Airlines.objects.all()
    serializer_class = AirlinesSerializers
    permission_classes = [IsAuthenticated]


class AirlinesRetriveDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Airlines.objects.all()
    serializer_class = AirlinesSerializers
    permission_classes = [IsAuthenticated]


