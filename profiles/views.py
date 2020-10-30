from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,Relationship
from .forms import ProfileModel
from django.views.generic import ListView,DetailView
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.
def profile_view(request):  # this function is created to view profile for the user
    profile = Profile.objects.get(user = request.user)  #instantiate profile details
    form = ProfileModel(request.POST or None, request.FILES or None, instance=profile)
    '''so the above variable is used to get the info from profile model
    by requesting the files
    '''
    confirm = False  #this is just flag
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm=True

    context = {
        'profile':profile,
        'form':form,
        'confirm':confirm,
    }
    return render(request,'profiles/my_profile.html',context)

def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)   #qs=query set
    results = list(map(lambda x:x.sender,qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    context = {
        'qs':results,
        'is_empty':is_empty,
    }

    return render(request,'profiles/my_invites.html',context)

def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk') #gets the primary key
        sender= Profile.objects.get(pk = pk) #this will get the pk of sender
        receiver = Profile.objects.get(user = request.user)  #this will get the pk of receiver
        rel = get_object_or_404(Relationship,sender = sender,receiver=receiver)
        if rel.status =='send':
            rel.status = 'accepted'
            rel.save()
    return render(request, 'profiles/my_invites.html')
def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk') #gets the primary key
        sender= Profile.objects.get(pk = pk) #this will get the pk of sender
        receiver = Profile.objects.get(user = request.user)  #this will get the pk of receiver
        rel = get_object_or_404(Relationship,sender = sender,receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')
def invite_profile_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)  # qs=query set
    context = {'qs': qs}
    return render(request, 'profiles/to_invite_list.html', context)


def profile_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)  # qs=query set
    context = {'qs': qs}
    return render(request, 'profiles/profile_list.html', context)

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    # def get_object(self):
    #     slug = self.kwargs.get('slug')
    #     profile = Profile.objects.get(slug=slug)
    #     return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:

            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context
class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    #context_object_name = 'qs'
    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact = self.request.user)
        profile = Profile.objects.get(user = user)
        rel_r = Relationship.objects.filter(sender = profile)
        rel_s = Relationship.objects.filter(receiver = profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context['rel_receiver']=rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context

    '''def get_context_date(self,**kwargs):    # this profile is to get the details of other users when clicked
        context = super().get_context_data(**kwargs)
        user= User.objects.get(username__iexact = self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)   #relationship recieve, we are going to query the relationships of profile
        rel_s = Relationship.objects.filter(receiver=profile)  # relationship saver
        rel_receiver = []
        rel_sender = []
        print('hello')
        for obj in rel_r:
            rel_receiver.append(obj.receiver.user)
        for obj in rel_s:
            rel_sender.append(obj.sender.user)
        print('these are the rel_receivers',rel_receiver)
        print('these are the rel_senders',rel_sender)
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context '''
def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user = user)
        receiver = Profile.objects.get(pk = pk)
        rel = Relationship.objects.create(sender = sender,receiver = receiver,status = 'send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles/my-profile-view')
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user = user)
        receiver = Profile.objects.get(pk = pk)

        rel = Relationship.objects.get(
            (Q(sender= sender) & Q(receiver= receiver)) | (Q(sender = receiver) & Q(receiver = sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles/my-profile-view')
