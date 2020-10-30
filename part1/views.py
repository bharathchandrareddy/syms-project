from django.shortcuts import render

def home_view(request): # this function is created for the home view
    user = request.user
    hello = 'hello world'
    context = {      #this dictionary is created to pass the dynamic data into html page
        user: user,
        hello: hello,
    }
    return render(request,'personal_post.html',context)