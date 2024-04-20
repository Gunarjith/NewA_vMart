import random
import time

import requests
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render,redirect
from vailodb_b.models import generic_campaign_info, campaign_customer_master, generic_campaign_history, \
    campaign_marketplace, campaign_payment_gateway_details, generic_campaign_history, Form, Form_Section, Form_Field, \
    Form_FieldChoice, Inflow_Setup_Details, campaign_footprint, campaign_group_types, campaign_groups, \
    campaign_group_customer_mappings, campaign_marketplace_settings
import json                                                                                                                                                                              
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from vailodb.models import admin_permission, facebook_details, payment_gateway_details,ticket_billing \
,Subclient, SubUserPreference,ticket_billing_details,  SUBCLIENT_CHOICE

from vailodb_b.models import template_info,template_info_details, campaign_formdata

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.

def  Bcampaign(request):
    return HttpResponse("Bcampaign")



def listCampaign(request, id=None):
    subclient_id = request.session.get('subclient_id') 
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = id
    print('listCampaign mk id', marketplace_id)
    campaign_group_name = campaign_group_customer_mappings.objects.filter(client_id=request.user.id)

    if id is not None:
        camgroups = campaign_groups.objects.filter(client_id=request.user.id)
        templatedata = template_info.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)
    else:
        camgroups = campaign_groups.objects.filter(client_id=request.user.id)
        templatedata = template_info.objects.filter(client_id=request.user.id, marketplace_id=None)

    context = {
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,
        'marketplace_id': marketplace_id,
        'templatedata': templatedata,
        'camgroups': camgroups,
        'id': id,  # Pass the id parameter in the context
    }

    return render(request, 'B_campaign/campaignList.html', context)


