from django.contrib import admin
from .models import Dates


class DatesAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "count", "created_at", "updated_at")
    list_filter = ("date", "user")
    search_fields = ("user__email", "user__username", "date")
    ordering = ("-date",)

    # Optional: if you want to make fields read-only
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Dates, DatesAdmin)
