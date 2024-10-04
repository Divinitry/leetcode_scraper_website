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

def add_cors_headers(response):
    response["Access-Control-Allow-Origin"] = "https://leetscraper.netlify.app"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE, PUT"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response["Access-Control-Allow-Credentials"] = "true"
    return response

def handle_options_request(request):
    if request.method == 'OPTIONS':
        response = JsonResponse({'message': 'CORS preflight response'}, status=status.HTTP_200_OK)
        return add_cors_headers(response)
    return None 

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        try:
            user = serializer.save()
        except Exception as e:
            return Response({'error': f"Error during registration: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'OPTIONS'])
@permission_classes([AllowAny])
def check_login_status(request):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    try:
        response = Response({"is_logged_in": request.user.is_authenticated}, status=status.HTTP_200_OK)
        return add_cors_headers(response)
    except Exception as e:
        return Response({'error': f"Error during login status check: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def add_leetcode_question(request):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    try:
        question_title = request.data.get('question_title', '').strip()

        if LeetCodeQuestion.objects.filter(question_title__iexact=question_title, user=request.user).exists():
            return Response({'error': 'Question already in your to-do list'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['question_title'] = question_title

        serializer = LeetCodeQuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f"Error while adding question: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def get_user_questions(request):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    try:
        user_questions = LeetCodeQuestion.objects.filter(user=request.user).order_by('created_at')
        serializer = LeetCodeQuestionSerializer(user_questions, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': f"Error retrieving questions: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def remove_leetcode_question(request, question_id):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    try:
        leetcode_question = LeetCodeQuestion.objects.get(id=question_id, user=request.user)
        leetcode_question.delete()
        return Response({"message": "LeetCodeQuestion deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except LeetCodeQuestion.DoesNotExist:
        return Response({"error": "LeetCodeQuestion not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error while deleting question: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def show_leetcode_question(request, question_id):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    try:
        leetcode_question = LeetCodeQuestion.objects.get(id=question_id, user=request.user)
        serializer = LeetCodeQuestionSerializer(leetcode_question)
        return Response(serializer.data)
    except LeetCodeQuestion.DoesNotExist:
        return Response({"error": "LeetCodeQuestion not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error while fetching question: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def create_note(request, question_id):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    try:
        leetcode_question = LeetCodeQuestion.objects.get(id=question_id, user=request.user)
    except LeetCodeQuestion.DoesNotExist:
        return Response({"error": "LeetCodeQuestion not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuestionNotesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(leetcodequestion=leetcode_question, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def get_note(request, question_id):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    try:
        notes = QuestionNotes.objects.filter(leetcodequestion__id=question_id, user=request.user)
        serializer = QuestionNotesSerializer(notes, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": f"Error retrieving notes: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def update_note(request, question_id, note_id):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    try:
        note = QuestionNotes.objects.get(id=note_id, user=request.user)
    except QuestionNotes.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuestionNotesSerializer(note, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def delete_note(request, question_id, note_id):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    try:
        note = QuestionNotes.objects.get(id=note_id, user=request.user)
        note.delete()
        return Response({"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except QuestionNotes.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error while deleting note: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def get_codesolution(request, question_id):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    try:
        leetcode_question = LeetCodeQuestion.objects.get(id=question_id)
        code_solutions = CodeSolution.objects.filter(user=request.user, leetcodequestion=leetcode_question)
        serializer = CodeSolutionSerializer(code_solutions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except LeetCodeQuestion.DoesNotExist:
        return Response({'error': 'LeetCode question not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f"Error retrieving code solutions: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def create_codesolution(request, question_id):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

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
        return Response({'error': f"Error while creating code solution: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def delete_codesolution(request, code_id):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    try:
        code_solution = CodeSolution.objects.get(id=code_id, user=request.user)
        code_solution.delete()
        return Response({"message": "Solution deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except CodeSolution.DoesNotExist:
        return Response({"error": "Code solution not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error while deleting code solution: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def send_and_getsearchinfo(request, search_string):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    if not search_string:
        return JsonResponse({"error": "No search string provided"}, status=400)

    try:
        data = get_leetscrape_data(search_string)

        if "error" in data:
            return JsonResponse(data, status=404)

        return JsonResponse(data, status=200)
    
    except Exception as e:
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)

@api_view(['POST', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def get_gptfeedback(request):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

    try:
        data = request.data
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

@api_view(['POST', 'OPTIONS'])
@permission_classes([IsAuthenticated])
def get_starter_code(request):
    options_response = handle_options_request(request)
    if options_response:
        return options_response

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
