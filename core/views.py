from django.shortcuts import get_object_or_404, render,redirect,HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.views import generic
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
# Create your views here.

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request,f"your Account has beeen created successfully!")
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


#  Question list display
class QuestionList(generic.ListView):
    template_name = 'index.html/'

    # search bar
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = Question.objects.filter(topic__icontains=query) or Question.objects.filter(description__icontains=query)
        else:
            object_list = Question.objects.all().order_by('-date_posted')
        return object_list

# add question form
class QuestionFormView(generic.FormView):
    template_name = 'question_form.html/'
    form_class = QuestionForm
    success_url = "/"

    def form_valid(self, form):
        # to link the user with the question
        form.instance.user = self.request.user
        # to save the form
        form.save()
        return super().form_valid(form)


# queetion detail
def question_detail(request,slug):
    template_name = 'question_detail.html/'
    question = get_object_or_404(Question,slug=slug)
    answers = question.answers.all()
    new_answer = None

    if request.method =="POST":
        answer_form = AnswerForm(request.POST,request.FILES)

        if answer_form.is_valid():
            new_answer = answer_form.save(commit=False)
            # to link the answer to the question
            new_answer.question= question
            # to link the user with the answer
            new_answer.user = request.user;
            # to save the answer to the database
            new_answer.save()
            # to print out empty form after saving
            answer_form = AnswerForm()


    
    else:
        answer_form = AnswerForm()

    return render (request,template_name,{  'question': question,
                                            'answers': answers,
                                            'new_answer': new_answer,
                                            'answer_form': answer_form})

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST,instance= request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Your Account has been updated")
            return redirect('/')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile.html', context)

