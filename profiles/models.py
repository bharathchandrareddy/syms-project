from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from.utils import *
from django.template.defaultfilters import slugify
from django.db.models import Q
# Create your models here.
class ProfileManager(models.Manager):   #this class is created to get the all users to send the request
    def get_all_profiles_to_invite(self,sender):
        profiles = Profile.objects.all().exclude(user = sender)
        profile = Profile.objects.get(user = sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        accepted = []
        for rel in qs:
            if rel.status == 'accepted':
                accepted.append(rel.receiver)
                accepted.append(rel.sender)
        print(accepted)
        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return available

    def get_all_profiles(self,me):
        profiles = Profile.objects.all().exclude(user = me)
        return profiles



class Profile(models.Model):    #this function creates the database tables for specified fields
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  #this is to connect one user to other users
    bio= models.TextField(max_length=150,default="nothing to say about..")
    email= models.EmailField(max_length=200)
    location= models.CharField(max_length=100)
    avatar= models.ImageField(default='avatar.png',upload_to='avatars/')
    profession= models.CharField(max_length=100)
    number= models.CharField(max_length=100)
    friends= models.ManyToManyField(User,blank=True,related_name='friends')
    slug = models.SlugField(unique=True)  # similar to username it will be unique
    gender= models.CharField(max_length=100)
    dob= models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)  # this tells us at when the account is created
    objects = ProfileManager()   # this modal can be used to manage the database in django

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"
    def get_absolute_url(self):
        return reverse('profiles:profile-detail-view',kwargs={'slug':self.slug})

    def get_friends(self):  # so this function will get all the list of user friends
        return self.friends.all()

    def get_friends_num(self): # this will get the number of friends
        return self.friends.all().count()

    def get_post_num(self):
        return self.posts.all().count()

    def get_all_authours_post(self):
        return self.posts.all()
    def get_likes_given_num(self):
        likes = self.like_set.all() # this syntax depends on the profile and likes relationship in post\models.py
        total_liked = 0
        for item in likes:
            if item.values =='Like':
                total_liked +=1
        return total_liked
    def get_likes_recieved(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked+=item.liked.all().count()
        return total_liked


    __initial_first_name = None
    __initial_last_name = None

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name


    def save(self,*args,**kwargs):   # this part hepls us to create a unique user_id by adding random characters generated in utils.py file
        ex = False
        to_slug = self.slug
        # this part is written to create a proper slug user name to the user
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug == '':
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug = to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_text()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args,**kwargs)
STATUS_CHOICES = (     # this is for the admin purpose to see whether the request sent or not
    ('send','send'),
    ('accepted','accepted')
)
class RelationshipManager(models.Manager):   #in django models we have a library called manager which helps user to interact wih the databases
    def invitations_received(self, receiver):
        qs= Relationship.objects.filter(receiver=receiver,status='send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    objects = RelationshipManager()
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"