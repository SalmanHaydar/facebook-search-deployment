from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$',views.newForm,name="new_form"),
]
