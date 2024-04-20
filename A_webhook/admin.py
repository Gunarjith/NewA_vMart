from django.contrib import admin
from vailodb.models import event_master, event_slots, event_ticket_category, event_settings, event_ticket_cart_header, \
    event_ticket_cart_details, ticket_information, ticket_customer_master, campaign_info, campaign_customer, \
    History_campaign_customer, History_campaign_infor, admin_permission, facebook_details, payment_gateway_details, \
    payment_settings,ticket_billing,ticket_billing_details,Subclient,SubUserPreference
from vailodb_b.models import template_info, template_info_details, campaign_group_types, campaign_group_categorys, \
    campaign_payment_gateway_details, campaign_marketplace_settings, campaign_marketplace, generic_campaign_info, \
    campaign_customer_master, generic_campaign_history, Form, Form_Section, Form_Field, Form_FieldChoice, \
    Inflow_Setup_Details, campaign_footprint, campaign_formdata, campaign_groups, campaign_group_customer_mappings
from vailodb_n.models import donation_settings, donation_types, donation_details, donation_marketplace, \
    donation_payment_settings, donation_payment_gateway_details, donation_marketplace_settings, donation_ngo_type, \
    donation_ngo_category

# from vailodb_a.models import Availablity,Main_settings,Consultant_settings,Holiday_leaves,Visitor,Bookings
from vailodb_s.models import Survey_list, Survey_Question, Survey_Customer, Survey_Customer_Response, \
    Survey_marketplace_settings, Survey_marketplace, survey_types, survey_categorys
from vailodb_a.models import appointment_marketplace, appointment_settings, Consultant_details, \
    Consultant_holiday_leaves, \
    Consultant_availablity, appointment_visitor, appointment_bookings, appointment_payment_settings, \
    appointment_payment_gateway_details, appointment_group_type, appointment_group_category,appointment_marketplace_settings


# Register your models here.
from vailodb_h.models import Hotel_marketplace_settings,Hotel_marketplace,Hotel_settings,Hotel_services,Food,Nearby_place,\
Hotel_rooms,Hotel_facilities,Selfhelp,Information,Food_Category,Food_catalogue,Food_catalogue_items,Hotel_rooms_type,Room_list,\
Hotel_services_settings,Food_order_header,Food_order_details,Service_order,Guest_info,Hotel_Room_Guest_info,Checkout_questions,\
Checkout_response_header,Checkout_responses,Complaint_settings,Complaint_info




class admin_permissionAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'client_permission_status', 'client_type', 'client_billing_status', 'client_auth_key', 'client_auth_secret',
    'client')
    list_filter = ('client',)

class facebook_detailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'fb_whatsapp_number', 'client')
    list_filter = ('client',)

class payment_settingsAdmin(admin.ModelAdmin):
    list_display = ('id','contact_name','payment_gateway','contact_number','client')
    list_filter = ('client',)

class payment_gateway_detailsAdmin(admin.ModelAdmin):
    list_display = ('id','payment_gateway','gateway_id','gateway_key','client')
    list_filter = ('client',)


class event_masterAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'Event_Name', 'Event_Description', 'Start_Date',
    'End_Date', 'Event_Logo', 'Event_ticket_image', 'client')
    list_filter = ('client',)

class event_slotsAdmin(admin.ModelAdmin):
    list_display = ('id', 'Slot_Name', 'Slot_Description', 'client')
    list_filter = ('client',)


class event_ticket_categoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'Category_Name', 'Category_Description', 'Category_Price', 'client')
    list_filter = ('client',)


# class event_ticket_blocksAdmin(admin.ModelAdmin):
#     list_display = ('id', 'Ticket_QR', 'Ticket_Status', 'client')
#     list_filter = ('client',)


class event_ticket_customerAdmin(admin.ModelAdmin):
    list_display = ('id', 'Customer_Phone_Number', 'Customer_Address', 'Customer_Email', 'client')
    list_filter = ('client',)


class event_settingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'welcome_header_text','welcome_message_text','welcome_header_image','client')
    list_filter = ('client',)


class event_ticket_cartAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'event_ticket_cartname', 'event_ticket_cartslots', 'event_ticket_cartcatg', 'event_number_of_tickets',
    'event_ticket_price', 'event_payment_status','client')
    list_filter = ('client',)

