from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views
from .views import RequestViewSet, ReturnRequests

router = SimpleRouter()
router.register('request', RequestViewSet)

urlpatterns = [
    path('return_requests/', views.ReturnRequests.as_view(), name='return_requests'),
    path('return_requests/<int:user_id>', views.ReturnRequests.as_view(), name='return_requests_by_id'),
    path('return_image/<int:pk>', views.ReturnImage.as_view(), name='return_image'),
    path('generate_images/', views.GenerateImages.as_view(), name='generate_images'),
]