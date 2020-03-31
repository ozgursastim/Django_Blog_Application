from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Create your views here.

def register(request):
    # 2. yöntem
    # bu yöntemde request'in GET olup olmadığın kontrol edilmesine gerek kalmamaktadır.
    # bu yöntemde eğer request POST ise form gelen bilgiler doldurulmakta, eğer GET ise boş oluşacaktır.
    form = RegisterForm(request.POST or None)
    # forms.py modülündeki clean() fonksiyonu is_valid() fonksiyonu çağrıldığı zaman çalışmaktadır.
    # clean() fonksiyonu içerisindeki kontroller çalışmaktadır
    # eğer fonksiyon true ise form içerisindeki kontroller sağlanmıştır demektir.
    if form.is_valid():
        # formdaki bilgiler geçerli ise bu fonsiyondan dönen değerler alınmaktadır.
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        # user modelinden bir obje oluşturulup kaydedilecektir.
        newUser = User(username=username)
        # kullanıcının password'ü şifreli bir şekilde kaydeilmesi için
        newUser.set_password(password)
        # kullanıcı bilgisi user modele kaydedilmektedir.
        newUser.save()
        # kayıt işleminden sonra bu kullanıcı ile giriş yapılmasını sağlamak için django.contrib.auth daki login fonksiyonu kullanılmaktadır.
        login(request, newUser)
        messages.info(request, "It was successfully registered")
        return redirect("index")
    else:
        # eğer bilgiler hatalı ise aynı sayfayı yüklemek için kullanılmıştır.
        context = {
            "form":form
        }
        return render(request, "register.html", context)
    
    # 1. yöntem
    """
    if request.method == "POST":
        # form objesine POST request'inden(form ekranından gelen) gelen bilgiler ile dolduruldu 
        form = RegisterForm(request.POST)
        # forms.py modülündeki clean() fonksiyonu is_valid() fonksiyonu çağrıldığı zaman çalışmaktadır.
        # clean() fonksiyonu içerisindeki kontroller çalışmaktadır
        # eğer fonksiyon true ise form içerisindeki kontroller sağlanmıştır demektir.
        if form.is_valid():
            # formdaki bilgiler geçerli ise bu fonsiyondan dönen değerler alınmaktadır.
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # user modelinden bir obje oluşturulup kaydedilecektir.
            newUser = User(username=username)
            # kullanıcının password'ü şifreli bir şekilde kaydeilmesi için
            newUser.set_password(password)
            # kullanıcı bilgisi user modele kaydedilmektedir.
            newUser.save()
            # kayıt işleminden sonra bu kullanıcı ile giriş yapılmasını sağlamak için django.contrib.auth daki login fonksiyonu kullanılmaktadır.
            login(request, newUser)
            return redirect("index")
        else:
            # eğer bilgiler hatalı ise aynı sayfayı yüklemek için kullanılmıştır.
            context = {
                "form":form
            }
            return render(request, "register.html", context)
    else:
        # eğer GET requesti ise formu boş oluşturyoruz.
        form = RegisterForm()
        context = {
            "form":form
        }
        # form bilgisi register.html'e gönderilmektedir.
        return render(request, "register.html", context)"""

def loginuser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password=password)
        if user is None:
            messages.info(request, "Wrong Information")
            return render(request, "login.html", context)
        
        messages.success(request, "Login Successfully")
        login(request, user)
        return redirect("index")
    return render(request, "login.html", context)
    
def logoutuser(request):
    logout(request)
    messages.success(request, "Successfully loguot")
    return redirect("index")

