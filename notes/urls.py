from django.urls import path
from . import views

urlpatterns = [
    path("notes", views.NotesListView.as_view(), name="notes.list"),
    path("notes/popular", views.PopularNotesListView.as_view(), name="notes.popular"),
    path("notes/<int:pk>", views.NotesDetailView.as_view(), name="notes.detail"),
    path("notes/<int:pk>/edit", views.NotesUpdateView.as_view(), name="notes.edit"),
    path("notes/<int:pk>/delete", views.NotesDeleteView.as_view(), name="notes.delete"),
    path("notes/new", views.NotesCreateView.as_view(), name="notes.new"),
    path("notes/<int:pk>/add_like", views.add_like_view, name="notes.add_like"),
]
