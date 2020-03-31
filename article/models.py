from django.db import models
from ckeditor.fields import RichTextField



# Create your models here.

class Article(models.Model):
    # Article tablosunda primary key belirlenen bir alan kullanılmaz ise otomatik olarak Id isimli auto increment bir alan oluşturulmaktadır.

    # auth.User tablosu ile foreignkey bağlantısı olan bir giriş alanı eklenmiştir.
    # on_delete=models.CASCADE ==> auth.User tablosundan bir kayıt silindiğinde bu tabloda bu user ile yaratılmış tüm kayıtlar silinecektir.
    # verbose_name ==> Article ekleme ekranında bu alanın görünen ismini değiştirmek için kullanılmaktadır.
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name = "Article Author")

    # Max 50 uzunlukta char giriş alanı eklenmiştir.
    # verbose_name ==> Article ekleme ekranında bu alanın görünen ismini değiştirmek için kullanılmaktadır.
    title = models.CharField(max_length=50, verbose_name="Article Title")
    
    # Free text alanı eklenmişmtir.
    # verbose_name ==> Article ekleme ekranında bu alanın görünen ismini değiştirmek için kullanılmaktadır.
    content = RichTextField(verbose_name="Article Content")

    # Otomatik olarak günü tarih ve saatinin ekleneceği bir alan eklenmiştir.
    # auto_now_add = True ==> otomatik olarak günün tarih ve saatinin eklenmesi kullanılan özellik
    createddate = models.DateTimeField(auto_now_add = True, verbose_name = "Article Created Date")
    
    article_image = models.FileField(blank = True, null = True, verbose_name = "Add Image to Article")
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-createddate']

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE, verbose_name = "Article", related_name="comments")
    comment_author = models.CharField(max_length=50, verbose_name = "Comment Author")
    comment_content = models.CharField(max_length = 200, verbose_name = "Comment Content")
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_content
    class Meta:
        ordering = ['-comment_date']