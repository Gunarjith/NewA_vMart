from django.contrib import admin
from django.urls import path
from K_Ticket import views


urlpatterns = [
    path('eventmaster/', views.eventmaster, name='eventmaster'),
    path('pulishCampaignList/<int:campaign_info_id>/',
         views.moveCampaignList, name='pulishCampaignList'),
    path('updateEventStatus/<int:event_id>/',
         views.updateEventStatus, name='updateEventStatus'),
    path('sunburst/', views.sunburst_chart, name='sunburst'),
    path('hierarchical/', views.event_treedata, name='hierarchical'),
    path('addevents', views.addevents, name='addevents'),
    path('submitevent', views.submitevent, name='submitevent'),
    path('updateevent/<int:id>/', views.updateevent, name='updateevent'),
    path('addslotINevent/', views.addslotINevent, name='addslotINevent'),
    path('submitslot/', views.submitslot, name='submitslot'),
    path('submitslot/<int:id>/', views.submitslot, name='submitslot'),
    path('eventOFslot/<int:id>/', views.eventOFslot, name='eventOFslot'),
    path('slotOFcategory/<int:id>/', views.slotOFcategory, name='slotOFcategory'),
    path('updateslot/<int:id>/', views.updateslot, name='updateslot'),
    path('modifycategory/<int:id>/', views.modifycategory, name='modifycategory'),
    path('addcateINslot/<int:slotID>/',
         views.addcateINslot, name='addcateINslot'),
    path('submitcategory/<int:id>/', views.submitcategory, name='submitcategory'),
    path('updatecategory/<int:id>/', views.updatecategory, name='updatecategory'),
    path('submitcattickets/<int:id>/',
         views.submitcattickets, name='submitcattickets'),
    path('submitticket/<int:id>/', views.submitticket, name='submitticket'),
    path('saveTickets/<int:id>/', views.saveTickets, name='saveTickets'),
    path('excel_tickets/<int:id>/', views.excel_tickets, name='excel_tickets'),

    path('modifyticket/<int:id>/', views.modifyticket, name='modifyticket'),
    path('updatetickets/<int:id>/', views.updatetickets, name='updatetickets'),
    path('generateqr/<int:id>/', views.generateqr, name='generateqr'),
    path('eventCustomer/', views.eventCustomer, name='eventCustomer'),
    path('billingTicket/', views.billingTicket, name='billingTicket'),
    path('viewDetail/<int:id>/', views.viewDetail, name='viewDetail'),

    path('home1/', views.home1, name='home1'),
    path('eventCampaign/<int:id>/', views.eventCampaign, name='eventCampaign'),

    path('eventCampaign/', views.eventCampaign, name='eventCampaign'),
#     path('eventCampaign/<int:id>/', views.eventCampaign, name='eventCampaign'),
    path('addCampaign/', views.addCampaign, name='addCampaign'),
    path('assignCampaign/<int:id>/', views.assignCampaign, name='assignCampaign'),
    path('sendCampaign/<int:id>/', views.sendCampaign, name='sendCampaign'),
    path('deleteCampaign/<int:id>/', views.deleteCampaign, name='deleteCampaign'),

#     path('ticketviewdisplaydata/', views.ticketviewdisplaydata,
#          name='ticketviewdisplaydata'),
#     path('fetch_slots', views.fetch_slots, name='fetch_slots'),
#     path('fetch_categories', views.fetch_categories, name='fetch_categories'),

#     path('fetch_ticket/', views.fetch_ticket, name='fetch_ticket'),

    path('addCampaignSubmit/', views.addCampaignSubmit, name='addCampaignSubmit'),
    path('updateCamaign/<int:id>/', views.updateCamaign, name='updateCamaign'),
    path('subUpdateCamaign/<int:id>/',
         views.subUpdateCamaign, name='subUpdateCamaign'),
#     path('ticketviewdisplaydata/', views.ticketviewdisplaydata,
#          name='ticketviewdisplaydata'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('eventinfo/', views.eventinfo, name='eventinfo'),
    path('generalinfo/', views.generalinfo, name='generalinfo'),
    path('levelSeting_page/', views.levelSeting_page, name='levelSeting_page'),

    path('editsettingsinfo/', views.editsettingsinfo, name='editsettingsinfo'),
    path('deleteevents/<int:id>/', views.deleteevents, name='deleteevents'),
    path('deleteslot/<int:id>/', views.deleteslot, name='deleteslot'),
    path('deletecategory/<int:id>/', views.deletecategory, name='deletecategory'),
    path('deleteticket/<int:id>/', views.deleteticket, name='deleteticket'),
    path('deleteCampaignList/<int:id>/',
         views.deleteCampaignList, name='deleteCampaignList'),

    path('download-excel/', views.download_excel, name='download_excel'),

    path('ticketviewdisplaydata/', views.ticketviewdisplaydata,
         name='ticketviewdisplaydata'),
    path('fetch_slots', views.fetch_slots, name='fetch_slots'),
    path('fetch_categories', views.fetch_categories, name='fetch_categories'),

    path('fetch_ticket/', views.fetch_ticket, name='fetch_ticket'),
    path('update_ticket_status/', views.update_ticket_status, name='update_ticket_status'),
    path('delete_ticket/', views.delete_ticket, name='delete_ticket'),
    path('ticket_dashboard',views.ticket_dashboard,name='ticket_dashboard'),
]
