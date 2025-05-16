from django.db import models

class Temple(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    deity = models.CharField(max_length=100)
    architecture_style = models.CharField(max_length=100)
    historical_significance = models.TextField()
    built_in = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='temples/', blank=True, null=True)
    is_world_heritage_site = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name}, {self.location}"

    class Meta:
        ordering = ['name']