from django.urls import path
from .views import index_view, login_view, signup_view, dashboard_view, logout_view, add_expense_api,export_monthly_spending
urlpatterns = [
    path('', index_view, name='index'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/',logout_view, name='logout'),
    path('api/add-expense/', add_expense_api, name='add_expense_api'),
    path("export-monthly/", export_monthly_spending, name="export_monthly"),
   
]
