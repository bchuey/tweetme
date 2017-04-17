import re

from django.conf import settings
# from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone


from hashtags.signals import parsed_hashtags

from .validators import validate_content



# Create your models here.


# custom validation function
# typicall put this in validators.py file

# def validate_content(value):
#     content = value
#     if content == 'abc':
#         raise ValidationError('Content cannot be ABC')
#
#     return value

# Tweet Manager
class TweetManager(models.Manager):
    def retweet(self, user, parent_obj):

        # if you retweet a retweet,
        # grab the very first/original
        # tweet
        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj

        qs = self.get_queryset().filter(
                user=user,
                parent=og_parent
                ).filter(
                timestamp__year=timezone.now().year,
                timestamp__month=timezone.now().month,
                timestamp__day=timezone.now().day,
                reply=False,
                )
        if qs.exists():
            return None

        obj = self.model(
                parent = og_parent,
                user = user,
                content = parent_obj.content,

            )

        obj.save()
        return obj

    def like_toggle(self, user, tweet_obj):
        # add the individual
        if user in tweet_obj.liked.all():
            is_liked = False
            tweet_obj.liked.remove(user)
        else:
            is_liked = True
            tweet_obj.liked.add(user)

        return is_liked

class Tweet(models.Model):

    # user association
    # everytime a tweet happens
    # must be associated w/ a user
    parent = models.ForeignKey("self", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.CharField(max_length=140, validators=[validate_content])
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    reply = models.BooleanField(verbose_name="Is a reply?", default=False)
    updated = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    objects = TweetManager()

    # how to describe to the admin
    def __str__(self):

        return str(self.content)


    def get_absolute_url(self):
        return reverse('tweet:detail', kwargs={'pk':self.pk})

    class Meta:
        ordering = ['-timestamp','content']

    # validation
    # first validation called
    # anytime a model is first saved

    # def clean(self, *args, **kwargs):
    #
    #     contet = self.content
    #     if content == 'abc':
    #         raise ValidationError('Cannot be ABC')
    #
    #     # return the default
    #     return super(Tweet,self).clean(*args,**kwargs)
    def get_parent(self):
        the_parent = self
        if self.parent:
            the_parent = self.parent
        return the_parent

    def get_children(self):
        parent = self.get_parent()
        qs = Tweet.objects.filter(parent=parent)
        qs_parent = Tweet.objects.filter(pk=parent.pk)
        return (qs | qs_parent)

def tweet_save_receiver(sender,instance,created,*args,**kwargs):
    if created and not instance.parent:
        user_regex = r'@(?P<username>[\w.@+-]+)'
        usernames = re.findall(user_regex, instance.content)
        # if m:
        #     username = m.group("username")
            # send notification to user here

        hashtag_regex = r'#(?P<hashtag>[\w\d-]+)'
        hashtags = re.findall(hashtag_regex, instance.content)
        # if hashtag_m:
        #     hashtag = hashtag_m.group("hashtag")
            # send hashtag signal
        parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)

post_save.connect(tweet_save_receiver, sender=Tweet)
