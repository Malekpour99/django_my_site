from django.contrib import admin
from .models import Post, Author, Tag

# Register your models here.


# class PostAdmin(admin.ModelAdmin):
#     readonly_fields = ()
#     prepopulated_fields = {"slug": ("title", )}
#     list_filter = ("date", )
#     list_display = ("title", "excerpt", "date", )


admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Tag)
