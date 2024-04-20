from django.http import HttpResponse
from django.shortcuts import render,redirect
from vailodb_s.models import Survey_list, Survey_Question, Survey_Customer, Survey_Question_Map, Survey_marketplace, \
    Survey_Customer_Response, survey_types, survey_categorys, Survey_marketplace_settings
from django.http import JsonResponse
import json
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from vailodb.models import admin_permission, Subclient, SubUserPreference, SUBCLIENT_CHOICE, facebook_details
from django.shortcuts import render, redirect
from django.urls import reverse
import json
import random

import requests
#fro marketplace_id 
def marketplace(request):
    request.session.pop('marketplace_id', None)
    request.session.save()
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient =subclient).first()
    marketplacedata = Survey_marketplace.objects.filter(client_id=request.user.id)

    context = {
        'subclient_preferences':subclient_preferences,
        'admin_permission_obj':admin_permission_obj,
        'marketplacedata':marketplacedata,
        'id':id,    }
    return render(request, 's_survey/marketplace.html', {'id':id, 'context':context,'admin_permission_obj':admin_permission_obj, 'marketplacedata':marketplacedata})


def addSurveygroup(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 's_survey/addsurveygroup.html', {'admin_permission_obj':admin_permission_obj})

def submitSurveyGroupsForm(request):

    if request.POST:
        createsurvey= Survey_marketplace()
        createsurvey.survey_name= request.POST.get('SurveyName')
        createsurvey.survey_type=request.POST.get('SurveyType')
        createsurvey.survey_category=request.POST.get('SurveyCategory')
        createsurvey.survey_location=request.POST.get('SurveyLocation')
        createsurvey.survey_description= request.POST.get('SurveyDescription')
        createsurvey.survey_contact_number = request.POST.get('SurveyContactNumber')
        createsurvey.client_id=request.user.id
        createsurvey.save()
        return redirect('marketplace')
    return render(request, 's_survey/addsurveygroup.html')


def editsurveygroup(request, id):
    client_id = request.user.id
    marketplace_id = request.POST.get('marketplace_id')
    print('editsurveygroup is ', marketplace_id)

    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifymarketplacedata = Survey_marketplace.objects.filter(client_id=request.user.id, id=id)
    return render(request, 's_survey/editsurveygroup.html', {'admin_permission_obj':admin_permission_obj, 'modifymarketplacedata':modifymarketplacedata})
    
def submiteditsurveygroup(request, id):
    updategroupdata = Survey_marketplace.objects.filter(client_id=request.user.id, id=id)
    if request.method == 'POST':
        for group in updategroupdata:
            updategroupdata = Survey_marketplace.objects.filter(client_id=request.user.id, id=id)
            admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
            if request.method == 'POST':
                for group in updategroupdata:
                    updategroup = Survey_marketplace.objects.get(id=group.id)
                    updategroup.survey_name = request.POST.get('resurveyName')
                    updategroup.survey_type= request.POST.get('resurveyType')
                    updategroup.survey_category = request.POST.get('resurveyCategory')
                    updategroup.survey_location = request.POST.get('resurveyLocation')
                    updategroup.survey_description = request.POST.get('resurveyDescription')
                    updategroup.survey_contact_number = request.POST.get('resurveyContactNumber')
                    updategroup.save()
                return redirect('marketplace')
    return render(request, 's_survey/addsurveygroup.html', {'updategroupdata':updategroupdata, 'admin_permission_obj':admin_permission_obj})


def deletemarketplace(request, id):
    deletesurveygroup=Survey_marketplace.objects.get(client_id = request.user.id, pk=id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    deletesurveygroup.delete()
    return redirect('marketplace')


# def surveyList(request, id=None):
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
#     client_id = request.user.id
#     marketplace_id = request.session.get('marketplace_id')
#     referer = request.META.get('HTTP_REFERER', '')
#     if 'surveyList' in referer or 'marketplace' in referer:
#         request.session.save()
#         messages.success(request, 'Session cleared successfully.')
#     if id:
#         request.session['marketplace_id'] = id
#         request.session.modified = True
#         request.session.save()
#     surveyDash = Survey_list.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)
#     if marketplace_id:
#         listsurvey = Survey_list.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)
#         return render(request, 's_survey/surveyList.html', {'listsurvey': listsurvey, 'id': id, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id})
#     else:
#         listsurvey = Survey_list.objects.filter(client_id=request.user.id)
#         return render(request, 's_survey/surveyList.html',{'listsurvey':listsurvey, 'admin_permission_obj':admin_permission_obj})



def surveyList(request, id=None):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    client_id = request.user.id

    if 'marketplace_id' not in request.session:
        request.session['marketplace_id'] = id 
        request.session.save()

    marketplace_id = request.session['marketplace_id']
    referer = request.META.get('HTTP_REFERER', '')

    if 'surveyList' in referer or 'marketplace' in referer:
        request.session.save()
        # messages.success(request, 'Session cleared successfully.')

    if id:
        request.session['marketplace_id'] = id
        request.session.modified = True
        request.session.save()

    surveyDash = Survey_list.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)

    if marketplace_id:
        listsurvey = Survey_list.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)
        return render(request, 's_survey/surveyList.html', {'listsurvey': listsurvey, 'id': id, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id})
    else:
        listsurvey = Survey_list.objects.filter(client_id=request.user.id)
        return render(request, 's_survey/surveyList.html', {'listsurvey': listsurvey, 'admin_permission_obj': admin_permission_obj})




