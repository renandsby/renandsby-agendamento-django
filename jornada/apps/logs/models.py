from django.db import models


class RequestLog(models.Model):
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        editable= False
    )
    
    user = models.ForeignKey(
        'custom_auth.CustomUser', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        editable= False,
    )
    username = models.CharField(
        "username",
        max_length=30,
        blank=True,
        null=True,
    )
    ip = models.CharField(
        "ip",
        max_length=30,
        blank=True,
        null=True, 
        editable= False,
    )
    path = models.CharField(
        "path",
        max_length=1054,
        blank=True,
        null=True, 
        editable= False,
    )
    method = models.CharField(
        "method",
        max_length=10,
        blank=True,
        null=True, 
        editable= False,
    )
    response_time = models.FloatField(
        "response_time",
        editable= False,
    )
    message = models.TextField(
        verbose_name='message',
        blank=True,
        null=True,  
        editable= False,
    )
    
    
    def __str__(self):
        return f"{self.timestamp}: {self.username}({self.ip}) {self.method}-{self.path}: {self.message}"

    class Meta:
        verbose_name_plural = "Request Logs"
        verbose_name = "Request Log"