class event_ticket_cart_headerAdmin(admin.ModelAdmin):
    list_display = ('id','customer_phone_number','cart_amount','total_tickets','payment_reference_id','payment_status','client')
    list_filter = ('client',)

class event_ticket_cart_detailsAdmin(admin.ModelAdmin):
    list_display = ('id','event_id','slot_id','category_id','number_of_tickets','ticket_price','ticket_sub_total','client')
    list_filter = ('client',)

class ticket_informationAdmin(admin.ModelAdmin):
    list_display = ('id','ticket_number','expiry_date','ticket_QR','ticket_status','payment_reference_id','customer_phone_number','customer_address','customer_email','client')
    list_filter = ('client',)

class ticket_customer_masterAdmin(admin.ModelAdmin):
    list_display = ('id','Customer_First_Name','Customer_Middle_Name','Customer_Last_Name','Customer_Email','Customer_Address_Line1','Customer_Address_Line2','Customer_Phone_Number','Customer_Whatsapp_Number','client')
    list_filter = ('client',)

class campaign_infoAdmin(admin.ModelAdmin):
    list_display = ('id','Campaign_Name','Campaign_Description','Campaign_Header_Image','Campaign_Message_Text','Campaign_Footer_Text','Campaign_First_Button_Name','Campaign_Second_Button_Name','Campaign_Status','client')
    list_filter = ('client',)

class campaign_customerAdmin(admin.ModelAdmin):
    list_display = ('id','Customer_First_Name','Customer_Whatsapp_Number','Customer_City','client')
    list_filter = ('client',)


class template_infoAdmin(admin.ModelAdmin):
    list_display = ('id','template_name','template_header_text','template_header_image','client')
    list_filter = ('client',)

class template_info_detailsAdmin(admin.ModelAdmin):
    list_display = ('id','template_button_num','template_button_name','template_button_type','client')
    list_filter = ('client',)


class generic_campaign_infoAdmin(admin.ModelAdmin):
    list_display = ('id','Campaign_Name','Campaign_message','Campaign_Image','client')
    list_filter = ('client',)


class campaign_customer_masterAdmin(admin.ModelAdmin):
    list_display = ('id','Customer_Name','Customer_Whatsapp_Number','Customer_email','client')
    list_filter = ('client',)


class generic_campaign_historyAdmin(admin.ModelAdmin):
    list_display = ('id','Customer_Whatsapp_Number','Campaign_message','Campaign_Status','client')
    list_filter = ('client',)

class campaign_group_typesAdmin(admin.ModelAdmin):
    list_display = ('id','campaign_group_type','client')
    list_filter = ('client',)


class campaign_group_categorysAdmin(admin.ModelAdmin):
    list_display = ('id','campaign_group_category','client')
    list_filter = ('client',)

class campaign_payment_gateway_detailsAdmin(admin.ModelAdmin):
    list_display = ('id','payment_gateway','client')
    list_filter = ('client',)


class campaign_marketplace_settingsAdmin(admin.ModelAdmin):
    list_display = ('id','generic_flow_id','specific_flow_id','my_campaign_flow_id','client')
    list_filter = ('client',)


class campaign_marketplaceAdmin(admin.ModelAdmin):
    list_display = ('id','campaign_name','campaign_type','campaign_category','client')
    list_filter = ('client',)

class History_campaign_customerAdmin(admin.ModelAdmin):
    list_display = ('id', 'Customer_First_Name', 'Customer_Whatsapp_Number', 'Customer_City', 'client')
    list_filter = ('client',)

class History_campaign_inforAdmin(admin.ModelAdmin):
    list_display = ('id', 'Campaign_Name', 'Campaign_Description', 'Campaign_Header_Image', 'client')
    list_filter = ('client',)

class ticket_billingAdmin(admin.ModelAdmin):
    list_display = ('id','month','billed_amount','paid_amount','status','client')
    list_filter = ('client',)

class ticket_billing_detailsAdmin(admin.ModelAdmin):
    list_display = ('id','transaction_type','transaction_name','transaction_count','date','client')
    list_filter = ('client',)

class donation_settingsAdmin(admin.ModelAdmin):
    list_display=('id','donation_image','donation_description','client')
    list_filter = ('client',)

class donation_typesAdmin(admin.ModelAdmin):
    list_display = ('id','donation_name','donation_short_description','donation_description','client')
    list_filter = ('client',)

