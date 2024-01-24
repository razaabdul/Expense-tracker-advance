from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import random
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
from .graph import get_graph
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from io import BytesIO
import base64,urllib
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.views.decorators.cache import cache_page
import os
from django.conf import settings
from django.conf.urls.static import static
from io import StringIO
from django.db.models import Sum
from django.db.models import Count
# matplotlib.backends.backend_agg.FigureCanvas
# import cufflinks as cf
# from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
# init_notebook_mode(connected=True)
# cf.go_offline()
plt.switch_backend('agg')
import calendar
import csv

# def generate_csv(request):
#     # Create an in-memory CSV file
#     csv_file = StringIO()
#     writer = csv.writer(csv_file)
#     writer.writerow(['Transaction ID', 'User', 'Amount', 'Date'])

#     transactions = Transition.objects.all()
#     for transaction in transactions:
#         writer.writerow([transaction.id, transaction.user.username, transaction.amount, transaction.Transition_date])

#     # Create a response with the CSV file
#     response = HttpResponse(csv_file.getvalue(), content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
#     return response
def process_csv(request):
    # Get transactions queryset
    transactions = Transition.objects.filter(user = request.user,type="Expense")

    # Create a DataFrame from the transactions
    data = []
    for transaction in transactions:
        data.append([transaction.id, transaction.user.username,transaction.type,transaction.category, transaction.amount, transaction.Transition_date])

    # Create DataFrame
    df = pd.DataFrame(data, columns=['Transaction ID', 'User','Type','Category' ,'Amount', 'Date'])

    # Now you can perform operations on the DataFrame
    total_amount = df['Amount'].sum()
    average_amount = df['Amount'].mean()
    highest_amount = df['Amount'].max()
    lowest_amount = df['Amount'].min()
    mask = df['Category'] == 'rent'
    dataframe = df['Category'].value_counts().plot(kind='pie')
    data1 = df['Category'].value_counts()
    plt.figure(figsize=(10,6))
    data1.plot(kind='bar')
    plt.title('Category Count')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('main/static/cat_count.png')
    





    # Example: Concatenate User and Transaction ID
    # df['User_Transaction'] = df['User'] + "_" + df['Transaction ID'].astype(str)

    # Convert DataFrame back to CSV (if needed)
    updated_csv = df.to_csv(index=False)

    return render(request, 'process_csv.html', {
        'total_amount': total_amount,
        'average_amount': average_amount,
        'highest_amount': highest_amount,
        'lowest_amount': lowest_amount,
        # 'updated_csv': updated_csv,
        'dataframe':dataframe
    })
def pay_wise(request,id):
     queryset = Payment_mode.objects.get(id=id)
     transition = Transition.objects.filter(user = request.user , mode = queryset)
     t_sum = 0
     for tr in transition:
          t_sum += float(tr.amount)
    #  print("----cat wise----------------->",queryset)
    #  for tr in transition:
    #         print("----------------------------------------------------++++++++++++++",tr.details)
     return render(request,"pay_wise.html",{'transitions':transition , 'queryset':queryset,'t_sum':t_sum})

def Ecat_wise(request,id):
     queryset = Ecategory.objects.get(id=id)
     transition = Transition.objects.filter(user = request.user , category = queryset)
     t_sum = 0
     for tr in transition:
          t_sum += float(tr.amount)
    #  print("----cat wise----------------->",queryset)
    #  for tr in transition:
    #         print("----------------------------------------------------++++++++++++++",tr.details)
     return render(request,"Ecat_wise.html",{'transitions':transition , 'queryset':queryset,'t_sum':t_sum})
     
def Icat_wise(request,id):
     queryset = Icategory.objects.get(id=id)
     transition = Transition.objects.filter(user = request.user , category = queryset)
     t_sum = 0
     for tr in transition:
          t_sum += float(tr.amount)
    #  for tr in transition:
    #       print("----------------------------------------------------++++++++++++++",tr.details)
    #  queryset = Transition.objects.filter(id = id).first()
    #  print("----cat wise----------------->",queryset)
     return render(request,"Icat_wise.html",{'transitions':transition,'queryset':queryset,'t_sum':t_sum})
          
def monthly_cate_mykhata(request,id,year = datetime.now().year ):
     queryset = Ecategory.objects.get(id=id)
     month_name =  s_month
     month_name = month_name.capitalize()  # Ensure the input is in title case
     l = list(calendar.month_name).index(month_name)
     transition = Transition.objects.filter(user = request.user , category = queryset ,Transition_date__month = l,Transition_date__year=year )


     dict3 = {}
    
    
    # month_nm = request.GET.get('search')
    # month_number = get_month_number(month_nm)
     str = ""
    
    #  title_val = 
     
     for tr in transition:
        print(".....................................>",tr.Transition_date,"..................>",tr.category)
        str = tr.details
        dict3[str] = float(tr.amount)
     for key in list(dict3.keys()):
            if dict3[key] == 0.0:
                del dict3[key]  
     print(dict3)  
     lab = list(dict3.keys())
              
     siz = list(dict3.values())
     fig1, bx1 = plt.subplots()
    
    #  plt.title(title_val)
    # plt.legend(labels=lab, loc="best") 
     bx1.pie(siz, labels=lab, autopct='%1.1f%%',radius=1.5 , startangle=90,shadow=True,wedgeprops={'linewidth':1})
     bx1.text(0, 0, queryset, ha='center', va='center', fontsize=16, fontweight='bold')
     bx1.pie([0.2],colors='w')
     plt.tight_layout()

     bx1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

     plt.savefig('main/static/mykhata_cate_table_monthly.png',dpi = 100)




     t_sum = 0
     for tr in transition:
          t_sum += float(tr.amount)
    #  for tr in transition:
    #       print("----------------------------------------------------++++++++++++++",tr.details)
    #  queryset = Transition.objects.filter(id = id).first()
    #  print("----cat wise----------------->",queryset)
     return render(request,"monthly_cate_mykhata.html",{'transitions':transition,'queryset':queryset,'t_sum':t_sum,'s_month':s_month})
          
          


def run(user):
         tr = Transition.objects.filter(user = user)
         run_process()
         for t in tr:
              print(t.category,"---------------",t.amount)
def run_process():
    # print(f"Processing at - {datetime.datetime.now()}")
        data = run(User)


def profile(request,year = datetime.now().year , month = datetime.now().strftime('%B')):
     dict = {}
     user  = User.objects.filter(username = request.user).first()
     ecat = Ecategory.objects.filter(user=request.user)
     icat = Icategory.objects.filter(user=request.user)
     
     month_name =  month
     month_name = month_name.capitalize()
     l = list(calendar.month_name).index(month_name)
     transition =  Transition.objects.filter(user = request.user ,Transition_date__month =l )
     for i in ecat:
        for tr in transition:
            if i.category == tr.category:
            #    print("----------------",tr.category,"---------------------------->",i.category)
          
               i.val   += float(tr.amount)
         
       
        v = i.val
        str  = i.category
        if str in dict:
            dict.update(v)
        else:
            dict[str] = v    
         
    #   account_details = Account_details.objects.filter(user=request.user).first()
    
     print(dict)      
    #  print("...................",ecat)
     pmode = Payment_mode.objects.filter(user=request.user)
     account_details = Account_details.objects.filter(user = request.user).first()
     print("------------------------",account_details.profile_pic)
     print(account_details)
     context = {
          'account_details':account_details ,
            'user':user,
            'ecat':ecat,
            'icat':icat,
            'pmode':pmode,
            'dict':dict,

          
     }
     return render(request,"profile.html",context )

def change_photo(request,id):
    #  queryset = User.objects.filter(user_id = id)
     queryset = User.objects.get(id=id)
     account_details = Account_details.objects.get(user = queryset.user)

     if request.method == "POST":
        #   data = request.POST 
          pic = request.FILES.get("userpic")
          account_details.profile_pic = pic
          account_details.save()
          return redirect("/profile/")
          
          


def delete_Ecat(request,id):
     queryset = Ecategory.objects.get(id=id)


     queryset.delete()
     return redirect('/profile/')

def delete_Icat(request,id):
     queryset = Icategory.objects.get(id=id)
   

     queryset.delete()
     return redirect('/profile/')
     
def delete_pmode(request,id):
     queryset = Payment_mode.objects.get(id=id)
   

     queryset.delete()
     return redirect('/profile/')

