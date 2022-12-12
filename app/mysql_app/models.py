from django.db import models

# Create your models here.

class Instance(models.Model):
    name = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=200,null=True)
    domain = models.CharField(max_length=200, null=True)
    log_file_path = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return (self.name)

class QueryData(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, blank=True, null=True)
    count = models.PositiveIntegerField()
    time = models.FloatField(default=0)
    lock = models.FloatField(max_length=64)
    rows = models.FloatField(max_length=64)
    host = models.CharField(max_length=200)
    slow_query = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return (self.slow_query[:20])