class donation_detailsAdmin(admin.ModelAdmin):
    list_display = ('id','donar_name','donar_email','donar_pan_number','donar_phone_number','client')
    list_filter = ('client',)

class donation_marketplaceAdmin(admin.ModelAdmin):
    list_display = ('id','ngo_name','ngo_type','ngo_category','ngo_location','client')
    list_filter = ('client',)

class donation_payment_settingsAdmin(admin.ModelAdmin):
    list_display = ('id','payment_gateway','contact_name','contact_number','client')
    list_filter = ('client',)


class donation_payment_gateway_detailsAdmin(admin.ModelAdmin):
    list_display = ('id','payment_gateway','gateway_id','gateway_key','currency','client')
    list_filter = ('client',)


class donation_marketplace_settingsAdmin(admin.ModelAdmin):
    list_display = ('id','marketplace_welcome_image','marketplace_welcome_message_body','generic_flow_id','generic_flow_cta_name','client')
    list_filter = ('client',)


class donation_ngo_typeAdmin(admin.ModelAdmin):
    list_display = ('id','donation_ngo_type','client')
    list_filter = ('client',)

class donation_ngo_categoryAdmin(admin.ModelAdmin):
    list_display = ('id','donation_ngo_category','client')
    list_filter = ('client',)


class SubclientAdmin(admin.ModelAdmin):
    list_display =('id','subclientname','client')
    list_filter = ('client',)

class SubUserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('id','preference','client')
    list_filter = ('client',)

class appointment_settingsAdmin(admin.ModelAdmin):
    list_display = ('id','welcome_image','welcome_message','client')
    list_filter = ('client',)

class Consultant_detailsAdmin(admin.ModelAdmin):
    list_display = ('id','consultant_name','consultant_photo','consultant_image','consultant_email','client')
    list_filter = ('client',)

class Consultant_availablityAdmin(admin.ModelAdmin):
    list_display = ('id','day_of_week','start_time','end_time','client')
    list_filter = ('client',)

class appointment_bookingsAdmin(admin.ModelAdmin):
    list_display = ('id','date','start_time','online_offline','customer_phone_number','client')
    list_filter = ('client',)

class appointment_visitorAdmin(admin.ModelAdmin):
    list_display = ('id','Visitor_Name','Visitor_email','Visitor_Whatsapp_Number','Visitor_City','client')
    list_filter = ('client',)

class Consultant_holiday_leavesAdmin(admin.ModelAdmin):
    list_display = ('id','date','start_time','end_time','client')
    list_filter = ('client',)


class appointment_marketplaceAdmin(admin.ModelAdmin):
    list_display = ('id','group_name','group_type','group_category','group_location','group_description','client')
    list_filter = ('client',)

class appointment_payment_settingsAdmin(admin.ModelAdmin):
    list_display = ('id','payment_gateway','contact_number','contact_name','client')
    list_filter = ('client',)

class appointment_payment_gateway_detailsAdmin(admin.ModelAdmin):
    list_display = ('id','payment_gateway','gateway_id','gateway_id','client')
    list_filter = ('client',)

class appointment_group_typeAdmin(admin.ModelAdmin):
    list_display = ('id','appointment_group_type','client')
    list_filter = ('client',)


class appointment_group_categoryAdmin(admin.ModelAdmin):
    list_display = ('id','appointment_group_category','client')
    list_filter = ('client',)

class appointment_marketplace_settingsAdmin(admin.ModelAdmin):
    list_display = ('id','generic_flow_id','specific_flow_id','my_appointment_flow_id','client')
    list_filter = ('client',)
class Survey_listAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey_type', 'survey_status', 'flow_id', 'survey_message', 'client')
    list_filter = ('client',)

class Survey_QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'question_type', 'response_option1', 'response_option2', 'client')
    list_filter = ('client',)

class Survey_CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'customer_whatsapp_number', 'customer_status', 'client')
    list_filter = ('client',)

class Survey_Customer_ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'Survey_Question', 'Survey_Customer', 'Survey_Response', 'Survey_comments', 'client')
    list_filter = ('client',)


class Survey_marketplace_settingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'generic_flow_id', 'specific_flow_id', 'my_survey_flow_id', 'generic_flow_cta_name', 'client')
    list_filter = ('client',)

class Survey_marketplaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey_name', 'survey_type', 'survey_category', 'survey_location', 'client')
    list_filter = ('client',)


