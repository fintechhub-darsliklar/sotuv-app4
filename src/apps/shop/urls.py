from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile_page, name="profile_page"),
    path("xodimlar/", views.xodimlar_page, name="xodimlar_page"),
    path("xodim/qoshish/", views.xodim_qoshish_page, name="xodim_qoshish_page"),
    path("xodim/delete/<int:xodim_id>/", views.xodim_delete_page, name="xodim_delete_page"),
    path("xodim/edit/<int:xodim_id>/", views.xodim_taxrirlash_page, name="xodim_taxrirlash_page"),
]