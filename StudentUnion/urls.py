from django.urls import path, include
from .views import *

app_name="StudentUnion"

urlpatterns = [
    path('', StudentReceiptsView.as_view(), name='home'),
    path('<int:pk>/', StudentReceiptsPerYearView.as_view(), name='year-based'),
    path('create/', StudentCreateReceiptView.as_view(), name='create-receipt'),
    path('detail/<int:pk>', StudentReceiptDetailView.as_view(), name='receipt-detail'),
    path('delete/<int:pk>', StudentReceiptDeleteView.as_view(), name='receipt-delete'),
    path('download/<int:pk>', generate_pdf, name='download-receipt'),
    # path('update/<int:pk>', StudentReceiptUpdateView.as_view(), name='receipt-update'),
]