class survey_typesAdmin(admin.ModelAdmin):
    list_display = ('id','survey_type','client')
    list_filter = ('client',)


class survey_categorysAdmin(admin.ModelAdmin):
    list_display = ('id','survey_category','client')
    list_filter = ('client',)


# class Survey_Customer_ResponseAdmin(admin.ModelAdmin):
#     list_display = ('id', 'Survey_Question', 'Survey_Customer', 'Survey_Response', 'Survey_comments', 'client')
#     list_filter = ('client',)
class Hotel_marketplace_settingsAdmin(admin.ModelAdmin):
    list_display= ('id','generic_flow_id','specific_flow_id','my_hotel_flow_id','marketplace_welcome_message_body','client')
    list_filter = ('client',)
class Hotel_marketplaceAdmin(admin.ModelAdmin):
    list_display= ('id','hotel_name','hotel_type','hotel_category','hotel_description','client')
    list_filter = ('client',)
class Hotel_settingsAdmin(admin.ModelAdmin):
    list_display= ('id','hotel_name', 'hotel_address','hotel_image','hotel_video','client')
    list_filter = ('client',)

class Hotel_servicesAdmin(admin.ModelAdmin):
    list_display= ('id','service_name', 'start_time', 'end_time','service_discription','client')
    list_filter = ('client',)

class FoodAdmin(admin.ModelAdmin):
    list_display= ('id','food_name', 'food_price', 'food_type','food_discription','client')
    list_filter = ('client',)

class Nearby_placeAdmin(admin.ModelAdmin):
    list_display= ('id','place_type', 'place_name', 'distance','distance_unit','client')
    list_filter = ('client',)
class Hotel_roomsAdmin(admin.ModelAdmin):
    list_display= ('id','room_number', 'room_floor', 'room_type','bed','client')
    list_filter = ('client',)
class Hotel_facilitiesAdmin(admin.ModelAdmin):
    list_display= ('id','facility_name', 'facility_location', 'start_time','end_time','client')
    list_filter = ('client',)

class SelfhelpAdmin(admin.ModelAdmin):
    list_display= ('id','selfhelp_name', 'selfhelp_discription', 'selfhelp_image','selfhelp_video','client')
    list_filter = ('client',)

class InformationAdmin(admin.ModelAdmin):
    list_display= ('id','information_name', 'information_discription', 'information_image','information_video','client')
    list_filter = ('client',)
class Food_CategoryAdmin(admin.ModelAdmin):
    list_display=('id','category_name','vailo_record_creation','client')
    list_filter = ('client',)
class Food_catalogueAdmin(admin.ModelAdmin):
    list_display=('id','catalogue_name','catalogue_discription','client')    
    list_filter = ('client',)
class Food_catalogue_itemsAdmin(admin.ModelAdmin):
    list_display=('id','Food_catalogue','Food_Item','client')
    list_filter = ('client',)
class Hotel_rooms_typeAdmin(admin.ModelAdmin):
    list_display=('id','l_room_type','room_type','client')
    list_filter = ('client',)
class Room_listAdmin(admin.ModelAdmin):
    list_display=('id','hotel_room_type','room_number','client')
    list_filter = ('client',)
class Hotel_services_settingsAdmin(admin.ModelAdmin):
    list_display=('id','name','description','client')
    list_filter=('client',)
class Food_order_headerAdmin(admin.ModelAdmin):
    list_display=('id','order_delivery_room','order_amount','client')
    list_filter=('client',)

class Service_orderAdmin(admin.ModelAdmin):
    list_display=('id','customer_phone_num','customer_room','client')
    list_filter=('client',)
class Food_order_detailsAdmin(admin.ModelAdmin):
    list_display=('id','Food_Item','Food_quantity','client')
    list_filter=('client',)
    
class Hotel_Room_Guest_infoAdmin(admin.ModelAdmin):
    list_display=('id','Check_In','Check_Out','client')
    list_filter=('client',)

class Guest_infoAdmin(admin.ModelAdmin):
    list_display=('id','Phone_number','Guest_name','client')
    list_filter=('client',)
class Checkout_questionsAdmin(admin.ModelAdmin):
    list_display=('id','Question','marketplace','client')
    list_filter=('client',)

class Checkout_response_headerAdmin(admin.ModelAdmin):
    list_display=('id',"Room_details","Comment","client")
    list_filter=('client',)
