from django.db import models
from users.models import CustomUser
from career.models import CareerPath

class Recommendation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recommendations')
    career_path = models.ForeignKey(CareerPath, on_delete=models.CASCADE)
    recommended_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.career_path.name}"
