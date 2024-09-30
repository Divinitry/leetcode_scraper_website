from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
    
class LeetCodeQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=225, default="No question provided")
    title_slug = models.CharField(max_length=225, default="No title slug provided")
    difficulty = models.CharField(max_length=50, default="No difficulty provided")
    hints = models.JSONField(default=list) 
    companies = models.TextField(blank=True, default="No companies provided")  
    topics = models.JSONField(default=list)
    similar_questions = models.TextField(blank=True, default="No similar questions provided")  
    code_stubs = models.TextField(blank=True, default="No code_stubs provided") 
    body = models.TextField(default="No Body Provided")  
    is_paid_only = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.question_title} - {self.difficulty}"
    
class CodeSolution(models.Model):
    leetcodequestion = models.ForeignKey(LeetCodeQuestion, on_delete=models.CASCADE, related_name='solutions', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    chatgpt_response = models.TextField()
    ratings = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Solution by {self.user.username} at {self.created_at}'

class QuestionNotes(models.Model):
    leetcodequestion = models.ForeignKey(LeetCodeQuestion, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="Untitled")
    body = models.TextField(blank=True, default="Click to add")

    def __str__(self):
        return f"{self.title} - {self.body}"
