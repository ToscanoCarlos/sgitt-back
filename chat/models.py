from django.db import models
from django.conf import settings

class Conversation(models.Model):
    name = models.CharField(max_length=255, blank=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    is_group = models.BooleanField(default=False)
    
    def clean(self):
        if self.is_group and self.participants.count() > 7:  # ejemplo de límite
            return print('Un grupo no puede tener más de 7 participantes')
        
    def mark_all_read_for_user(self, user):
        self.messages.exclude(read_by=user).update(read_by=user)
    
    def get_participants(self):
        """Método auxiliar para obtener participantes"""
        return self.participants.all()
    
    def is_participant(self, user):
        """Método auxiliar para verificar si un usuario es participante"""
        return self.participants.filter(id=user.id).exists()
    
    def __str__(self):
        if self.is_group:
            return self.name
        return f"Conversation between {', '.join(user.email for user in self.participants.all())}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='read_messages', blank=True)
    
    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['conversation', 'timestamp']),
        ]
    
    def mark_as_read(self, user):
        """
        Marca el mensaje como leído por un usuario específico
        """
        if user not in self.read_by.all():
            self.read_by.add(user)
    
    def is_read_by(self, user):
        return self.read_by.filter(id=user.id).exists()