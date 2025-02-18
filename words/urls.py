from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_loader)
    # path('', views.get_merchant_by_user),
    # path('<int:pk>', views.get_merchant_by_pk, name='merchant-detail-by-pk'),
    # path('<str:name>', views.get_merchant_by_name, name='merchants-detail-by-name'),
    # path('terminal/', views.get_merchant_terminal),
    # path('terminal/<int:pk>', views.get_merchant_terminal_by_pk, name='merchant-terminal-detail')
]