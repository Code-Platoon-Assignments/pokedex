from datetime import date

from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=50, unique=True)
    level = models.PositiveIntegerField(default=1)
    type = models.CharField(max_length=20, default="normal")
    description = models.TextField(default="Unknown")
    captured = models.BooleanField(default=False)
    date_encountered = models.DateField(default=date.today)

    def __str__(self):
        status = "captured" if self.captured else "not captured"
        return f"{self.name} (Lv. {self.level}) - {status}"

    def level_up(self):
        self.level += 1
        self.save()

    def change_caught_status(self):
        self.captured = not self.captured
        self.save()
