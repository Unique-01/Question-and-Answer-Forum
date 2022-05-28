from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.views import generic
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your views here.

""" Users Attributes and registration"""


############### User Signup View ################
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(
                request, f"Your Account has been created successfully!")
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


############### User Lists View ################
def user_list(request):
    # User = get_user_model().objects.all
    users = User.objects.all()
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query)
    return render(request, 'users.html', {'users': users})


############### users profile ################
def profile(request, username):
    user = User.objects.get(username=username)
    query = request.GET.get('tab')
    question_obj = ''
    answer_obj = ''
    page = None
    page_obj = None
    if query == 'question':
        question_obj = Question.objects.filter(
            user=user).order_by('-date_posted')
        answer_obj = ''
        # user questions pagination
        page = Paginator(question_obj, 10)
        page_number = request.GET.get('page')
        page_obj = page.get_page(page_number)
    elif query == 'answer':
        question_obj = ''
        answer_obj = Answer.objects.filter(user=user).order_by('-date_posted')
        # user answers pagination
        page = Paginator(answer_obj, 10)
        page_number = request.GET.get('page')
        page_obj = page.get_page(page_number)

    context = {'user': user, 'question_obj': question_obj,
               'answer_obj': answer_obj, 'page_obj': page_obj}
    return render(request, 'profile.html', context)


############### User profile update ################
@login_required
def profile_update(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Profile has been updated")
            return redirect('profile', request.user.username)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile_update.html', context)


"""
    Question Attributes
"""


############### Question Lists Display ################
def question_list(request):
    questions = Question.objects.all().order_by('-date_posted')
    query = request.GET.get('q')
    question_list = Question.objects.all().order_by('-date_posted')
    if query:
        question_list = Question.objects.filter(
            topic__icontains=query) or Question.objects.filter(content__icontains=query)
    else:
        question_list = Question.objects.all().order_by('-date_posted')

    page = Paginator(question_list, 10)
    page_number = request.GET.get('page')
    page_obj = page.get_page(page_number)

    return render(request, 'index.html', {'questions': questions, 'question_list': question_list, 'page_obj': page_obj})


############### Question Create Form ################
class QuestionFormView(generic.FormView):
    template_name = 'question_form.html/'
    form_class = QuestionForm
    success_url = "/"

    def form_valid(self, form):
        # to link the user with the question
        form.instance.user = self.request.user
        # to save the form
        form.save()
        messages.success(self.request,
                         f"Your question has been posted successfully!")
        return super().form_valid(form)


############### Question detail ################
def question_detail(request, slug, pk):
    template_name = 'question_detail.html/'
    question = get_object_or_404(Question, slug=slug, pk=pk)
    answers = question.answers.all()
    new_answer = None

    if request.method == "POST":
        answer_form = AnswerForm(request.POST, request.FILES)

        if answer_form.is_valid():
            new_answer = answer_form.save(commit=False)
            # to link the answer to the question
            new_answer.question = question
            # to link the user with the answer
            new_answer.user = request.user
            # to save the answer to the database
            new_answer.save()
            messages.success(request, "Your answer has been posted")
            # to print out empty form after saving
            answer_form = AnswerForm()

    else:
        answer_form = AnswerForm()

    return render(request, template_name, {'question': question,
                                           'answers': answers,
                                           'new_answer': new_answer,
                                           'answer_form': answer_form})


############### Question Update Form ################
@login_required
def question_update(request, id):
    obj = get_object_or_404(Question, id=id)
    update_form = QuestionForm(request.POST or None, instance=obj)
    context = {'update_form': update_form,'obj':obj}

    if update_form.is_valid():
        obj = update_form.save(commit=False)

        obj.save()

        messages.success(request, "Question Updated Successfully")

        return redirect('question_detail', obj.slug, obj.pk)

    else:
        context = {'update_form': update_form,
                   'error': 'The form was not updated successfully. Please enter in a title and content','obj':obj}
    return render(request, 'question_update.html', context)


############### Question Delete ################
class QuestionDelete(generic.DeleteView):
    model = Question
    success_url = '/'
    template_name = 'question_delete.html'

    def form_valid(self, form):
        messages.success(self.request, "Question has been deleted")


############### Answer Delete ################
class AnswerDelete(generic.DeleteView):
    model = Answer
    success_url = '/'
    template_name = 'answer_delete.html'

    def form_valid(self, form):
        messages.success(self.request, "Answer has been deleted")


############ Answer Update #############
@login_required
def answer_update(request, id):
    obj = get_object_or_404(Answer, id=id)
    update_form = AnswerForm(None, instance=obj)
    if request.method == 'POST':
        update_form = AnswerForm(request.POST or None, instance=obj)

        if update_form.is_valid:
            obj = update_form.save(commit=False)

            obj.save()

            messages.success(request, "Answer has been Updated Successfully")

            return redirect('question_detail', obj.question.slug, obj.question.pk)
        else:
            messages.error(request, "Answer not updated")

    context = {'update_form': update_form ,'obj':obj}

    return render(request, 'answer_update.html', context)
