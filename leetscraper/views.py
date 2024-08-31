from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ToDoList, LeetCodeQuestion, QuestionNotes
from .serializer import ToDoListSerializer, LeetCodeQuestionSerializer, QuestionNotesSerializer

@api_view(['GET'])
def get_todolist(request):
    try:
        todolist = ToDoList.objects.get(id=1, user=request.user)
        serializer = ToDoListSerializer(todolist)
        return Response(serializer.data)
    except ToDoList.DoesNotExist:
        return Response({"error": "ToDoList not found"}, status=status.HTTP_404_NOT_FOUND)   

@api_view(['POST'])
def add_leetcode_question(request):
    try:
        todolist = ToDoList.objects.get(id=1, user=request.user)
    except ToDoList.DoesNotExist:
        return Response({"error": "ToDoList not found"}, status=status.HTTP_404_NOT_FOUND)
    
    question_title = request.data.get('question_title')
    title_slug = request.data.get('title_slug') 

    if LeetCodeQuestion.objects.filter(todolist=todolist, title_slug=title_slug, user=request.user).exists():
        return Response({"error": "LeetCodeQuestion already exists in the To Do List"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = LeetCodeQuestionSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(todolist=todolist, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def remove_leetcode_question(request, question_id):
    try:
        todolist = ToDoList.objects.get(id=1, user=request.user)
    except ToDoList.DoesNotExist:
        return Response({"error": "ToDoList not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        leetcode_question = LeetCodeQuestion.objects.get(id=question_id, todolist=todolist, user=request.user)
        leetcode_question.delete()
        return Response({"message": "LeetCodeQuestion deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except LeetCodeQuestion.DoesNotExist:
        return Response({"error": "LeetCodeQuestion not found"}, status=status.HTTP_404_NOT_FOUND)
 
@api_view(['GET'])
def show_leetcode_question(request, question_id):
    try:
        leetcode_question = LeetCodeQuestion.objects.get(id=question_id, user=request.user)
        serializer = LeetCodeQuestionSerializer(leetcode_question)
        return Response(serializer.data)
    except LeetCodeQuestion.DoesNotExist:
        return Response({"error": "LeetCodeQuestion not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_note(request, question_id):
    try:
        leetcode_question = LeetCodeQuestion.objects.get(id=question_id, user=request.user)
    except LeetCodeQuestion.DoesNotExist:
        return Response({"error": "LeetCodeQuestion not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QuestionNotesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(leetcodequestion=leetcode_question, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_note(request, note_id):
    try:
        note = QuestionNotes.objects.get(id=note_id, user=request.user)
        serializer = QuestionNotesSerializer(note)
        return Response(serializer.data)
    except QuestionNotes.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_note(request, note_id):
    try:
        note = QuestionNotes.objects.get(id=note_id, user=request.user)
    except QuestionNotes.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QuestionNotesSerializer(note, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_note(request, note_id):
    try:
        note = QuestionNotes.objects.get(id=note_id, user=request.user)
        note.delete()
        return Response({"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except QuestionNotes.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)