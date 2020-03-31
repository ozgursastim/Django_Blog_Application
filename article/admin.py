from django.contrib import admin

from .models import Article, Comment

# Register your models here.

admin.site.register(Comment)

# admin.site.register(Article)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    
    # Article listeleme sayfasında birden fazla alanın gösterilmesi için list_display özellği kullanılmaktadır.
    list_display = ["title", "author", "createddate"]

    # listelenen tüm alanlara link eklemek için list_display_links özelliği kullanılmaktadır.
    list_display_links = ["title", "createddate"]

    # Article listesinde arama özelliği eklemek search_fields özelliği kullanılmaktadır.
    search_fields = ["title"]

    # Filtreleme özelliği eklemek için list_filter özelliği kullanılmaktadır.
    list_filter = ["createddate"]

    # model'in Article'dan türetildiği bir Meta isminde sınıf oluşturulmalıdır.
    class Meta:
        model = Article

