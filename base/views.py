from django.shortcuts import render
from .models import ProductType, Product, Purchase, Sell, Department, Customer, Suppliers
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductTypeSerializer, ProductSerializer, UserSerializer, CustomerSerializer, PurchaseSerializer, SellSerializer,DepartmentSerializer, GroupSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, DjangoModelPermissions
from .permission import CustomPermissions
from django.contrib.auth.models import Group
import requests
from django.conf import settings
from django.http import JsonResponse

# Create your views here.
class ProductTypeViewset(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [CustomPermissions]

class DepartmentViewset(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [CustomPermissions]

class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomPermissions]

class SuppliersViewset(ModelViewSet):
    queryset = Suppliers.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomPermissions]

class ProductViewset(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CustomPermissions]
    filterset_fields = ['type','department']
    search_fields = ['name']

    def get(self,request):
        Product_objs = self.get_queryset()
        filter_objs = self.filter_queryset(Product_objs)
        serializer = ProductSerializer(filter_objs,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data Created')
        else:
            return Response(serializer.errors)

class ProductdetailViewset(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CustomPermissions]
   
    def get(self,request,pk):
        try:
            product_obj = Product.objects.get(id=pk)
        except:
            return Response('Data not found')
        serializer = ProductSerializer(product_obj)
        return Response(serializer.data)

    def put(self,request,pk):
        try:
            product_obj = Product.objects.get(id=pk)
        except:
            return Response('Data not found')
        serializer = ProductSerializer(product_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data Updated')
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        try:
            product_obj = Product.objects.get(id=pk)
        except:
            return Response('Data not found')
        product_obj.delete()
        return Response('Data Deleted!')

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email,password=password)

    if user == None:
        return Response('Invalid credentials!')
    else:
        token,_ = Token.objects.get_or_create(user=user)
        return Response(token.key)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    password = request.data.get('password')
    hash_password = make_password(password)
    request.data['password'] = hash_password
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response('Data Created!')
    else:
        return Response(serializer.errors)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def group_listing(request):
    groups_objs = Group.objects.all()
    serializer = GroupSerializer(groups_objs,many=True)
    return Response(serializer.data)

class PurchaseViewset(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [CustomPermissions]

class SellViewset(ModelViewSet):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
    permission_classes = [CustomPermissions]



