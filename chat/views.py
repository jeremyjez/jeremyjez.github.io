from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message
from chat.forms import SignUpForm
from chat.serializers import MessageSerializer, UserSerializer







from django.http import HttpResponse


from django.shortcuts import render, redirect
from .forms import Registration #,Student_picture
from .models import New,Event
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random


def index2(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return render(request, 'chat/index.html', {'error':"Incorrect Username or Password"})
        return redirect('chats')



@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def register_view(request):
    """
    Render registration template
    """
    if request.method == 'POST':
        print("working1")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('chats')
    else:
        print("working2")
        form = SignUpForm()
    template = 'chat/register.html'
    context = {'form':form}
    return render(request, template, context)


@login_required (login_url="login")
def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username),
                       'getUser': str(request.user),
                       'crawford':User.objects.get(username="Crawford")})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'getUser': str(request.user),
                       'receiver': User.objects.get(id=receiver),
                      'crawford':User.objects.get(username="Crawford"),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})



















from django.shortcuts import render





def index(request):
    #FOR EVENTS
    events=[]
    rememberevent= None
    if Event.objects.all():
        while True:
            #print("Look Here: ", events[0])
            rememberevent=random.choice(list(Event.objects.all()))
            if rememberevent not in events:
                events.append(rememberevent)
                if len(events) == 3:
                    break
    #END

    #FOR EXCO-BRIEF-WRITEUPS
    exco_brief= ""
    #END

    #FOR NEWS
    news= []
    lastnews= len (New.objects.all())
    if New.objects.all():
        news.append(New.objects.all()[lastnews-1]),news.append(New.objects.all()[lastnews-2]),news.append(New.objects.all()[lastnews-3])

    #NEWS END
    return render (request,"index.html",{"events":events,"exco_brief":exco_brief,"news":news})



def news_details(request,news):
    if request.method == "POST":
        return HttpResponse("It is a POST request")
    else:
        # RECENT NEWS
        recent_news = []
        if len(New.objects.all()) >= 3:
            lastnews = len(New.objects.all())
            recent_news.append(New.objects.all()[lastnews - 1]), recent_news.append(
                New.objects.all()[lastnews - 2]), recent_news.append(
                New.objects.all()[lastnews - 3])
        # END

        news= New.objects.get(identification_code=news)
        return render(request, "news-details.html", {"details": news,
                                              "recent_news": recent_news})


