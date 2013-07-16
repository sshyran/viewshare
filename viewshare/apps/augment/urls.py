from django.conf.urls import *
from viewshare.apps.augment import views

urlpatterns = patterns('',
    url(r'^transform/$', views.transform, name="akara_augment"),
    url(r'^patterns.json$', views.pattern_json, name="list_pattern_json"),
    url(r'^errors.json$', views.error_json, name="augmentation_error_json"),
)
