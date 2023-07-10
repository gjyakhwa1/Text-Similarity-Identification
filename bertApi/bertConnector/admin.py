from django.contrib import admin
from .models import Question,QuestionCountHistory, ServerStatus
from import_export.admin import ImportExportModelAdmin

# Register your models here.


@admin.register(Question)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ["id", "question","date","examinationType","examYear","user"]
    from_encoding = 'utf-8'

class CustomQuestionCountHistory(admin.ModelAdmin):
    readonly_fields =('updated_at',)

admin.site.register(ServerStatus)
    
admin.site.register(QuestionCountHistory,CustomQuestionCountHistory)
