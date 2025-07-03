import uuid
from django.db import models
from django.contrib.auth import get_user_model

class URL(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=8, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)

    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='urls',
        default=1
    )

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url[:50]}"