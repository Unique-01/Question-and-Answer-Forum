from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

class Question(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    topic = models.CharField(max_length=500)
    slug = models.SlugField()
    content = RichTextField(null=True, blank=True)

    #  to auto generate the slug from the topic
    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        super(Question, self).save(*args, **kwargs)

    class Meta:
        verbose_name = ("question")
        verbose_name_plural = ("questions")

    def __str__(self):
        return self.topic

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk})


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    date_posted = models.DateTimeField(auto_now_add=True)
    answer = RichTextField('Your Answer', null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True )

    def __str__(self):
        return f"{self.answer} by {self.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to="img/", null=True, blank=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    bio = RichTextField('About me', null=True, blank=True)
    location = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.user.username
