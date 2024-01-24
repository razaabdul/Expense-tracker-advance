from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import graph_view

urlpatterns = [
    path('',  views.home , name ='home' ),
    path('login/' , views.login_page ,  name = "login_page"),
    path('register/' , views.register ,  name = "register"),
    path('logout/' , views.logout_page , name = "logout_page"),
    path('add_transition/',views.add_transition , name = "add_transition") ,
  
    path('all_expenses/' , views.all_expenses  ,name ='all_expenses'),
    path('all_incomes/' , views.all_incomes  ,name ='all_incomes'),
    path("all_transition/" , views.all_transition , name = 'all_transition'),
    # path('demo2/' , views.demo2 ,name = 'demo2' ),
    path('results/' , views.results ,name = 'results' ),
    path('addextraPaymode/',views.addextraPaymode , name='addextraPaymode'),
    path('addextraEcategory/' , views.addextraEcategory , name ='addextraEcategory'),
    path('addextraIcategory/' , views.addextraIcategory , name ='addextraIcategory'),
    path('delete_all_transaction/<id>/' , views.delete_all_transaction , name = "delete_all_transaction"),
    path('delete_mykhata/<id>/' , views.delete_mykhata , name = "delete_mykhata"),
    path('delete_all_incomes/<id>/' , views.delete_all_incomes , name = "delete_all_incomes"),
    path('add_expense/' , views.add_expense , name = 'add_expense'),
    path('add_expense_mpage/' , views.add_expense_mpage , name = 'add_expense_mpage'),
    path('add_income/' , views.add_income , name = 'add_income'),
    path('update_transition/<int:id>/' , views.update_transition , name = 'update_transition'),
    path('update_transition_all/<int:id>/' , views.update_transition_all , name = 'update_transition_all'),
    path('update_all_incomes/<int:id>/' , views.update_all_incomes , name = 'update_all_incomes'),
    # path('graph/', graph_view, name='graph'),
    # path('pie_chart/', views.generate_pie_chart, name='pie_chart'),
    # path('filter_by_month/<int:month>/', views.filter_by_month_view, name='filter_by_month'),
    # path('user_info/', views.user_info, name='user_info'),
    # path('histo/', views.histo, name='histo'),
    path('most_exp/', views.most_exp, name='most_exp'),
    path('contact_Us/' , views.demo , name = 'demo'),
    path('histogram/', views.histogram, name='histogram'),
    path('generate_pdf/',views.generate_pdf, name='generate_pdf'),
    path('generate_pdf_yearly/',views.generate_pdf_yearly, name='generate_pdf_yearly'),
    path('generate_pdf_mykhatabook/',views.generate_pdf_mykhatabook, name='generate_pdf_mykhatabook'),
    path('generate_pdf_all_transaction/',views.generate_pdf_all_transaction, name='generate_pdf_all_transaction'),
    path('run/',views.run, name='run'),
    path('profile/',views.profile, name='profile'),
    path('change_photo/<id>/',views.change_photo, name='change_photo'),
    path('delete_Ecat/<id>/',views.delete_Ecat, name='delete_Ecat'),
    path('delete_Icat/<id>/',views.delete_Icat, name='delete_Icat'),
    path('delete_pmode/<id>/',views.delete_pmode, name='delete_pmode'),
    path('Icat_wise/<id>/',views.Icat_wise, name='Icat_wise'),
    path('Ecat_wise/<id>/',views.Ecat_wise, name='Ecat_wise'),
    path('pay_wise/<id>/',views.pay_wise, name='pay_wise'),
    # path('generate_csv/', views.generate_csv, name='generate_csv'),
    path('process_csv/', views.process_csv, name='process_csv'),
    path('mykhatabook/', views.mykhatabook, name='mykhatabook'),
    path('all_trans_category/<id>/', views.all_trans_category, name='all_trans_category'),
    path('monthly_cate_mykhata/<id>/', views.monthly_cate_mykhata, name='monthly_cate_mykhata'),

]
if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)