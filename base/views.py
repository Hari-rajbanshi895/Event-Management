from django.shortcuts import render
from .models import ProductType, Product, Purchase, Sell, Department, Customer, Suppliers, Payment
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

@api_view(['POST'])
def initiate_payment(request):
    amount = request.data.get('amount')
    email = request.data.get('email')

    payment_data = {
        'amount': amount,
        'email': email,
    }

    headers = {
        'Authorization': f"Bearer {settings.KHALTI_SECRET_KEY}"
    }
    response = requests.post(settings.KHALTI_URL, data=payment_data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        payment_url = response_data.get('payment_url')
        payment_id = response_data.get('token')  
        Payment.objects.create(payment_id=payment_id, amount=amount)
        return JsonResponse({'payment_url': payment_url})
    else:
        return Response({'error': 'Failed to initiate payment'}, status=response.status_code)

@api_view(['POST'])
def verify_payment(request):
    token = request.data.get('token')

    headers = {
        'Authorization': f"Bearer {settings.KHALTI_SECRET_KEY}"
    }
    response = requests.get(f"{settings.KHALTI_URL}/{token}/", headers=headers)

    if response.status_code == 200:
        payment_info = response.json()
        payment = Payment.objects.filter(payment_id=token).first()

        if payment:
            payment.status = 'success' if payment_info['status'] == 'Completed' else 'failed'
            payment.save()
        
        return JsonResponse({'status': 'Payment verified', 'data': payment_info})
    else:
        return Response({'error': 'Payment verification failed'}, status=response.status_code)

