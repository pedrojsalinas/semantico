from django.urls import path
from recog_entities.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('info/', InfoView.as_view(), name='info'),
    path('lee/', LeeView.as_view(), name='lee'),
]
