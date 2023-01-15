from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import QuestionForm, AnswerForm
from ..models import Question, Answer

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo answer registration
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            # return redirect('pybo:detail', question_id=question.id)
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
        # return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "No authority of modify")
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer=form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            # return redirect('pybo:detail', question_id = answer.question.id)
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer':answer, 'form':form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "No autholity of Delete")
        # return redirect('pybo:detail', question_id=answer.question.id)
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)
    # return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, 'You can not vote by yourslef.')
    else:
        answer.voter.add(request.user)
    # return redirect('pybo:detail', question_id=answer.question.id)
    return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))