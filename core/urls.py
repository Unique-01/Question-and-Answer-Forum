from core import views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.question_list, name='home'),
    path('ask_question/', views.QuestionFormView.as_view(), name='question_form'),
    path('profile/', views.profile_update, name='profile_update'),
    path('delete_question/<slug>/<pk>', views.QuestionDelete.as_view(), name='delete_question'),
    path('update_question/<id>', views.question_update, name='update_question'),
    path('delete_answer/<pk>', views.AnswerDelete.as_view(), name='delete_answer'),
    path('update_answer/<id>',views.answer_update,name='update_answer'),
    path('users/<username>/', views.profile, name='profile'),
    path('users/', views.user_list, name='users'),
    path('<slug:slug>/<pk>', views.question_detail, name='question_detail'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
