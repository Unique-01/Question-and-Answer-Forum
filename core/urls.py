from core import views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('',views.QuestionList.as_view(),name='home'),
    path('addquestion/',views.QuestionFormView.as_view(),name='question_form'),
    path('profile/',views.profile, name='profile'),
    # path('hello/<in/',views.Update_pro, name='profile'),
    path('<slug:slug>/',views.question_detail,name='question_detail'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
