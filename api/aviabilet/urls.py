from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.aviabilet.views import AviabiletViewSet, AirlinesListCreateView, AirlinesRetriveDeleteUpdateView, \
    PassengerViewSet, AirlinesViewSet, PlanesListCreateView, PlanesRetriveDeleteUpdateView

router = DefaultRouter()
router.register('', AviabiletViewSet)
router.register('passenger', PassengerViewSet)
router.register('airlines', AirlinesViewSet)

urlpatterns = [
    path('airlines/', AirlinesListCreateView.as_view()),
    path('airlines/<str:slug>/', AirlinesRetriveDeleteUpdateView.as_view()),
    path('planes/', PlanesListCreateView.as_view()),
    path('planes/<int:pk>/', PlanesRetriveDeleteUpdateView.as_view()),

    path('', include(router.urls)),
    # path('passenger/',include(router.urls)),
    # path('airlines/',include(router.urls)),
]