def generate_pdf(request,year = datetime.now().year):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transaction_history.pdf"'
    month_name =  select_months
    month_name = month_name.capitalize()  # Ensure the input is in title case
    l = list(calendar.month_name).index(month_name)
    pt = canvas.Canvas(response)

    # Create PDF document
    p = SimpleDocTemplate(response)
    # p.drawString(100, 750, "Transaction History")  # Add title
    elements = []
    # p.drawString(200, 750, "Transaction History")  
    styles = getSampleStyleSheet()
    hr = Paragraph('<font color="#9B0707"><b>My Expense Tracker</b></font> - {}'.format(month_name), styles['Title'])
    elements.append(hr)
    # heading = Paragraph('<b>{}</b>  History'.format(month_name), styles['Title'])
    # elements.append(heading)

    pt.drawString(400,500, f"mode: {select_months}")
    # Add table header
    table_data = [['Date', 'Amount', 'Category', 'Mode']]
    
    # Retrieve user's transaction history and add it to the PDF
    transactions = Transition.objects.filter(user = request.user,Transition_date__month =l,type = 'Expense',Transition_date__year=year) 
    for transaction in transactions:
        # Format the date
        formatted_date = transaction.Transition_date.strftime('%Y-%m-%d %H:%M')
        row = [formatted_date, transaction.amount, transaction.category, transaction.mode]
        table_data.append(row)
     
    num_columns = len(table_data[0])  # Get the number of columns
    total_width = 500  # Total width of the table (adjust as needed)
    col_width = total_width / num_columns
    
    col_widths = [col_width] * num_columns



    # Create the table with specified column widths
    table = Table(table_data, colWidths=col_widths)

    # Apply table styles
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    
    # Add the table to the PDF document
    # elements.append(table)
    total_amount = sum(float(row[1]) for row in table_data[1:])  # Assuming amount is in the second column
    print(total_amount)
    
    # Add row with total amount
    # total_row = ['', f'Total: {total_amount}', '', '']
    # table_data.append(total_row)
  
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(style)
    elements.append(table)
    styles = getSampleStyleSheet()
    # hr = Paragraph('<b>Total :</b>', styles['Title'])
    # elements.append(hr)
    footer = Paragraph('<b>{}</b> rupee'.format(total_amount), styles['Title'])
    elements.append(footer)
    # Build the PDF document
    p.build(elements)
    
    return response
    

