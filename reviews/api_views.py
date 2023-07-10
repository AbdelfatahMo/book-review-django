from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import *
from .serializers import *

class Login(APIView):
    def post(self, request):
        user=authenticate(username=request.data.get("username"), password=request.data.get('password'))
        if not user:
            return Response({'error': 'Credentials are incorrect or user does not exist'},status=HTTP_404_NOT_FOUND)
        token, _ =Token.objects.get_or_create(user=user)
        return Response({"token": token.key},status=HTTP_200_OK)

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # not need authentication here its just exercise
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset=Review.objects.order_by("-date_created")
    serializer_class=ReviewSerializer
    pagination_class=LimitOffsetPagination
    authentication_classes=[]



# @api_view()
# def first_api_view(request):
#     num_of_books=Book.objects.count()
#     return Response({'num_of_books':num_of_books})

# #FBV
# # @api_view()
# # def all_books(request):
# #     books=Book.objects.all()
# #     books_serializer=BookSerializer(books,many=True)
# #     return Response(books_serializer.data)
# #CBV
# class AllBooks(ListAPIView):
#     queryset=Book.objects.all()
#     serializer_class=BookSerializer
    
# class ContributorView(ListAPIView):
#     queryset=Contributor.objects.all()
#     serializer_class = ContributorSerializer