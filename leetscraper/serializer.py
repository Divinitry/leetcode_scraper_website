from django.contrib.auth.models import User
from rest_framework import serializers
from .models import LeetCodeQuestion, QuestionNotes, CodeSolution

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class QuestionNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionNotes
        fields = ['id', 'title', 'body']

class CodeSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSolution
        fields = '__all__'

class LeetCodeQuestionSerializer(serializers.ModelSerializer):
    notes = QuestionNotesSerializer(many=True, read_only=True)

    class Meta:
        model = LeetCodeQuestion
        fields = ['id', 'question_title', 'title_slug', 'difficulty', 'hints', 'companies', 'topics', 'similar_questions', 'code_stubs', 'body', 'is_paid_only', 'created_at' ,'notes' ]
