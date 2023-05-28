from django.contrib import admin

from .models import Category, Course, Comment, CourseMaterials


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']


class CourseMaterialsAdmin(admin.TabularInline):
    model = CourseMaterials
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseMaterialsAdmin]
    list_display = ['title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content']
