from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import DateEntrySerializer
from .models import Dates


class DateEntryCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DateEntrySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        date = serializer.validated_data["date"]
        count = serializer.validated_data["count"]
        print(f"user-date-:{date} , count-: {count}")

        obj = Dates.objects.filter(user=user, date=date).first()

        # If entry exists
        if obj:
            if count == 0:
                obj.delete()
                return Response(
                    {"message": "Entry deleted successfully."},
                    status=status.HTTP_200_OK,
                )
            if obj.count != count:
                obj.count = count
                obj.save(update_fields=["count"])  # ✅ Optimized update
                return Response(
                    {"message": "Entry updated successfully.", "count": obj.count},
                    status=status.HTTP_200_OK,
                )
            return Response({"message": "No changes made."}, status=status.HTTP_200_OK)

        # If entry doesn't exist
        if count == 0:
            return Response(
                {"message": "No entry found, nothing to delete."},
                status=status.HTTP_200_OK,
            )

        Dates.objects.create(user=user, date=date, count=count)
        return Response(
            {"message": "Entry created successfully.", "count": count},
            status=status.HTTP_201_CREATED,
        )


class StoredDatesListAPIView(APIView):
    """
    List all stored dates for the authenticated user according to perticular year and month.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        year = request.query_params.get("year")
        month = request.query_params.get("month")

        # Validate inputs
        if not year or not month:
            return Response({"error": "year and month are required."}, status=400)

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({"error": "year and month must be integers."}, status=400)

        # Query DB for matching dates
        dates_qs = Dates.objects.filter(
            user=user, date__year=year, date__month=month
        ).only("date", "count")

        # Build response
        result = [
            {"date": date_obj.date.strftime("%Y-%m-%d"), "count": date_obj.count}
            for date_obj in dates_qs
        ]

        return Response(result, status=200)
