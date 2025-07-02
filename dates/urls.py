from django.urls import path
from .views import DateEntryCreateAPIView, StoredDatesListAPIView

urlpatterns = [
    path("add-date/", DateEntryCreateAPIView.as_view(), name="add-date"),
    path("stored/", StoredDatesListAPIView.as_view(), name="stored-dates"),
]
