from rest_framework import serializers
from .models import ToDoList, LeetCodeQuestion, QuestionNotes, CodeSolution

class QuestionNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionNotes
        fields = '__all__'

class CodeSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSolution
        fields = '__all__'

class LeetCodeQuestionSerializer(serializers.ModelSerializer):
    notes = QuestionNotesSerializer(many=True, read_only=True)

    class Meta:
        model = LeetCodeQuestion
        fields = '__all__'

class ToDoListSerializer(serializers.ModelSerializer):
    questions = LeetCodeQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = ToDoList
        fields = '__all__'
