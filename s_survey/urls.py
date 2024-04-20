from django.contrib import admin
from django.urls import path,include


from s_survey import views

#
urlpatterns = [
     # for marketplace_id
     path('marketplace', views.marketplace, name='marketplace'),
     path('addSurveygroup', views.addSurveygroup, name='addSurveygroup'),
     path('submitSurveyGroupsForm', views.submitSurveyGroupsForm, name='submitSurveyGroupsForm'),
     path('editsurveygroup/<int:id>/', views.editsurveygroup, name='editsurveygroup'),
     path('submiteditsurveygroup/<int:id>/', views.submiteditsurveygroup, name='submiteditsurveygroup'),
     path('deletemarketplace/<int:id>/', views.deletemarketplace, name='deletemarketplace'),


     path('surveyList',views.surveyList,name='surveyList'),
     path('surveyList/<int:id>/', views.surveyList, name='surveyList'),





     path('addSurvey', views.addSurvey, name='addSurvey'),

     path('addSurveySubmit',views.addSurveySubmit,name='addSurveySubmit'),

     path('addSurveySubmit/<int:id>/',views.addSurveySubmit,name='addSurveySubmit'),
     
     path('updateSurvey/<int:id>/',views.updateSurvey,name='updateSurvey'),
     path('assignSuveyCustomer/<int:id>/',views.assignSuveyCustomer,name='assignSuveyCustomer'),
     path('subUpdateSurvey/<int:id>/',
          views.subUpdateSurvey, name='subUpdateSurvey'),
     path('deleteSurvey/<int:id>/', views.deleteSurvey, name='deleteSurvey'),
     # path('updateSurveyType/',views.updateSurveyType,name='updateSurveyType'),
     path('survey_question/<int:id>/', views.survey_question_view, name='survey_question'),
     path('deleteAssigned/<int:id>/', views.deleteAssigned, name='deleteAssigned'),
     path('moveSelectedCustomers/<int:survey_id>/', views.moveSelectedCustomers, name='moveSelectedCustomers'),
     # path('assign-survey-customer/<int:id>/', views.assignSurveyCustomer, name='assignSurveyCustomer'),
     path('genericsurvey',views.genericsurvey,name='genericsurvey'),
     path('specificsurvey',views.specificsurvey,name='specificsurvey'),
     path('mysurvey',views.mysurvey,name='mysurvey')
]
