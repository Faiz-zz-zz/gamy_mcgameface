from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^get_current_events$', views.current_events),
    url(r'^mark_attendance$', views.post_participation),
    url(r'^register_new_user$', views.register_user)
]