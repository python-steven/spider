from django.contrib import admin

# Register your models here.
from .models import User,Customer,Department,BudgetCodeForm,PartItemResult,PartItem,MaintenanceLog,Configuration

class UserAdmin(admin.ModelAdmin):
    list_display = ('Id','EmployeeId','Name','DepartmentId','Password','Email','Role','IsActivated','CreatedTime','UpdatedTime')
    search_fields = ('Name',)
    ordering = ('Name',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('Id','Customer','IsActivated','UpdatedTime')
    search_fields = ('Customer',)
    ordering = ('Customer',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('Id','Department','IsActivated','UpdatedTime')
    search_fields = ('Department',)
    ordering = ('Department',)


class BudgetCodeFormAdmin(admin.ModelAdmin):
    list_display = ('Id','DepartmentId','Department','Remark','Attachment','BillingType','BudgetCode','ApplyDate'
                    ,'ExternalNumberType','ExternalNumber','ExternalNumberEffectiveDate','PicId','Pic','ProductName'
                    ,'Model', 'PurchaseType', 'UnitPrice', 'Quantity', 'Unit','Currency','CustomerId','Customer'
                    ,'TypeOfMachine', 'ProjectCode', 'ApplyReason', 'SignerId', 'Signer', 'Status', 'CreatedTime'
                    , 'UpdatedTime','OwnerId','MergeId','SignRemarks','AttachmentPath'
                    )
    search_fields = ('ExternalNumber',)
    ordering = ('Id',)


class PartItemResultAdmin(admin.ModelAdmin):
    list_display = ('Id','USN','SN','OSN','Asset','PN','PartName','Spec','UsedTimes','Stage','FixtureId','Result'
                    ,'ErrorCode','TrnDate','UpdatedTime')
    search_fields = ('PartName',)
    ordering = ('Id',)


class PartItemAdmin(admin.ModelAdmin):
    list_display = ('Id','SN','OSN','PN','PartName','Spec','UsedTimes','CreatedTime','UpdatedTime','CheckCycle'
                    ,'CheckCycleCount','NextCheckCount','NextCheckDate','ErrorCounts','TrnDate','NGRate')
    search_fields = ('PartName',)
    ordering = ('Id',)


class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ('Id','PartItemId','PartName','UpdatedTime','Status','Content','OperatorId','CheckDueDate'
                    ,'CheckCount','UsedTimes')
    search_fields = ('PartName',)
    ordering = ('Id',)

class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('Id','Type','Max','Min','Reminders')
    search_fields = ('Type',)
    ordering = ('Id',)


admin.site.register(User,UserAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(BudgetCodeForm,BudgetCodeFormAdmin)
admin.site.register(PartItemResult,PartItemResultAdmin)
admin.site.register(PartItem,PartItemAdmin)
admin.site.register(MaintenanceLog,MaintenanceLogAdmin)
admin.site.register(Configuration,ConfigurationAdmin)
