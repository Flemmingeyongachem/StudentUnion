from django.contrib import admin,messages
from .models import Student,SessionYearModel,DueReceipt, Level, Department
import csv
from django.http import HttpResponse

class SessionYearModelAdmin(admin.ModelAdmin):
    list_display = ['session_start_year','session_end_year','session_president']
    ordering = ['session_end_year']
    search_fields = ['session_president__matricule_number']
    def save_model(self,request,obj,form,change):
        if obj.session_start_year == obj.session_end_year:
            return messages.error(request,message='session start year must be different from session end year!')
        if (obj.session_start_year > obj.session_end_year):
            return messages.error(request,message='session start year must be less than session end year!')
        if (obj.session_end_year < obj.session_start_year):
            return messages.error(request,message='session end year must not be less than session start year!')
        if ((obj.session_end_year-obj.session_start_year)>1):
            return messages.error(request,message='difference between session end year and  session start year! must be 1')
        verify = self.model.objects.filter(session_end_year=obj.session_end_year, session_start_year=obj.session_start_year).exists()
        if verify:
             return messages.error(request,message='session year already exists')
        return super(SessionYearModelAdmin,self).save_model(request,obj,form,change)

admin.site.register(SessionYearModel, SessionYearModelAdmin)

class DueReceiptAdmin(admin.ModelAdmin):
    @admin.action(description="Generate CSV")
    def generateCSV(self, request, queryset):
        meta = self.model._meta
        field_names = ('receipt_owner','account_name', 'account_address', 'our_reference', 'transaction_amount','transaction_account')
        # field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;   filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response
    
    @admin.action(description='validate selected receipts')
    def validate_receipt(modeladmin, request, queryset):
        for obj in queryset:
            if not obj.is_validated:
                obj.is_validated = True
                obj.save()
            messages.success(request, "Successfully validated receipts!")

    list_display = ['receipt_owner', 'transaction_account','account_address', 'our_reference', 'transaction_amount','is_validated']
    ordering = ['receipt_owner']
    list_filter = ['academic_session','department','level']
    actions = [generateCSV, validate_receipt]

admin.site.register(DueReceipt, DueReceiptAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['dept_name',]

    def count_students(self):
        pass

admin.site.register(Department, DepartmentAdmin)

class LevelAdmin(admin.ModelAdmin):
    list_display = ['level_name',]

    def count_students(self):
        pass

admin.site.register(Level, LevelAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['user','matricule_number','my_level','my_department']

admin.site.register(Student, StudentAdmin)