from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'psys'

urlpatterns = [
    # index
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='psys/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),

    # Main menu
    path('main/', views.MainMenu, name='main_menu'),
    path('MainMenu/', views.MainMenu, name='MainMenu'),

    # Customer pages
    path('customer-list/', views.customer_list, name='customer_list'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customer-regist/', views.customer_regist, name='customer_regist'),
    path('customer/update/<str:pk>/', views.customer_update, name='customer_update'),
    path('customer/delete/<str:code>/', views.customer_delete, name='customer_delete'),
    path('customer_search/', views.customer_search, name='customer_search'),
    path('customer_management/', views.CustomerManagementMenu, name='customer_management'),
    path('customerReportMenu/', views.CustomerReportMenu, name='CustomerReportMenu'),
    path('customer/summary/', views.customer_summary, name='customer_summary'),

    # Employee
    path('employee-regist/', views.employee_regist, name='employee_regist'),
    path("employees/", views.employee_list, name="employee_list"),
    path("employee/update/<str:employee_no>/", views.employee_update, name="employee_update"),
    path("employee/delete/<str:employee_no>/", views.employee_delete, name="employee_delete"),

    # Item
    path("items/", views.item_list, name="item_list"),
    path("item/update/<str:item_code>/", views.item_update, name="item_update"),


    # Inline update
    path('customer/update_inline/<str:pk>/', views.customer_update_inline, name='customer_update_inline'),
]
