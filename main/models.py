from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.utils.html import format_html
import datetime
from django.utils.timezone import now
 
 

# Create your models here.
class Account_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Account_holder = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='users_pic')  
    account_number = models.CharField(max_length=100)
    current_balance=models.FloatField(default=0)
    expenses=models.FloatField(default=0)
    incomes=models.FloatField(default=0)
 

    def image(self): #new
        return format_html('<img src = " /media/{}" width = "40" border-redious:80%/>'.format(
              self.profile_pic
         ))
    # def current_balance(self):
    #     total_income = Income.objects.all()
    #     total_expense = Expense.objects.all()
    #     expense = 0
    #     income =0
    #     for i in total_income:
    #         income += i.income_amount
    #     for e in total_expense:
    #         expense += e.expense_amount    

    #     remain = 0
    #     return remain   

     
 

class Payment_mode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100) 
    val =models.FloatField(default=0)

    def __str__(self) -> str:
        return self.payment_type
    

class Ecategory(models.Model):
  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    val = models.FloatField(default=0)
    def __str__(self) -> str:
        return self.category  

    


class Icategory(models.Model):
  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    val = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.category  

class contact(models.Model):
    name = models.CharField(max_length=200)
    user_email = models.EmailField(max_length = 254)
    phone_number = models.CharField(max_length=12)
    description = models.TextField(max_length=1000)

# class Income(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # Sender_name =  models.ForeignKey(Source,on_delete=models.CASCADE)
#     # income_way =  models.ForeignKey(Payment_mode, on_delete=models.CASCADE)
#     income_way =  models.CharField(max_length=100)
#     # current_account_detail = models.ForeignKey(Account_details,on_delete=models.CASCADE)
    
#     income_category = models.CharField(max_length=100)
#     # income_category =models.ForeignKey(Category, on_delete=models.CASCADE)
#     income_amount = models.DecimalField(max_digits=8 , decimal_places=2)
#     income_date  = models.DateTimeField( default=now)
#     income_details = models.TextField(max_length=200) 
#     Transition_id = models.IntegerField(blank=True, null=True)
#     total_income = models.DecimalField(max_digits=8 , decimal_places=2)
    
 
# class Other_income_source(models.Model):
#      income = models.ForeignKey(Income,on_delete=models.CASCADE)  
#      other_income_source = models.CharField(max_length=100)
#      other_income_amount = models.DecimalField(max_digits=8 ,decimal_places=2)  

#      def __str__(self) -> str:
#           return self.other_income_source

# class Expense(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # Receiver_name =  models.ForeignKey(Source,on_delete=models.CASCADE)
#     # expense_way =models.ForeignKey(Payment_mode, on_delete=models.CASCADE)
#     expense_way = models.CharField(max_length=100)
#     expense_category = models.CharField(max_length=100)
#     # expense_category= models.ForeignKey(Category, on_delete=models.CASCADE)
#     expense_amount = models.DecimalField(max_digits=8 , decimal_places=2)
#     expense_date = models.DateTimeField( default=now)
#     expense_details = models.TextField(max_length=500)
#     Transition_id = models.IntegerField(blank=True, null=True)
#     total_expense = models.DecimalField(max_digits=8 , decimal_places=2)
    
 
    

class Transition(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    Name = models.CharField(max_length=100) 
    type = models.CharField(max_length=100)
    mode = models.CharField(max_length=100)
    category = models.CharField(max_length=100) 
    amount = models.DecimalField(max_digits=8 , decimal_places=2)
    Transition_date  = models.DateTimeField()
    details = models.TextField(max_length=500)
    Transition_id = models.IntegerField(blank=True, null=True)
  
    


# class Total(models.Model):
#     total = models.DecimalField(max_digits=8 , decimal_places=2)

# class Salary(models.Model):
#     user = models.ForeignKey(User , on_delete=models.CASCADE)
#     monthly_salary = models.DecimalField(max_digits=8,decimal_places=2)    

     


 
