from django.contrib import admin
from django.urls import path
from H_hotel import views



urlpatterns =[
    #marketplace id yes 
    
    path('H_hotel/hotelmarketplacemain', views.hotelmarketplacemain, name='hotelmarketplacemain'),
    path('H_hotel/hotelmarketplacemain/<str:delete>', views.hotelmarketplacemain,name='hotelmarketplacemain' ),
    # path('H_hotel/hotelmarketplaceSetting', views.hotelmarketplaceSetting, name='hotelmarketplaceSetting'),
    path('H_hotel/groupnameinfo', views.groupnameinfo, name='groupnameinfo'),
    path('H_hotel/submitlisthotels', views.submitlisthotels, name='submitlisthotels'),
    path('H_hotel/edithotelsgroups/<int:id>/', views.edithotelsgroups, name='edithotelsgroups'),
    path('H_holtel/deletelisthotels/<int:id>/', views.deletelisthotels, name='deletelisthotels'),
    path('H_hotel/editsubmitlisthotels/<int:id>/', views.editsubmitlisthotels, name='editsubmitlisthotels'),
    path('H_hotel/addhotelgroup', views.addhotelgroup, name='addhotelgroup'),
    path('H_hotel/marketplaceConfig', views.marketplaceConfig, name='marketplaceConfig'),



    path('H_hotel/hotelmaininfo', views.hotelmaininfo, name='hotelmaininfo'),
   
    path('H_hotel/hotelmaininfo1', views.hotelmaininfo1, name='hotelmaininfo1'),
    path('H_hotel/updatemaindata', views.updatemaindata, name='updatemaindata'),
    path('H_hotel/updatemaindata/<str:resize>', views.updatemaindata, name='updatemaindata'),
    path('H_hotel/hotelmaininfo/<int:id>/', views.hotelmaininfo, name='hotelmaininfo'),
    path('H_hotel/hotelmaininfo1/<int:id>/', views.hotelmaininfo1, name='hotelmaininfo1'),
    path('H_hotel/hotelmaininfo/<int:id>/<str:deletefile>', views.hotelmaininfo, name='hotelmaininfo'),
    # path('H_hotel/hotelmaininfo/<int:id>/', views.hotelmaininfo, name='hotelmaininfo'),


    path("H_hotel/submithotelmain", views.submithotelmain, name='submithotelmain'),
    path('H_hotel/hotelservice', views.hotelservice, name='hotelservice'),
    path('H_hotel/addservices', views.addservices, name='addservices'),
    path('H_hotel/submitservices', views.submitservices, name='submitservices'),
    path('H_hotel/editservicedata/<int:id>/', views.editservicedata, name='editservicedata'),
    path('H_hotel/editservicedata/<int:id>/<str:deletefile>', views.editservicedata, name='editservicedata'),
    path('H_hotel/updateservices/<int:id>/', views.updateservices, name='updateservices'),
    path('H_hotel/deleteservicedata/<int:id>/', views.deleteservicedata, name='deleteservicedata'),

    path('H_hotel/foodconfig', views.foodconfig, name='foodconfig'),
    path('H_hotel/addcategory', views.addcategory, name='addcategory'),
    path('H_hotel/submitcategory', views.submitcategory, name='submitcategory'),
    path('H_hotel/deletevalue/<int:id>/', views.deletevalue, name='deletevalue'),
    path('H_hotel/foodtypeinfo', views.foodtypeinfo, name='foodtypeinfo'),
    path('H_hotel/foodinfo', views.foodinfo, name='foodinfo'),
    path('H_hotel/addfoodlist', views.addfoodlist, name='addfoodlist'),
    path('H_hotel/submitfoodlist', views.submitfoodlist, name='submitfoodlist'),
    path('H_hotel/editfoodlist/<int:id>/', views.editfoodlist, name='editfoodlist'),
    path('H_hotel/editfoodlist/<int:id>/<str:deletefile>', views.editfoodlist, name='editfoodlist'),
    path('H_hotel/submiteditfoodlist<int:id>/', views.submiteditfoodlist, name='submiteditfoodlist'),
    path('H_hotel/deletefooddata/<int:id>/', views.deletefooddata, name='deletefooddata'),
    path('H_hotel/catalogueinfo', views.catalogueinfo, name='catalogueinfo'),
    path('H_hotel/addcatalogue', views.addcatalogue, name='addcatalogue'),
    path('H_hotel/submitcatelogulist', views.submitcatelogulist, name='submitcatelogulist'),
    path('H_hotel/editcataloguelist/<int:id>/', views.editcataloguelist, name='editcataloguelist'),
    path('H_hotel/submiteditcatelogulist/<int:id>/', views.submiteditcatelogulist, name='submiteditcatelogulist'),
    path('H_hotel/deletecataloguelist/<int:id>/', views.deletecataloguelist, name='deletecataloguelist'),
    path('H_hotel/insertfood/<int:id>/', views.insertfood, name='insertfood'),
    path('H_hotel/submitselectedfoods/<int:id>/', views.submitselectedfoods, name='submitselectedfoods'),
    path('H_hotel/deletefooditem/<int:id>/', views.deletefooditem, name='deletefooditem'),

    path('H_hotel/catalogueitemsinfo', views.catalogueitemsinfo, name='catalogueitemsinfo'),
    path('H_hotel/addcatalogueitems', views.addcatalogueitems, name='addcatalogueitems'),
    path('H_hotel/submitcatalogue', views.submitcatalogue, name='submitcatalogue'),
    path('H_hotel/editcatalogueitemlist/<int:id>/', views.editcatalogueitemlist, name='editcatalogueitemlist'),
    path('H_hotel/edtsubmitcatalogue/<int:id>/',views.edtsubmitcatalogue, name='edtsubmitcatalogue'),
    path('H_hotel/deletecatalogueitemlist/<int:id>/', views.deletecatalogueitemlist, name='deletecatalogueitemlist'),


    path('H_hotel/hotelnearbyinfo', views.hotelnearbyinfo, name='hotelnearbyinfo'),
    path('H_hotel/addplaces', views.addplaces, name='addplaces'),
    path('H_hotel/submitplacelist', views.submitplacelist, name='submitplacelist'),
    path('H_hotel/editplacelist/<int:id>/', views.editplacelist, name='editplacelist'),
    path('H_hotel/editplacelist/<int:id>/<str:deletefile>', views.editplacelist, name='editplacelist'),
    path('H_hotel/submiteditplacelist/<int:id>/', views.submiteditplacelist, name='submiteditplacelist'),
    path('H_hotel/deletenearbyplace/<int:id>/', views.deletenearbyplace, name='deletenearbyplace'),


    path('H_hotel/hotelfacilitesinfo', views.hotelfacilitesinfo, name='hotelfacilitesinfo'),
    path('H_hotel/addfacilities', views.addfacilities, name='addfacilities'),
    path('H_hotel/submitfacilitylist', views.submitfacilitylist, name='submitfacilitylist'),
    path('H_hotel/editfacilitylist/<int:id>/', views.editfacilitylist, name='editfacilitylist'),
    path('H_hotel/editfacilitylist/<int:id>/<str:deletefile>', views.editfacilitylist, name='editfacilitylist'),
    path('H_hotel/submiteditfacilitylist<int:id>/', views.submiteditfacilitylist, name='submiteditfacilitylist'),
    path('H_hotel/deletefacility/<int:id>/', views.deletefacility, name='deletefacility'),
     path('H_hotel/getroomlist', views.getroomlist, name='getroomlist'),
    path('H_hotel/roomsinfo', views.roomsinfo, name='roomsinfo'),
    path('H_hotel/roomconfig', views.roomconfig, name='roomconfig'),
    path('H_hotel/addhotelrooms', views.addhotelrooms, name='addhotelrooms'),
    path('H_hotel/submitroomlist', views.submitroomlist, name='submitroomlist'),
    path('H_hotel/editroomslist/<int:id>/', views.editroomslist, name='editroomslist'),
    path('H_holel/submiteditroomist/<int:id>/', views.submiteditroomist, name='submiteditroomist'),
    path('H_hotel/deleterooms/<int:id>/', views.deleterooms, name='deleterooms'),
    path('H_hotel/listofrooms', views.listofrooms, name='listofrooms'),
    path('H_hotel/addhotelroomslist', views.addhotelroomslist, name='addhotelroomslist'),
    path('H_hotel/submitroomlista', views.submitroomlista, name='submitroomlista'),
    path('H_hotel/editlistofrooms/<int:id>/', views.editlistofrooms, name='editlistofrooms'),
    path('H_hotel/edisubmitroomlista<int:id>/', views.edisubmitroomlista, name='edisubmitroomlista'),
    path('H_hotel/deletelistofrooms/<int:id>/', views.deletelistofrooms, name='deletelistofrooms'),


    path('H_hotel/selfhelpinfo', views.selfhelpinfo, name='selfhelpinfo'),
    path('H_hotel/addselphelp', views.addselphelp, name='addselphelp'),
    path('H_hotel/submithelplist', views.submithelplist, name='submithelplist'),
    path('H_hotel/edithelplist/<int:id>/', views.edithelplist, name='edithelplist'),
    path('H_hotel/submitedithelplist/<int:id>/', views.submitedithelplist, name='submitedithelplist'),
    path('H_hotel/deletehelpsdata/<int:id>/', views.deletehelpsdata, name='deletehelpsdata'),


    path('H_hotel/hotelinformation', views.hotelinformation, name='hotelinformation'),

    path('H_hotel/addinformation', views.addinformation, name='addinformation'),
    path('H_hotel/submitinfolist', views.submitinfolist, name='submitinfolist'),
    path('H_hotel/editinfolist/<int:id>/', views.editinfolist, name='editinfolist'),
    path('H_hotel/submitediinfolist/<int:id>/', views.submitediinfolist, name='submitediinfolist'),
    path('H_hotel/deleteinfodata/<int:id>/', views.deleteinfodata, name='deleteinfodata'),


    # path('H_hotel/hotelinfo', views.hotelinfo, name='hotelinfo'),
    path('H_hotel/guestinfo', views.guestinfo, name='guestinfo'),
    path('H_hotel/getguestlist', views.getguestlist, name='getguestlist'),

    path('H_hotel/gethotels', views.gethotels, name='gethotels'),
    path('H_hotel/getorders', views.getorders, name='getorders'),
    path('H_hotel/viewrequest/<int:id>/', views.viewrequest, name='viewrequest'),
    path('H_hotel/viewrequest', views.viewrequest, name='viewrequest'),


    path('H_hotel/guestinfo/<int:id>/', views.guestinfo, name='guestinfo'),
    path('H_hotel/foodrequest', views.foodrequest, name='foodrequest'),
    path('H_hotel/foodrequest/<int:id>/', views.foodrequest, name='foodrequest'),

    # path('H_hotel/fooddetails', views.fooddetails, name= 'fooddetails'), 
    path('H_hotel/fooddetails/<int:id>/', views.fooddetails, name= 'fooddetails'), 

    path('H_hotel/roominfo', views.roominfo, name='roominfo'),
    path('H_hotel/roominfo/<int:id>/', views.roominfo, name='roominfo'),

    path('H-hotel/feedbackresponses/',views.feedbackresponses, name='feedbackresponses'),
    path('H-hotel/feedbackresponses/<int:id>',views.feedbackresponses, name='feedbackresponses'),
    path('H-hotel/viewfeedbackresponses/',views.viewfeedbackresponses, name='viewfeedbackresponses'),
    path('H-hotel/submitfeedbackquestions/',views.submitfeedbackquestions, name='submitfeedbackquestions'),
    path("H-hotel/editfeedbackquestions/<int:id>/",views.editfeedbackquestions, name='editfeedbackquestions'),
    path('H-hotel/submiteditfeedbackquestions/<int:id>',views.submiteditfeedbackquestions, name='submiteditfeedbackquestions'),
    path('H-hotel/deletefeedbackquestions/<int:id>',views.deletefeedbackquestions, name='deletefeedbackquestions'),
    path("H_hotel/feedbackQuestions",views.feedbackQuestions, name="feedbackQuestions"),
    path("H_hotel/addfeedbackquestions",views.addfeedbackquestions, name="addfeedbackquestions"),
    path("H_hotel/complaintcategories/",views.complaintcategories, name="complaintcategories"),
    path("H_hotel/addcomplaintcategories/",views.addcomplaintcategories, name="addcomplaintcategories"),
    path('H_hotel/submitcomplaintcaregories/',views.submitcomplaintcaregories, name='submitcomplaintcaregories'),
    path("H_hotel/editcomplaintcategories/<int:id>/",views.editcomplaintcategories, name='editcomplaintcategories'),
    path("H_hotel/submiteditcomplaintcategories/<int:id>/",views.submiteditcomplaintcategories, name='submiteditcomplaintcategories'),
    path('H_hotel/deletecomplaintcategories/<int:id>/',views.deletecomplaintcategories, name='deletecomplaintcategories'),
    path('H_hotel/viewcomplaints/',views.viewcomplaints, name='viewcomplaints'),
    path('H_hotel/viewcomplaints/<int:id>/',views.viewcomplaints, name='viewcomplaints'),
    path('H_hotel/Dashboard/', views.Dashboard, name='Dashboard')

]



