from django.db import models
from django.conf import settings

class CaseStudy(models.Model):
    title = models.CharField(max_length=200)
    client = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='case_studies/')
    is_featured = models.BooleanField(default=False)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Case Studies"

    def __str__(self):
        return self.title
