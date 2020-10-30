from django.shortcuts import render,redirect
from django.urls import reverse_lazy   # we use reverse_lazy for class based view
from.models import Post,Like,Comment
from profiles.models import Profile
from.forms import PostModelForm,CommentModelForm
from django.views.generic import UpdateView,DeleteView
from django.contrib import messages
# Create your views here.
def post_view(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user = request.user)
    #initialising the post_form and comment_form
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False  # flag_value

    if 'submit_p_form' in request.POST:
        p_form = PostModelForm(request.POST,request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True
    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user=profile
            instance.post= Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

    context = {
        'posts':posts,
        'profile': profile,
        'p_form':p_form,   #this is for post form
        'c_form':c_form    # this is for comment form
    }
    return render(request,'posts/personal_post.html',context)

def like_post(request):   #if the button is clicked then this code executes
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user = user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like,created = Like.objects.get_or_create(user=profile, post_id = post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'

        else:
            like.value ='Like'

            post_obj.save()
            like.save()

    return redirect('posts:main-post-view')

class PostDeleteView(DeleteView):  #this class is created to handel when a specific post is deleted
    model = Post   #we will be working on post model
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main-post-view')   #this code will take us to the main post view

    def get_object(self,*args,**kwargs):   # to check whether the author is same as the request user
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, "this post doesn't belongs to you, You cannot delete the post ")
        return obj

class PostUpdateView(UpdateView):   #since this class is about editing the excisting post we need to work on forms file of post
    model = Post
    form_class = PostModelForm
    template_name='posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self,form):
        profile=Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "this post doesn't belongs to you, You cannot edit the post ")
            return super().form_invalid(form)




