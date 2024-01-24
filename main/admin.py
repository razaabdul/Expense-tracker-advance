from . import models
from django.contrib import admin
import random
color = "%06x" % random.randint(0, 0xFFFFFF)

class Account_detailsAdmin(admin.ModelAdmin):
    list_display = ['id','image','Account_holder','account_number','current_balance','expenses','incomes']
admin.site.register(models.Account_details,Account_detailsAdmin)

class Payment_modeAdmin(admin.ModelAdmin):
    list_display = ['payment_type','user']
admin.site.register(models.Payment_mode,Payment_modeAdmin)   


class IcategoryAdmin(admin.ModelAdmin):
    list_display = ['category','user']
admin.site.register(models.Icategory ,IcategoryAdmin)  

class EcategoryAdmin(admin.ModelAdmin):
    list_display = ['category','user']
admin.site.register(models.Ecategory ,EcategoryAdmin)  

# class  SourceAdmin(admin.ModelAdmin):
#     list_display = ['source',]
# admin.site.register(models.Source ,SourceAdmin)


# class IncomeAdmin(admin.ModelAdmin):
#     list_display = ['user' ,'Transition_id','income_way','income_category','income_amount','income_details','total_income']    
# admin.site.register(models.Income,IncomeAdmin)


# class ExpenseAdmin(admin.ModelAdmin):
#     list_display = ['user','Transition_id','expense_way','expense_category','expense_amount','expense_details','total_expense']
# admin.site.register(models.Expense,ExpenseAdmin)


class TransitionAdmin(admin.ModelAdmin):
    list_display = ['user','Transition_id','type','mode','category','amount','details']
admin.site.register(models.Transition,TransitionAdmin)

# admin.site.register(models.Salary)