class Checkout_responsesAdmin(admin.ModelAdmin):
    list_display=('id','Checkout_question','Checkout_response','client')
    list_filter=('client',)


class Complaint_settingsAdmin(admin.ModelAdmin):
    list_display=('id','Complaint_category','client')
    list_filter=('client',)
class Complaint_infoAdmin(admin.ModelAdmin):
    list_display=('id','Complaint_category','Complaint_comments','client')
    list_filter=('client',)


class FormAdmin(admin.ModelAdmin):
    list_display=('id','form_name','flow_id','status','client')
    list_filter=('client',)

class Form_SectionAdmin(admin.ModelAdmin):
    list_display=('id','name','client')
    list_filter=('client',)


class Form_FieldAdmin(admin.ModelAdmin):
    list_display=('id','label','field_type','client')
    list_filter=('client',)

class Form_FieldChoiceAdmin(admin.ModelAdmin):
    list_display=('id','choice_text','client')
    list_filter=('client',)


class Inflow_Setup_DetailsAdmin(admin.ModelAdmin):
    list_display=('id','Parent_ID','open_button_type','open_button_name','short_title','short_description','client')
    list_filter=('client',)

class campaign_footprintAdmin(admin.ModelAdmin):
    list_display=('id','date','time','From_number','button','campaign_name','client')
    list_filter=('client',)

class campaign_formdataAdmin(admin.ModelAdmin):
    list_display=('id','generic_campaign_info','Campaign_Form_data','client')
    list_filter=('client',)


class campaign_groupsAdmin(admin.ModelAdmin):
    list_display=('id','group_name','client')
    list_filter=('client',)


class campaign_group_customer_mappingsAdmin(admin.ModelAdmin):
    list_display=('id','campaign_groups','campaign_customer_master','client')
    list_filter=('client',)



