from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import LeetCodeQuestion, QuestionNotes, CodeSolution
from .serializer import LeetCodeQuestionSerializer, QuestionNotesSerializer, CodeSolutionSerializer, UserSerializer
from .services.leetscrape_api import get_leetscrape_data
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework import generics
from .services.chatgpt_api import get_feedback, get_start_code

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_leetcode_question(request):
    question_title = request.data.get('question_title')
    
    if LeetCodeQuestion.objects.filter(question_title=question_title, user=request.user).exists():
        return Response({'error': 'Question already in your to do list'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = LeetCodeQuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_questions(request):
    user_questions = LeetCodeQuestion.objects.filter(user=request.user)
    
    serializer = LeetCodeQuestionSerializer(user_questions, many=True)
    
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_leetcode_question(request, question_id):
    try:
        leetcode_question = LeetCodeQuestion.objects.get(id=question_id, user=request.user)
        leetcode_question.delete()
        return Response({"message": "LeetCodeQuestion deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except LeetCodeQuestion.DoesNotExist:
        return Response({"error": "LeetCodeQuestion not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_leetcode_question(request, question_id):
    try:
        leetcode_question = LeetCodeQuestion.objects.get(id=question_id, user=request.user)
        serializer = LeetCodeQuestionSerializer(leetcode_question)
        return Response(serializer.data)
    except LeetCodeQuestion.DoesNotExist:
        return Response({"error": "LeetCodeQuestion not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def get_note(request, question_id):
    try:
        notes = QuestionNotes.objects.filter(leetcodequestion__id=question_id, user=request.user)
        serializer = QuestionNotesSerializer(notes, many=True)
        return Response(serializer.data)
    except QuestionNotes.DoesNotExist:
        return Response({"error": "No notes found for this question"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_note(request, question_id, note_id):
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
@permission_classes([IsAuthenticated])
def delete_note(request, question_id, note_id):
    try:
        note = QuestionNotes.objects.get(id=note_id, user=request.user)
        note.delete()
        return Response({"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except QuestionNotes.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_codesolution(request, question_id):
    try:
        leetcode_question = LeetCodeQuestion.objects.get(id=question_id)
        code_solutions = CodeSolution.objects.filter(user=request.user, leetcodequestion=leetcode_question)
        serializer = CodeSolutionSerializer(code_solutions, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except LeetCodeQuestion.DoesNotExist:
        return Response({'error': 'LeetCode question not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_codesolution(request, question_id):
    try:
        leetcode_question = LeetCodeQuestion.objects.get(id=question_id)
        
        code_solution = CodeSolution.objects.create(
            user=request.user,
            leetcodequestion=leetcode_question, 
            code=request.data.get('code'),
            chatgpt_response=request.data.get('chatgpt_response'),
            ratings=request.data.get('ratings')
        )
        
        serializer = CodeSolutionSerializer(code_solution)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except LeetCodeQuestion.DoesNotExist:
        return Response({'error': 'LeetCode question not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_codesolution(request, code_id):
    try:
        code_solution = CodeSolution.objects.get(id=code_id, user=request.user)
        code_solution.delete()
        return Response({"message": "Solution deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except CodeSolution.DoesNotExist:
        return Response({"error": "Code solution not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def send_and_getsearchinfo(request, search_string):
    print(f"Received search string: {search_string}")
    
    if not search_string:
        return JsonResponse({"error": "No search string provided"}, status=400)

    try:
        data = get_leetscrape_data(search_string)
        print(f"Data fetched: {data}")

        if "error" in data:
            return JsonResponse(data, status=404)

        return JsonResponse(data, status=200)
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_gptfeedback(request):
    try:
        data = request.data

        # .get lets you retrieve the value within a key value pair (dictionary) by calling the key super useful

        leetcode_question = data.get('question_title') 
        leetcode_question_topics = data.get('question_topics')
        user_code = data.get('user_code') 

        feedback, rating = get_feedback(leetcode_question, user_code, leetcode_question_topics)
        return Response({
            "feedback": feedback,
            "rating": rating
        }, status=200)
    except Exception as e: 
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_starter_code(request):
    try:
        code_body = request.data

        javascript_startercode, typescript_startercode, python_startercode, java_startercode, csharp_startercode = get_start_code(code_body)

        return Response({
            "javascript_starter_code": javascript_startercode,
            "typescript_starter_code": typescript_startercode,
            "python_starter_code": python_startercode,
            "java_starter_code": java_startercode,
            "csharp_starter_code": csharp_startercode,
        }, status=200)

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)
    