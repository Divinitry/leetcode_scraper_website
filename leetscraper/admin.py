from django.contrib import admin
from .models import LeetCodeQuestion, CodeSolution, QuestionNotes

# Register your models here.
admin.site.register(LeetCodeQuestion)
admin.site.register(CodeSolution)
admin.site.register(QuestionNotes)
