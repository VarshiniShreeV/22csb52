import string
import random
from datetime import timedelta

from django.db import models
from django.utils import timezone


def generate_shortcode(length=6):
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choices(alphabet, k=length))


class ShortURL(models.Model):
    original_url = models.URLField()
    shortcode = models.CharField(max_length=15, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    validity_minutes = models.PositiveIntegerField(default=30)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.shortcode:
            for _ in range(10): 
                candidate = generate_shortcode()
                if not self.__class__.objects.filter(shortcode=candidate).exists():
                    self.shortcode = candidate
                    break
            else:
                raise ValueError("Unable to generate a unique shortcode. Try again.")
            
        if not self.expires_at:
            now = timezone.now()
            self.expires_at = now + timedelta(minutes=self.validity_minutes)

        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"{self.shortcode} -> {self.original_url}"