def generate_pdf_yearly(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transaction_history.pdf"'
    year = year_name
    
    pt = canvas.Canvas(response)

    # Create PDF document
    p = SimpleDocTemplate(response)
    # p.drawString(100, 750, "Transaction History")  # Add title
    elements = []
    styles = getSampleStyleSheet()
    heading = Paragraph('<font color="#9B0707"><b>My Expense Tracker</b></font> - {}'.format(year), styles['Title'])
    elements.append(heading)
    # p.drawString(200, 750, "Transaction History")  
    styles = getSampleStyleSheet()
    hr = Paragraph('<b>Expenses History</b>', styles['Title'])
    elements.append(hr)

    # pt.drawString(400,500, f"mode: {select_months}")
    # Add table header
    table_data = [['Date', 'Amount', 'Category', 'Mode']]
   
    transactions = Transition.objects.filter(user = request.user,Transition_date__year =year,type = 'Expense').order_by('Transition_date') 
    for transaction in transactions:
        # Format the date
        formatted_date = transaction.Transition_date.strftime('%Y-%m-%d %H:%M')
        row = [formatted_date, transaction.amount, transaction.category, transaction.mode]
        table_data.append(row)
     
    num_columns = len(table_data[0])   
    total_width = 500  
    col_width = total_width / num_columns
    
    col_widths = [col_width] * num_columns



    # Create the table with specified column widths
    table = Table(table_data, colWidths=col_widths)

    # Apply table styles
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    
    # Add the table to the PDF document
    # elements.append(table)
    total_amount = sum(float(row[1]) for row in table_data[1:])  # Assuming amount is in the second column
    print(total_amount)
    
    # Add row with total amount
    # total_row = ['', f'Total: {total_amount}', '', '']
    # table_data.append(total_row)
  
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(style)
    elements.append(table)
    styles = getSampleStyleSheet()
    footer = Paragraph('<b>{}</b> Total Expenses'.format(total_amount), styles['Title'])
    elements.append(footer)
    # elements.append()
    hr = Paragraph('<b>-------------------------------------------------------------------------</b>', styles['Title'])
    elements.append(hr)
    # Build the PDF document----------------------------------------------------------------------
    
    q = SimpleDocTemplate(response)
    # p.drawString(100, 750, "Transaction History")  # Add title
    # elements = []
    # p.drawString(200, 750, "Transaction History")  
    styles = getSampleStyleSheet()
    hr = Paragraph('<b>Income History</b>', styles['Title'])
    elements.append(hr)

    # pt.drawString(400,500, f"mode: {select_months}")
    # Add table header
    table_data = [['Date', 'Amount', 'Category', 'Mode']]
   
    transactions = Transition.objects.filter(user = request.user,Transition_date__year =year,type = 'Income').order_by('Transition_date') 
    for transaction in transactions:
        # Format the date
        formatted_date = transaction.Transition_date.strftime('%Y-%m-%d %H:%M')
        row = [formatted_date, transaction.amount, transaction.category, transaction.mode]
        table_data.append(row)
     
    num_columns = len(table_data[0])   
    total_width = 500  
    col_width = total_width / num_columns
    
    col_widths = [col_width] * num_columns



    # Create the table with specified column widths
    table = Table(table_data, colWidths=col_widths)

    # Apply table styles
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    
    # Add the table to the PDF document
    # elements.append(table)
    total_amount = sum(float(row[1]) for row in table_data[1:])  # Assuming amount is in the second column
    print(total_amount)
    
    # Add row with total amount
    # total_row = ['', f'Total: {total_amount}', '', '']
    # table_data.append(total_row)
    
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(style)
    elements.append(table)
    styles = getSampleStyleSheet()
    footer = Paragraph('<b>{}</b> Total Incomes'.format(total_amount), styles['Title'])
    elements.append(footer)



    # ---------------------------------------------------------------------------------
   
    p.build(elements)
    
    return response


def generate_pdf_all_transaction(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transaction_history.pdf"'
    year = select_year
    
    pt = canvas.Canvas(response)

    # Create PDF document
    p = SimpleDocTemplate(response)
    # p.drawString(100, 750, "Transaction History")  # Add title
    elements = []
    styles = getSampleStyleSheet()
    heading = Paragraph('<font color="#9B0707"><b>My Expense Tracker</b></font> - {}'.format(year), styles['Title'])
    elements.append(heading)
    # p.drawString(200, 750, "Transaction History")  
    styles = getSampleStyleSheet()
    hr = Paragraph('<b>Expenses History</b>', styles['Title'])
    elements.append(hr)

    # pt.drawString(400,500, f"mode: {select_months}")
    # Add table header
    table_data = [['Date', 'Amount', 'Category', 'Mode']]
   
    transactions = Transition.objects.filter(user = request.user,Transition_date__year =year,type = 'Expense').order_by('Transition_date') 
    for transaction in transactions:
        # Format the date
        formatted_date = transaction.Transition_date.strftime('%Y-%m-%d %H:%M')
        row = [formatted_date, transaction.amount, transaction.category, transaction.mode]
        table_data.append(row)
     
    num_columns = len(table_data[0])   
    total_width = 500  
    col_width = total_width / num_columns
    
    col_widths = [col_width] * num_columns



    # Create the table with specified column widths
    table = Table(table_data, colWidths=col_widths)

    # Apply table styles
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    
    # Add the table to the PDF document
    # elements.append(table)
    total_amount = sum(float(row[1]) for row in table_data[1:])  # Assuming amount is in the second column
    print("000000000000000000000yearly0000000000000000",total_amount)
    
    # Add row with total amount
    # total_row = ['', f'Total: {total_amount}', '', '']
    # table_data.append(total_row)
  
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(style)
    elements.append(table)
    styles = getSampleStyleSheet()
    footer = Paragraph('<b>{}</b> Total Expenses'.format(total_amount), styles['Title'])
    elements.append(footer)
    # elements.append()
    hr = Paragraph('<b>-------------------------------------------------------------------------</b>', styles['Title'])
    elements.append(hr)
    # Build the PDF document----------------------------------------------------------------------
    
    q = SimpleDocTemplate(response)
    # p.drawString(100, 750, "Transaction History")  # Add title
    # elements = []
    # p.drawString(200, 750, "Transaction History")  
    styles = getSampleStyleSheet()
    hr = Paragraph('<b>Income History</b>', styles['Title'])
    elements.append(hr)

    # pt.drawString(400,500, f"mode: {select_months}")
    # Add table header
    table_data = [['Date', 'Amount', 'Category', 'Mode']]
   
    transactions = Transition.objects.filter(user = request.user,Transition_date__year =year,type = 'Income').order_by('Transition_date') 
    for transaction in transactions:
        # Format the date
        formatted_date = transaction.Transition_date.strftime('%Y-%m-%d %H:%M')
        row = [formatted_date, transaction.amount, transaction.category, transaction.mode]
        table_data.append(row)
     
    num_columns = len(table_data[0])   
    total_width = 500  
    col_width = total_width / num_columns
    
    col_widths = [col_width] * num_columns



    # Create the table with specified column widths
    table = Table(table_data, colWidths=col_widths)

    # Apply table styles
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    
    # Add the table to the PDF document
    # elements.append(table)
    total_amount = sum(float(row[1]) for row in table_data[1:])  # Assuming amount is in the second column
    print(total_amount)
    
    # Add row with total amount
    # total_row = ['', f'Total: {total_amount}', '', '']
    # table_data.append(total_row)
    
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(style)
    elements.append(table)
    styles = getSampleStyleSheet()
    footer = Paragraph('<b>{}</b> Total Incomes'.format(total_amount), styles['Title'])
    elements.append(footer)



    # ---------------------------------------------------------------------------------
   
    p.build(elements)
    
    return response
 

def generate_pdf_mykhatabook(request,year = datetime.now().year):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transaction_history.pdf"'
    month_name =  s_month
    month_name = month_name.capitalize()  # Ensure the input is in title case
    l = list(calendar.month_name).index(month_name)
    pt = canvas.Canvas(response)

    # Create PDF document
    p = SimpleDocTemplate(response)
    # p.drawString(100, 750, "Transaction History")  # Add title
    elements = []
    # p.drawString(200, 750, "Transaction History")  
    styles = getSampleStyleSheet()
    heading = Paragraph('<font color="#9B0707"><b>My Expense Tracker</b></font> - {}-{}'.format(month_name,year), styles['Title'])
    elements.append(heading)

    pt.drawString(400,500, f"mode: {month_name}")
    # Add table header
    table_data = [['Date', 'Amount', 'Category', 'Mode']]
    
    # Retrieve user's transaction history and add it to the PDF
    transactions = Transition.objects.filter(user = request.user,Transition_date__month =l,type = 'Expense',Transition_date__year = year ) 
    for transaction in transactions:
        # Format the date
        formatted_date = transaction.Transition_date.strftime('%Y-%m-%d %H:%M')
        row = [formatted_date, transaction.amount, transaction.category, transaction.mode]
        table_data.append(row)
     
    num_columns = len(table_data[0])  # Get the number of columns
    total_width = 500  # Total width of the table (adjust as needed)
    col_width = total_width / num_columns
    
    col_widths = [col_width] * num_columns



    # Create the table with specified column widths
    table = Table(table_data, colWidths=col_widths)

    # Apply table styles
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    
    # Add the table to the PDF document
    # elements.append(table)
    total_amount = sum(float(row[1]) for row in table_data[1:])  # Assuming amount is in the second column
    print("0000000000000000mykhatabook0000000000000000000",total_amount)
    
    # Add row with total amount
    # total_row = ['', f'Total: {total_amount}', '', '']
    # table_data.append(total_row)
  
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(style)
    elements.append(table)
    styles = getSampleStyleSheet()
    footer = Paragraph('<b>{}</b> Total Expenses'.format(total_amount), styles['Title'])
    elements.append(footer)
    # Build the PDF document
    p.build(elements)
    
    return response



def most_exp(request):
        repeat  = Transition.objects.filter(user = request.user,type = "Expense")
        dict = {}
        for tr in repeat:
            str = tr.category
            if str in dict:
                dict[str] += 1
            else:
                dict[str] = 1     
            

        labels = list(dict.keys())
        size = list(dict.values())
        # size.sort(reverse=True)
        # print("sorted---------",size)
        sorted_list = sorted(dict.items(), key = lambda x:x[1], reverse = True)
        print(sorted_list)
        print("--------------------------->",dict)  
        return render(request,"most_exp.html")

 
    
 

def home(request):
    return render(request,"home.html")


def user_account_details(request):
    details = Account_details.objects.all()

    return render(request ,'user_account_details.html',{'details':details})


def register(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        account = data.get('account')
        initial_balance = data.get('initial_balance')
        initial_expense = data.get('initial_expense')
        initial_income = data.get('initial_income')
        # balance = data.get('balance')

        user = request.user
        
        picture = request.FILES.get('picture')
        print(picture)
         
        
        user = User.objects.filter(username = username,first_name=first_name ,last_name = last_name )
        if user.exists():
            messages.info(request,'username already exist')
            return redirect('/register/')

        user = User.objects.create(username =username,first_name = first_name , last_name = last_name )
        
        user.set_password(password)
        user.save()
        
        # print("============================",initial_balance)
        details = Account_details.objects.create( user = user ,profile_pic = picture , account_number = account ,Account_holder = username ,current_balance  = initial_balance  , expenses = initial_expense , incomes = initial_income)
        details.save()
       
        messages.info(request, 'account created successfully')
        return redirect('/login/')
       
    
    return render(request,"authentication/register.html")


def login_page(request):
     
     if request.method == "POST":
        data = request.POST
         
        username = data.get('username')
        password = data.get('password')
        Account_number=  data.get('Account_number')

        if not User.objects.filter(username = username).exists():
            messages.error(request,'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username = username , password = password , Account_number = Account_number)
        # give a object if username and pswd is right

        if user is None:
             messages.error(request,'Invalid Password')
             return redirect('/login/')
        else:
             login(request,user)
             return redirect('/')

     return render(request,"authentication/login.html")

def logout_page(request):
    logout(request)
    return redirect("/")


# def demo2(request):
    # return render(request,"demo2.html")

 

@login_required(login_url="/login/")
def add_transition(request):
    global unique_id
    unique_id = random.randint(100000000,999999999)
    # mode = Payment_mode.objects.all()

    account_details = Account_details.objects.get(user = request.user)
    if request.method == "POST":
        data = request.POST 
        select_Transition = data.get('select_Transition')
        select_Category = data.get('select_Category')
        amount = data.get('amount')
        details = data.get('details')
        mode = data.get('Payment_mode')
        date  = data.get('date')
        user = request.user
         
        if select_Transition == "Income":
                         
            account_details.incomes +=  float(account_details.incomes) +  float(amount) 
            account_details.current_balance = float(account_details.incomes) - float(account_details.expenses)  
            account_details.save()          
             
            transition = Transition(type =select_Transition , mode = mode , amount =amount , category = select_Category , details = details ,user = user , Transition_id = unique_id ,Transition_date = date  )
        
            transition.save() 
            messages.info(request, 'Transition added successfully')
            
        else:
            account_details.expenses = float(account_details.expenses) + float(amount)

            account_details.current_balance  = float(account_details.incomes) - float(account_details.expenses)
            if account_details.current_balance < 0:
                 messages.info(request, 'insufficient Balance') 
                 return redirect('/add_transition/')
            
             
            transition = Transition(type =select_Transition , mode = mode , amount =amount , category = select_Category , details = details ,user = user , Transition_id = unique_id ,Transition_date= date)
        
            transition.save()
            messages.info(request, 'Transition added successfully') 
            redirect("/mykhatabook/") 
            
            
        account_details.save();
                      
    Icat = Icategory.objects.all()
    Ecat = Ecategory.objects.all()
    pm =  Payment_mode.objects.all()
    context = {
            'Icat':Icat,
            'Ecat':Ecat,
            'pm':pm
    }                     
    return render(request,"add_transition.html",context )

def add_income(request):
    global unique_id
    unique_id = random.randint(100000000,999999999)
    # mode = Payment_mode.objects.all()
    cate_val_sum = Icategory.objects.filter(user=request.user)
    account_details = Account_details.objects.get(user = request.user)
    if request.method == "POST":
        data = request.POST 
        select_Transition = data.get('select_Transition')
        select_Category = data.get('select_Category')
        amount = data.get('amount')
        details = data.get('details')
        mode = data.get('Payment_mode')
        date  = data.get('date')
        user = request.user
        # for cat in cate_val_sum:
        #      if cat == select_Category:
        #           cat.val = float(cat.val) + float(amount)
        # cate_val_sum.save()
        for i in cate_val_sum:
         print("-------------------------------------->",i)                  
        account_details.incomes =  float(account_details.incomes) +  float(amount)

      
        
        # total = float(inc_total) - float(exp_total)  
        account_details.current_balance = float(account_details.incomes) - float(account_details.expenses)  
        account_details.save()         
         
        transition = Transition(type =select_Transition , mode = mode , amount =amount , category = select_Category , details = details ,user = user , Transition_id = unique_id ,Transition_date = date )
        transition.save() 
        messages.info(request, 'Transition added successfully')
        return redirect('/mykhatabook/')
        

    
                       
    return HttpResponse("not found")


   
def add_expense(request):

    global unique_id
    unique_id = random.randint(100000000,999999999)
    # mode = Payment_mode.objects.all()
    account_details = Account_details.objects.get(user = request.user)
    if request.method == "POST":
        data = request.POST 
        select_Transition = data.get('select_Transition')
        select_Category = data.get('select_Category')
        amount = data.get('amount')
        details = data.get('details')
        mode = data.get('Payment_mode')
        date  = data.get('date')
        user = request.user
         
        account_details.expenses = float(account_details.expenses) + float(amount)

        account_details.current_balance  = float(account_details.incomes) - float(account_details.expenses)
        print("------------------>",account_details.current_balance)
        if account_details.current_balance  < 0 :
            messages.info(request, 'insufficient Balance') 
            return redirect('/mykhatabook/')
        
        
        transition = Transition(type =select_Transition , mode = mode , amount =amount , category = select_Category , details = details ,user = user , Transition_id = unique_id ,Transition_date = date  )
    
        transition.save()
        account_details.save()
                 
        # expense = Expense(expense_way=mode ,expense_category =select_Category , expense_amount = amount , expense_details = details ,  user = user , Transition_id = unique_id , total_expense = exp_total)
        # expense.save()
        messages.info(request, 'Transition added successfully') 
        return redirect("/mykhatabook/") 
    
                    
                    
    return HttpResponse("not found")
def add_expense_mpage(request):

    global unique_id
    unique_id = random.randint(100000000,999999999)
    # mode = Payment_mode.objects.all()
    account_details = Account_details.objects.get(user = request.user)
    if request.method == "POST":
        data = request.POST 
        select_Transition = data.get('select_Transition')
        select_Category = data.get('select_Category')
        amount = data.get('amount')
        details = data.get('details')
        mode = data.get('Payment_mode')
        date  = data.get('date')
        user = request.user
         
        account_details.expenses = float(account_details.expenses) + float(amount)

        account_details.current_balance  = float(account_details.incomes) - float(account_details.expenses)
        print("------------------>",account_details.current_balance)
        if account_details.current_balance  < 0 :
            messages.info(request, 'insufficient Balance') 
            return redirect('/all_expenses/')
        
        
        transition = Transition(type =select_Transition , mode = mode , amount =amount , category = select_Category , details = details ,user = user , Transition_id = unique_id ,Transition_date = date  )
    
        transition.save()
        account_details.save()
                 
        # expense = Expense(expense_way=mode ,expense_category =select_Category , expense_amount = amount , expense_details = details ,  user = user , Transition_id = unique_id , total_expense = exp_total)
        # expense.save()
        messages.info(request, 'Transition added successfully') 
        return redirect("/all_expenses/") 
    
                    
                    
    return HttpResponse("not found")

 
 
def update_transition(request,id):
    global unique_id
    unique_id = random.randint(100000000,999999999)
    queryset = Transition.objects.get(id=id)
    account_details = Account_details.objects.get(user = queryset.user)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>", queryset.amount)
   
    if request.method == "POST":
      

        data = request.POST 
        select_Transition = data.get('select_Transition')
        select_Category = data.get('select_Category')
        date  = data.get('date')
        amount = data.get('amount')
        details = data.get('details')
        mode = data.get('Payment_mode')
        user = request.user


        if queryset.type == "Income":
            if select_Transition == "Income":
                if (float(account_details.current_balance) - float(queryset.amount) + float(amount) )>= 0 :
                         
                         print("1111111111111111111111111111111111111",queryset.amount,amount)
                         account_details.current_balance = float(account_details.current_balance) - float(queryset.amount) + float(amount)
                         account_details.incomes = float(account_details.incomes) - float(queryset.amount) + float(amount)
                         account_details.save()
                         print("1111111111111111111111111111",account_details.current_balance)
                         queryset.category = select_Category
                         queryset.type = select_Transition
                         queryset.mode = mode
                         queryset.details = details
                         queryset.user = user
                         queryset.Transition_id = unique_id
                         queryset.Transition_date = date
                          
                         queryset.amount = amount
                         queryset.save()
                         messages.info(request, 'Transition update successfully')
                         return redirect('/mykhatabook/')
                else:
                         messages.info(request, 'insufficient income')  
                         return redirect(f"/update_transition/{queryset.id}/")
                


            else:
                if (float(account_details.current_balance) - float(queryset.amount)) >= float(amount):
                         
                         account_details.current_balance = float(account_details.current_balance) - float(queryset.amount) - float(amount)
                         account_details.incomes = float(account_details.incomes) - float(queryset.amount)
                         account_details.expenses = float(account_details.expenses) + float(amount)
                         account_details.save()
                         print("2222222222222222222222222222222222222",account_details.current_balance)
                         queryset.category = select_Category
                         queryset.type = select_Transition
                         queryset.mode = mode
                         queryset.details = details
                         queryset.user = user
                         queryset.Transition_date = date
                         queryset.Transition_id = unique_id
                         
                         queryset.amount = amount
                         queryset.save()
                         messages.info(request, 'Transition update successfully')
                         return redirect('/mykhatabook/')
                else:
                         messages.info(request, 'expense is too high according Balance')  
                         return redirect(f"/update_transition/{queryset.id}/")
                


        else:
             if select_Transition == "Expense":
                if (float(account_details.current_balance) + float(queryset.amount) ) >= float(amount)  :
                        
                         account_details.current_balance = float(account_details.current_balance) + float(queryset.amount) - float(amount)
                         account_details.expenses = float(account_details.expenses) - float(queryset.amount) + float(amount)
                         account_details.save()
                         print("111333333333333333333333333333333333333333",account_details.current_balance)
                         queryset.category = select_Category
                         queryset.type = select_Transition
                         queryset.mode = mode
                         queryset.details = details
                         queryset.user = user
                         queryset.Transition_date = date
                         queryset.Transition_id = unique_id
                          
                         queryset.amount = amount
                         queryset.save()
                         messages.info(request, 'Transition update successfully')
                         return redirect('/mykhatabook/')
                else:
                         messages.info(request, 'expense is too high according Balance')  
                         return redirect(f"/update_transition/{queryset.id}/")
                
             else:
                     
                        account_details.current_balance = float(account_details.current_balance) + float(queryset.amount) + float(amount)
                        account_details.expenses = float(account_details.expenses) - float(queryset.amount)
                        account_details.incomes = float(account_details.incomes) + float(amount)
                        account_details.save()
                        print("1144444444444444444444444444444444444444",account_details.current_balance)
                        queryset.category = select_Category
                        queryset.type = select_Transition
                        queryset.mode = mode
                        queryset.details = details
                        queryset.user = user
                        queryset.Transition_date = date
                        queryset.Transition_id = unique_id
                       
                        queryset.amount = amount
                        queryset.save()
                        messages.info(request, 'Transition update successfully')
                        return redirect('/mykhatabook/')
    
    Icat = Icategory.objects.all()
    Ecat = Ecategory.objects.all()
    pm =  Payment_mode.objects.all()
    context = {
            'Icat':Icat,
            'Ecat':Ecat,
            'pm':pm,   
           'queryset':queryset   
    }           
    return  render(request,"update_transition.html",context)
    
def update_transition_all(request,id):
    global unique_id
    unique_id = random.randint(100000000,999999999)
    queryset = Transition.objects.get(id=id)
    account_details = Account_details.objects.get(user = queryset.user)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>", queryset.amount)
   
    if request.method == "POST":
      

        data = request.POST 
        select_Transition = data.get('select_Transition')
        select_Category = data.get('select_Category')
        date  = data.get('date')
        amount = data.get('amount')
        details = data.get('details')
        mode = data.get('Payment_mode')
        user = request.user


        if queryset.type == "Income":
            if select_Transition == "Income":
                if (float(account_details.current_balance) - float(queryset.amount) + float(amount) )>= 0 :
                         
                         print("1111111111111111111111111111111111111",queryset.amount,amount)
                         account_details.current_balance = float(account_details.current_balance) - float(queryset.amount) + float(amount)
                         account_details.incomes = float(account_details.incomes) - float(queryset.amount) + float(amount)
                         account_details.save()
                         print("1111111111111111111111111111",account_details.current_balance)
                         queryset.category = select_Category
                         queryset.type = select_Transition
                         queryset.mode = mode
                         queryset.details = details
                         queryset.user = user
                         queryset.Transition_id = unique_id
                         queryset.Transition_date = date
                          
                         queryset.amount = amount
                         queryset.save()
                         messages.info(request, 'Transition update successfully')
                         return redirect('/all_transition/')
                else:
                         messages.info(request, 'insufficient income')  
                         return redirect(f"/update_transition/{queryset.id}/")
                


            else:
                if (float(account_details.current_balance) - float(queryset.amount)) >= float(amount):
                         
                         account_details.current_balance = float(account_details.current_balance) - float(queryset.amount) - float(amount)
                         account_details.incomes = float(account_details.incomes) - float(queryset.amount)
                         account_details.expenses = float(account_details.expenses) + float(amount)
                         account_details.save()
                         print("2222222222222222222222222222222222222",account_details.current_balance)
                         queryset.category = select_Category
                         queryset.type = select_Transition
                         queryset.mode = mode
                         queryset.details = details
                         queryset.user = user
                         queryset.Transition_date = date
                         queryset.Transition_id = unique_id
                         
                         queryset.amount = amount
                         queryset.save()
                         messages.info(request, 'Transition update successfully')
                         return redirect('/all_transition/')
                else:
                         messages.info(request, 'expense is too high according Balance')  
                         return redirect(f"/update_transition/{queryset.id}/")
                


        else:
             if select_Transition == "Expense":
                if (float(account_details.current_balance) + float(queryset.amount) ) >= float(amount)  :
                        
                         account_details.current_balance = float(account_details.current_balance) + float(queryset.amount) - float(amount)
                         account_details.expenses = float(account_details.expenses) - float(queryset.amount) + float(amount)
                         account_details.save()
                         print("111333333333333333333333333333333333333333",account_details.current_balance)
                         queryset.category = select_Category
                         queryset.type = select_Transition
                         queryset.mode = mode
                         queryset.details = details
                         queryset.user = user
                         queryset.Transition_date = date
                         queryset.Transition_id = unique_id
                          
                         queryset.amount = amount
                         queryset.save()
                         messages.info(request, 'Transition update successfully')
                         return redirect('/all_transition/')
                else:
                         messages.info(request, 'expense is too high according Balance')  
                         return redirect(f"/update_transition/{queryset.id}/")
                
             else:
                     
                        account_details.current_balance = float(account_details.current_balance) + float(queryset.amount) + float(amount)
                        account_details.expenses = float(account_details.expenses) - float(queryset.amount)
                        account_details.incomes = float(account_details.incomes) + float(amount)
                        account_details.save()
                        print("1144444444444444444444444444444444444444",account_details.current_balance)
                        queryset.category = select_Category
                        queryset.type = select_Transition
                        queryset.mode = mode
                        queryset.details = details
                        queryset.user = user
                        queryset.Transition_date = date
                        queryset.Transition_id = unique_id
                       
                        queryset.amount = amount
                        queryset.save()
                        messages.info(request, 'Transaction update successfully')
                        return redirect('/all_transition/')
    
    Icat = Icategory.objects.all()
    Ecat = Ecategory.objects.all()
    pm =  Payment_mode.objects.all()
    context = {
            'Icat':Icat,
            'Ecat':Ecat,
            'pm':pm,   
           'queryset':queryset   
    }           
    return  render(request,"update_transition.html",context)
# def add(request):
    # return render(request,"stylish/index.html")
def update_all_incomes(request,id):
    global unique_id
    unique_id = random.randint(100000000,999999999)
    queryset = Transition.objects.get(id=id)
    account_details = Account_details.objects.get(user = queryset.user)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>", queryset.amount)
   
    if request.method == "POST":
      

        data = request.POST 
        select_Transition = data.get('select_Transition')
        select_Category = data.get('select_Category')
        date  = data.get('date')
        amount = data.get('amount')
        details = data.get('details')
        mode = data.get('Payment_mode')
        user = request.user


        if queryset.type == "Income":
            if select_Transition == "Income":
                if (float(account_details.current_balance) - float(queryset.amount) + float(amount) )>= 0 :
                         
                         print("1111111111111111111111111111111111111",queryset.amount,amount)
                         account_details.current_balance = float(account_details.current_balance) - float(queryset.amount) + float(amount)
                         account_details.incomes = float(account_details.incomes) - float(queryset.amount) + float(amount)
                         account_details.save()
                         print("1111111111111111111111111111",account_details.current_balance)
                         queryset.category = select_Category
                         queryset.type = select_Transition
                         queryset.mode = mode
                         queryset.details = details
                         queryset.user = user
                         queryset.Transition_id = unique_id
                         queryset.Transition_date = date
                          
                         queryset.amount = amount
                         queryset.save()
                         messages.info(request, 'Transition update successfully')
                         return redirect('/all_incomes/')
                else:
                         messages.info(request, 'insufficient income')  
                         return redirect(f"/update_transition/{queryset.id}/")
                


            else:
                if (float(account_details.current_balance) - float(queryset.amount)) >= float(amount):
                         
                         account_details.current_balance = float(account_details.current_balance) - float(queryset.amount) - float(amount)
                         account_details.incomes = float(account_details.incomes) - float(queryset.amount)
                         account_details.expenses = float(account_details.expenses) + float(amount)
                         account_details.save()
                         print("2222222222222222222222222222222222222",account_details.current_balance)
                         queryset.category = select_Category
                         queryset.type = select_Transition
                         queryset.mode = mode
                         queryset.details = details
                         queryset.user = user
                         queryset.Transition_date = date
                         queryset.Transition_id = unique_id
                         
                         queryset.amount = amount
                         queryset.save()
                         messages.info(request, 'Transition update successfully')
                         return redirect('/all_incomes/')
                else:
                         messages.info(request, 'expense is too high according Balance')  
                         return redirect(f"/update_transition/{queryset.id}/")
                


        else:
             if select_Transition == "Expense":
                if (float(account_details.current_balance) + float(queryset.amount) ) >= float(amount)  :
                        
                         account_details.current_balance = float(account_details.current_balance) + float(queryset.amount) - float(amount)
                         account_details.expenses = float(account_details.expenses) - float(queryset.amount) + float(amount)
                         account_details.save()
                         print("111333333333333333333333333333333333333333",account_details.current_balance)
                         queryset.category = select_Category
                         queryset.type = select_Transition
                         queryset.mode = mode
                         queryset.details = details
                         queryset.user = user
                         queryset.Transition_date = date
                         queryset.Transition_id = unique_id
                          
                         queryset.amount = amount
                         queryset.save()
                         messages.info(request, 'Transition update successfully')
                         return redirect('/all_incomes/')
                else:
                         messages.info(request, 'expense is too high according Balance')  
                         return redirect(f"/update_transition/{queryset.id}/")
                
             else:
                     
                        account_details.current_balance = float(account_details.current_balance) + float(queryset.amount) + float(amount)
                        account_details.expenses = float(account_details.expenses) - float(queryset.amount)
                        account_details.incomes = float(account_details.incomes) + float(amount)
                        account_details.save()
                        print("1144444444444444444444444444444444444444",account_details.current_balance)
                        queryset.category = select_Category
                        queryset.type = select_Transition
                        queryset.mode = mode
                        queryset.details = details
                        queryset.user = user
                        queryset.Transition_date = date
                        queryset.Transition_id = unique_id
                       
                        queryset.amount = amount
                        queryset.save()
                        messages.info(request, 'Transaction update successfully')
                        return redirect('/all_incomes/')
    
    Icat = Icategory.objects.all()
    Ecat = Ecategory.objects.all()
    pm =  Payment_mode.objects.all()
    context = {
            'Icat':Icat,
            'Ecat':Ecat,
            'pm':pm,   
           'queryset':queryset   
    }           
    return  render(request,"update_transition.html",context)


def addextraIcategory(request):
    print("----------------------->")
    if request.method == "POST":
        data = request.POST 
        new_category = data.get('new_category')
        val = data.get('val')
        user = request.user

        cate = Icategory.objects.filter(category=new_category,user=user)
        if cate.exists():
            messages.info(request,'category already exist')
            return redirect('/mykhatabook/')
        
        category = Icategory(category=new_category , user = user,val=val) 
        category.save()
        messages.info(request, 'category added successfully') 
        return redirect('/mykhatabook/')
        
    return HttpResponse( "not found")

def addextraEcategory(request):
    print("----------------------->")
    if request.method == "POST":
        data = request.POST 
        new_category = data.get('new_category')
        val = data.get('val')
        user = request.user

        cate = Ecategory.objects.filter(category=new_category,user=user)
        if cate.exists():
            messages.info(request,'category already exist')
            return redirect('/mykhatabook/')
        
        category = Ecategory(category=new_category , user = user,val=val) 
        category.save()
        messages.info(request, 'category added successfully') 
        return redirect('/mykhatabook/')
        
    return HttpResponse( "not found")


def delete_all_transaction(request,id):
     queryset = Transition.objects.get(id=id)
     
    
     account_details = Account_details.objects.get(user = queryset.user)
   
     if queryset.type == "Expense":
     
        account_details.current_balance = float(account_details.current_balance) +  float(queryset.amount) 
        account_details.expenses  = float(account_details.expenses) - float(queryset.amount) 
        account_details.save()
         
     else:
        if  queryset.amount > account_details.current_balance:
            messages.info(request,'you can not delete, because after this your balence will go in -ve')
            return redirect('/all_transition/')
        account_details.current_balance =  float(account_details.current_balance) - float(queryset.amount)
        print("...............................",account_details.current_balance)
        account_details.incomes = float(account_details.incomes) - float(queryset.amount)
        account_details.save()
        
    
     queryset.delete()
     messages.info(request,'successfully delete')
     return redirect('/all_transition/')
     
def delete_all_incomes(request,id):
     queryset = Transition.objects.get(id=id)
     
    
     account_details = Account_details.objects.get(user = queryset.user)
   
     if queryset.type == "Expense":
     
        account_details.current_balance = float(account_details.current_balance) +  float(queryset.amount) 
        account_details.expenses  = float(account_details.expenses) - float(queryset.amount) 
        account_details.save()
         
     else:
        if  queryset.amount > account_details.current_balance:
            messages.info(request,'you can not delete, because after this your balence will go in -ve')
            return redirect('/all_incomes/')
        account_details.current_balance =  float(account_details.current_balance) - float(queryset.amount)
        print("...............................",account_details.current_balance)
        account_details.incomes = float(account_details.incomes) - float(queryset.amount)
        account_details.save()
        
    
     queryset.delete()
     messages.info(request,'successfully delete')
     return redirect('/all_incomes/')


def delete_mykhata(request,id):
     queryset = Transition.objects.get(id=id)
     
    
     account_details = Account_details.objects.get(user = queryset.user)
   
     if queryset.type == "Expense":
     
        account_details.current_balance = float(account_details.current_balance) +  float(queryset.amount) 
        account_details.expenses  = float(account_details.expenses) - float(queryset.amount) 
        account_details.save()
         
     else:
        if  queryset.amount > account_details.current_balance:
            messages.info(request,'you can not delete, because after this your balence will go in -ve')
            return redirect('/mykhatabook/')
        account_details.current_balance =  float(account_details.current_balance) - float(queryset.amount)
        print("...............................",account_details.current_balance)
        account_details.incomes = float(account_details.incomes) - float(queryset.amount)
        account_details.save()
        
    
     queryset.delete()
     messages.info(request,'successfully delete')
     return redirect('/mykhatabook/')


def addextraPaymode(request):
    if request.method == "POST":
        data = request.POST 
        new_pay_mode = data.get('new_pay_mode')
        val = data.get('val')
        user = request.user
        print("-------------------------------------->",new_pay_mode)
        pmode = Payment_mode.objects.filter(payment_type=new_pay_mode,user=user)
        if pmode.exists():
            messages.info(request,'paymentmode already exist')
            return redirect('/mykhatabook/')
        
        payment = Payment_mode(payment_type=new_pay_mode , user = user,val=val) 
        payment.save()
        messages.info(request, 'payment_mode added successfully') 
        return redirect('/mykhatabook/')
        

    return HttpResponse( "not found")
         
@login_required(login_url="/login/")
def results(request,year = datetime.now().year , month = datetime.now().strftime('%B')):
    # ,year = datetime.now().year , month = datetime.now().strftime('%B')
    # month_naam = 0
    # if request.method == 'POST':
    #     data = request.POST
    #     select_month = data.get('select_month')
    #     month_naam = select_month
    # month = month.capitalize()
    # month_number = list(calendar.month_name).index(month)
    # month_number = int(month_number)
    

    str = ""
    dict3 = {}
    transitions = Transition.objects.filter(user  = request.user)[::-1]
    # for t in transitions:
    #      print("-----------date--------------------------",t.Transition_date)
    # queryset = Transition.objects.all()
    ttt = Transition.objects.filter(user = request.user , type = 'Expense')
    if ttt:
        if request.GET.get('search'):
            # n = request.GET.get('search')
            month_name =  request.GET.get('search')
            month_name = month_name.capitalize()  # Ensure the input is in title case
            l = list(calendar.month_name).index(month_name)
            print ("---------------------=====================",l)
                    
            transitions = transitions.filter(Transition_date__month__icontains = l)
  
        elif len(transitions)==0:
            messages.info(request, "you have no expenses in this month")
            return redirect('/results/')
    # tr = Transition.objects.filter(user = request.user).first()
    


 
   
    # global total  
    # total = 0
    # exp_total = 0
    # inc_total = 0
    account_details = Account_details.objects.get(user=request.user)
    # # income = Income.objects.filter(user=request.user).first()
    # # expense = Expense.objects.filter(user=request.user).first()
    exp_total = account_details.expenses
    inc_total  =  account_details.incomes
    total = account_details.current_balance
    # exp_total = exp_total
    # queryset = Transition.objects.all()

    transition = Transition.objects.filter(user = request.user)
    user_category = Ecategory.objects.filter(user = request.user)
   
    str = ""
    v = 0
    # j = 0
    dict = {}
    # dates = transition['Transition_date'].to_numpy()
    for i in user_category:
        for tr in transition:
            if i.category == tr.category:
            #    print("----------------",tr.category,"---------------------------->",i.category)
          
               i.val   += float(tr.amount)
         
       
        v = i.val
        str  = i.category
        if str in dict:
            dict.update(v)
        else:
            dict[str] = v    
         
    print(dict)
    for key in list(dict.keys()):
      if dict[key] == 0.0:
         del dict[key]
    print(dict)     
    lab = list(dict.keys())
    siz = list(dict.values())
    print(lab)
    print(siz)
  
    fig1, ax1 = plt.subplots()
    plt.title("Total Expences Ratio")
    plt.switch_backend('agg')
    ax1.pie(siz, labels=lab, autopct='%1.1f%%',radius=1.5 , startangle=90,shadow=True,wedgeprops={'linewidth':1})
    ax1.pie([0.2],colors='w')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Saving the chart as an image file
    plt.savefig('main/static/total.png',dpi = 100)
    
    context = {}
    
   
    repeat_demo  = Transition.objects.filter(user = request.user,type = "Expense")
    demo_dict = {}
    list_demo = []
    # for tr in repeat_demo:
    #         str = tr.category
    #         list_demo.append(str)

    # label = unique(list_demo)        
    # print("------------",label)
#    ----------------------------------------------------------------------
    for tr in repeat_demo:
            str = tr.category
            amt = tr.amount
            if str in demo_dict:
               common_values = [demo_dict[str][0]+float(amt),demo_dict[str][1]+1]

               demo_dict[str] = common_values

            else:
                 common_values = [float(amt) , 1]
                 demo_dict[str] = common_values

    sorted_list2 = sorted(demo_dict.items(), key = lambda x:x[1], reverse = True)           
    print("-------------------system-----------",sorted_list2)   

    for l in sorted_list2:
         print("-------------demo------------------",l[0],"------------" , l[1][0],"-----------"  , l[1][1])
    
    
    
    Icat = Icategory.objects.all()
    Ecat = Ecategory.objects.all()
    pm =  Payment_mode.objects.all()
    context = {
            # 'graph':graph,
            'Icat':Icat,
            'Ecat':Ecat,
            'pm':pm,
            'exp_total':exp_total ,'inc_total':inc_total , 'total':total  , 'transitions':transitions,'sorted_list':sorted_list2,
    }  

    print("---------------------------->",total)
    return render(request,"results.html", context)
 
def mykhatabook(request,year = datetime.now().year , month = datetime.now().strftime('%B')):
    Icat = Icategory.objects.all()
    Ecat = Ecategory.objects.all()
    pm =  Payment_mode.objects.all()
    account_details = Account_details.objects.filter(user = request.user).first()
    exp_total = account_details.expenses
    inc_total = account_details.incomes
    total = account_details.current_balance
    global s_month
    s_month = month
    month_total = 0
    
    month_income = 0
    if request.method =='POST':
         data = request.POST
         s_month = data.get('select_month')
 
    expenses = Transition.objects.filter(user = request.user)
    
    month_dict = {}
    lst = []
    siz = []
    title_val = s_month
    title_val += " month exp. "
    month_name =  s_month
    month_name = month_name.capitalize()  # Ensure the input is in title case
    l = list(calendar.month_name).index(month_name)
    expenses = expenses.filter(Transition_date__month =l,type = 'Expense',Transition_date__year=year)
    for tr in expenses:
            str = tr.category
            amt = tr.amount
            month_total += float(amt)
            if str in month_dict:
               common_values = [month_dict[str][0]+float(amt),month_dict[str][1]+1]

               month_dict[str] = common_values

            else:
                 common_values = [float(amt) , 1]
                 month_dict[str] = common_values
    # print(Ecat,"------>")
    # print(month_dict)
    sorted_list2 = sorted(month_dict.items(), key = lambda x:x[1], reverse = True)
     
    
  
    for key, (value1, value2) in  month_dict.items():
       siz.append(value1)
       lst.append(key)
     
    fig1, bx1 = plt.subplots()
    
    # plt.title(title_val)
    # plt.legend(labels=lab, loc="best") 
    bx1.pie(siz, labels=lst, autopct='%1.1f%%',radius=1.5 , startangle=90,shadow=True,wedgeprops={'linewidth':1})
    bx1.text(0, 0, s_month, ha='center', va='center', fontsize=16, fontweight='bold')
    bx1.pie([0.2],colors='w')
    plt.tight_layout()

    bx1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('main/static/mykhatabook_month.png',dpi = 100)
    dif = 0

    transactions  = Transition.objects.filter(user=request.user , Transition_date__year=year,type="Income",Transition_date__month =l)
    for tr in transactions:
         month_income += float(tr.amount)
    print(month_total)
    print(month_income)
    percent = 0
    per = 0
    # if month_income == 0:
    #        messages.info(request, "you have no Income in this month")
    #        return redirect('/mykhatabook/')
    monthly_balance = month_income - month_total
    if month_total > 0 and month_income > 0:
       percent = ((month_total*100)/month_income)
       percent = round(percent, 2)
    #    percent = format(percent,'.2f')  
    # percent = per   
    print("========----------------=========",percent)
    ttt = Transition.objects.filter(user=request.user)
    ecat = Ecategory.objects.filter(user=request.user)
          
    expenses_by_category = expenses.values('category').annotate(total_amount=Sum('amount'), freq = Count('category')) 

    total_expense = sum(item['total_amount'] for item in expenses_by_category)
    num_categories = len(expenses_by_category)
    # distributed_amount = total_expense / num_categories
    # # for item in expenses_by_category:
    # #     category = item['category']
    # #     distributed_amount = item['total_amount'] 
    # #     freq = item['freq']
    # #     print("11111111111111111",category)
    # #     print("22222222222222222",distributed_amount)
    # #     print("22222222222222222",freq)


    # # print(".....................",total_expense)
    # # print(">>>>>>>>>>>>>>",num_categories)
    # # print(">>>>>>>>>>>>>>",expenses_by_category)

    # # for cat in Ecat:
    # #      c = cat.category
    # #      if c  in month_dict:
    # #           value = month_dict[c]
    # #           print(cat)
    # #           print("val-----------",value[0])
    # #           print("val2---------",value[1])
              


    context = {
         'pm':pm,
         'dif':dif,
         'Ecat':Ecat,
         'total':total,
         'year':year,
         'Icat' : Icat,
         'ecat':ecat,
         'percent': percent,
         's_month':s_month,
         'expenses':expenses,
         'exp_total':exp_total, 
         'inc_total':inc_total,
         'month_dict':month_dict,  
         'month_total':month_total,
         'month_income':month_income,
         'monthly_balance':monthly_balance,
         'sorted_list2':sorted_list2,
         'expenses_by_category':expenses_by_category
        
          

    }

    return render(request,"mykhatabook.html",context)


def all_trans_category(request,id):
     return render(request,"all_trans_category.html")

def demo(request):
    if request.method == "POST":
         data = request.POST
         u_name = data.get("name")
         u_email = data.get("email")
         u_phonne = data.get("phone")
         u_message = data.get("message")


         user_data = contact.objects.create(name = u_name,  user_email = u_email , phone_number = u_phonne , description = u_message)
         user_data.save()
         messages.info(request,"Thanku for response")





    return render(request,"demo.html")

def all_incomes(request):
    income = Transition.objects.all()
    inc_total = 0
    
    account_details = Account_details.objects.get(user = request.user)
    inc_total = float(account_details.incomes)
    

    return render(request,"all_incomes.html",{'income':income , 'inc_total':inc_total})

# def expense(request):
    # user_id = request.user.id
    # expense = Transition.objects.all()
    # exp_total = 0
    # for e in expense:
    #     if request.user.is_authenticated : 
    #         if e.user_id == request.user.id:  
    #              if e.type == "Expense":
    #                exp_total -= e.expense_amount    
    # print("-------------------------------------->",exp_total)
    # return render(request,"expense.html",{'expense':expense , 'user_id':user_id , 'exp_total' : exp_total})

def all_expenses(request,year = datetime.now().year , month = datetime.now().strftime('%B')):
    user_id = request.user.id
    # expense = Transition.objects.all()
    account_detail = Account_details.objects.get(user = request.user)
    exp_amt = float(account_detail.expenses)
    print("--------exp---------------------",exp_amt)
    expense = Transition.objects.filter(user  = request.user)
    global select_months
    select_months = month
    account_details = Account_details.objects.get(user = request.user) 
    exp_total = account_details.expenses
    if request.method == 'POST':
        data = request.POST
        select_months = data.get('select_month')
    exp_total = 0
     
    dict3 = {}
    import calendar
    
    title_val = select_months
    title_val += " month exp. "
    month_name =  select_months
    month_name = month_name.capitalize()  # Ensure the input is in title case
    l = list(calendar.month_name).index(month_name)
    print ("---------------------=====================",l)
    # month_nm = request.GET.get('search')
    # month_number = get_month_number(month_nm)
    str = ""
    val = 0
    expense = expense.filter(Transition_date__month =l,type = 'Expense',Transition_date__year=year)
    for tr in expense:
        
        str = tr.category
        val = tr.amount
        if str in dict3:
             dict3[str]  += float(val)

        else:
            dict3[str] = float(val)
    for key in list(dict3.keys()):
            if dict3[key] == 0.0:
                del dict3[key]  
    # print(dict3)  
    lab = list(dict3.keys())
    if exp_amt>0:
       if len(lab) == 0:
            messages.info(request, "you have no Expenses in "+ select_months) 
            return redirect("/all_expenses/")  

    print("==========--------------------->",dict3)           
    siz = list(dict3.values())
    fig1, bx1 = plt.subplots()
    
    plt.title(title_val)
    # plt.legend(labels=lab, loc="best") 
    bx1.pie(siz, labels=lab, autopct='%1.1f%%',radius=1.5 , startangle=90,shadow=True,wedgeprops={'linewidth':1})
    bx1.pie([0.2],colors='w')
    plt.tight_layout()

    bx1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('main/static/ch.png',dpi = 100)

    for exp in expense:
        exp_total += float(exp.amount)
    if select_months == "":
        expense = Transition.objects.filter(user  = request.user)
        exp_total = account_details.expenses

      
    Ecat = Ecategory.objects.all()
    pm =  Payment_mode.objects.all()


    print("-----------exp2------------",exp_amt)
    return render(request,"all_expenses.html",{'expense':expense , 'user_id':user_id , 'exp_total' : exp_total,'select_months':select_months,'exp':exp_amt, 'Ecat':Ecat,
            'pm':pm,})
# @cache_page(60 * 1)
def histogram(request,year = datetime.now().year , month = datetime.now().strftime('%B')):
    global year_name
    account_details = Account_details.objects.filter(user = request.user).first()
    expense = account_details.expenses
    income = account_details.incomes
    balance = account_details.current_balance
    ttt = Transition.objects.filter(user = request.user )
    year_name = str(year)
    if ttt:
        if request.GET.get('search'):
            # n = request.GET.get('search')
            year_name =  request.GET.get('search')
            # year_name = year_name.capitalize()  # Ensure the input is in title case
            # l = list(calendar.year_name).index(year_name)
            # print ("---------------------=====================",l)
                    
            transitions = ttt.filter(Transition_date__year__icontains = year_name)
  
            if len(transitions)==0:
                messages.info(request, "you have no Transactions in " + year_name)
                return redirect('/histogram/')
    nvalue = 0
    
    dict = {}
    # dict1 = {}
    dict2  = {}
    for i in range(13):
    #    nvalue = month_number  - i 
       sum_monthly = 0
       sum_inc = 0
    #    if nvalue <= 0 :
    #      nvalue = nvalue + 12 
       if i == 0:
             continue
       transition = Transition.objects.filter(user=request.user,Transition_date__year = year_name, Transition_date__month = i , type = 'Expense')
       for tr in transition:
         
                print("............................yes.............",tr.category,"..............",tr.Transition_date)
                # print(month_number)
                sum_monthly += float(tr.amount)
       dict[i] = sum_monthly
       transition2 = Transition.objects.filter(user=request.user,Transition_date__year = year_name, Transition_date__month = i , type = 'Income')
       for tr in transition2:
         
              
                sum_inc += float(tr.amount)
       dict2[i] = sum_inc   
    months = ['Jan' , 'Feb' , 'Mar' , "Apr" , 'May' , 'June' , 'July' , 'Aug' , 'Sep' , 'Oct' , 'Nov' , 'Dec']
    expenses = list(dict.values())
    incomes = list(dict2.values())

    xpos= np.arange(len(months))
    ypos = np.arange(len(incomes))
    plt.xticks(ypos,months)
    # plt.ylabel()
    #    income
    # width = 0.4
    print(months)
    plt.bar(xpos-0.2, expenses,width = 0.4, color='red' , alpha = 0.7 , label = 'Expenses')
    plt.bar(xpos+0.2,incomes,width=0.4, color='blue' ,alpha = 0.2 , label = 'Incomes')
    
    plt.xlabel('Months')
    plt.ylabel('Amount (rupee)')
    plt.title(year_name +' Annually Expenses details')
    plt.legend()
    plt.tight_layout()
    
    buffer = BytesIO()
    # plt.switch_backend('agg')
    plt.savefig(buffer, format='png')
    plt.close()
    graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
    # plt.savefig('main/static/pie_chart.png',dpi = 100)
    #  return render(request,"")
    return render(request,"histogram.html",{'graph':graph,'income':income , 'expense':expense , 'balance':balance})




def all_transition(request,year = datetime.now().year , month = datetime.now().strftime('%B')):
    global select_year
    select_year = str(year)
    ecat = Ecategory.objects.filter(user=request.user)
    print(ecat)
    transitions = Transition.objects.filter(user = request.user,type='Expense' )
    # year_name = str(year)
    if transitions:
        if request.GET.get('search'):
            # n = request.GET.get('search')
            select_year =  request.GET.get('search')
            # year_name = year_name.capitalize()  # Ensure the input is in title case
            # l = list(calendar.year_name).index(year_name)
            # print ("---------------------=====================",l)
                    
            transitions = transitions.filter(Transition_date__year__icontains = select_year)[::-1]
  
            if len(transitions)==0:
                messages.info(request, "you have no Transactions in " + select_year)
                return redirect('/all_transition/')
    # if request.GET.get('search'):
    #         # n = request.GET.get('search')
    #         select_year =  request.GET.get('search')
    
    # transitions = Transition.objects.filter(user=request.user,Transition_date__year = select_year)[::-1]

    user_category = Ecategory.objects.filter(user = request.user)
   
    str1 = ""
    v = 0
    # j = 0
    dict = {}
    # dates = transition['Transition_date'].to_numpy()
    # print("-------------------len-------------",len(user_category))
    if len(user_category)>0:
        for i in user_category:
            for tr in transitions:
                if i.category == tr.category:
                #    print("----------------",tr.category,"---------------------------->",i.category)
            
                   i.val   += float(tr.amount)
            
        
            v = i.val
            str1  = i.category
            if str1 in dict:
                dict.update(v)
            else:
                dict[str1] = v    
            
        # print(dict)
        for key in list(dict.keys()):
          if dict[key] == 0.0:
              del dict[key]
        print("11111111111111111111111111111111111111111111111",dict)     
        lab = list(dict.keys())
        siz = list(dict.values())
        # print(lab)
        # print(siz)
    
        fig1, ax1 = plt.subplots()
        plt.title("Total Expences Ratio")
        plt.switch_backend('agg')
        ax1.pie(siz, labels=lab, autopct='%1.1f%%',radius=1.5 , startangle=90,shadow=True,wedgeprops={'linewidth':1})
        ax1.text(0, 0, select_year, ha='center', va='center', fontsize=16, fontweight='bold')
        ax1.pie([0.2],colors='w')
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Saving the chart as an image file
        plt.savefig('main/static/all_year.png',dpi = 100)
    
    

    data = []
    for transaction in transitions:
        data.append([transaction.id, transaction.user.username,transaction.type,transaction.category, transaction.amount, transaction.Transition_date])

    # Create DataFrame
    df = pd.DataFrame(data, columns=['Transaction ID', 'User','Type','Category' ,'Amount', 'Date'])

    categories = df['Category'].unique()
    

    for category in categories:
        category_data = df[df['Category'] == category]
        category_counts = category_data['Category'].value_counts()
    title_val = select_year
    title_val += " Most Used category"
    dataframe = df['Category'].value_counts().plot(kind='bar')
    data1 = df['Category'].value_counts()
    plt.figure(figsize=(8,5))
    data1.plot(kind='bar')
    plt.title(title_val) 
    plt.xlabel('Category')
    plt.ylabel('Repeat time')
    # for i, v in enumerate(category_counts):
    #     ax.text(i, v + 0.1, str(v), color='black', ha='center')
    # for i, v in enumerate(category_counts):
    #     plt.hlines(y=v, xmin=-0.4, xmax=i, linestyles='dotted', colors='black')
    plt.tight_layout()
    plt.savefig('main/static/cat_yearly.png')
    
    context = {
         'transitions':transitions,
         'year':select_year,
         'ecat':ecat,
         'dict':dict,



    }
    return render(request,"all_transition.html",context)


# def all_transitions(request):
#     transitions = Transition.objects.all()
#     global total  
#     total = 0
#     exp_total = 0
#     inc_total = 0
#     # income = Income.objects.all()
#     # expense = Expense.objects.all()
#     for i in transitions: 
#         if request.user.is_authenticated : 
#             if i.user_id == request.user.id: 
#                   if e.type == "Income":
#                      inc_total += i.income_amount 
    
     
#     for e in transitions:
#         if request.user.is_authenticated : 
#             if e.user_id == request.user.id:
#                    if e.type == "Expense":  
#                         exp_total -= e.expense_amount    

#     total = inc_total + exp_total    
#     exp_total = -exp_total
#     print("===================>",total)
#     return render(request,"all_transitions.html",{'transitions':transitions , 'total':total})