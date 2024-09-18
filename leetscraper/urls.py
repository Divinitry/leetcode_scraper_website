from django.urls import path
from .views import (
    add_leetcode_question, 
    remove_leetcode_question, 
    show_leetcode_question,
    create_note, 
    get_note, 
    update_note, 
    delete_note,
    get_codesolution,
    create_codesolution,
    delete_codesolution,
    send_and_getsearchinfo,
    get_user_questions
)

urlpatterns = [
    path('todolist/questions/add/', add_leetcode_question, name='add_leetcode_question'),
    path('todolist/questions/all/', get_user_questions, name='get_user_questions'),
    path('todolist/questions/remove/<int:question_id>/', remove_leetcode_question, name='remove_leetcode_question'),
    path('todolist/questions/<int:question_id>/', show_leetcode_question, name='show_leetcode_question'),
    path('todolist/questions/<int:question_id>/notes/create/', create_note, name='create_note'),
    path('todolist/questions/<int:question_id>/notes/', get_note, name='get_note'),
    path('todolist/questions/<int:question_id>/notes/<int:note_id>/update/', update_note, name='update_note'),
    path('todolist/questions/<int:question_id>/notes/<int:note_id>/delete/', delete_note, name='delete_note'),
    path('todolist/questions/<int:question_id>/codesolutions/', get_codesolution, name='get_codesolution'),
    path('todolist/questions/<int:question_id>/codesolutions/create/', create_codesolution, name='create_codesolution'),
    path('todolist/questions/<int:question_id>/codesolutions/<int:code_id>/delete/', delete_codesolution, name='delete_codesolution'),
    path('api/search/<str:search_string>', send_and_getsearchinfo, name='send_and_getsearchinfo')
]

