from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('list/', views.board_list, name = 'board_list'),
    path('write/', views.board_write, name = 'board_write'),
    path('new/', views.new, name="new"),
    path('detail/<int:id>/', views.board_detail, name="board_detail"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('update/<int:id>', views.update, name="update"),
    path('delete/<int:id>', views.delete, name="delete"),
    # 댓글 crud
    path('<int:board_id>/create_comment', views.create_comment, name="create_comment"),
    path('<int:comment_id>/edit_comment', views.edit_comment, name="edit_comment"),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('<int:comment_id>/update_comment', views.update_comment, name="update_comment"),
]