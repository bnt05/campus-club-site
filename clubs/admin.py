from django.contrib import admin

from .models import Club, ClubRating, CrossSchoolEvent, KnowledgeCategory, KnowledgeItem, Membership, Post


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_at')
    search_fields = ('name', 'description')
    raw_id_fields = ('creator',)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('club', 'user', 'is_admin', 'joined_at')
    list_filter = ('is_admin',)
    search_fields = ('club__name', 'user__username')
    raw_id_fields = ('club', 'user')


@admin.register(KnowledgeCategory)
class KnowledgeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'club')
    search_fields = ('name', 'club__name')
    raw_id_fields = ('club',)


@admin.register(KnowledgeItem)
class KnowledgeItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_by', 'created_at')
    search_fields = ('title', 'description', 'category__name', 'uploaded_by__username')
    raw_id_fields = ('category', 'uploaded_by')


@admin.register(ClubRating)
class ClubRatingAdmin(admin.ModelAdmin):
    list_display = ('club', 'user', 'score', 'created_at')
    list_filter = ('score',)
    search_fields = ('club__name', 'user__username', 'comment')
    raw_id_fields = ('club', 'user')


@admin.register(CrossSchoolEvent)
class CrossSchoolEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'partner_school', 'start_date', 'end_date', 'is_public')
    search_fields = ('title', 'partner_school', 'club__name')
    list_filter = ('is_public', 'start_date', 'end_date')
    raw_id_fields = ('club',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('club', 'author', 'created_at')
    search_fields = ('content',)
    list_filter = ('club', 'author')
