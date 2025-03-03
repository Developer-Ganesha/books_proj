from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BooksSerializer
from django.contrib.auth import authenticate 
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import  filters ,status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import BooksSerializer ,UpdateBookDetailSerializer
from .models import Book

def get_tokens_for_user(book):
    refresh = RefreshToken.for_user(book)
    return{
        'refresh':str(refresh),
        'access':str(refresh.access_token),
          }
class BookView(APIView):
       authentication_classes =[JWTAuthentication]
       def post(self, request, format=None):
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            book=serializer.save()
            token = get_tokens_for_user(book)
            return Response({'token':token,'Msg':'Book Register SuccessFull'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class BookDetailView(APIView):
    authentication_classes =[JWTAuthentication]
    queryset = Book.objects.all() 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'author']
    search_fields = ['title', 'author']

    def get(self, request,pk,format=None):
        book = get_object_or_404(Book,pk=pk) 
        serializer = BooksSerializer(book)
        return Response(serializer.data)

class BookDetailUpdateView(APIView):
    authentication_classes =[JWTAuthentication]
    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = UpdateBookDetailSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"book details update successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailDeleteView(APIView):
    authentication_classes =[JWTAuthentication]
    def delete(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)        
    
