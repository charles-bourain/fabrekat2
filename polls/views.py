from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Question, Choice

class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name= 'latest_question_list'
    
    def get_queryset(self):
        ##Returns the last five published questions
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        
class DetailView(generic.DetailView):
    model=Question
    template_name='polls/detail.html'
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
        
    
class ResultsView(generic.DetailView):
    model=Question
    template_name='polls/results.html'

def vote(request, question_id): #passes in request and question Id
    p=get_object_or_404(Question, pk=question_id) #pulls object from question_id in Question Dictionary.
    try:
        selected_choice=p.choice_set.get(pk=request.POST['choice']) #returns requested Choice
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question':p,
            'error_message':"You didn't Select a Choice",
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(p.id,))) #always perform a redirect after dealing with a POST.  POST changes serverside object.  #reverse allows us to not hard-code URL into the code.  the ':' will be replaced with 'p.id', and display the correct results for the associated question for p.id.  IE URL will be polls/p.id/results.







#def index(request):
#    return HttpResponse("Hello, world.  You're at the polls index.")
    
#def detail(request, question_id):
#    question=get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/detail.html', {'question':question})
    
#def results(request, question_id):
#    question=get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/results.html', {'question':question})

#def index(request):
#    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
#    context={'latest_question_list': latest_question_list}
#    return render(request, 'polls/index.html', context)