def news(request):
    if request.method=="POST":
        token = ""
        getSearch= request.POST.get("text")
        # getSearch= getSearch.lower()
        news_obj= New.objects.all()
        object_store= []


        #SEARCH ALGORITHM
        # RECENT NEWS
        recent_news = []
        if len(New.objects.all()) >= 3:
            lastnews = len(New.objects.all())
            recent_news.append(New.objects.all()[lastnews - 1]), recent_news.append(
                New.objects.all()[lastnews - 2]), recent_news.append(
                New.objects.all()[lastnews - 3])
        # END

        for i in news_obj:
            if getSearch.lower() == i.title.lower():
                object_store.append(i)
                return render(request, "newssearch.html", {"s_result": object_store,
                                                           "recent_news": recent_news})


        # INTELLIGENT SEARCH ALORITHM SPLIT SEARCH TOKEN
        # SPLIT SEARCH TOKEN
        getSearchList = []
        compilelist=""
        for i in getSearch.lower():
            if i == " ":
                getSearchList.append(compilelist)
                compilelist=""
            else:
                compilelist+=i
        getSearchList.append(compilelist)
        print(getSearchList)

        # INTELLIGENT SEARCH ALORITHM
        appendletter= []
        storeletter = ""
        countletter=-1
        for i in news_obj:
            for j in i.title.lower():
                #print(len(i.title))
                countletter+=1
                if j == " ":
                    #print(storeletter)
                    if storeletter in getSearchList:
                        object_store.append(i)
                        print(storeletter)
                        appendletter.append(storeletter)
                        break
                    storeletter = ""
                else:
                    storeletter+= j
                    if countletter== len(i.title)-1:
                        print(storeletter)
                        if storeletter in getSearchList:
                            object_store.append(i)
                        appendletter.append(storeletter)
                        #print(storeletter)
            storeletter = ""
            countletter = -1

        print(appendletter)

        if object_store != []:
            #RECENT NEWS
            recent_news = []
            if len(New.objects.all()) >= 3:
                lastnews = len(New.objects.all())
                recent_news.append(New.objects.all()[lastnews - 1]), recent_news.append(
                    New.objects.all()[lastnews - 2]), recent_news.append(
                    New.objects.all()[lastnews - 3])
            # END
            return render(request, "newssearch.html", {"s_result": object_store,
                                                         "recent_news": recent_news})
        #END

        return HttpResponse("It is a POST request")
    else:
        #RECENT NEWS
        recent_news = []
        if len(New.objects.all())>=3:
            lastnews = len(New.objects.all())
            recent_news.append(New.objects.all()[lastnews - 1]), recent_news.append(New.objects.all()[lastnews - 2]), recent_news.append(
            New.objects.all()[lastnews - 3])
        #END

        global keeprow
        keeprow = []
        all_c = New.objects.all()
        keepobj=[]
        keepno=0
        nmbr=0
        for i in all_c:
            keepno+=1
            keepobj.append(i)
            if keepno==9:
                keepno=0
                keeprow.append(keepobj)
                keepobj = []

        if keepno != 0:#(1)if there is second row but its not up to 9 fields add the remaining fields OR (2)add keepobj because we only have one page only and it's not up to 9 fields
            keeprow.append(keepobj)
        if len(keeprow)> 1: #to enable page
            return render(request, "news.html", {"enablepage": True, "nmbr": nmbr,"curr_page":nmbr+1,
                                "pageno":len(keeprow),"keeprow":keeprow[0], "recent_news":recent_news})
        return render(request, "news.html",{"enablepage": False, "nmbr": nmbr, "keeprow": keeprow[0],
                                             "curr_page":nmbr+1, "recent_news":recent_news})


def npage(request,nmbr):
    global keeprow
    nmbr+=1
    return render(request, "news.html", {"enablepage": True, "nmbr": nmbr, "keeprow": keeprow[nmbr],"pageno":len(keeprow),
                                          "curr_page":nmbr+1})

def ppage(request,nmbr):
    global keeprow
    nmbr-=1
    return render(request, "news.html", {"enablepage": True, "nmbr": nmbr, "keeprow": keeprow[nmbr],"pageno":len(keeprow),
                                          "curr_page":nmbr+1})



def events(request):
    global keeprow2
    keeprow2 = []
    all_c = Event.objects.all()
    keepobj = []
    keepno = 0
    nmbr = 0
    for i in all_c:
        keepno += 1
        keepobj.append(i)
        if keepno == 9:
            keepno = 0
            keeprow2.append(keepobj)
            keepobj = []

    if keepno != 0:  # (1)if there is second row but its not up to 9 fields add the remaining fields OR (2)add keepobj because we only have one page only and it's not up to 9 fields
        keeprow2.append(keepobj)
    if len(keeprow2) > 1:  # to enable page
        return render(request, "event.html", {"enablepage": True, "nmbr": nmbr, "curr_page": nmbr + 1,"pageno": len(keeprow2),
                                              "keeprow": keeprow2[0]})
    return render(request, "event.html", {"enablepage": False, "nmbr": nmbr, "keeprow": keeprow2[0],"curr_page": nmbr + 1})


def enpage(request,nmbr):
    global keeprow2
    nmbr+=1
    return render(request, "news.html", {"enablepage": True, "nmbr": nmbr, "keeprow": keeprow2[nmbr],"pageno":len(keeprow2),
                                          "curr_page":nmbr+1})

def eppage(request,nmbr):
    global keeprow2
    nmbr-=1
    return render(request, "news.html", {"enablepage": True, "nmbr": nmbr, "keeprow": keeprow2[nmbr],"pageno":len(keeprow2),
                                          "curr_page":nmbr+1})




def student_login(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'login.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return render(request, 'login.html', {'err':"Incorrect Username or Password"})
        return redirect('chats')


def student_logout(request):
    logout(request)
    return redirect("index")