def addBCampaign(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    print('addBCampaign mk id', marketplace_id)
    context = {
        'subclient_preferences': subclient_preferences,

        'admin_permission_obj':admin_permission_obj,
        'marketplace_id':marketplace_id
    }
  
    return render(request, 'B_campaign/addBCampaign.html',context)


from django.shortcuts import render, redirect, get_object_or_404

def addBCampaignSubmit(request):
    marketplace_id = request.GET.get('marketplace_id')
    print('addBCampaignSubmit mk id', marketplace_id)
    if request.method == 'POST':
        submitAddBCampaign = generic_campaign_info()

        submitAddBCampaign.Campaign_Name = request.POST.get('campaignName')
        submitAddBCampaign.client_id = request.user.id
        if marketplace_id:
            submitAddBCampaign.marketplace_id = marketplace_id

        submitAddBCampaign.save()

        template_name = request.POST.get('template_name')
        template_header_text = request.POST.get('nameInput')
        template_body_message = request.POST.get('template_body_message')
        template_header_type = request.POST.get('selectsoptionbtn')
        template_footer = request.POST.get('footer_name')
        template_header_image = None
        if 'mediaFile' in request.FILES:
            template_header_image = request.FILES.get('mediaFile')
        
        marketplace_instance = None
        if marketplace_id:
            marketplace_instance = get_object_or_404(campaign_marketplace, pk=marketplace_id)

        templatedata = template_info.objects.create(
            client_id=request.user.id,
            marketplace=marketplace_instance,
            generic_campaign_info=submitAddBCampaign,
            template_name=template_name,
            template_header_text=template_header_text,
            template_body_message=template_body_message,
            template_header_image=template_header_image,  
            template_header_type=template_header_type,
            template_footer = template_footer,


        )

        if submitAddBCampaign.marketplace_id:
            return redirect("campaignList", id=submitAddBCampaign.marketplace_id)
        return redirect("campaignList")

    return render(request, 'B_campaign/addBCampaign.html')




def updateBCamaign(request, id=None):
 
    updateBCampaign = template_info.objects.filter(client_id=request.user.id, id=id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    subclient_id = request.session.get('subclient_id')  
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    marketplace_id= request.GET.get('marketplace_id')
    print('updateBCamaign mk id', marketplace_id)
    if id is not None:
        listbtn = template_info_details.objects.filter(client_id=request.user.id, template_info=id, )
        print('aqqqq')
    else:
        listbtn = template_info_details.objects.filter(client_id=request.user.id)
        print('bqqqq')
    

    context ={
        "updateBCampaign": updateBCampaign,
        'admin_permission_obj':admin_permission_obj,
        "id":id,
        'subclient_preferences':subclient_preferences,
        'listbtn':listbtn,
        'marketplace_id':marketplace_id,
        
    }
    return render(request, 'B_campaign/editBCampaign.html', context)


def addcampaignbtn(request, id):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    formdata = Form.objects.filter(client_id= request.user.id)
    templatedata = template_info.objects.filter(client_id=request.user.id, status='APPROVED')

    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    print('addcampaignbtn mk id',marketplace_id )

    template_info_id = id
    context = {
        'subclient_preferences': subclient_preferences,
        'marketplace_id':marketplace_id,
        'admin_permission_obj':admin_permission_obj,
        'template_info_id':template_info_id,
        'id':id,
        'formdata':formdata,
        'templatedata':templatedata,

    }
  
    return render(request, 'B_campaign/addBtnBCampaign.html',context)

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect


def addBtnBCampaignSubmit(request, id):
    if request.method == 'POST':
        marketplace_id = request.GET.get('marketplace_id')
        print('addBtnBCampaignSubmit mk id', marketplace_id)        

        submitAddBtnBCampaign = template_info_details()
        submitAddBtnBCampaign.template_button_num = request.POST.get('btnNum')
        submitAddBtnBCampaign.template_button_name = request.POST.get('btnName')
        submitAddBtnBCampaign.template_button_type = request.POST.get('template_button_type')
        
        # Determine the type of button and set additional info accordingly
        if submitAddBtnBCampaign.template_button_type == 'IMAGE':
            if 'fileInput1' in request.FILES:
                submitAddBtnBCampaign.template_file_path = request.FILES['fileInput1']
        elif submitAddBtnBCampaign.template_button_type == 'VIDEO':
            if 'fileInput2' in request.FILES:
                submitAddBtnBCampaign.template_file_path = request.FILES['fileInput2']
        elif submitAddBtnBCampaign.template_button_type == 'DOCUMENT':
            if 'fileInput3' in request.FILES:
                submitAddBtnBCampaign.template_file_path = request.FILES['fileInput3']
        elif submitAddBtnBCampaign.template_button_type == 'PHONE_NUMBER':
            submitAddBtnBCampaign.template_additional_info = request.POST.get('phoneNumberInput')
        elif submitAddBtnBCampaign.template_button_type == 'URL':
            submitAddBtnBCampaign.template_additional_info = request.POST.get('urlInput')
        elif submitAddBtnBCampaign.template_button_type == 'STOP':
            submitAddBtnBCampaign.template_additional_info = request.POST.get('stopInput')
        elif submitAddBtnBCampaign.template_button_type == 'FORM':
            selected_form_id = request.POST.get('formInput')
            selected_form = Form.objects.get(id=selected_form_id) 
            submitAddBtnBCampaign.template_file_path = selected_form.form_name
            submitAddBtnBCampaign.template_additional_info = selected_form_id
        elif submitAddBtnBCampaign.template_button_type == 'CAMPAIGN':
            selected_campaign_id = request.POST.get('template_id')
            selected_campaign = template_info.objects.get(id=selected_campaign_id)
            submitAddBtnBCampaign.template_file_path = selected_campaign.generic_campaign_info.Campaign_Name
            submitAddBtnBCampaign.template_additional_info = selected_campaign_id

        submitAddBtnBCampaign.client_id = request.user.id

        template_info_instance = template_info.objects.filter(id=id, client_id=request.user.id).first()
        if template_info_instance:
            submitAddBtnBCampaign.template_info = template_info_instance
            submitAddBtnBCampaign.generic_campaign_info = template_info_instance.generic_campaign_info
            submitAddBtnBCampaign.marketplace = template_info_instance.marketplace

        submitAddBtnBCampaign.save()

        if marketplace_id and marketplace_id != 'None':
            return HttpResponseRedirect(reverse('updateBCamaign', args=[submitAddBtnBCampaign.marketplace_id]))
        else:
            return HttpResponseRedirect(reverse('updateBCamaign', args=[id]))
    
    return render(request, 'B_campaign/editBCampaign.html')




def updateBtnBCamaign(request, id):
 
    updateBtnBCamaign = template_info_details.objects.filter(client_id=request.user.id, id=id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    formdata = Form.objects.filter(client_id= request.user.id)
    templatedata = template_info.objects.filter(client_id=request.user.id, status='APPROVED')

    context ={
        "updateBtnBCamaign": updateBtnBCamaign,
        'admin_permission_obj':admin_permission_obj,
        "id":id,
        'marketplace_id':marketplace_id,
        'subclient_preferences':subclient_preferences,
        'formdata':formdata,
        'templatedata':templatedata,

        
    }
    return render(request, 'B_campaign/editBtnBCampaign.html', context)

def subUpdateBtnBCamaign(request, id = None):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    subUpdateBCamaign = template_info_details.objects.filter(client_id=request.user.id, id=id)

    if request.method == 'POST':
        for i in subUpdateBCamaign:
            editinfo = template_info_details.objects.get(id=i.id)

            if request.POST.get('rebtnNum'):
                editinfo.template_button_num = request.POST.get('rebtnNum')

            if request.POST.get('reBtnName'):
                editinfo.template_button_name = request.POST.get('reBtnName')
            if request.POST.get('reBtnName1'):
                editinfo.template_button_type = request.POST.get('reBtnName1')


            if request.POST.get('reBtnInfo'):
                editinfo.template_additional_info = request.POST.get('reBtnInfo')
            # if request.POST.get('refootername'):
            #     editinfo.template_footer = request.POST.get('refootername')

            if 'refileInput' in request.FILES:
                editinfo.template_file_path = request.FILES['refileInput']

            if 'rephoneNumberInput' in request.POST and request.POST['rephoneNumberInput'] != '':
                editinfo.template_file_path = request.POST.get('rephoneNumberInput')

            elif 'reurlInput1' in request.POST and request.POST['reurlInput1'] != '':
                editinfo.template_file_path = request.POST.get('reurlInput1')

            elif 'reurlInput' in request.POST and request.POST['reurlInput'] != '':
                editinfo.template_file_path = request.POST.get('reurlInput')

            elif 'reformInput' in request.POST and request.POST['reformInput'] != '':
                editinfo.template_file_path = request.POST.get('reformInput')

            elif  'refileInput1' in request.POST and  request.POST['refileInput1'] !='':
                editinfo.template_file_path = request.POST.get('refileInput1')

            elif 'refoodvideo' in request.FILES:
                editinfo.template_file_path = request.FILES['refoodvideo']

            editinfo.save()
        

            if editinfo.marketplace_id:
                return redirect("updateBCamaign", id=editinfo.marketplace_id)
            else:
                return redirect("updateBCamaign", id) 
    return render(request, 'B_campaign/editBtnBCampaign.html') #,{'updateCampaign': subUpdateBCamaign, 'subclient_preferences':subclient_preferences,'admin_permission_obj':admin_permission_obj })  




def dashbord(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    form_5_records = Form.objects.order_by('-id')[:5]
    template_5_records = template_info.objects.order_by('-id')[:5]
    return render(request,  'B_campaign/dashbord.html',{'admin_permission_obj':admin_permission_obj, 'template_5_records':template_5_records, 'form_5_records':form_5_records} )


def deleteBtnBCampaign(request,id):
    client_id= request.user.id
    marketplace_id = request.GET.get('marketplace_id')

    deleteBBtncampaign = template_info_details.objects.get(client_id=request.user.id, pk=id)
    mkid = deleteBBtncampaign.template_info_id
    deleteBBtncampaign.delete()
    if mkid:
        return redirect('updateBCamaign' , id=mkid)
    else:
        return redirect('updateBCamaign')














from django.shortcuts import redirect
def subUpdateBCamaign(request, id):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    subUpdateBCamaign = generic_campaign_info.objects.filter(client_id=request.user.id, id=id)

    if request.method == 'POST':
        updateBCampaign_instance = template_info.objects.get(id=id)

        updateBCampaign_instance.generic_campaign_info.Campaign_Name = request.POST.get('reCampaignName')
        # updateBCampaign_instance.save()   


        updateBCampaign_instance.template_name = request.POST.get('retemplate_name')
        updateBCampaign_instance.template_header_text = request.POST.get('retemplate_header_text')
        updateBCampaign_instance.template_body_message = request.POST.get('template_body_message')
        updateBCampaign_instance.template_header_type = request.POST.get('selectsoptionbtn')
                    # if request.POST.get('refootername'):
        updateBCampaign_instance.template_footer = request.POST.get('refootername')

        if 'reCampaignHeaderImg' in request.FILES:
            updateBCampaign_instance.template_header_image = request.FILES['reCampaignHeaderImg']
        updateBCampaign_instance.generic_campaign_info.save()
        updateBCampaign_instance.save()

        if updateBCampaign_instance.marketplace_id is not None:
            return redirect('campaignList', id=updateBCampaign_instance.marketplace_id)
        else:
            return redirect('campaignList')  

    return render(request, 'B_campaign/editBCampaign.html', {'updateCampaign': subUpdateBCamaign, 'subclient_preferences':subclient_preferences,'admin_permission_obj':admin_permission_obj })


def deleteBCampaign(request,id):

    deleteBcampaign = template_info.objects.get(
        client_id=request.user.id, pk=id)
    mkid = deleteBcampaign.marketplace_id
    deleteBcampaign.delete()
    if mkid is not None:
        return redirect('campaignList' , id=mkid)
    else:
        return redirect('campaignList')


def addcustomer(request, id):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    context ={
       'admin_permission_obj':admin_permission_obj,
        'marketplace_id':marketplace_id,
        'subclient_preferences':subclient_preferences
    }
    return render(request, 'B_campaign/assignBCampaign.html', context)


def assignBCampaign(request, id):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')

    subUpdateBCamaign = template_info.objects.filter(client_id=request.user.id, id=id)
    campaignBList = generic_campaign_history.objects.filter(client_id=request.user.id, template_info_id=id)
    assignBCampaign = campaign_customer_master.objects.filter(client_id=request.user.id, marketplace_id=id)
    assignBCampaign = campaign_customer_master.objects.filter(client_id=request.user.id, marketplace_id=None)



    selectedItems = {} 

    context = {
        'assignBCampaign': assignBCampaign,
        'subUpdateBCamaign': subUpdateBCamaign,
        'selectedItems': selectedItems,
        'campaignBList': campaignBList,
        'id':id,
        'admin_permission_obj':admin_permission_obj,
        'subclient_preferences':subclient_preferences,
        'marketplace_id':marketplace_id,
        
    }
    return render(request, 'B_campaign/assignBCampaign.html', context)



def add_customer(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    print('add_customer mk id', marketplace_id)
    cantext ={
        'marketplace_id':marketplace_id,
        'admin_permission_obj':admin_permission_obj,
        'id':id,
        'subclient_preferences':subclient_preferences,
    }
    return render(request, 'B_campaign/addcustomer.html',cantext )



#  setup out flow 

def inflowaoutflowconfig(request):
    return render(request, 'B_campaign/inflowaoutflowconfig.html')

# def createtemplate(request, id):
#     subclient_id = request.session.get('subclient_id')
#     subclient = Subclient.objects.filter(id=subclient_id).first()
#     subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
#     marketplace_id = request.GET.get('marketplace_id')
#     campaign_Id= 0
#     infovalue = template_info.objects.filter(client_id= request.user.id, id=id)
#     listbtnvalue = template_info_details.objects.filter(client_id=request.user.id, template_info_id=id, generic_campaign_info_id=campaign_Id)
#
#
#     return render(request, 'B_campaign/createtemplate.html',{'admin_permission_obj':admin_permission_obj,'marketplace_id':marketplace_id,'listbtnvalue':listbtnvalue, 'infovalue':infovalue})


def createdynamicform(request):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient .objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient = subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id = request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')


    return render(request, 'B_campaign/createdynamicform.html', {'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})


def create_form(request):
    if request.method == 'POST':
        form_name = request.POST.get('form_name')
        form_header_type = request.POST.get('form_header_type')
        form_header_text = request.POST.get('form_header_text')
        form_header_image = request.POST.get('form_header_image')
        form_body_text = request.POST.get('form_body_text')
        form_body_footer = request.POST.get('form_body_footer')
        form_submit_button_name = request.POST.get('form_submit_button_name')
        form_open_button_name = request.POST.get('form_open_button_name')
        client = request.user  # Assuming User is the correct user model
        status = "draft"
        form = Form.objects.create(form_name=form_name,
                                   form_header_type=form_header_type,
                                   form_header_text=form_header_text,
                                   form_header_image=form_header_image,
                                   form_body_footer=form_body_footer,
                                   form_submit_button_name=form_submit_button_name,
                                   form_open_button_name=form_open_button_name,
                                   form_body_text=form_body_text,
                                   status=status,
                                   client=client)

        num_sections = int(request.POST.get('num_sections'))
        for i in range(num_sections):
            section_name = request.POST.get(f'section_{i}_name')
            section = Form_Section.objects.create(
                name=section_name, client=client, form=form)

            num_fields = int(request.POST.get(f'section_{i}_num_fields'))
            for j in range(num_fields):
                label = request.POST.get(f'section_{i}_field_{j}_label')
                field_type = request.POST.get(f'section_{i}_field_{j}_type')
                field = Form_Field.objects.create(
                    label=label, field_type=field_type, client=client, section=section)

                if field_type in ['radio', 'checkbox', 'dropdown']:
                    num_options = int(request.POST.get(
                        f'section_{i}_field_{j}_num_options'))
                    for k in range(num_options):
                        option_label = request.POST.get(
                            f'section_{i}_field_{j}_option_{k}')
                        choice = Form_FieldChoice.objects.create(
                            client=client, field=field, choice_text=option_label)

        return redirect('forminfo')
    # else:
    return render(request, 'B_campaign/createdynamicform.html')




import json
import logging
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# Define logger
logger = logging.getLogger(__name__)

@login_required
def save_form_data(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        form_id = request.POST.get("form_id")  # Assuming you're passing the form_id from the frontend
        form_instance = get_object_or_404(Form, pk=form_id, client_id=request.user.id)
        data = json.loads(request.body)
        logger.info(f"Received form data: {data}")

        client_id = request.user.id  
        farmdata = Form.objects.filter(client_id=request.user.id, id=id)
        print('farmdata', farmdata)
        try:
            # # Create the Form object
            # form = Form.objects.create(
            #     client_id=client_id,
            #     form_name=data.get('formname'),
            #     form_header_text=data.get('formheadertext'),
            #     form_header_image=data.get('formheaderimage'),
            #     form_body_text=data.get('formbodytext'),
            #     form_body_footer=data.get('formbodyfooter'),
            #     form_open_button_name=data.get('formopenbuttonname')
            # )
            # logger.info(f"Created form object: {form}")

            for section_data in data.get('sections', []):
                section_name = section_data.get('name')
                # fields_data = section_data.get('fields')

                section = Form_Section.objects.create(
                    client_id=client_id,
                    name=section_name,
                    form_id=farmdata
                )
                logger.info(f"Created section object: {section}")

                for field_data in fields_data:
                    field_label = field_data.get('label')
                    field_type = field_data.get('type')
                    field_options = field_data.get('options')

                    field = Form_Field.objects.create(
                        client_id=client_id,
                        label=field_label,
                        field_type=field_type,
                        section=section
                    )
                    logger.info(f"Created field object: {field}")

                    if field_options:
                        for option in field_options:
                            choice = Form_FieldChoice.objects.create(
                                client_id=client_id,
                                choice_text=option,
                                field=field
                            )
                            logger.info(f"Created field choice: {option} for field: {field}")
                            if not choice.id: 
                                raise Exception("Failed to save field choice")
            
            return JsonResponse({'success': True})
        
        except Exception as e:
            logger.error(f"Error saving form data: {e}")

            return JsonResponse({'success': False, 'error': str(e)})
    
    logger.error("Invalid request: Not a POST request or not an AJAX request")
    return JsonResponse({'success': False, 'error': 'Invalid request'})



def deteleform(request, id):
    formdata = Form.objects.get(client_id= request.user.id, pk=id)
    formdata.delete()
    return redirect('forminfo')

# def generateform(request, id):
#     print('generateform', id)
#     return redirect('forminfo')
def generateform(request, id):
    print('generateform', id)
    facebook_detailsObj = facebook_details.objects.filter(client_id=request.user.id)
    phonenumberID = 0
    facebook_token = ''
    waba_id = 0
    for f_i in facebook_detailsObj:
        phonenumberID = f_i.fb_phone_number_id
        facebook_token = f_i.fb_access_token
        waba_id = f_i.fb_Whatsapp_business_account_id
    print(phonenumberID)
    print(facebook_token)
    print("rrr")
    random_number = random.randint(1, 1000)
    print("fffff")
    formDetObj = Form.objects.filter(client_id=request.user.id, id=id)
    formName = ''
    word = ''
    f_base_name = ''
    formSubmitButton = ''
    for r_i in formDetObj:
        formName = r_i.form_name
        formSubmitButton = r_i.form_submit_button_name


    if " " in formName:
        word = formName.replace(" ", "_")
        f_base_name = word
    else:
        f_base_name = formName

    # if any(char.isdigit() for char in word):
    #     word = ''.join(char for char in word if not char.isdigit())

    print(f_base_name)
    print("formmmmmmmm name")

    base_name = f_base_name
    print("base name---->", base_name)
    new_name = f'{base_name}{random_number}'
    url = f"https://graph.facebook.com/v18.0/{waba_id}/flows"

    payload = {'name': new_name,
               'categories': '["OTHER"]'}

    headers = {
        'Authorization': f'Bearer {facebook_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    response_data = json.loads(response.text)
    id_value = response_data.get('id')
    if id_value is not None:
        print("ID:", id_value)
        print("narrri")
        Saveflowobj = Form.objects.filter(client_id=request.user.id, id=id)
        for s_i in Saveflowobj:
            s_i.flow_id = id_value
            s_i.screen_name = base_name
            s_i.save()
        All_fields = []
        Saveflowobj = Form.objects.filter(client_id=request.user.id, id=id)
        for s_i in Saveflowobj:
            Saveflowobj1 = Form_Section.objects.filter(client_id=request.user.id, form_id=s_i.id)
            for z_i in Saveflowobj1:
                fieldsObj = Form_Field.objects.filter(client_id=request.user.id, section_id=z_i.id)
                print(fieldsObj)
                print("om")
                for i, f_i in enumerate(fieldsObj):
                    field_name = f_i.label
                    print(f_i.field_type)
                    if 'text' in f_i.field_type:
                        text_info = {
                            "type": "TextInput",
                            "label": f_i.label,
                            "input-type": "text",
                            "name": field_name,
                            "required": True
                        }
                        All_fields.append(text_info)
                    elif 'select' in f_i.field_type:
                        f_id = f_i.id
                        all_text = []
                        choice_textInfo = Form_FieldChoice.objects.filter(client_id=request.user.id, field_id=f_id)
                        for c_i in choice_textInfo:
                            all_text.append(c_i.choice_text)
                        list_all_text = []
                        for g_i in range(len(all_text)):
                            list_all_text.append({
                                "id": all_text[g_i],
                                "title": all_text[g_i]
                            })
                        select_info = {
                            "type": "Dropdown",
                            "label": f_i.label,
                            "required": False,
                            "name": field_name,
                            "data-source": list_all_text
                        }
                        All_fields.append(select_info)
                    elif 'radio' in f_i.field_type:
                        f_id = f_i.id
                        all_text = []
                        choice_textInfo = Form_FieldChoice.objects.filter(client_id=request.user.id, field_id=f_id)
                        for c_i in choice_textInfo:
                            all_text.append(c_i.choice_text)
                        list_all_text = []
                        for g_i in range(len(all_text)):
                            list_all_text.append({
                                "id": all_text[g_i],
                                "title": all_text[g_i]
                            })
                        radio_info = {
                            "type": "RadioButtonsGroup",
                            "label": f_i.label,
                            "required": False,
                            "name": field_name,
                            "data-source": list_all_text
                        }
                        All_fields.append(radio_info)
                    elif 'checkbox' in f_i.field_type:
                        f_id = f_i.id
                        all_text = []
                        choice_textInfo = Form_FieldChoice.objects.filter(client_id=request.user.id, field_id=f_id)
                        for c_i in choice_textInfo:
                            all_text.append(c_i.choice_text)
                        list_all_text = []
                        for g_i in range(len(all_text)):
                            list_all_text.append({
                                "id": all_text[g_i],
                                "title": all_text[g_i]
                            })
                        checkbox_info = {
                            "type": "CheckboxGroup",
                            "label": f_i.label,
                            "required": False,
                            "name": field_name,
                            "data-source": list_all_text
                        }
                        All_fields.append(checkbox_info)
                    elif 'number' in f_i.field_type or 'phone' in f_i.field_type:
                        number_info = {
                            "type": "TextInput",
                            "label": f_i.label,
                            "input-type": "number",
                            "name": field_name,
                            "required": False
                        }
                        All_fields.append(number_info)
                    elif 'email' in f_i.field_type:
                        email_info = {
                            "type": "TextInput",
                            "label": f_i.label,
                            "name": field_name,
                            "input-type": "email",
                            "required": False
                        }
                        All_fields.append(email_info)
                    elif 'password' in f_i.field_type:
                        password_info = {
                            "type": "TextInput",
                            "label": f_i.label,
                            "name": field_name,
                            "input-type": "password",
                            "required": False
                        }
                        All_fields.append(password_info)

                footer_payload = {
                    "type": "Footer",
                    "label": formSubmitButton,
                    "on-click-action": {
                        "name": "complete",
                        "payload": {field["name"]: "${form." + field["name"] + "}" for field in All_fields}
                    }
                }
                All_fields.append(footer_payload)
                print("namah")
                print(All_fields)
                data = {
                    "version": "2.1",
                    "screens": [
                        {
                            "id": base_name,
                            "title": formName,
                            "data": {},
                            "terminal": True,
                            "layout": {
                                "type": "SingleColumnLayout",
                                "children": [
                                    {
                                        "type": "Form",
                                        "name": "form",
                                        "children": All_fields

                                    }
                                ]
                            }
                        }
                    ]
                }
                file_name = f'{new_name}.json'
                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=2)
                print("succesfully generated the json file..")

                url = f" https://graph.facebook.com/v18.0/{id_value}/assets"

                payload = {'name': 'flow.json',
                           'asset_type': 'FLOW_JSON'}
                file_path = f'C:/Vailo/20-03-2024 new dashboard/A_vMart/A_vMart/{new_name}.json'
                files = [
                    ('file',
                     ('file', open(file_path, 'rb'), 'application/json'))
                ]
                headers = {
                    'Authorization': f'Bearer {facebook_token}'
                }

                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                print("king nag")

                print(response.text)
                print("s successfully updated json asset")
                url = f"https://graph.facebook.com/v18.0/{id_value}/publish"

                payload = {}
                headers = {
                    'Authorization': f'Bearer {facebook_token}'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                if response.status_code == 200:
                    print("Publish successful")

                else:
                    print(f"Publish failed with status code: {response.status_code}")




    return redirect('forminfo')





def editdynamicform(request, id):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient .objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient = subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id = request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    form = get_object_or_404(Form.objects.prefetch_related('sections__form_fields__choices'), pk=id)
    form = Form.objects.get(client_id=request.user.id, id=id)
    sectiondata = Form_Section.objects.filter(client_id=request.user.id, form_id=id)
    return render(request, 'B_campaign/editdynamicform.html',{'id':id, 'admin_permission_obj':admin_permission_obj, 'form':form, 'sectiondata':sectiondata})
   



def update_form(request, form_id):
    if request.method == 'POST':
        form = get_object_or_404(Form, id=form_id)
        form_name = request.POST.get('form_name')
        form.form_name = form_name
        form.save()

        # Update sections
        for section in form.sections.all():

            section_name = request.POST.get(f'section_name_{section.id}')
            section.name = section_name
            section.save()

            # Update fields
            for field in section.form_fields.all():
                field_label = request.POST.get(f'field_label_{field.id}')
                field.label = field_label
                field.save()

                # Update choices if any
                if field.choices.all():
                    for choice in field.choices.all():
                        choice_text = request.POST.get(f'choice_text_{choice.id}')
                        choice.choice_text = choice_text
                        choice.save()

        messages.success(request, 'Form updated successfully!')
        return redirect('forminfo') 



def forminfo(request):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient .objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient = subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id = request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    form_data = Form.objects.filter(client_id= request.user.id)
    return render(request, 'B_campaign/forminfo.html', {'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'form_data':form_data})



def view_form_details(request, form_id):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    # Fetch the specific form along with its related sections, fields, and choices
    form = get_object_or_404(Form.objects.prefetch_related('sections__form_fields__choices'), pk=form_id)

    return render(request, 'B_campaign/view_form_details.html', {'form': form, 'admin_permission_obj':admin_permission_obj} )


def view_form(request, form_id):
    form = get_object_or_404(Form, id=form_id, client_id=request.user.id)
    return render(request, 'B_campaign/view_form.html', {'form': form})






def eupdate_form(request, form_id):
    form = get_object_or_404(Form, id=form_id, client_id=request.user.id)

    if request.method == 'POST':
        num_sections = int(request.POST.get('num_sections'))
        for i in range(num_sections):
            section_id = request.POST.get(f'section_{i}_id')
            section_name = request.POST.get(f'section_{i}_name')

            if section_id:
                section = get_object_or_404(Form_Section, id=section_id)
                section.name = section_name
                section.save()
            else:
                section = Form_Section.objects.create(
                    name=section_name, form=form)

            num_fields = int(request.POST.get(f'section_{i}_num_fields'))
            for j in range(num_fields):
                field_id = request.POST.get(f'field_{i}_{j}_id')
                field_label = request.POST.get(f'field_{i}_{j}_label')
                field_type = request.POST.get(f'field_{i}_{j}_type')

                if field_id:
                    field = get_object_or_404(Form_Field, id=field_id)
                    field.field_label = field_label
                    field.field_type = field_type
                    field.save()
                else:
                    field = Form_Field.objects.create(
                        field_label=field_label, field_type=field_type, section=section)

                if field_type in ['radio', 'checkbox', 'dropdown']:
                    num_options = int(request.POST.get(
                        f'field_{i}_{j}_num_options'))
                    for k in range(num_options):
                        option_id = request.POST.get(f'option_{i}_{j}_{k}_id')
                        option_text = request.POST.get(
                            f'option_{i}_{j}_{k}_text')

                        if option_id:
                            option = get_object_or_404(
                                Form_FieldChoice, id=option_id)
                            option.option_text = option_text
                            option.save()
                        else:
                            option = Form_FieldChoice.objects.create(
                                option_text=option_text, field=field)

        return redirect('setupdetails')  # Redirect after successful update
    else:
        return render(request, 'B_campaign/edit_form.html', {'form': form})



# setup inflow

def setupdetails(request):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    parentdata = Inflow_Setup_Details.objects.filter(client_id= request.user.id)
    return render(request, 'B_campaign/setupdetails.html', {'parentdata':parentdata, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})


def addparent(request):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    return render(request, 'B_campaign/addparent.html', {'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id })


def submitparentdata(request):
    if request.method == 'POST':
        createparentdata = Inflow_Setup_Details(client_id = request.user.id)
        createparentdata.Parent_ID = request.POST.get('ParentID')
        createparentdata.open_button_type = request.POST.get('openbuttontype')
        createparentdata.open_button_name = request.POST.get('openbuttonname')
        createparentdata.short_title = request.POST.get('shorttitle')
        createparentdata.short_description = request.POST.get('shortdescription')
        createparentdata.additional_info = request.POST.get('additionalinfo')
        createparentdata.additional_info1 = request.POST.get('additionalinfo1')
        createparentdata.additional_info2 = request.POST.get('additionalinfo2')
        if 'additionalfilepath' in request.FILES:
            createparentdata.additional_file_path = request.FILES['additionalfilepath']
        if 'additionalfilepath1' in request.FILES:
            createparentdata.additional_file_path1 = request.FILES['additionalfilepath1']
        if 'additionalfilepath2' in request.FILES:
            createparentdata.additional_file_path2 = request.FILES['additionalfilepath2']
        if 'inflowheaderfilepath' in request.FILES:
            createparentdata.inflowheader_file_path = request.FILES['inflowheaderfilepath']
        createparentdata.inflow_header_type = request.POST.get('inflowheadertype')
        createparentdata.inflow_header_text = request.POST.get('inflowheadertext')
        createparentdata.inflow_body_text = request.POST.get('inflowbodytext')
        createparentdata.inflow_footer_text = request.POST.get('inflowfootertext')
        createparentdata.client_id= request.user.id
        createparentdata.save()
        return redirect('setupdetails')

    return render(request, 'B_campaign/addparent.html')




def addchiled(request, id):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    parentdata = Inflow_Setup_Details.objects.filter(client_id= request.user.id, id=id)

    return render(request, 'B_campaign/addchield.html',{'id':id, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'parentdata':parentdata})

from django.shortcuts import render, redirect, get_object_or_404

def submitchailddata(request, id):
    # Get the parent object based on the provided id
    parent_object = get_object_or_404(Inflow_Setup_Details, id=id)

    if request.method == 'POST':
        # Create a new child object associated with the parent
        childdate = Inflow_Setup_Details()
        childdate.Parent_ID = request.POST.get('ParentID')
        # childdate.Parent_ID = parent_object  # Associate the child with the parent
        childdate.open_button_type = request.POST.get('openbuttontype')
        childdate.open_button_name = request.POST.get('openbuttonname')
        childdate.short_title = request.POST.get('shorttitle')
        childdate.short_description = request.POST.get('shortdescription')
        childdate.additional_info = request.POST.get('additionalinfo')
        childdate.additional_info1 = request.POST.get('additionalinfo1')
        childdate.additional_info2 = request.POST.get('additionalinfo2')

        if 'additionalfilepath' in request.FILES:
            childdate.additional_file_path = request.FILES['additionalfilepath']
        if 'additionalfilepath1' in request.FILES:
            childdate.additional_file_path1 = request.FILES['additionalfilepath1']
        if 'additionalfilepath2' in request.FILES:
            childdate.additional_file_path2 = request.FILES['additionalfilepath2']
        if 'inflowheaderfilepath' in request.FILES:
            childdate.inflowheader_file_path = request.FILES['inflowheaderfilepath']

        childdate.inflow_header_type = request.POST.get('inflowheadertype')
        childdate.inflow_header_text = request.POST.get('inflowheadertext')
        childdate.inflow_body_text = request.POST.get('inflowbodytext')
        childdate.inflow_footer_text = request.POST.get('inflowfootertext')
        childdate.client_id = request.user.id

        childdate.save()
        return redirect('setupdetails')

    return render(request, 'B_campaign/addchield.html')

def editinflowsetup(request, id):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    inflowsetupdata = Inflow_Setup_Details.objects.filter(client_id= request.user.id, id=id)
    return render(request, 'B_campaign/editinflowsetup.html', {'id':id, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'inflowsetupdata':inflowsetupdata})


def editsubmitflowdata(request, id):
    flowdate = Inflow_Setup_Details.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('updateservices_marketplace_id', marketplace_id)
    if request.method =='POST':
        for i in flowdate:
            flowdate = Inflow_Setup_Details.objects.filter(client_id=request.user.id, id=id)
            if i in flowdate:
                flowdateedit = Inflow_Setup_Details.objects.get(id=i.id)
                flowdateedit.Parent_ID = request.POST.get('reParentID')
                flowdateedit.open_button_type = request.POST.get('reopenbuttontype')
                flowdateedit.open_button_name = request.POST.get('reopenbuttonname')
                flowdateedit.short_title = request.POST.get('reshorttitle')
                flowdateedit.short_description = request.POST.get('reshortdescription')
                flowdateedit.additional_info = request.POST.get('readditionalinfo')
                flowdateedit.additional_info1 = request.POST.get('readditionalinfo1')
                flowdateedit.additional_info2 = request.POST.get('readditionalinfo2')

                if 'reAdditionalFile' in request.FILES:
                    flowdateedit.additional_file_path = request.FILES['reAdditionalFile']
                if 'reAdditionalFile1' in request.FILES:
                    flowdateedit.additional_file_path1 = request.FILES['reAdditionalFile1']
                if 'reAdditionalFile2' in request.FILES:
                    flowdateedit.additional_file_path2 = request.FILES['reAdditionalFile2']
                if 'reHeaderType' in request.FILES:
                    flowdateedit.inflowheader_file_path = request.FILES['reHeaderType']

                flowdateedit.inflow_header_type = request.POST.get('reinflowheadertype')
                flowdateedit.inflow_header_text = request.POST.get('reinflowheadertext')
                flowdateedit.inflow_body_text = request.POST.get('reinflowbodytext')
                flowdateedit.inflow_footer_text = request.POST.get('reinflowfootertext')
                flowdateedit.save()

                return redirect('setupdetails')

    return render(request, 'B_campaign/editinflowsetup.html')




def deleteparent(request, id):
    deleteparent = Inflow_Setup_Details.objects.filter(client_id= request.user.id, id=id)
    marketplace_id =request.GET.get('marketplace_id')
    deletedata = Inflow_Setup_Details.objects.filter(client_id= request.user.id, pk=id)
    deletedata.delete()
    return redirect('setupdetails')



def contactlist(request):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    customerdata = campaign_customer_master.objects.filter(client_id=request.user.id)
    total_contacts = customerdata.count()  # Counting total contacts
    return render(request, 'B_campaign/contactlist.html', {'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id, 'customerdata': customerdata, 'total_contacts': total_contacts})

def addcustomer(request):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    customerdata = campaign_customer_master.objects.filter(client_id=request.user.id)
    return render(request, 'B_campaign/addcustomer.html', {'admin_permission_obj':admin_permission_obj, 'customerdata':customerdata})

from django.contrib import messages

def delete_selected_contacts(request):
    if request.method == 'POST':
        selected_contact_ids = request.POST.get('selected_contacts')
        selected_contact_ids = selected_contact_ids.split(',')  # Convert string to list
        try:
            # Delete selected contacts from the database
            campaign_customer_master.objects.filter(id__in=selected_contact_ids).delete()
            messages.success(request, 'Selected contacts deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting contacts: {str(e)}')
    return redirect('contactlist')  # Redirect back to the contact list page



def submitcustomer(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    
    if request.method == 'POST':
        customer_name = request.POST.get('CustomerName')
        customer_email = request.POST.get('CustomerEmail')
        customer_whatsapp_number = request.POST.get('Customernumber')
        
        # if campaign_customer_master.objects.filter(client_id= request.user.id, Customer_email=customer_email).exists() or \
        if campaign_customer_master.objects.filter(client_id= request.user.id, Customer_Whatsapp_Number=customer_whatsapp_number).exists():
            messages.error(request, 'Duplicate Entry Detected')
            return redirect('contactlist') 
        createdata = campaign_customer_master(
            Customer_Name=request.POST.get('CustomerName'),
            Customer_email=request.POST.get('CustomerEmail'),
            Customer_Whatsapp_Number=request.POST.get('Customernumber'),
            Customer_City=request.POST.get('Customercity'),
            Customer_Status=request.POST.get('Customerstatus'),
            Customer_Address_Line1=request.POST.get('Customeraddr1'),
            Customer_Address_Line2=request.POST.get('Customeraddr2'),
            Customer_Address_Landmark=request.POST.get('Customerlandmark'),
            Customer_Address_Pincode=request.POST.get('Customerpincode'),
            Customer_State=request.POST.get('Customerstate'),
            Customer_Country=request.POST.get('Customercountry'),
            Customer_Alternate_Number=request.POST.get('Customeralterna'),
            client_id=request.user.id,
            # createdata.save()
        )

        createdata.save()
        return redirect('contactlist')
        
    return render(request, 'B_campaign/addcustomer.html',{'messages':messages})


import csv

def excel_customers1(request):
    if request.method == 'POST' and request.FILES['file']:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return render(request, 'B_campaign/addcustomer.html', {'error_message': 'Please upload a CSV file.'})
        
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        skipped_entries = []
        for row in reader:
            email = row['Email address']
            whatsapp_number = row['Contact number']
            # Check if email or WhatsApp number already exists in the database
            if campaign_customer_master.objects.filter(client_id = request.user.id, Customer_email=email).exists() or \
               campaign_customer_master.objects.filter(client_id = request.user.id, Customer_Whatsapp_Number=whatsapp_number).exists():
                skipped_entries.append(row)
            else:
                customer = campaign_customer_master(
                    Customer_Name=row['Name '],
                    Customer_email=email,
                    Customer_Whatsapp_Number=whatsapp_number,
                    # Customer_tag = row['tag'],
                    # Customer_City = row['city'],
                    # Customer_Status = row['status'],
                    # Customer_Address_Line1 = row['address1'],
                    # Customer_Address_Line2 = row['address2'],
                    # Customer_Address_Landmark = row['landmark'],
                    # Customer_Address_Pincode = row['pincode'],
                    # Customer_State = row['state'],
                    # Customer_Country = row['country'],
                    # Customer_Alternate_Number = row ['alternate number'],
                    client_id=request.user.id
                )
                customer.save()
        
        if skipped_entries:
            messages.warning(request, 'Duplicate Entry Detected.')

        return redirect('contactlist')
    
    return render(request, 'B_campaign/contactlist.html', {'messages':messages})


def editcustomerdata(request, id):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    editdata =  campaign_customer_master.objects.filter(client_id=request.user.id, id=id)
    
    return render(request, 'B_campaign/editcustomer.html',{'admin_permission_obj':admin_permission_obj, 'editdata':editdata})

def updatecustomer(request, id):
    editdata = campaign_customer_master.objects.filter(client_id = request.user.id, id=id)
    if request.method == 'POST':
        for i in editdata:
            editdata = campaign_customer_master.objects.filter(client_id = request.user.id, id=id)
            if i in editdata:
                editcustomerdata =campaign_customer_master.objects.get(id=i.id)
                editcustomerdata.Customer_Name = request.POST.get('editCustomerName')
                editcustomerdata.Customer_email = request.POST.get('editCustomerEmail')
                editcustomerdata.Customer_Whatsapp_Number = request.POST.get('editCustomernumber')
                editcustomerdata.Customer_City = request.POST.get('editCustomercity')
                editcustomerdata.Customer_Status = request.POST.get('editCustomerstatus')
                editcustomerdata.Customer_Address_Line1 = request.POST.get('editCustomeraddr1')
                editcustomerdata.Customer_Address_Line2 = request.POST.get('editCustomeraddr2')
                editcustomerdata.Customer_Address_Landmark = request.POST.get('editCustomerlandmark')
                editcustomerdata.Customer_Address_Pincode = request.POST.get('editCustomerpincode')
                editcustomerdata.Customer_State = request.POST.get('editCustomerstate')
                editcustomerdata.Customer_Country = request.POST.get('editCustomercountry')
                editcustomerdata.Customer_Alternate_Number = request.POST.get('editCustomeralterna')
                editcustomerdata.save()
                return redirect('contactlist')
    return render(request, 'B_campaign/editcustomer.html')


def deletecustomer(request, id):
    deletedata =campaign_customer_master.objects.filter(client_id=request.user.id, pk=id)
    deletedata.delete()
    return redirect('contactlist')



def footprint(request):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    foodprintdata = campaign_footprint.objects.filter(client_id = request.user.id)
    return render(request, 'B_campaign/foodprintinfo.html',{'admin_permission_obj':admin_permission_obj, 'foodprintdata':foodprintdata})


from django.shortcuts import render

def search_results(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    if request.method == "GET":
        campaign_name = request.GET.get('campaign_name', '')
        button = request.GET.get('button', '')
        number = request.GET.get('number', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')

        foodprintdata = campaign_footprint.objects.filter(
            client_id=request.user.id
        )

        if campaign_name:
            foodprintdata = foodprintdata.filter(campaign_name__icontains=campaign_name)
        if button:
            foodprintdata = foodprintdata.filter(button__icontains=button)
        if number:
            foodprintdata = foodprintdata.filter(From_number__icontains=number)
        if start_date:
            foodprintdata = foodprintdata.filter(date__gte=start_date)
        if end_date:
            foodprintdata = foodprintdata.filter(date__lte=end_date)

        return render(request, 'B_campaign/foodprintinfo.html', {'foodprintdata': foodprintdata, 'admin_permission_obj':admin_permission_obj})


def addcomgroup(request):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    grouplist = campaign_groups.objects.filter(client_id=request.user.id)
    templatedata = template_info.objects.filter(client_id=request.user.id, status='APPROVED')

    return render(request, 'B_campaign/addcamgroup.html',{'admin_permission_obj':admin_permission_obj, 'grouplist':grouplist, 'templatedata':templatedata})

def addgroups(request):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
   
    return render(request, 'B_campaign/addgroups.html',{'admin_permission_obj':admin_permission_obj})

def submitgrouptype(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    if request.method == 'POST':
        creategroup = campaign_groups()
        creategroup.group_name = request.POST.get('groupname')
        creategroup.client_id = request.user.id
        creategroup.save()

        return redirect('addcomgroup')
    return render(request, 'B_campaign/addgroups.html')


def editgroupdata(request, id):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    editgroupdata = campaign_groups.objects.filter(client_id= request.user.id, id=id)
    return render(request, 'B_campaign/editgroupdata.html',{'admin_permission_obj':admin_permission_obj, 'editgroupdata':editgroupdata})

def updatesubmitgrouptype(request, id):
    editgroups= campaign_groups.objects.filter(client_id= request.user.id, id=id)
    if request.method == 'POST':
        for i in editgroups:
            editdata = campaign_groups.objects.filter(client_id=request.user.id, id=id)
            if i in editdata:
                editgroupsdata = campaign_groups.objects.get(id=i.id)
                editgroupsdata.group_name = request.POST.get('regroupname')
                editgroupsdata.save()

                return redirect('addcomgroup')
    return render(request, 'B_campaign/editgroupdata.html')

def detelegroup(request, id):
    deletegroupdata = campaign_groups.objects.filter(client_id= request.user.id, pk=id)
    deletegroupdata.delete()
    return redirect('addcomgroup')


def numbermapping(request, id):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    assignBCampaign = campaign_customer_master.objects.filter(client_id=request.user.id )
    subUpdateBCamaign = campaign_groups.objects.filter(client_id=request.user.id, id=id)
    campaignBList = campaign_group_customer_mappings.objects.filter(client_id=request.user.id, campaign_groups_id=id)

    return render(request, 'B_campaign/customermapping.html',{'assignBCampaign':assignBCampaign, 'campaignBList':campaignBList, 'subUpdateBCamaign':subUpdateBCamaign,  'admin_permission_obj':admin_permission_obj})







def insrtuctions(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    return render(request, 'B_campaign/insrtuctions.html',{'admin_permission_obj':admin_permission_obj})

@transaction.atomic
def moveBCampaignList(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_items = data.get('selected_items')
        duplicate_entries = [] 
        moved_data = []

        try:
            with transaction.atomic():
                for item in selected_items:
                    campaign_customer_master_id = item.get('campaign_customer_master_id')
                    if campaign_customer_master_id is None:
                        print("Campaign Customer Master ID is missing.")
                        continue

                    try:
                        campaign_customer_master_instance = campaign_customer_master.objects.get(
                            id=campaign_customer_master_id)
                    except ObjectDoesNotExist:
                        print(
                            f"Campaign Customer Master with ID {campaign_customer_master_id} does not exist.")
                        continue

                    try:
                        # Check if marketplace is provided, otherwise use the marketplace from generic_campaign_info
                        marketplace_id = data.get('marketplace')
                        if marketplace_id is None:
                            marketplace_id = campaign_groups.objects.get(id=id).marketplace_id

                        campaign_history = campaign_group_customer_mappings.objects.create(
                        campaign_customer_master=campaign_customer_master_instance,
                        client=request.user,
                        campaign_groups_id=id,
                        marketplace_id=marketplace_id
                        )
                        moved_data.append({
                            'campaign_customer_master_id': campaign_customer_master_id
                        })
                        print(f"Campaign created successfully: {campaign_history}")
                    except IntegrityError:
                        print(
                            "Duplicate entry: The combination of campaign_customer_master, client, and template_info_id must be unique.")

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})

        # Check if there are any duplicate entries
        if duplicate_entries:
            return JsonResponse({'success': False, 'duplicate_entries': duplicate_entries})
        else:
            return JsonResponse({'success': True, 'moved_data': moved_data})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def deleteBCampaignList(request, id):
    client_id = request.user.id
    deletefooditems = campaign_group_customer_mappings.objects.filter(client_id=request.user.id, pk=id)
    deletevall =0
    for i in deletefooditems:
        deletevall = i.campaign_groups_id
    deletefooditems.delete()
    return redirect('numbermapping', id=deletevall)



def submitform(request):
    if request.method == 'POST':
        createformdata = Form()
        createformdata.form_name = request.POST.get('formname')
        
        createformdata.form_header_text = request.POST.get('formheadertext')
        if 'formheaderimage' in request.FILES:
            createformdata.form_header_image = request.FILES['formheaderimage']
        createformdata.form_header_type = request.POST.get('screenname')
        createformdata.form_body_text = request.POST.get('formbodytext')
        createformdata.form_body_footer = request.POST.get('formbodyfooter')
        createformdata.form_submit_button_name = request.POST.get('formsubmitbuttonname')
        createformdata.form_open_button_name = request.POST.get('formopenbuttonname')
        createformdata.client_id= request.user.id
        createformdata.save()
        return redirect('forminfo')
    return render(request, 'B_campaign/createdynamicform.html')


def addsection(request, id):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    formdata = Form.objects.filter(client_id= request.user.id,id=id)

    return render(request, 'B_campaign/addsections.html',{'admin_permission_obj':admin_permission_obj})



def formconfig(request):
    return render(request, 'B_campaign/formconfig.html')



def formdata(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    All_forms = Form.objects.filter(client_id=request.user.id,status='APPROVED')
    context={
        'formdata':All_forms,
        'admin_permission_obj':admin_permission_obj
    }
    return render(request,'B_campaign/formData.html',context)





def getformdata(request):
    All_forms = Form.objects.filter(client_id=request.user.id, status='APPROVED')
    print(All_forms)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    # formdataobj = ''
    if request.method == 'POST':
        selected_value = request.POST.get("form_select")
        print("selected_value",selected_value)
        formdataobj = campaign_formdata.objects.filter(client_id=request.user.id, Form_id=selected_value)

# Form_id
    message="Below is the form data"
    context={
        'message': message,
        'formdata': All_forms,
        'formdataobj':formdataobj,
        'admin_permission_obj':admin_permission_obj
    }
    return render(request,'B_campaign/formData.html',context)



















from vailodb.models import admin_permission

# def addTempleteBtn(request, id=None):
#     print('hhhhh')
#     subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
#     subclient = Subclient.objects.filter(id=subclient_id).first()
#     subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
#     marketplace_id = request.GET.get('marketplace_id')
#     print('addTempleteBtn mk id', marketplace_id)
#     template_info_id = id
#     print('qqqq')
#     if id is not None:
#         listbtn = template_info_details.objects.filter(client_id=request.user.id, template_info_id=template_info_id)
#         # Additional logic for handling the case when id is present
#         print('aqqqq')
#     else:
#         listbtn = template_info_details.objects.filter(client_id=request.user.id, marketplace_id=None)
#         print('bqqqq')
    
#     context = {
#         'subclient_preferences': subclient_preferences,
#         'listbtn': listbtn, 
#     #     'infoCampaign': infoCampaign, 
#         'admin_permission_obj': admin_permission_obj,
#         "template_info_id" :template_info_id,
#     }

#     return render(request, 'B_campaign/btnTemplateList.html', context)




def addcampMarketPlace(request):
    # Clear the 'marketplace_id' key from the session
    request.session.pop('marketplace_id', None)
    request.session.save()
    print('Cleared entire session')

    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    addcampMarketPlace = campaign_marketplace.objects.filter(client=request.user.id)
    
    context = {
        'addcampMarketPlace': addcampMarketPlace, 
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,
    }

    return render(request, 'B_campaign/addcamMarketPlace.html', context)


def addcampForm(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    addcampMarketPlace = campaign_marketplace.objects.filter(client=request.user.id)
    
    context = {
        'addcampMarketPlace': addcampMarketPlace, 
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,
    }

    return render(request, 'B_campaign/addcampFormMarketPlace.html',context)


def submitcamp(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    if request.method == "POST":
        submitcamp = campaign_marketplace()
        submitcamp.campaign_name = request.POST.get('campaignName')
        submitcamp.campaign_type = request.POST.get('campaignType')
        submitcamp.campaign_category = request.POST.get('campaignCategory')
        # submitDonation.Event_Message_Header = request.POST.get('eventmessageheader')
        #  submitDonation.Event_Body = request.POST.get('eventbody')
        # submitDonation.Event_Footer = request.POST.get('eventfooter')
        submitcamp.campaign_location = request.POST.get('campaignLocation')
        # submitDonation.Event_Logo = request.FILES['Eventlogo']
        # submitDonation.Event_ticket_image = request.FILES['Eventticketimg']
        submitcamp.campaign_description =request.POST.get('campaignDescription')
        submitcamp.campaign_link_text =request.POST.get('campaign_link_text')
        submitcamp.campaign_url =request.POST.get('campaign_url')
        submitcamp.campaign_id =request.POST.get('campaign_id')
        submitcamp.campaign_key =request.POST.get('campaign_key')
        submitcamp.campaign_contact_number = request.POST.get('campaignContactNumber')
        # submitDonation.Event_Message_Header_Text = request.POST.get(
        #     'eventheadertext')
        # submitDonation.Event_Message_Body_Text = request.POST.get(
        #     'eventbodytext')
        # submitDonation.Event_Message_Footer_Text = request.POST.get(
        #     'eventfootertext')
        # submitDonation.Event_slots_button_name = request.POST.get(
        #     'eventslotbuttonname')
        submitcamp.client_id = request.user.id

        # Get the selected status value from the form
        # status_value = int(request.POST.get('status', 1))
        # submitDonation.status = status_value
        submitcamp.save()
        return redirect("addcampMarketPlace")
    return render(request, 'B_campaign/addcampFormMarketPlace.html',{'subclient_preferences':subclient_preferences,'admin_permission_obj':admin_permission_obj})


def editcampMarketPlace(request, id):
    client_id = request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
 
    modifyCamp = campaign_marketplace.objects.filter(client_id=client_id, id=id)

    

    return render(request, 'B_campaign/editcampMarketPlace.html',
                  {'modifyCamp': modifyCamp, 'mkId': id, 'admin_permission_obj':admin_permission_obj,'subclient_preferences':subclient_preferences})


def updateCampMarketPlace(request, id):
    updatecamp = campaign_marketplace.objects.filter(client_id=request.user.id, id=id)
    if request.method == 'POST':
        for i in updatecamp:
            updatecamp = campaign_marketplace.objects.filter(
                client_id=request.user.id, id=id)
            admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
            subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
            subclient = Subclient.objects.filter(id=subclient_id).first()
            subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
            if request.method == 'POST':
                for i in updatecamp:
                    updatecampEdit = campaign_marketplace.objects.get(id=i.id)
                    updatecampEdit.campaign_name = request.POST.get(
                        'reCampnName')
                    updatecampEdit.campaign_type = request.POST.get(
                        'reCampType')
                    updatecampEdit.campaign_category = request.POST.get(
                        'reCampCategory')
                    updatecampEdit.campaign_location = request.POST.get(
                        'reCampLocation')
                    updatecampEdit.campaign_description = request.POST.get(
                        'reCampdesc')
                    updatecampEdit.campaign_link_text = request.POST.get(
                        'reCamp_link_text')
                    updatecampEdit.campaign_url = request.POST.get(
                        'reCamp_url')
                    updatecampEdit.campaign_id = request.POST.get(
                        'reCamp_id')
                    updatecampEdit.campaign_key = request.POST.get(
                        'rekey')
                    updatecampEdit.campaign_contact_number = request.POST.get(
                        'reCampContactNumber')
           
                    updatecampEdit.save()
                return redirect('addcampMarketPlace')
            return render(request, 'B_campaign/addcamMarketPlace.html', {'modifycamp': updatecamp, "admin_permission_obj":admin_permission_obj,'subclient_preferences':subclient_preferences})

def deleteCampMarketPlace(request, id):
    print("dvjndv")
    deleteCamp = campaign_marketplace.objects.get(client_id=request.user.id, pk=id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    deleteCamp.delete()
    return redirect('addcampMarketPlace')


def camppayment(request, id):
    client_id = request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    print('marketplace_id', marketplace_id)
    payment_gatewa = campaign_payment_gateway_details.objects.filter(client_id=client_id, marketplace_id=id)
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    
    return render(request, 'B_campaign/camppayment.html', {'payment_gatewa':payment_gatewa, 'id':id, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id,'subclient_preferences':subclient_preferences})
from django.shortcuts import get_object_or_404

#submit payment based on the marketplace_id 
def camppayment_page(request, id):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    payment_gatewa = campaign_payment_gateway_details.objects.filter(client_id=request.user.id, marketplace_id=id)
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    if request.method == 'POST':
        marketplace, created = campaign_marketplace.objects.get_or_create(client=request.user, id=id)
        
        for gateway in payment_gatewa:
            gateway_id = request.POST.get(f'{gateway.payment_gateway}_gateway_id')
            gateway_key = request.POST.get(f'{gateway.payment_gateway}_gateway_key')
            currency = request.POST.get(f'{gateway.payment_gateway}_currency')

            gateway.gateway_id = gateway_id
            gateway.gateway_key = gateway_key
            gateway.currency = currency
            gateway.marketplace = marketplace  
            gateway.save()

        selected_methods = ['rozorpay', 'cashfree', 'paypal', 'stripe']
        existing_methods = [gateway.payment_gateway for gateway in payment_gatewa]

        new_methods = set(selected_methods) - set(existing_methods)
        for method in new_methods:
            gateway_id = request.POST.get(f'{method}_gateway_id')
            gateway_key = request.POST.get(f'{method}_gateway_key')
            currency = request.POST.get(f'{method}_currency')

            campaign_payment_gateway_details.objects.create(
                client=request.user,
                marketplace=marketplace,
                payment_gateway=method,
                gateway_id=gateway_id,
                gateway_key=gateway_key,
                currency=currency,
            )
        # return redirect('addgroupname')
        
        return redirect('camppayment', id=id, marketplace_id=marketplace.id)

    return render(request, 'B_campaign/camppayment.html', {'payment_gatewa': payment_gatewa, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id, 'id': id, 'subclient_preferences':subclient_preferences})


def GenerateCampId(request,id):

    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()


    facebookNu = facebook_details.objects.filter(client_id=request.user.id)
    idmkplace = campaign_marketplace.objects.filter(client_id=request.user.id,id=id )
    fb_whatsapp_number = facebookNu.first().fb_whatsapp_number if facebookNu.exists() else None
    campId = idmkplace.first().campaign_id if idmkplace.exists() else None
    campText = idmkplace.first().campaign_link_text if idmkplace.exists() else None
    campUrl = idmkplace.first().campaign_url if idmkplace.exists() else None
    # print('fb_whatsapp_number',facebookNu)
   
    
    context = {
        "facebook": facebookNu,
        "donationplace": idmkplace,
        'fb_whatsapp_number':fb_whatsapp_number,
        'campId':campId,
        'campText':campText,
        'campUrl':campUrl,
        
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,

    }
    
    return render(request, 'B_campaign/GenerateId.html', context)

def GenerateCampkey(request,id):

    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()


    facebookNu = facebook_details.objects.filter(client_id=request.user.id)
    keymkplace = campaign_marketplace.objects.filter(client_id=request.user.id,id=id )
    fb_whatsapp_number = facebookNu.first().fb_whatsapp_number if facebookNu.exists() else None
    campKey = keymkplace.first().campaign_key if keymkplace.exists() else None
    campText = keymkplace.first().campaign_link_text if keymkplace.exists() else None
    campUrl = keymkplace.first().campaign_url if keymkplace.exists() else None

    
    context = {
        "facebook": facebookNu,
        "keymkplace": keymkplace,
        'fb_whatsapp_number':fb_whatsapp_number,
        'campKey':campKey,
        'campText':campText,
        'campUrl':campUrl,
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,
        

    }
    
    return render(request, 'B_campaign/generateKey.html', context)


def generateCampKeyBarcode(request,id):
    
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()


    
    facebookNu = facebook_details.objects.filter(client_id=request.user.id)
    keymkplace = campaign_marketplace.objects.filter(client_id=request.user.id,id=id )
    fb_whatsapp_number = facebookNu.first().fb_whatsapp_number if facebookNu.exists() else None
    campKey = keymkplace.first().campaign_key if keymkplace.exists() else None
    campText = keymkplace.first().campaign_link_text if keymkplace.exists() else None
    campUrl = keymkplace.first().campaign_url if keymkplace.exists() else None
    
    context = {
        "facebook": facebookNu,
        "keymkplace": keymkplace,
        'fb_whatsapp_number':fb_whatsapp_number,
        'campKey':campKey,
        'campText':campText,
        'campUrl':campUrl,
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,

    }
    
    return render(request, 'B_campaign/generateKeyBarcode.html', context)



def GeneratecampIdBar(request,id):

    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    facebookNu = facebook_details.objects.filter(client_id=request.user.id)
    keymkplace = campaign_marketplace.objects.filter(client_id=request.user.id,id=id )
    fb_whatsapp_number = facebookNu.first().fb_whatsapp_number if facebookNu.exists() else None
    campKey = keymkplace.first().campaign_key if keymkplace.exists() else None
    campText = keymkplace.first().campaign_link_text if keymkplace.exists() else None
    campUrl = keymkplace.first().campaign_url if keymkplace.exists() else None
  
    context = {
        "facebook": facebookNu,
        "keymkplace": keymkplace,
        'fb_whatsapp_number':fb_whatsapp_number,
        'campKey':campKey,
        'campText':campText,
        'campUrl':campUrl,
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,

    }
    
    return render(request, 'B_campaign/GenerateIdBar.html', context)


def historyCampaign(request, id=None):
    subclient_id = request.session.get('subclient_id')
    subclient_preferences = SubUserPreference.objects.filter(subclient_id=subclient_id).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    print('id',id)
    generic_campaign_info_instances = None

    if id is not None:
        # Handle logic when id is present (filter by both client_id and marketplace_id)
        custmerCampaign = generic_campaign_history.objects.filter(client_id=request.user.id, marketplace_id=id)

        # Retrieve the generic_campaign_info instances associated with custmerCampaign
        generic_campaign_info_instances = generic_campaign_info.objects.filter(
            id__in=custmerCampaign.values_list('generic_campaign_info_id', flat=True)
        )

    else:
        # Handle logic when id is not present (filter only by client_id)
        # custmerCampaign = generic_campaign_history.objects.filter(client_id=request.user.id, marketplace__isnull=True)
        custmerCampaign = generic_campaign_history.objects.filter(client_id=request.user.id)
        # Retrieve the generic_campaign_info instances associated with custmerCampaign
        generic_campaign_info_instances = generic_campaign_info.objects.filter(
            id__in=custmerCampaign.values_list('generic_campaign_info_id', flat=True)
        )
        print('custmerCampaign',custmerCampaign)

    context = {
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,
        'custmerCampaign': custmerCampaign,
        'generic_campaign_info_instances': generic_campaign_info_instances,
    }


    return render(request, 'B_campaign/histoyCampaign.html', context)


# def sendgroupcampaign(request):
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
#     camgroups = campaign_groups.objects.filter(client_id=request.user.id)
#     templatedata = template_info.objects.filter(client_id=request.user.id, marketplace_id=None)
#     grouplist = campaign_groups.objects.filter(client_id=request.user.id)
#     if request.method == 'POST':
#         template_id = request.POST.get('template_id')
#         group_name = request.POST.get('group_name')
     
        

#         print("Group Name:", group_name)
#         print("Template ID:", template_id)
#         success_message = 'Template sent Successfully'

#         context = {
#                 'message': success_message,
#                 'templatedata':templatedata,
#                 'camgroups':camgroups,
#                 'admin_permission_obj':admin_permission_obj,
#                 'grouplist':grouplist,
#                 }
#         return render(request, 'B_campaign/addcamgroup.html', context)        
        






def preview(request, id):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first() 
    listbtn = template_info_details.objects.filter(client_id=request.user.id, template_info=id, )
    updateBCampaign = template_info.objects.filter(client_id=request.user.id, id=id)

    return render(request, 'B_campaign/preview.html',{'listbtn':listbtn, 'updateBCampaign':updateBCampaign,'admin_permission_obj':admin_permission_obj})




def sendcampaign(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    camgroups = campaign_groups.objects.filter(client_id=request.user.id)
    templatedata = template_info.objects.filter(client_id=request.user.id, marketplace_id=None)
    if request.method == 'POST':
        template_id = request.POST.get('template_id')
        group_name = request.POST.get('group_name')
        print("Template ID:", template_id)
        print("Group Name:", group_name)
        campaign_data = template_info.objects.filter(client_id=request.user.id,id=template_id)
        customer_data = campaign_group_customer_mappings.objects.filter(client_id=request.user.id, campaign_groups_id=group_name)
        print("rr")
        first_value = ''
        second_value = ''
        third_value = ''
        camapaign_Name = ''

        marketplace_id = 0
        campaignID = 0
        g_campaign_ID = 0
        for campaign in campaign_data:
            marketplace_id = campaign.marketplace_id
            g_campaign_ID = campaign.generic_campaign_info_id
            campaignObj = generic_campaign_info.objects.filter(client_id=request.user.id,id=campaign.generic_campaign_info_id)
            for c_i in campaignObj:
                campaignID = c_i.id
                camapaign_Name = c_i.Campaign_Name

        All_Number = []
        for c_i in customer_data:
            customer_info = campaign_customer_master.objects.filter(client_id=request.user.id,id=c_i.campaign_customer_master_id)
            for h_i in customer_info:
                All_Number.append(h_i.Customer_Whatsapp_Number)

        print(All_Number)
        facebook_detailsObj = facebook_details.objects.filter(client_id=request.user.id)
        phonenumberID = 0
        facebook_token = ''
        for f_i in facebook_detailsObj:
            phonenumberID = f_i.fb_phone_number_id
            facebook_token = f_i.fb_access_token

        template_infoobj = template_info.objects.filter(client_id=request.user.id,id=template_id)
        template_Name = ''
        header_type = ''
        header_text = ''
        template_image = ''
        for t_i in template_infoobj:
            template_Name = t_i.template_name
            header_type = t_i.template_header_type
            header_text = t_i.template_header_text
            template_image = t_i.template_header_image

        print(template_Name)
        print("tempalte name")



        # Important code dynamic button taking in json
        button_componets = []
        index_counter = 8
        index_counter1 = 0
        details_infoobj = template_info_details.objects.filter(client_id=request.user.id,template_info_id=template_id)
        for d_i in details_infoobj:
            if 'url' in d_i.template_button_type.lower():
                url_button = {
                    "type": "button",
                    "sub_type": "url",
                    "index": str(index_counter),
                    "parameters": [
                        {
                            "type": "text",
                            "text": "admin"
                        }
                    ]
                }
                button_componets.append(url_button)
                index_counter += 1
            elif 'image' in d_i.template_button_type.lower() or 'brochure' in d_i.template_button_type.lower() or 'document' in d_i.template_button_type.lower() or 'video' in d_i.template_button_type.lower() or 'stop' in d_i.template_button_type.lower() or 'form' in d_i.template_button_type.lower() or 'inflow' in d_i.template_button_type.lower() or 'campaign' in d_i.template_button_type.lower():
                print(d_i.template_button_type)
                print("s send camaign code payaload")
                reply_button = {
                                "type": "button",
                                "sub_type": "quick_reply",
                                "index": str(index_counter1),
                                "parameters": [
                                    {
                                        "type": "payload",
                                        "payload": f"B{d_i.id}"
                                    }
                                ]
                }
                button_componets.append(reply_button)
                index_counter1 += 1
        print("button data")
        print(button_componets)


        if header_type == 'text' or header_type == 'TEXT':
            for num in All_Number:
                url = f"https://graph.facebook.com/v15.0/{phonenumberID}/messages"

                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": num,
                    "type": "template",
                    "template": {
                        "name": template_Name,
                        "language": {
                            "code": "en_Us"
                        },
                        "components": [
                            {
                                "type": "header",
                                "parameters": [

                                ]
                            },
                            {
                                "type": "body",
                                "parameters": [

                                ]
                            },
                            *button_componets
                        ]
                    }
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {facebook_token}'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                if response.status_code == 200:
                    historyObj = generic_campaign_history.objects.create(
                        client_id=request.user.id,
                        marketplace_id=marketplace_id,
                        generic_campaign_info_id=g_campaign_ID,
                        Campaign_Name=camapaign_Name,
                        Campaign_Status='Sent',
                        Customer_Whatsapp_Number=num

                    )
                    historyObj.save()
                    print("successfully created one record")
            success_message = 'Template Sent Successfully'

            context = {
                'message': success_message,
                'templatedata':templatedata,
                'camgroups':camgroups,
                'admin_permission_obj':admin_permission_obj,
                }
            return render(request, 'B_campaign/campaignList.html', context)


        else:
            for num in All_Number:

                url = f"https://graph.facebook.com/v15.0/{phonenumberID}/messages"

                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": num,
                    "type": "template",
                    "template": {
                        "name": template_Name,
                        "language": {
                            "code": "en_Us"
                        },
                        "components": [
                            {
                                "type": "header",
                                "parameters": [
                                    {
                                        "type": "image",
                                        "image": {
                                            "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                            (template_image)
                                        }
                                    }
                                ]
                            },
                            {
                                "type": "body",
                                "parameters": [

                                ]
                            },
                            *button_componets
                        ]
                    }
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {facebook_token}'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                if response.status_code == 200:
                    historyObj = generic_campaign_history.objects.create(
                        client_id=request.user.id,
                        marketplace_id=marketplace_id,
                        generic_campaign_info_id=g_campaign_ID,
                        Campaign_Name=camapaign_Name,
                        Campaign_Status='Sent',
                        Customer_Whatsapp_Number=num
                    )
                    historyObj.save()
                    print("successfully created one record")
            success_message = 'Template Sent Successfully'

            context = {
                'message': success_message,
                'templatedata': templatedata,
                'camgroups': camgroups,
                'admin_permission_obj': admin_permission_obj,
            }
            return render(request, 'B_campaign/campaignList.html', context)

            # return HttpResponse('Template Successfully')



def sendgroupcampaign(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    camgroups = campaign_groups.objects.filter(client_id=request.user.id)
    templatedata = template_info.objects.filter(client_id=request.user.id, marketplace_id=None)
    grouplist = campaign_groups.objects.filter(client_id=request.user.id)
    if request.method == 'POST':
        template_id = request.POST.get('template_id')
        group_name = request.POST.get('group_name')

        print("Group Name:", group_name)
        print("Template ID:", template_id)
        campaign_data = template_info.objects.filter(client_id=request.user.id,id=template_id)
        customer_data = campaign_group_customer_mappings.objects.filter(client_id=request.user.id, campaign_groups_id=group_name)
        print("rr")
        first_value = ''
        second_value = ''
        third_value = ''
        camapaign_Name = ''

        marketplace_id = 0
        campaignID = 0
        g_campaign_ID = 0
        for campaign in campaign_data:
            marketplace_id = campaign.marketplace_id
            g_campaign_ID = campaign.generic_campaign_info_id
            campaignObj = generic_campaign_info.objects.filter(client_id=request.user.id,id=campaign.generic_campaign_info_id)
            for c_i in campaignObj:
                campaignID = c_i.id
                camapaign_Name = c_i.Campaign_Name

        All_Number = []
        for c_i in customer_data:
            customer_info = campaign_customer_master.objects.filter(client_id=request.user.id,id=c_i.campaign_customer_master_id)
            for h_i in customer_info:
                All_Number.append(h_i.Customer_Whatsapp_Number)

        print(All_Number)
        facebook_detailsObj = facebook_details.objects.filter(client_id=request.user.id)
        phonenumberID = 0
        facebook_token = ''
        for f_i in facebook_detailsObj:
            phonenumberID = f_i.fb_phone_number_id
            facebook_token = f_i.fb_access_token

        template_infoobj = template_info.objects.filter(client_id=request.user.id,id=template_id)
        template_Name = ''
        header_type = ''
        header_text = ''
        template_image = ''
        for t_i in template_infoobj:
            template_Name = t_i.template_name
            header_type = t_i.template_header_type
            header_text = t_i.template_header_text
            template_image = t_i.template_header_image



        # Important code dynamic button taking in json
        button_componets = []
        index_counter1 = 8
        index_counter = 0
        details_infoobj = template_info_details.objects.filter(client_id=request.user.id,template_info_id=template_id)
        for d_i in details_infoobj:
            if 'url' in d_i.template_button_type.lower() or 'phone_number' in d_i.template_button_type.lower() or 'phone number' in d_i.template_button_type.lower():
                url_button = {
                    "type": "button",
                    "sub_type": "url",
                    "index": str(index_counter1),
                    "parameters": [
                        {
                            "type": "text",
                            "text": "admin"
                        }
                    ]
                }
                button_componets.append(url_button)
                index_counter1 += 1
            elif 'image' in d_i.template_button_type.lower() or 'brochure' in d_i.template_button_type.lower() or 'document' in d_i.template_button_type.lower() or 'video' in d_i.template_button_type.lower() or 'stop' in d_i.template_button_type.lower() or 'form' in d_i.template_button_type.lower() or 'inflow' in d_i.template_button_type.lower() or 'campaign' in d_i.template_button_type.lower():
                reply_button = {
                    "type": "button",
                    "sub_type": "quick_reply",
                    "index": str(index_counter),
                    "parameters": [
                      {
                        "type": "payload",
                        "payload": f"B{d_i.id}"
                      }
                    ]
                }
                button_componets.append(reply_button)
                index_counter += 1
            # elif 'phone_number' in d_i.template_button_type.lower() or 'phone number' in d_i.template_button_type.lower():
            #     phone_button = {
            #         "type": "button",
            #         "sub_type": "url",
            #         "index": str(index_counter)
            #
            #     }
            #     button_componets.append(phone_button)
            #     index_counter += 1


        if header_type == 'text' or header_type == 'TEXT':
            for num in All_Number:
                url = f"https://graph.facebook.com/v15.0/{phonenumberID}/messages"

                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": num,
                    "type": "template",
                    "template": {
                        "name": template_Name,
                        "language": {
                            "code": "en_Us"
                        },
                        "components": [
                            {
                                "type": "header",
                                "parameters": [

                                ]
                            },
                            {
                                "type": "body",
                                "parameters": [

                                ]
                            },
                            *button_componets
                        ]
                    }
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {facebook_token}'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                if response.status_code == 200:
                    historyObj = generic_campaign_history.objects.create(
                        client_id=request.user.id,
                        marketplace_id=marketplace_id,
                        generic_campaign_info_id=g_campaign_ID,
                        Campaign_Name=camapaign_Name,
                        Campaign_Status='Sent',
                        Customer_Whatsapp_Number=num

                    )
                    historyObj.save()
                    print("successfully created one record")
            success_message = 'Group Sent Successfully'
            context = {
                    'message': success_message,
                    'templatedata':templatedata,
                    'camgroups':camgroups,
                    'admin_permission_obj':admin_permission_obj,
                    'grouplist':grouplist,
                    }
            return render(request, 'B_campaign/addcamgroup.html', context)


        else:
            for num in All_Number:

                url = f"https://graph.facebook.com/v15.0/{phonenumberID}/messages"

                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": num,
                    "type": "template",
                    "template": {
                        "name": template_Name,
                        "language": {
                            "code": "en_Us"
                        },
                        "components": [
                            {
                                "type": "header",
                                "parameters": [
                                    {
                                        "type": "image",
                                        "image": {
                                            "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                            (template_image)
                                        }
                                    }
                                ]
                            },
                            {
                                "type": "body",
                                "parameters": [

                                ]
                            },
                            *button_componets
                        ]
                    }
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {facebook_token}'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                if response.status_code == 200:
                    historyObj = generic_campaign_history.objects.create(
                        client_id=request.user.id,
                        marketplace_id=marketplace_id,
                        generic_campaign_info_id=g_campaign_ID,
                        Campaign_Name=camapaign_Name,
                        Campaign_Status='Sent',
                        Customer_Whatsapp_Number=num
                    )
                    historyObj.save()
                    print("successfully created one record")
            success_message = 'Group Sent Successfully'
            context = {
                'message': success_message,
                'templatedata': templatedata,
                'camgroups': camgroups,
                'admin_permission_obj': admin_permission_obj,
                'grouplist': grouplist,
            }
            return render(request, 'B_campaign/addcamgroup.html', context)


            # return HttpResponse('Template Successfully')



        # context = {
        #         'message': success_message,
        #         'templatedata':templatedata,
        #         'camgroups':camgroups,
        #         'admin_permission_obj':admin_permission_obj,
        #         'grouplist':grouplist,
        #         }
        # return render(request, 'B_campaign/addcamgroup.html', context)


def createtemplate(request,id):
    print(id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    camgroups = campaign_groups.objects.filter(client_id=request.user.id)
    templatedata = template_info.objects.filter(client_id=request.user.id, marketplace_id=None)
    facebook_detailsObj = facebook_details.objects.filter(client_id=request.user.id)
    phonenumberID = 0
    facebook_token = ''
    waba_id = 0
    for f_i in facebook_detailsObj:
        phonenumberID = f_i.fb_phone_number_id
        facebook_token = f_i.fb_access_token
        waba_id = f_i.fb_Whatsapp_business_account_id
    print(phonenumberID)
    print(facebook_token)
    print("rrr")
    random_number = random.randint(1, 1000)
    print("fffff")

    template_new_name = ''
    All_buttons = []
    template_Name = ''
    temp_Header_Text = ''
    temp_body_text = ''
    header_type = ''
    campaign_Id = 0
    template_infoobj = template_info.objects.filter(client_id=request.user.id,id=id)
    for t_i in template_infoobj:
        campaign_Id = t_i.generic_campaign_info
        template_Name = t_i.template_name
        temp_Header_Text = t_i.template_header_text
        temp_body_text = t_i.template_body_message
        header_type = t_i.template_header_type
        formatted_name = template_Name.lower().replace(' ', '_')
        template_new_name = f'{formatted_name}_{random_number}'
        t_i.template_name = template_new_name
        t_i.save()
        details_infoobj = template_info_details.objects.filter(client_id=request.user.id,template_info_id=id,generic_campaign_info_id=campaign_Id)
        for data in details_infoobj:
            if data.template_button_type == 'URL' or data.template_button_type == 'url':
                button_url = {
                    "type": "URL",
                    "text": data.template_button_name,
                    "url": data.template_additional_info
                }
                All_buttons.append(button_url)
            elif data.template_button_type.lower() == 'image' or data.template_button_type.lower() == 'video' or data.template_button_type.lower() == 'document' or data.template_button_type.lower() == 'stop' or data.template_button_type.lower() == 'form' or data.template_button_type.lower() == 'inflow' or data.template_button_type.lower() == 'campaign':
                button_reply = {
                    "type": "QUICK_REPLY",
                    "text": f'{data.template_button_name}',

                }
                All_buttons.append(button_reply)
            elif data.template_button_type.strip().lower() == 'phone_number':
                button_number = {
                    "type": "PHONE_NUMBER",
                    "text": data.template_button_name,
                    "phone_number": data.template_additional_info
                }
                All_buttons.append(button_number)

            print("vgain")
            print(All_buttons)

    if header_type == 'text' or header_type == 'TEXT':
        url = f"https://graph.facebook.com/v18.0/{waba_id}/message_templates"

        payload = json.dumps({
            "name": template_new_name,
            "language": "en_US",
            "category": "MARKETING",
            "components": [
                {
                    "type": "HEADER",
                    "format": "TEXT",
                    "text": temp_Header_Text,

                },
                {
                    "type": "BODY",
                    "text": temp_body_text,

                },
                {
                    "type": "BUTTONS",
                    "buttons": All_buttons

                }
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {facebook_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        success_message = 'Template Sent Successfully'

        context = {
            'message': success_message,
            'templatedata': templatedata,
            'camgroups': camgroups,
            'admin_permission_obj': admin_permission_obj,
        }
        return render(request, 'B_campaign/campaignList.html', context)
        # return HttpResponse("successfully creating template")
    else:
        url = "https://graph.facebook.com/v19.0/879780240223291/uploads"
        access_token = facebook_token  # Replace this with your actual access token

        params = {
            "file_length": 21116,
            "file_type": "image/jpg",
            "access_token": access_token
        }

        response = requests.post(url, params=params)
        data = response.text
        print("manula")
        print(data)
        print(response.text)

        url = f"https://graph.facebook.com/v19.0/{data}"
        authorization_header = f"OAuth {facebook_token}"  # Replace this with your actual authorization header
        file_offset_header = "0"  # Replace this with your actual file_offset value

        headers = {
            "Authorization": authorization_header,
            "file_offset": file_offset_header,
        }

        with open("marketingimage.jpg", "rb") as file:
            files = {'file': file}
            response = requests.post(url, headers=headers, files=files)

        print(response.text)
        file_handle = response.text
        print("manjamma")
        print(file_handle)

        url = f"https://graph.facebook.com/v18.0/{waba_id}/message_templates"

        payload = json.dumps({
            "name": template_new_name,
            "language": "en_US",
            "category": "MARKETING",
            "components": [
                {
                    "type": "HEADER",
                    "format": "IMAGE",
                    "example": {
                        "header_handle": [
                            "4::aW1hZ2UvanBn:ARZEhgmTrQqQUb37evJ9VhCtDqzMV5W76XiayjaB_h46EhJmALeX-5w2HmM9RypQojHu73TpE3fjqXzMCffZ8FO0RV7jm6IFc7xRyQdDtEwIxw:e:1713251994:755696335878147:61552521835241:ARZA3eLiraabk7sloXE"
                        ]
                    }
                },
                {
                    "type": "BODY",
                    "text": temp_body_text,

                },
                {
                    "type": "BUTTONS",
                    "buttons": All_buttons

                }
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {facebook_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        success_message = 'Template Sent Successfully'

        context = {
            'message': success_message,
            'templatedata': templatedata,
            'camgroups': camgroups,
            'admin_permission_obj': admin_permission_obj,
        }
        return render(request, 'B_campaign/campaignList.html', context)
        # return HttpResponse("successfully creating template")


def createCarousel(request):
    facebook_detailsObj = facebook_details.objects.filter(client_id=request.user.id)
    phonenumberID = 0
    facebook_token = ''
    waba_id = 0
    for f_i in facebook_detailsObj:
        phonenumberID = f_i.fb_phone_number_id
        facebook_token = f_i.fb_access_token
        waba_id = f_i.fb_Whatsapp_business_account_id
    print(phonenumberID)
    print(facebook_token)
    print("rrr")
    random_number = random.randint(1, 1000)
    print("fffff")
    template_name = 'campaign_cards_list_set'
    mastercardobj = campaign_marketplace_settings.objects.create(
        client_id=request.user.id,
        master_card_template_name=template_name

    )
    mastercardobj.save()
    print("successfully saved the template name")
    base_components = [
        {
            "type": "HEADER",
            "format": "IMAGE",
            "example": {
                "header_handle": [
                    "4::aW1hZ2UvanBn:ARaBp3GsnKZrD7uodQEENp-ATb_GqOujuKXlIalUUDIC2KFD0dInqSWbSGNwL2CC7ii3tT_-2oQ_FIF2unpircw_hHqBhYA_opkPGAIhdjh3Hg:e:1711265645:755696335878147:61552521835241:ARYQYxSfz6IVwJyr6zU"
                ]
            }
        },
        {
            "type": "BODY",
            "text": "Details:{{1}}",
            "example": {
                "body_text": [
                    [
                        "A villa plot with modern amenities."
                    ]
                ]
            }
        },
        {
            "type": "BUTTONS",
            "buttons": [
                {
                    "type": "QUICK_REPLY",
                    "text": "Select"
                }
            ]
        }
    ]
    for i in range(1,11):
        carouseltemplatename = f'{template_name}_{i}'
        num_components = i
        url = f"https://graph.facebook.com/v18.0/{waba_id}/message_templates"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {facebook_token}'
        }

        cards=[]
        for j in range(num_components):
            card = {"components": base_components}
            cards.append(card)

        payload = json.dumps({
            "name": carouseltemplatename,
            "language": "en_US",
            "category": "MARKETING",
            "components": [
                {
                    "type": "BODY",
                    "text": "Choose from various options.{{1}}",
                    "example": {
                        "body_text": [
                            [
                                "Properties that meet your needs and budget"
                            ]
                        ]
                    }
                },
                {
                    "type": "CAROUSEL",
                    "cards": cards
                }
            ]
        })
        response = requests.post(url, headers=headers, data=payload)
        print("s created one by one")

        print(response.text)
        time.sleep(30)


    return HttpResponse("done")

def templatestatus(request,id):
    print(id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    camgroups = campaign_groups.objects.filter(client_id=request.user.id)
    templatedata = template_info.objects.filter(client_id=request.user.id, marketplace_id=None)
    facebook_detailsObj = facebook_details.objects.filter(client_id=request.user.id)
    phonenumberID = 0
    facebook_token = ''
    waba_id = 0
    for f_i in facebook_detailsObj:
        phonenumberID = f_i.fb_phone_number_id
        facebook_token = f_i.fb_access_token
        waba_id = f_i.fb_Whatsapp_business_account_id
    print(phonenumberID)
    print(facebook_token)
    template_Name = ''
    template_infoobj = template_info.objects.filter(client_id=request.user.id, id=id)
    for t_i in template_infoobj:
        campaign_Id = t_i.generic_campaign_info
        template_Name = t_i.template_name

    url = f"https://graph.facebook.com/v18.0/{waba_id}/message_templates?name={template_Name}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {facebook_token}',
        'Cookie': 'ps_l=0; ps_n=0'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    data = response.text
    response_data = json.loads(data)
    print(response_data)
    status = response_data['data'][0]['status']
    print("dd")
    print(status)
    success_message = str(status)
    template_infoobj = template_info.objects.filter(client_id=request.user.id, id=id)
    for t_i in template_infoobj:
        t_i.status = status
        t_i.save()
    context = {

        'templatedata': templatedata,
        'camgroups': camgroups,
        'admin_permission_obj': admin_permission_obj,
    }

    return render(request, 'B_campaign/campaignList.html',context)