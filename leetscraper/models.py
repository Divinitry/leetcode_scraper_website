from django.db import models
from django.contrib.auth.models import User

class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, default="To Code List")
    created_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_time}"
    
class LeetCodeQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    question_title = models.CharField(max_length=225, default="No question provided")
    title_slug = models.CharField(max_length=225, default="No title slug provided")
    difficulty = models.CharField(max_length=50, default="No difficulty provided")
    hints = models.TextField(blank=True, default="No hints provided") 
    companies = models.TextField(blank=True, default="No companies provided")  
    topics = models.TextField(blank=True, default="No topics provided") 
    similar_questions = models.TextField(blank=True, default="No similar questions provided")  
    code_stubs = models.TextField(blank=True, default="No code_stubs provided") 
    body = models.TextField(default="No Body Provided")  
    is_paid_only = models.BooleanField(default=False)
    completion = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question_title} - {self.difficulty}"
    
class CodeSolution(models.Model):
    leetcodequestion = models.ForeignKey(LeetCodeQuestion, on_delete=models.CASCADE, related_name='solutions', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    code = models.TextField()
    chatgpt_response = models.TextField()
    ratings = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Solution by {self.user.username} at {self.created_at}'

class QuestionNotes(models.Model):
    leetcodequestion = models.ForeignKey(LeetCodeQuestion, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50)
    body = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.body}"
