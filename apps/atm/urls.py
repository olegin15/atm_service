from django.urls import path
from apps.atm import views


urlpatterns = (
    path('deposit/', views.DepositView.as_view(), name='deposit'),
    path('withdraw/', views.WithdrawView.as_view(), name='withdraw'),
)