def addSurvey(request):
    client_id = request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.session.get('marketplace_id')
    print('addSurvey marketplace_id is ', marketplace_id)
    return render(request, 's_survey/addSurvey.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})


def addSurveySubmit(request):
    marketplace_id = request.GET.get('marketplace_id')
    print('submitDonation_marketplace_id', marketplace_id)

    if request.method == "POST":
        submitAddsurvey = Survey_list()

        if 'surveyImg' in request.FILES:
            submitAddsurvey.survey_image = request.FILES['surveyImg']
        if 'surveyStatus' in request.POST:
            submitAddsurvey.survey_status = request.POST.get('surveyStatus')
        submitAddsurvey.survey_message = request.POST.get('surveyMessageText')
        submitAddsurvey.survey_footer = request.POST.get('surveyFooter')
        submitAddsurvey.survey_type = request.POST.get('surveyType')
        submitAddsurvey.flow_id = request.POST.get('flowid')

        submitAddsurvey.client_id = request.user.id
        if marketplace_id:
            submitAddsurvey.marketplace_id = marketplace_id
        submitAddsurvey.save()

        if marketplace_id:
             return redirect(reverse('surveyList') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('surveyList')

    return render(request, 's_survey/addSurvey.html')



def updateSurvey(request, id):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    client_id = request.user.id
    marketplace_id = request.session.get('marketplace_id')
    print('updateSurveymarketplace_id', marketplace_id)
    updateSurvey = Survey_list.objects.filter(client_id=request.user.id, id=id)
    return render(request, 's_survey/editSurvey.html', {'admin_permission_obj':admin_permission_obj, 'updateSurvey':updateSurvey, 'marketplace_id':marketplace_id })



def subUpdateSurvey(request, id):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    client_id = request.user.id
    marketplace_id = request.session.get('marketplace_id')
    print('updateSurveymarketplace_id', marketplace_id)
    subUpdateSurvey = Survey_list.objects.filter(
        client_id=request.user.id, id=id)
    if request.method == 'POST':
        for i in subUpdateSurvey:
            editinfo = Survey_list.objects.get(id=i.id)
            if request.POST.get('resurveyMessageText'):
                editinfo.survey_message = request.POST.get('resurveyMessageText')
            if request.POST.get('resurveyFooter'):
                editinfo.survey_footer = request.POST.get(
                    'resurveyFooter')
            if request.POST.get('resurveyType'):
                editinfo.survey_type = request.POST.get(
                    'resurveyType') 
            survey_status = request.POST.get('reSurveyStatus')
            if survey_status is not None and survey_status != '':
                editinfo.survey_status = int(survey_status)

            if 'reresurvey_image' in request.FILES and len(request.FILES['reresurvey_image']) != 0:
                editinfo.survey_image = request.FILES['reresurvey_image']

            editinfo.save()
            if marketplace_id:
                return redirect(reverse('surveyList') + f'?marketplace_id={marketplace_id}')
            else:
                return redirect('surveyList')

    return render(request, 's_survey/editSurvey.html')

def deleteSurvey(request,id):
    deleteSurvey = Survey_list.objects.get(
        client_id=request.user.id, pk=id)
    deleteSurvey.delete()
    return redirect('surveyList')



def survey_question_view(request, id):
    # Retrieve the specific Survey_list object
    surveyType = Survey_list.objects.get(client_id=request.user.id, id=id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    client_id = request.user.id
    marketplace_id = request.session.get('marketplace_id')
    print('survey_question_view marketplace_id', marketplace_id)
    try:
        # Try to retrieve an existing Survey_Question object
        detailSurvey = Survey_Question.objects.get(client_id=request.user.id, id=id)
    except Survey_Question.DoesNotExist:
        # If it doesn't exist, create a new one
        detailSurvey, created = Survey_Question.objects.get_or_create(
            client=request.user,
            id=id,
            Survey_list=surveyType,  # Associate the Survey_list with the Survey_Question
            question=request.POST.get('question', ''),  # Provide an empty string
            response_option1=request.POST.get('response_option1', ''),
            response_option2=request.POST.get('response_option2', ''),
            response_option3=request.POST.get('response_option3', ''),
            response_option4=request.POST.get('response_option4', ''),
            question_type=request.POST.get('question_type', ''),
        )

    if request.method == 'POST':
        if 'submitQuestionOptions' in request.POST:
            # Handle the form data from the survey_question form
            detailSurvey.question = request.POST.get('question', '')  # Provide an empty string
            detailSurvey.response_option1 = request.POST.get('response_option1', '')
            detailSurvey.response_option2 = request.POST.get('response_option2', '')
            detailSurvey.response_option3 = request.POST.get('response_option3', '')
            detailSurvey.response_option4 = request.POST.get('response_option4', '')
            detailSurvey.question_type = request.POST.get('question_type', '')
            detailSurvey.Survey_list = surveyType
            # Survey_list is already associated during creation
            # Update other fields as needed
            detailSurvey.save()
        elif 'submitSurveyType' in request.POST:
            # Update the survey_type for the specific Survey_list object
            surveyType.survey_type = request.POST.get('updateSurveyType')
            surveyType.save()

    return render(request, 's_survey/survey_question.html', {'detailSurvey': detailSurvey, 'surveyType': surveyType, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})








def assignSuveyCustomer(request, id):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    client_id = request.user.id
    marketplace_id = request.session.get('marketplace_id')
    if marketplace_id:

        surveyType = Survey_list.objects.get(client_id=request.user.id, id=id, marketplace_id=marketplace_id)
        assignCustomer = Survey_Customer.objects.filter(client_id=request.user.id,  marketplace_id=marketplace_id)
        selectedCustomer = list(Survey_Question_Map.objects.filter(client_id=request.user.id, Survey_list_id=id))
        print(selectedCustomer)
        return render(request, 's_survey/survey_assignn.html', { 'assignCustomer': assignCustomer,'surveyType': surveyType,'selectedCustomer': selectedCustomer,'admin_permission_obj':admin_permission_obj,'marketplace_id':marketplace_id})
    else:
        surveyType = Survey_list.objects.get(client_id=request.user.id, id=id)
        assignCustomer = Survey_Customer.objects.filter(client_id=request.user.id)
        selectedCustomer = list(Survey_Question_Map.objects.filter(client_id=request.user.id, Survey_list_id=id))
        print(selectedCustomer)

        return render(request, 's_survey/survey_assignn.html', {
            'assignCustomer': assignCustomer,
            'surveyType': surveyType,
            'selectedCustomer': selectedCustomer,
            'admin_permission_obj':admin_permission_obj,
            'marketplace_id':marketplace_id
        })
 
 


@transaction.atomic
def moveSelectedCustomers(request, survey_id):
    if request.method == 'POST':
        selected_customer_ids = request.POST.getlist('selected_customer_ids')
        print('selected_customer_ids',selected_customer_ids)
        if not selected_customer_ids:
            return JsonResponse({'success': False, 'message': 'No customers selected.'})

        try:
            with transaction.atomic():
                survey = Survey_list.objects.get(client=request.user, id=survey_id)
                duplicate_entries = []  # List to store duplicate entry messages

                for customer_id in selected_customer_ids:
                    customer = Survey_Customer.objects.get(client=request.user, id=customer_id)

                    try:
                        # Check for duplicates
                        existing_mapping = Survey_Question_Map.objects.get(
                            client=request.user, Survey_list=survey, Survey_Customer=customer)

                        duplicate_entries.append(f"Duplicate entry: Customer '{customer.customer_name}' is already assigned to this survey.")
                    except Survey_Question_Map.DoesNotExist:
                        try:
                            Survey_Question_Map.objects.create(
                                client=request.user,
                                Survey_list=survey,
                                Survey_Customer=customer
                            )
                        except IntegrityError:
                            # Handle other errors if necessary
                            pass

                if duplicate_entries:
                    # Notify duplicates and skip them
                    messages.error(request, "Duplicate entries: Some customers were already assigned and skipped.")
                else:
                    # Notify success
                    messages.success(request, "Customers assigned successfully.")

                return redirect('assignSuveyCustomer', id=survey_id)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})  
   


def deleteAssigned(request,id):
    deleteAssigned = Survey_Question_Map.objects.get(
        client_id=request.user.id, pk=id)
    generic_campaign_info_id = deleteAssigned.Survey_list_id
    deleteAssigned.delete()
    return redirect('assignSuveyCustomer',id=generic_campaign_info_id)


def genericsurvey(request):
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
    market_settingsObj = Survey_marketplace_settings.objects.filter(client_id=request.user.id)
    for m_i in market_settingsObj:
        random_number = random.randint(1, 1000)
        print("fffff")
        base_name = 'generic_flow'
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
            donation_obj = Survey_marketplace_settings.objects.filter(client_id=request.user.id)
            for d_i in donation_obj:
                d_i.generic_flow_id = id_value
                d_i.save()
                print("successfully saved the flow id")
                type_obj = survey_types.objects.filter(client_id=request.user.id)
                group_Type = []
                for r_i in type_obj:
                    group_Type.append(r_i.survey_type)
                list_group_type = []
                for h_i in range(len(group_Type)):
                    list_group_type.append({"id": group_Type[h_i],
                                            "title": group_Type[h_i]
                                            })
                category_obj = survey_categorys.objects.filter(client_id=request.user.id)
                category_Type = []
                for c_i in category_obj:
                    category_Type.append(c_i.survey_category)

                list_category_type = []
                for j in range(len(category_Type)):
                    list_category_type.append({
                        "id": category_Type[j],
                        "title": category_Type[j]
                    })
                data = {
                  "version": "2.1",
                  "data_api_version": "3.0",
                  "data_channel_uri": "https://vmart.ai/surveydata",
                  "routing_model": {
                    "DETAILS": [
                      "SURVEY_INFO"
                    ],
                    "SURVEY_INFO":[
                      "SURVEY_DATA"
                    ]

                  },
                  "screens": [
                    {
                      "id": "DETAILS",
                      "title": "Your details",
                      "layout": {
                        "type": "SingleColumnLayout",
                        "children": [
                          {
                            "type": "Form",
                            "name": "details_form",
                            "children": [
                              {
                                "type": "TextInput",
                                "label": "Survey Name",
                                "input-type": "text",
                                "name": "name",
                                "required": False
                              },
                              {
                                "type": "Dropdown",
                                "label": "Survey Type",
                                "required": False,
                                "name": "ngo_type",
                                "data-source": list_group_type
                              },
                              {
                                "type": "Dropdown",
                                "label": "Survey Category",
                                "required": False,
                                "name": "ngo_category",
                                "data-source": list_category_type
                              },
                              {
                                "type": "TextInput",
                                "label": "Survey Location",
                                "input-type": "text",
                                "name": "location",
                                "required": False
                              },
                              {
                                "type": "Footer",
                                "label": "Continue",
                                "on-click-action": {
                                  "name": "data_exchange",
                                  "payload": {
                                    "s_Name": "${form.name}",
                                    "s_type": "${form.ngo_type}",
                                    "s_category": "${form.ngo_category}",
                                    "s_location": "${form.location}"
                                  }
                                }
                              }
                            ]
                          }
                        ]
                      }
                    },

                    {
                      "id": "SURVEY_INFO",
                      "title": "SURVEY_INFO",
                      "terminal": True,
                      "data": {

                        "options": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "string"
                              },
                              "title": {
                                "type": "string"
                              }
                            }
                          },
                          "__example__": []
                        }
                      },
                      "layout": {
                        "type": "SingleColumnLayout",
                        "children": [
                          {
                            "type": "Form",
                            "name": "cover_form",
                            "children": [

                              {
                                "type": "RadioButtonsGroup",
                                "name": "options",
                                "data-source": "${data.options}",
                                "label": "Options",
                                "required": True
                              },
                              {
                                "type": "Footer",
                                "label": "continue",
                                "on-click-action": {
                                  "name": "data_exchange",
                                  "payload": {
                                    "slots_data": "${form.options}"
                                  }
                                }
                              }
                            ]
                          }
                        ]
                      }
                    },

                    {
                      "id": "SURVEY_DATA",
                      "title": "SURVEY_DATA",
                      "terminal": True,
                      "data": {
                        "details": {
                          "type": "string",
                          "__example__": ""
                        },
                        "options": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "string"
                              },
                              "title": {
                                "type": "string"
                              }
                            }
                          },
                          "__example__": []
                        }
                      },
                      "layout": {
                        "type": "SingleColumnLayout",
                        "children": [
                          {
                            "type": "Form",
                            "name": "cover_form",
                            "children": [
                              {
                                "type": "TextHeading",
                                "text": "${data.details}"
                              },
                              {
                                "type": "RadioButtonsGroup",
                                "name": "options",
                                "data-source": "${data.options}",
                                "label": "Options",
                                "required": True
                              },
                              {
                                "type": "Footer",
                                "label": "complete",
                                "on-click-action": {
                                  "name": "complete",
                                  "payload": {
                                    "slots_data": "${form.options}"
                                  }
                                }
                              }
                            ]
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
                file_path = f'C:/Vailo/04-01-2023/A_vMart/A_vMart/{new_name}.json'
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
    return HttpResponse("wait for generating flow id")


def specificsurvey(request):
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
    market_settingsObj = Survey_marketplace_settings.objects.filter(client_id=request.user.id)
    for m_i in market_settingsObj:
        random_number = random.randint(1, 1000)
        print("fffff")
        base_name = 'generic_flow'
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
            donation_obj = Survey_marketplace_settings.objects.filter(client_id=request.user.id)
            for d_i in donation_obj:
                d_i.specific_flow_id = id_value
                d_i.save()
                print("successfully saved the flow id")
                data = {
                  "version": "2.1",
                  "data_api_version": "3.0",
                  "data_channel_uri": "https://vmart.ai/specificsurveydata",
                  "routing_model": {
                    "MYSPECIFIC_DETAILS": []
                  },
                  "screens": [
                    {
                      "id": "MYSPECIFIC_DETAILS",
                      "title": "MYSPECIFIC_DETAILS",
                      "terminal": True,
                      "data": {
                        "details": {
                          "type": "string",
                          "__example__": ""
                        },
                        "options": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "string"
                              },
                              "title": {
                                "type": "string"
                              },
                              "description": {
                                                "type": "string"
                                            }
                            }
                          },
                          "__example__": []
                        }
                      },
                      "layout": {
                        "type": "SingleColumnLayout",
                        "children": [
                          {
                            "type": "Form",
                            "name": "cover_form",
                            "children": [
                              {
                                "type": "TextHeading",
                                "text": "${data.details}"
                              },
                              {
                                "type": "RadioButtonsGroup",
                                "name": "options",
                                "data-source": "${data.options}",
                                "label": "Options",
                                "required": True
                              },
                              {
                                "type": "Footer",
                                "label": "complete",
                                "on-click-action": {
                                  "name": "complete",
                                  "payload": {
                                    "MY_data": "${form.options}"
                                  }
                                }
                              }
                            ]
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
                file_path = f'C:/Vailo/04-01-2023/A_vMart/A_vMart/{new_name}.json'
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

    return HttpResponse("wait for generating flow id")


def mysurvey(request):
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
    market_settingsObj = Survey_marketplace_settings.objects.filter(client_id=request.user.id)
    for m_i in market_settingsObj:
        random_number = random.randint(1, 1000)
        print("fffff")
        base_name = 'generic_flow'
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
            donation_obj = Survey_marketplace_settings.objects.filter(client_id=request.user.id)
            for d_i in donation_obj:
                d_i.my_survey_flow_id = id_value
                d_i.save()
                print("successfully saved the flow id")
                data = {
                  "version": "2.1",
                  "data_api_version": "3.0",
                  "data_channel_uri": "https://vmart.ai/mysurveydata",
                  "routing_model": {
                    "MYSURVEY_DETAILS": []
                  },
                  "screens": [
                    {
                      "id": "MYSURVEY_DETAILS",
                      "title": "MYSURVEY_DETAILS",
                      "terminal": True,
                      "data": {
                        "details": {
                          "type": "string",
                          "__example__": ""
                        },
                        "options": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "string"
                              },
                              "title": {
                                "type": "string"
                              },
                              "description": {
                                                "type": "string"
                                            }
                            }
                          },
                          "__example__": []
                        }
                      },
                      "layout": {
                        "type": "SingleColumnLayout",
                        "children": [
                          {
                            "type": "Form",
                            "name": "cover_form",
                            "children": [
                              {
                                "type": "TextHeading",
                                "text": "${data.details}"
                              },
                              {
                                "type": "RadioButtonsGroup",
                                "name": "options",
                                "data-source": "${data.options}",
                                "label": "Options",
                                "required": True
                              },
                              {
                                "type": "Footer",
                                "label": "complete",
                                "on-click-action": {
                                  "name": "complete",
                                  "payload": {
                                    "MY_data": "${form.options}"
                                  }
                                }
                              }
                            ]
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
                file_path = f'C:/Vailo/04-01-2023/A_vMart/A_vMart/{new_name}.json'
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

    return HttpResponse("wait for generating flow id")
