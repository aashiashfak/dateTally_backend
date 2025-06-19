from django.db import models
from accounts.models import CustomUser, TimeStampedModel

class Dates(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='date_tallies')
    date = models.DateField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "date"], name="unique_user_date")
        ]
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.count}"
