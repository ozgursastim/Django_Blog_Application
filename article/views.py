from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import ArticleForm
from .models import Article, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def articles(request):
    # search işleminin yapılması sonucunda search alanındaki değer alınmaktadır.
    keyword = request.GET.get("keyword")
    # eğer bir arama işlemi ile articles safyası get yapıldıysa mı diye kontrol edilmektedir.
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
    else:
        articles = Article.objects.all()
    
    return render(request, "articles.html", {"articles":articles})

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

# eğer login yapılmadıysa login sayfasına yönlendirme yapılmaktadır.
@login_required(login_url = "user:loginuser")
def dashboard(request):
    # article modülünden ilgili kaydın seçilmesi için article.objects.filter özelliği kullanılmaktadır.
    articles = Article.objects.filter(author = request.user)
    # filtrelenen kayıtlar bir dictionary nesnesine aktaılmaktadır.
    context = {
        "articles":articles
    }
    # oluşan dictionary nesnesi dashboard sayfasına gönderilmektedir.
    return render(request, "dashboard.html", context)

@login_required(login_url = "user:loginuser")
def addarticle(request):
    # File upload işlemlerinde POST üzerinden değil FILES üzerinden gelmektedir.
    # Bu sebeple form oluşturulurken file upload işlemi için articleform nesnesi oluştururken "request.FILES or None" eklenmelidir.
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # commit = False özelliği kullanılarak form'un otomatik olarak kaydedilmesi engellenmiştir.
        article = form.save(commit=False)
        # form'un kaydeden kullanıcı bilgisi mevuct kullanıcının atanması sağlanmıştır.
        article.author = request.user
        # formun kaydedilmesi sağlamıştır.
        article.save()
        messages.success(request, "Article added successfully")
        return redirect("article:dashboard")
    
    return render(request, "addarticle.html", {"form":form})

@login_required(login_url = "user:loginuser")
def detail(request, id):
    # article = Article.objects.filter(id=id).first()
    # eğer ilgili Id ile bir article yoksa "Page 404 hatası" alması sağlanmıştır.
    article = get_object_or_404(Article, id = id)

    comments = article.comments.all()

    return render(request, "detail.html", {"article":article, "comments":comments})

@login_required(login_url = "user:loginuser")
def updateArticle(request, id):
    # Eğer gönderilen Id ile bir kayıt yoksa 404 hatası vermesi için get_object_or_404 özelliği kullanılmaktadır
    article = get_object_or_404(Article, id = id)
    # Oluşturulan örneğin bilgilerinin forma gönderilmesi için "instance = <instance_name>" özelliği kullanılmaktadır
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)
    if form.is_valid():
        # commit = False özelliği kullanılarak form'un otomatik olarak kaydedilmesi engellenmiştir.
        article = form.save(commit=False)
        # form'un kaydeden kullanıcı bilgisi mevuct kullanıcının atanması sağlanmıştır.
        article.author = request.user
        # formun kaydedilmesi sağlamıştır.
        article.save()
        messages.success(request, "Article updated successfully")
        return redirect("article:dashboard")

    return render(request, "update.html", {"form":form})

@login_required(login_url = "user:loginuser")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id = id)
    article.delete()
    messages.success(request, "Article deleted successfully")
    return redirect("article:dashboard")

def addComment(request, id):
    article = get_object_or_404(Article, id = id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()
    # return redirect("/articles/article/" + str(id))
    # redirect işlemini parametrik hale getirmek için reverse fonksiyonu kullanılmaktadır.
    return redirect(reverse("article:detail", kwargs={"id":id}))