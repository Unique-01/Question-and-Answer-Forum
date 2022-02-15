from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    topic = models.CharField( max_length=300)
    description = models.TextField()
    slug = models.SlugField()
    image_description = models.CharField(max_length=300,blank=True)
    image = models.ImageField( upload_to="img", height_field=None, width_field=None, max_length=None, blank=True)
    another_image_description = models.CharField(max_length=300, blank=True)
    another_image = models.ImageField( upload_to="img", height_field=None, width_field=None, max_length=None, blank=True)
    other_image_description = models.CharField(max_length=300, blank=True)
    other_image = models.ImageField( upload_to="img", height_field=None, width_field=None, max_length=None, blank=True)

    #  to auto generate the slug from the topic
    def save(self,*args, **kwargs):
        self.slug = slugify(self.topic)
        super(Question,self).save(*args, **kwargs)

   
    class Meta:
        verbose_name = ("question")
        verbose_name_plural = ("questions")

    def __str__(self):
        return self.topic

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk})

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    email = models.EmailField(max_length=254)
    answer = models.TextField()
    image = models.ImageField( upload_to="img/", height_field=None, width_field=None, max_length=None, blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"{self.answer} by {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    image = models.ImageField(upload_to="img/",null=True,blank=True)
    bio = models.TextField(null=True,blank=True,default="Not ")

    def __str__(self):
        return self.user.username