from django.urls import path
from .views import (
    get_todolist, 
    add_leetcode_question, 
    remove_leetcode_question, 
    show_leetcode_question,
    create_note, 
    get_note, 
    update_note, 
    delete_note
)

urlpatterns = [
    path('todolist/', get_todolist, name='get_todolist'),
    path('todolist/questions/add/', add_leetcode_question, name='add_leetcode_question'),
    path('todolist/questions/remove/<int:question_id>/', remove_leetcode_question, name='remove_leetcode_question'),
    path('todolist/questions/<int:question_id>/', show_leetcode_question, name='show_leetcode_question'),
    path('todolist/questions/<int:question_id>/notes/create/', create_note, name='create_note'),
    path('todolist/questions/<int:question_id>/notes/<int:note_id>/', get_note, name='get_note'),
    path('todolist/questions/<int:question_id>/notes/<int:note_id>/update/', update_note, name='update_note'),
    path('todolist/questions/<int:question_id>/notes/<int:note_id>/delete/', delete_note, name='delete_note'),
]
