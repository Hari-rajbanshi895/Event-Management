from django.urls import path
from .views import *

urlpatterns = [
    path('Product-type/', ProductTypeViewset.as_view({'get':'list','post':'create'})),
    path('Department/',DepartmentViewset.as_view({'get':'list','post':'create'})),
    path('product/', ProductViewset.as_view()),
    path('Product/<int:pk>/', ProductdetailViewset.as_view()),
    path('Purchase/',PurchaseViewset.as_view({'get':'list','put':'create'})),
    path('Purchase/<int:pk>/',PurchaseViewset.as_view({'get':'retrive','put':'update','delete':'destory'})),
    path('Sell/',SellViewset.as_view({'get':'list','put':'create'})),
    path('Sell/<int:pk>/',SellViewset.as_view({'get':'retrive','put':'update','delete':'destory'})),
    path('Customer/', CustomerViewset.as_view({'get':'list','post':'create'})),
    path('Customer/<int:pk>/',CustomerViewset.as_view({'get':'retrive','put':'update','delete':'destory'})),
    path('Suppliers/', SuppliersViewset.as_view({'get':'list','post':'create'})),
    path('Suppliers/<int:pk>/',SuppliersViewset.as_view({'get':'retrive','put':'update','delete':'destory'})),
    path('group/',group_listing),
    path('login/',login),
    path('register/',register),
    

]
