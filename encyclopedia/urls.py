from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.entry, name="entry"),
    path('entry-search/', views.search_entries, name="entries"),
    path('newpage/', views.create_new_page, name="new"),
    path('random/', views.rando_entry, name='rando'),
    path('edit_entry/<str:title>', views.edit_page, name='edit')
]
