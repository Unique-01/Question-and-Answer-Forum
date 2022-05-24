from core import views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.question_list, name='home'),
    path('addquestion/', views.QuestionFormView.as_view(), name='question_form'),
    path('profile/', views.profile_update, name='profile_update'),
    path('delete/<slug>', views.QuestionDelete.as_view(), name='delete_question'),
    path('update_question/<id>', views.question_update, name='update_question'),
    path('delete_answer/<pk>', views.AnswerDelete.as_view(), name='delete_answer'),
    path('users/<username>/', views.profile, name='profile'),
    path('users/', views.user_list, name='users'),
    path('<slug:slug>/', views.question_detail, name='question_detail'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
