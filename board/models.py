from django.db import models
from django.shortcuts import reverse

class Post(models.Model):

    title = models.CharField(max_length=30)
    content = models.TextField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_at',)
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("board:detail", kwargs={"pk": self.pk})
    
