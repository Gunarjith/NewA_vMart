from django.contrib import admin
from django.urls import path, include

from B_campaign import views
#
urlpatterns = [

    path('', views.Bcampaign, name='Bcampaign'),


    # path('campaign',views.payment,name='payment'),
    # path('payment2', views.payment2, name='payment2'),
    # path('paymentdone',views.payment_done,name='paymentdone'),
    # path('paymenthis',views.payment_history,name='paymenthis')
    path('campaignList', views.listCampaign, name='campaignList'),
    path('campaignList/<int:id>/', views.listCampaign, name='campaignList'),
    path('addBCampaign', views.addBCampaign, name='addBCampaign'),
    path('addBCampaign/<int:id>/', views.addBCampaign, name='addBCampaign'),
    
    path('addBCampaignSubmit', views.addBCampaignSubmit, name='addBCampaignSubmit'),
    path('updateBCamaign' , views.updateBCamaign, name='updateBCamaign'),
    path('subUpdateBCamaign/<int:id>/', views.subUpdateBCamaign, name='subUpdateBCamaign'),
    path('assignBCampaign/<int:id>/',
         views.assignBCampaign, name='assignBCampaign'),
#     path('templateBCampaign/<int:id>/', views.templateBCampaign, name='templateBCampaign'),
#     path('templateBCampaignmkNo/<int:id>/', views.templateBCampaignmkNo, name='templateBCampaignmkNo'),

    path('sendgroupcampaign', views.sendgroupcampaign, name='sendgroupcampaign'),
    path('addcampaignbtn', views.addcampaignbtn, name='addcampaignbtn'),
    path('addcampaignbtn/<int:id>/', views.addcampaignbtn, name='addcampaignbtn'),
#     path('addTempleteBtn/<int:id>/', views.addTempleteBtn, name='addTempleteBtn'),
    path('addBtnBCampaignSubmit/<int:id>', views.addBtnBCampaignSubmit, name='addBtnBCampaignSubmit'),
     path('updateBtnBCamaign/<int:id>/', views.updateBtnBCamaign, name='updateBtnBCamaign'),

     path('B_campaign/updateBCamaign/<int:id>/', views.updateBCamaign, name='updateBCamaign'),
     # path('B_campaign/updateBCamaign/<int:id>/', views.updateBCamaign, name='updateBCamaign'),

    path('subUpdateBtnBCamaign/<int:id>/',
         views.subUpdateBtnBCamaign, name='subUpdateBtnBCamaign'),

    path('deleteBtnBCampaign/<int:id>/',
         views.deleteBtnBCampaign, name='deleteBtnBCampaign'),

    path('deleteBCampaign/<int:id>/',
         views.deleteBCampaign, name='deleteBCampaign'),
#     path('pulishBCampaignList/<int:campaign_info_id>/',
#          views.moveBCampaignList, name='pulishBCampaignList'),

    path('addcampForm/', views.addcampForm, name='addcampForm'),
    path('addcampMarketPlace/', views.addcampMarketPlace, name='addcampMarketPlace'),
    path('submitcamp', views.submitcamp, name='submitcamp'),
    path('updateCampMarketPlace/<int:id>/',
         views.updateCampMarketPlace, name='updateCampMarketPlace'),

     path('add_customer/', views.add_customer, name='add_customer'),
     path('submitcustomer/', views.submitcustomer , name='submitcustomer'),


    path('editcampMarketPlace/<int:id>/',
         views.editcampMarketPlace, name='editcampMarketPlace'),
    path('deleteCampMarketPlace/<int:id>/',
         views.deleteCampMarketPlace, name='deleteCampMarketPlace'),
     path('camppayment/<int:id>/',  views.camppayment, name='camppayment'),
    path('camppayment_page/<int:id>/', views.camppayment_page, name='camppayment_page'),
     path('GenerateCampId/<int:id>/', views.GenerateCampId, name='GenerateCampId'),
     path('GenerateCampkey/<int:id>/', views.GenerateCampkey, name='GenerateCampkey'),
     path('generateCampKeyBarcode/<int:id>/', views.generateCampKeyBarcode, name='generateCampKeyBarcode'),
     path('GeneratecampIdBar/<int:id>/', views.GeneratecampIdBar, name='GeneratecampIdBar'),
     path('historyCampaign/<int:id>/', views.historyCampaign, name='historyCampaign'),
     path('historyCampaign/', views.historyCampaign, name='historyCampaign'),
    path('createtemplate/<int:id>/',views.createtemplate,name='createtemplate'),
    path('sendcampaign/',views.sendcampaign,name='sendcampaign'),
    path('delete_selected_contacts/', views.delete_selected_contacts, name='delete_selected_contacts'),
#     path('sendCampaigndata/<int:id>/', views.sendCampaign, name='sendCampaigndata'),
    path('createdynamicform', views.createdynamicform, name='createdynamicform'),
     path('forminfo', views.forminfo, name='forminfo'),
     path('update_form/<int:form_id>/', views.update_form, name='update_form'),
     path('create_form/<int:id>/', views.create_form, name='create_form'),
     path('create_form/', views.create_form, name='create_form'),

     path('submitform/', views.submitform, name='submitform'),
     path('addsection/<int:id>/', views.addsection, name='addsection'),
     path('save_form_data/', views.save_form_data, name='save_form_data'),
    #  path('save-form-data/', views.save_form_data, name='save_form_data'),s
     path('form/<int:form_id>/', views.view_form_details, name='view_form_details'),
     path('inflowaoutflowconfig/', views.inflowaoutflowconfig, name='inflowaoutflowconfig'),
     path('setupdetails', views.setupdetails, name='setupdetails'),
     path('addparent/', views.addparent, name='addparent'),
     path('editdynamicform/<int:id>/', views.editdynamicform, name='editdynamicform'),
     path('deteleform/<int:id>/', views.deteleform, name='deteleform'),
     path('generateform/<int:id>/', views.generateform, name='generateform'),
     path('submitparentdata/', views.submitparentdata, name='submitparentdata'),
     path('addchiled/<int:id>/', views.addchiled, name='addchiled'),
     path('submitchailddata/<int:id>/', views.submitchailddata, name='submitchailddata'),
     path('editinflowsetup/<int:id>/', views.editinflowsetup, name='editinflowsetup'),
     path('deleteparent/<int:id>/', views.deleteparent, name='deleteparent'),
     path('editsubmitflowdata/<int:id>/', views.editsubmitflowdata, name='editsubmitflowdata'),
     path('contactlist/', views.contactlist, name='contactlist'),
     path('excel_customers1', views.excel_customers1, name='excel_customers1'),
     path('addcustomer/', views.addcustomer, name='addcustomer'),
     path('editcustomerdata/<int:id>', views.editcustomerdata, name='editcustomerdata'),
     path('updatecustomer/<int:id>/', views.updatecustomer, name='updatecustomer'),
     path('deletecustomer/<int:id>/', views.deletecustomer, name='deletecustomer'),
     path('footprint/', views.footprint, name='footprint'),
     path('search_results/', views.search_results, name='search_results'),
     path('addcomgroup/', views.addcomgroup, name='addcomgroup'),
     path('addgroups/', views.addgroups, name='addgroups'),
     path('insrtuctions/', views.insrtuctions, name='insrtuctions'),
     path('submitgrouptype/', views.submitgrouptype, name='submitgrouptype'),
     path('editgroupdata/<int:id>/', views.editgroupdata, name='editgroupdata'),
     path('updatesubmitgrouptype/<int:id>/', views.updatesubmitgrouptype, name='updatesubmitgrouptype'),
     path('detelegroup/<int:id>/', views.detelegroup, name='detelegroup'),
     path('numbermapping/<int:id>/', views.numbermapping, name='numbermapping'),
     path('pulishBCampaignList/<int:id>/', views.moveBCampaignList, name='moveBCampaignList'),
     path('deleteBCampaignList/<int:id>/', views.deleteBCampaignList, name='deleteBCampaignList'),
     path('formconfig', views.formconfig, name='formconfig'),
     path('formdata/', views.formdata, name='formdata'),
     path('getformdata', views.getformdata, name='getformdata'),
     path('eupdate_form/<int:form_id>/', views.eupdate_form, name='eupdate_form'),
     path('dashbord/', views.dashbord, name='dashbord'),
     path('preview/<int:id>/', views.preview, name='preview'),
    path('templatestatus/<int:id>/', views.templatestatus, name='templatestatus'),
]