admin.site.register(event_master, event_masterAdmin)
admin.site.register(event_slots, event_slotsAdmin)
admin.site.register(event_ticket_category, event_ticket_categoryAdmin)
admin.site.register(event_settings, event_settingsAdmin)
admin.site.register(event_ticket_cart_header,event_ticket_cart_headerAdmin)
admin.site.register(event_ticket_cart_details,event_ticket_cart_detailsAdmin)
admin.site.register(ticket_information,ticket_informationAdmin)
admin.site.register(ticket_customer_master,ticket_customer_masterAdmin)
admin.site.register(campaign_info,campaign_infoAdmin)
admin.site.register(campaign_customer,campaign_customerAdmin)
admin.site.register(History_campaign_customer,History_campaign_customerAdmin)
admin.site.register(History_campaign_infor,History_campaign_inforAdmin)
admin.site.register(admin_permission, admin_permissionAdmin)
admin.site.register(facebook_details,facebook_detailsAdmin)
admin.site.register(payment_settings,payment_settingsAdmin)
admin.site.register(payment_gateway_details,payment_gateway_detailsAdmin)
admin.site.register(ticket_billing,ticket_billingAdmin)
admin.site.register(ticket_billing_details,ticket_billing_detailsAdmin)
admin.site.register(donation_settings,donation_settingsAdmin)
admin.site.register(donation_types,donation_typesAdmin)
admin.site.register(donation_details,donation_detailsAdmin)
admin.site.register(Subclient,SubclientAdmin)
admin.site.register(SubUserPreference,SubUserPreferenceAdmin)
admin.site.register(appointment_settings,appointment_settingsAdmin)
admin.site.register(Consultant_details,Consultant_detailsAdmin)
admin.site.register(Consultant_availablity,Consultant_availablityAdmin)
admin.site.register(appointment_bookings,appointment_bookingsAdmin)
admin.site.register(appointment_visitor,appointment_visitorAdmin)
admin.site.register(Consultant_holiday_leaves,Consultant_holiday_leavesAdmin)
admin.site.register(appointment_marketplace,appointment_marketplaceAdmin)
admin.site.register(appointment_payment_settings,appointment_payment_settingsAdmin)
admin.site.register(appointment_payment_gateway_details,appointment_payment_gateway_detailsAdmin)
admin.site.register(Survey_list,Survey_listAdmin)
admin.site.register(Survey_Question,Survey_QuestionAdmin)
admin.site.register(Survey_Customer,Survey_CustomerAdmin)
admin.site.register(Survey_Customer_Response,Survey_Customer_ResponseAdmin)
admin.site.register(donation_marketplace,donation_marketplaceAdmin)
admin.site.register(donation_payment_settings,donation_payment_settingsAdmin)
admin.site.register(donation_payment_gateway_details,donation_payment_gateway_detailsAdmin)
admin.site.register(donation_marketplace_settings,donation_marketplace_settingsAdmin)
admin.site.register(donation_ngo_type,donation_ngo_typeAdmin)
admin.site.register(donation_ngo_category,donation_ngo_categoryAdmin)
admin.site.register(appointment_group_type,appointment_group_typeAdmin)
admin.site.register(appointment_group_category,appointment_group_categoryAdmin)
admin.site.register(appointment_marketplace_settings,appointment_marketplace_settingsAdmin)
admin.site.register(Hotel_marketplace_settings,Hotel_marketplace_settingsAdmin)
admin.site.register(Hotel_marketplace,Hotel_marketplaceAdmin)
admin.site.register(Hotel_settings,Hotel_settingsAdmin)
admin.site.register(Hotel_services,Hotel_servicesAdmin)
admin.site.register(Food,FoodAdmin)
admin.site.register(Nearby_place,Nearby_placeAdmin)
admin.site.register(Hotel_rooms,Hotel_roomsAdmin)
admin.site.register(Hotel_facilities,Hotel_facilitiesAdmin)
admin.site.register(Selfhelp,SelfhelpAdmin)
admin.site.register(Information,InformationAdmin)
admin.site.register(Food_Category,Food_CategoryAdmin)
admin.site.register(Food_catalogue,Food_catalogueAdmin)
admin.site.register(Food_catalogue_items,Food_catalogue_itemsAdmin)
admin.site.register(Hotel_rooms_type,Hotel_rooms_typeAdmin)
admin.site.register(Room_list,Room_listAdmin)
admin.site.register(Hotel_services_settings,Hotel_services_settingsAdmin)
admin.site.register(Service_order,Service_orderAdmin)
admin.site.register(Food_order_details,Food_order_detailsAdmin)
admin.site.register(Food_order_header,Food_order_headerAdmin)
admin.site.register(Guest_info,Guest_infoAdmin)
admin.site.register(Hotel_Room_Guest_info,Hotel_Room_Guest_infoAdmin)
admin.site.register(Checkout_questions,Checkout_questionsAdmin)
admin.site.register(Checkout_response_header,Checkout_response_headerAdmin)
admin.site.register(Checkout_responses,Checkout_responsesAdmin)
admin.site.register(Complaint_settings,Complaint_settingsAdmin)
admin.site.register(Complaint_info,Complaint_infoAdmin)
admin.site.register(Survey_marketplace_settings,Survey_marketplace_settingsAdmin)
admin.site.register(Survey_marketplace,Survey_marketplaceAdmin)
admin.site.register(survey_types,survey_typesAdmin)
admin.site.register(survey_categorys,survey_categorysAdmin)
admin.site.register(template_info,template_infoAdmin)
admin.site.register(template_info_details,template_info_detailsAdmin)
admin.site.register(campaign_group_types,campaign_group_typesAdmin)
admin.site.register(campaign_group_categorys,campaign_group_categorysAdmin)
admin.site.register(campaign_payment_gateway_details,campaign_payment_gateway_detailsAdmin)
admin.site.register(campaign_marketplace_settings,campaign_marketplace_settingsAdmin)
admin.site.register(campaign_marketplace,campaign_marketplaceAdmin)
admin.site.register(generic_campaign_info,generic_campaign_infoAdmin)
admin.site.register(campaign_customer_master,campaign_customer_masterAdmin)
admin.site.register(generic_campaign_history,generic_campaign_historyAdmin)
admin.site.register(Form,FormAdmin)
admin.site.register(Form_Section,Form_SectionAdmin)
admin.site.register(Form_Field,Form_FieldAdmin)
admin.site.register(Form_FieldChoice,Form_FieldChoiceAdmin)
admin.site.register(Inflow_Setup_Details,Inflow_Setup_DetailsAdmin)
admin.site.register(campaign_footprint,campaign_footprintAdmin)
admin.site.register(campaign_formdata,campaign_formdataAdmin)
admin.site.register(campaign_groups,campaign_groupsAdmin)
admin.site.register(campaign_group_customer_mappings,campaign_group_customer_mappingsAdmin)
