from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
# Create your models here.
class Post(models.Model):  #this class is to get the privatepost model
    content = models.TextField(max_length=150)
    image = models.ImageField(upload_to='posts',validators=[FileExtensionValidator(['png','jpeg','jpg'])],blank=True)
    '''validators = these models are used to valid the data which is entered by custom user
        FileExtensionValidator = this metod used to validate the file in our required format
    '''
    liked = models.ManyToManyField(Profile,blank=True, related_name='likes')    #related name is used to write reverse relations.
    '''this attribute will get all the profiles which liked this particular post
    '''
    time_stamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='posts')  #related name is used to write reverse relations.

    def __str__(self):
        return str(self.content[:150]) # this will make the content limited to 150 characters

    def num_likes(self):  # it'll get number of likes
        return self.liked.all().count()

    def num_comment(self):   #it'll get the number of comments on a post
        return self.comment_set.all().count()    #comment_set is the syntax to get those date(based on the relationships)





    class Meta:
        ordering = ('-time_stamp',)

class Comment(models.Model): # this will create the comment model

    user = models.ForeignKey(Profile,on_delete=models.CASCADE)   #this is used to conect with the Profile model
    post = models.ForeignKey(Post,on_delete=models.CASCADE)   #this is used to conect with the Post model
    body = models.TextField(max_length=300)
    time_stamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

LIKE_CHOICES = (      #this tuple creates 1 columns for the like field in db
    ('Like', 'Like') ,   #left part is for database and right for user interaction in admin site
    ('Unlike','Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    time_stamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-f{self.post}-f{self.value}"






