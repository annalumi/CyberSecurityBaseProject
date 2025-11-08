from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Security flaw no 1 Broken Access Control:
#from django.views.decorators.http import require_POST
# Security flaw no 3 Sofware and Data Integrity Failures:
# from django.db.models import F
# Security flaw no 4 Identification and Authentication Failures:  
# from django.contrib.auth.decorators import login_required
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# Security flaw no 1 Broken Access Control:
#def get_queryset(self):
 #       return Question.objects.filter(pub_date__lte=timezone.now())

#@require_POST


# Security flaw no 4 Identification and Authentication Failures:  
#@login_required

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # Security flaw number 5 Insecure Design:
    #voted_questions = request.session.get('voted_questions', [])
    #if question_id in voted_questions:
    #    return render(request, 'polls/detail.html', {
    #        'question': question,
    #        'error_message': "You have already voted on this question.",
     #   })
    # Security flaw no 1 Broken Access Control:
    # question = get_object_or_404(
     #   Question, pk=question_id, pub_date__lte=timezone.now()
    #)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Security flaw no 3 Sofware and Data Integrity Failures:
        # selected_choice.votes = F('votes') + 1
        # selected_choice.save()
    # Security flaw number 5 Insecure Design:    
     #   voted_questions.append(question_id)
      #  request.session['voted_questions'] = voted_questions

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))