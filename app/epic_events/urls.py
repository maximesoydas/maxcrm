from django.urls import path
from .views import Index
from django.urls import include, path
from rest_framework import routers
from .views import ClientViewSet, ContractViewSet, EventViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'events', EventViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('index/', Index.as_view(), name='index'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
