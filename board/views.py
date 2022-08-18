from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.models import User

# Create your views here.



def board_list(request) :
    boards = Board.objects.filter().order_by('-created_at')
    paginator = Paginator(boards,10)
    pagnum = request.GET.get('page')
    boards = paginator.get_page(pagnum)
    
    return render(request, 'board/board_list.html',{'boards':boards})


def board_detail(request, id):
    board = get_object_or_404(Board, pk = id)
    all_comments = board.comments.all().order_by('-created_at')
    return render(request, 'board/board_detail.html', {'board':board,'comments':all_comments})
    
def new(request) :
    return render(request, 'board/board_write.html')


def board_write(request):
    new_board = Board()
    new_board.title = request.POST['title']
    new_board.writer = request.user
    new_board.created_at = timezone.now()
    new_board.contents = request.POST['contents']
    new_board.save()

    return redirect('board:board_detail', new_board.id)


def edit(request, id) :
    edit_board = Board.objects.get(id = id)
    return render(request, 'board/board_edit.html', {'board' : edit_board})

def update(request, id):
    update_board = Board.objects.get(id=id)
    update_board.title = request.POST['title']
    update_board.writer = request.user
    update_board.updated_at = timezone.now()
    update_board.contents = request.POST['contents']
    update_board.save()
    return redirect('board:board_detail', update_board.id)

def delete(request, id) :
    delete_board = Board.objects.get(id = id)
    delete_board.delete()
    return redirect('board:board_list')

def create_comment(request, board_id):
   new_comment = Comment()
   new_comment.writer = request.user
   new_comment.content = request.POST['content']
   new_comment.board = get_object_or_404(Board, pk = board_id)
   new_comment.save() 
   return redirect('board:board_detail', board_id)

def edit_comment(request, comment_id):
    edit_comment = Comment.objects.get(id = comment_id)
    return render(request, 'board/comment_edit.html', {'comment' : edit_comment})

def update_comment(request, comment_id):
    update_comment = get_object_or_404(Comment, pk = comment_id)
    update_comment.writer = request.user
    update_comment.content = request.POST['content']
    update_comment.save()
    return redirect('board:board_detail', update_comment.board.id)    

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return board_detail(request, comment.board.id)



 


