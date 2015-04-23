from __future__ import unicode_literals
from django.contrib import admin
import swapper
from imagestore.models.album import Album
from imagestore.models.image import Image
from imagestore.models.upload import AlbumUpload
from sorl.thumbnail.admin import AdminInlineImageMixin


class InlineImageAdmin(AdminInlineImageMixin, admin.TabularInline):
    model = Image
    fieldsets = ((None, {'fields': ['image', 'order', 'album']}),)
    extra = 0


class AlbumAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['order']}),)
    list_display = ('admin_thumbnail', 'order')
    list_editable = ('order', )
    inlines = [InlineImageAdmin]


class ImageAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['user', 'title', 'image', 'description', 'order', 'tags', 'album']}),)
    list_display = ('admin_thumbnail', 'order', 'album')
    list_filter = ('album', )


class AlbumUploadAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

if not swapper.is_swapped('imagestore', 'Image'):
    admin.site.register(Image, ImageAdmin)

if not swapper.is_swapped('imagestore', 'Album'):
    admin.site.register(Album, AlbumAdmin)
    admin.site.register(AlbumUpload, AlbumUploadAdmin)
