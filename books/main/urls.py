from django.urls import path
from .views import BookView ,BookDetailView,BookDetailDeleteView,BookDetailUpdateView

urlpatterns = [
    path('books/', BookView.as_view(), name='book-list'),
    path('book-detail/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('update/<int:pk>/', BookDetailUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BookDetailDeleteView.as_view(), name='delete'),
]
