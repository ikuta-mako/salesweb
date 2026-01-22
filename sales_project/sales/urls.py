from django.urls import path
from . import views

urlpatterns = [
    path("", views.top, name="top"),
    path("tenpo/<int:tenpo_id>/", views.tenpo_detail, name="tenpo_detail"),
    path("tenpo/<int:tenpo_id>/graph/", views.tenpo_graph, name="tenpo_graph"),
    path("tenpo/<int:tenpo_id>/dashboard/", views.dashboard, name="dashboard"),

]   