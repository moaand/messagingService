from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    date_accessed = models.DateTimeField(null=True)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    content = models.CharField(max_length=1000)
    
    # This is an assumption that we don't want to be able to read 
    # old messages where the sender or receiver has been removed.
    sender =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='sentMessage')
    receiver =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="receivedMessage")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content