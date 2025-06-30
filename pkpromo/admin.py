import os
import shutil
from io import BytesIO

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
import zipfile

from django.utils.six import StringIO
from django.utils.text import slugify

from .models import Abiturientus, AbiturientusFile, FILE_TYPES_DICT

# Register your models here.
from .utils.utils import transliterate


class FileInline(admin.TabularInline):
    readonly_fields = ["file_type", "file"]
    model = AbiturientusFile

class AbiturientusAdmin(admin.ModelAdmin):
    exclude = ['code', ]
    inlines = [FileInline, ]
    list_filter = ('status', 'apply_date')
    readonly_fields = ['fio', 'apply_date']
    change_form_template = "admin/admin_download_files.html"

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def response_change(self, request, obj):
        if "_download-file" in request.POST:
            abitur_docs = AbiturientusFile.objects.filter(abiturientus=obj)
            filenames = [{'path': file.file.path, 'file_type': file.file_type} for file in abitur_docs]
            zip_subdir = transliterate(obj.fio)
            zip_filename = "%s docs.zip" % zip_subdir
            s = BytesIO()
            zf = zipfile.ZipFile(s, "w")

            for fpath in filenames:
                fdir, fname = os.path.split(fpath['path'])
                zip_path = os.path.join(FILE_TYPES_DICT[fpath['file_type']], fname)
                zf.write(fpath['path'], zip_path)
            zf.close()

            response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
            response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
            return response
        return super().response_change(request, obj)

admin.site.register(Abiturientus, AbiturientusAdmin)