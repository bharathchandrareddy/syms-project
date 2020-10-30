from django.urls import path

from.views import profile_view,invites_received_view,profile_list_view,invite_profile_list_view,\
    ProfileListView,accept_invitation,reject_invitation,send_invitation,remove_from_friends,ProfileDetailView

app_name = 'profiles'
urlpatterns=[
    path('myprofile/',profile_view,name='my-profile-view'),
    path('myinvites/',invites_received_view,name='my-invites-view'),
    path('/',ProfileListView.as_view(),name='all-profiles-view'), # when using class based views we need to put (.as_view())
    path('to-invites/',invite_profile_list_view,name='invite-profiles-view'),
    path('acceptinvite/',accept_invitation,name='accept-invite'),
    path('rejectinvite/',reject_invitation,name='reject-invite'),
    path('sendinvite/',send_invitation,name = 'send-invite'),
    path('removefriend/',remove_from_friends,name= 'remove-friend'),
    path('<slug>/',ProfileDetailView.as_view(),name='profile-detail-view')
]


