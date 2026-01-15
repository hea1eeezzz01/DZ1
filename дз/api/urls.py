from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user-requests', views.UserRequestViewSet, basename='userrequest')
router.register(r'input-data', views.InputDataViewSet, basename='inputdata')
router.register(r'results', views.CalculationResultViewSet, basename='result')

urlpatterns = [
    path('calculate/', views.calculate_segment_tree, name='calculate'),
    path('', include(router.urls)),
]
