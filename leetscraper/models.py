from django.db import models

# Create your models here.
class LeetCodeQuestion(models.Model): # update this according to what we want saved in the database
    question_title = models.CharField(max_length=225)
    difficulty = models.CharField(max_length=50)
    description = models.TextField()
    url = models.URLField()
    # set up foreignkey here and connect it to the ToDoList class

    def __str__(self):
        return f"{self.question_title} - {self.difficulty} - {self.description} - {self.url}"

class ToDoList(models.Model):
    list_name = models.CharField(max_length=30)
    list_description = models.CharField(max_length=200)
    created_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_time}"
