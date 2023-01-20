from django.contrib import admin
from .models import Question,UploadDocument,DocumentQuestions
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(Question)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ["id", "question"]
    from_encoding = 'utf-8'

admin.site.register(UploadDocument)
admin.site.register(DocumentQuestions)
