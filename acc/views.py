
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib import messages

# Create your views here.
def chpass(request):
    u = request.user
    if request.POST.get("npass"):
        if request.POST.get("npass") == request.POST.get("cfpass"):
            p = request.POST.get("npass")
            u.set_password(p)
            u.save()
            return redirect("acc:index")
        else:pass
    else:pass
    
    cp = request.POST.get("cpass")
    if check_password(cp, u.password):
        return render(request, "acc/chpass.html")
    else:
        pass

def update(request):
    if request.method == "POST":
        ue = request.POST.get("uemail")
        uf = request.POST.get("fname")
        ul = request.POST.get("lname")
        uc = request.POST.get("ucomment")
        upic = request.FILES.get("upic")
        try:
            u = request.user
            u.email, u.first_name, u.last_name, u.comment = ue, uf, ul, uc
            if upic:
                u.pic.delete()
                u.pic = upic
            u.save()
            messages.success(request, "게시글이 수정되었습니다.")
            return redirect("acc:profile")
        except:
            messages.error(request, "오류가 있어 수정이 실패하였습니다.")
    return render(request, "acc/update.html")

def index(request):
    return render(request, "acc/index.html")

def userlogin(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        u = authenticate(username=un, password=up)
        if u:
            login(request, u)
            messages.success(request, f"{un} 님 환영합니다!")
            return redirect("acc:index")
        else:
            messages.error(request, "계정정보가 일치하지 않습니다.")
    return render(request, "acc/login.html")

def userlogout(request):
    logout(request)
    messages.success(request, "로그아웃되었습니다.")
    return redirect("acc:index")

def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        ue = request.POST.get("uemail")
        uf = request.POST.get("fname")
        ul = request.POST.get("lname")
        uc = request.POST.get("ucomment")
        upic = request.FILES.get("upic")
        # print(un,up,ue,uf,ul,uc,upic)
        try:
            User.objects.create_user(username=un, password=up, email=ue, 
                                 first_name=uf, last_name=ul, comment=uc, pic=upic)
            return redirect("acc:index")
        except:
                messages.info(request, "USERNAME 이 중복되어 계정이 생성되지 않았습니다")
    return render(request, "acc/signup.html")

def profile(request):
    return render(request, "acc/profile.html")

def delete(request):
    u = request.user
    cp = request.POST.get("cpass")
    #print(cp) 인자 넘어오는지 확인
    if check_password(cp, u.password):
        u.pic.delete()
        u.delete()
        return redirect("acc:index")
    else:
        messages.error(request, "인증정보가 일치하지 않아 삭제되지 않았습니다.")
    return redirect("acc:profile")
    