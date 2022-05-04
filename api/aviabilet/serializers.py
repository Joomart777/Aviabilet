from rest_framework import serializers


from api.aviabilet.models import *


class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class PlanesSerializers(serializers.ModelSerializer):
        class Meta:
            model = Planes
            fields = "__all__"


class RatingSerializers(serializers.ModelSerializer):
    owner = serializers.EmailField(required=False)
    class Meta:
        model = Rating
        fields = ('rating',)

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("review",)

class FavoriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"





class PlaneImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class PassengerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'

class AirlinesSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    images = PlaneImageSerializers(many=True, read_only=True)
    class Meta:
        model = Airlines
        fields = "__all__"
    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        airline = Airlines.objects.create(**validated_data)
        for image in images_data.getlist('images'):
            Image.objects.create(airlines=airline, image=image)
        return airline
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rating_result = 0
        for i in instance.rating.all():
            rating_result += int(i.rating)
        if instance.rating.all().count() == 0:
            representation['rating'] = rating_result
        else:
            representation['rating'] = rating_result / instance.rating.all().count()
        representation['likes'] = instance.like.filter(like=True).count()

        return representation


class AviabiletSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    images = PlaneImageSerializers(many=True, read_only=True)
    passenger = PassengerSerializers(many=True, read_only=True)


    class Meta:
        model = Aviabilet
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        aviabilet = Aviabilet.objects.create(**validated_data)
        for image in images_data.getlist('images'):
                Image.objects.create(airlines=aviabilet, image=image)
        return aviabilet

    # pl = Planes.objects.get(id = self.planes.id)
    # if not pl.capacity == 0:
    # else:
    # av = Aviabilet.objects.get(id=self.id)
    # av.status = 'F'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['airlines'] = instance.planes.airlines.slug
        representation['plane'] = instance.planes.plane
        representation['Flight_from'] = instance.planes.origin
        representation['Destination'] = instance.planes.destination
        representation['depart_day'] = instance.planes.depart_day
        representation['depart_time'] = instance.planes.depart_time
        representation['arrival_time'] = instance.planes.arrival_time

        return representation


