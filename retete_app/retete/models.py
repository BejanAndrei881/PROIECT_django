from django import forms
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Categorie(models.Model):
    objects = None
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipient(models.Model):
    objects = None
    title = models.CharField(max_length=255)
    descriere = models.TextField()
    incrediente = models.TextField()
    instructiuni = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    is_private = models.BooleanField(default=False)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    imagine = models.ImageField(upload_to='retete_imagini/', null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class SavedRecipient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    date_saved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} a salvat {self.recipe.title}"
