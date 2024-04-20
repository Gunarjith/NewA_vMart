import plotly.express as px
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import openpyxl
import json
from django.views.decorators.csrf import csrf_exempt

import io

import matplotlib.pyplot as plt
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.db import connection
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import logging
import boto3
from vailodb.models import event_master, ticket_information, ticket_customer_master, campaign_customer, event_settings, \
    event_slots, event_ticket_category, ticket_billing, admin_permission, ticket_billing_details, campaign_info, \
    Subclient, SubUserPreference, History_campaign_customer, History_campaign_infor, facebook_details

# from botocore.exceptions import ClientError
# from botocore.client import Config
from A_vMart.settings import AWS_STORAGE_BUCKET_NAME, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID
import requests
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.urls import reverse
import pandas as pd

import plotly as px
from django.http import JsonResponse


from django.db.models import Count
import plotly.graph_objects as go
import datetime
import math
import numpy as np
#




def dashboard(request):
    # Ticket Graph
    # Ticket Graph
    events = event_master.objects.filter(client_id=request.user.id)
    data = []
    for event in events:
        event_data = {
            'text': f"{event.Event_Name} - {event.Event_Description} - {event.Start_Date}",
            'id': event.id,
        }
        data.append(event_data)

    selected_event_id = request.GET.get('event_id')
    selected_event = None
    event_name = 'All events'

    if selected_event_id:
        if selected_event_id != 'all':  # Handle case when specific event is selected
            try:
                selected_event = event_master.objects.get(id=selected_event_id)
                event_name = selected_event.Event_Name
            except event_master.DoesNotExist:
                messages.error(request, "Selected event does not exist.")
                return redirect('dashboard')

    ticket_data = ticket_information.objects.values('event_master_id').annotate(ticket_count=Count('id'))

    event_data = event_master.objects.values('id', 'Start_Date', 'Event_Name')  # Include 'Event_Name' in the query
    ticket_df = pd.DataFrame.from_records(ticket_data)
    event_df = pd.DataFrame.from_records(event_data)
    try:
        merged_df = event_df.merge(ticket_df, left_on='id', right_on='event_master_id', how='left')
    except KeyError:
        return render(request, 'K_Ticket/EventDashboard.html',
                      {'message': 'No tickets available for the selected event.', 'data': data,
                       'selected_event': selected_event})

    merged_df['Start_Date'] = pd.to_datetime(merged_df['Start_Date'])
    merged_df['Month_Year'] = merged_df['Start_Date'].dt.strftime('%b-%Y')

    fig = go.Figure()

    # ...
    tick_interval = 1  # Add this line to set a default value for tick_interval

    # ...

    if selected_event:
        event_ticket_count = merged_df[merged_df['event_master_id'] == selected_event.id]
        if len(event_ticket_count) > 0:
            ticket_colors = px.colors.qualitative.Alphabet[:len(event_ticket_count)]
            max_count = event_ticket_count['ticket_count'].max()  # Find the maximum campaign count
            tick_interval = max(1, math.ceil(max_count / 10))  # Find the maximum campaign count

            fig.add_trace(
                go.Bar(
                    x=[selected_event.Start_Date.strftime('%b-%Y')],
                    y=[event_ticket_count['ticket_count'].sum()],
                    name=selected_event.Event_Name,
                    text=[selected_event.Event_Name],
                    textposition='inside',
                    marker_color=ticket_colors,
                )
            )
            fig.update_layout(
                yaxis=dict(
                    tickformat='d',
                    tickmode='linear',
                    tick0=0,  # Start the tick marks from 0
                    dtick=tick_interval,  # Set the tick interval
                ),
                dragmode=False,
                title=f"Ticket Count for {event_name}",
            )
            tick_interval = max(1, math.ceil(max_count / 10))  # Adjust the divisor to control the number of tick marks

            fig.update_layout(
                title=f" Tickets for {event_name}",
                showlegend=True
            )
        # else:
        #     messages.warning(request, "No event selected.")


    else:
        monthly_ticket_count = merged_df.groupby(['Month_Year', 'event_master_id'])['ticket_count'].sum().reset_index()
        ordered_months = sorted(monthly_ticket_count['Month_Year'].unique(),
                                key=lambda x: datetime.strptime(x, '%b-%Y'))
        monthly_ticket_count['Month_Year'] = pd.Categorical(monthly_ticket_count['Month_Year'],
                                                            categories=ordered_months,
                                                            ordered=True)
        monthly_ticket_count.sort_values('Month_Year', inplace=True)

        if len(monthly_ticket_count) > 0:
            unique_events = monthly_ticket_count['event_master_id'].unique()
            num_events = len(unique_events)
            ticket_colors = px.colors.qualitative.Alphabet[:num_events]
            max_count = monthly_ticket_count['ticket_count'].max()  # Find the maximum campaign count

            for i, event_id in enumerate(unique_events):
                event_data = monthly_ticket_count[monthly_ticket_count['event_master_id'] == event_id]
                color = ticket_colors[i]

                event_name = event_df[event_df['id'] == event_id]['Event_Name'].values[0]

                fig.add_trace(go.Bar(
                    x=event_data['Month_Year'],
                    y=event_data['ticket_count'],
                    name=event_name,
                    text=event_data['ticket_count'],
                    textposition='inside',
                    marker_color=color,
                ))
            tick_interval = max(1, math.ceil(max_count / 10))  # Adjust the divisor to control the number of tick marks

            fig.update_layout(
                title='Ticket Count by Month',
                xaxis_title='Month',
                yaxis_title='Ticket Count',
                barmode='stack',
                xaxis=dict(categoryorder='array', categoryarray=ordered_months),
                yaxis=dict(
                    tickformat='d',
                    tickmode='linear',
                    tick0=0,  # Start the tick marks from 0
                    dtick=tick_interval,  # Set the tick interval
                ),
                dragmode=False,

            )
        else:
            fig.update_layout(
                title='Ticket Count by Month',
                xaxis_title='Month',
                yaxis_title='Ticket Count',
            )
            messages.warning(request, "No tickets available for any event.")

    fig.update_traces(marker_line_width=1.5)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    config = {'displayModeBar': False}
    ticket_html = fig.to_html(full_html=False, include_plotlyjs='cdn', config=config)

    # Customer Graph
    customer_data = ticket_customer_master.objects.filter(client_id=request.user.id).values('Customer_Status',
                                                                                            'vailo_record_creation').annotate(
        customer_count=Count('id'))
    customer_df = pd.DataFrame.from_records(customer_data)
    customer_fig = go.Figure()

    if not customer_df.empty:
        customer_df['vailo_record_creation'] = pd.to_datetime(customer_df['vailo_record_creation'])
        customer_df['Month_Year'] = customer_df['vailo_record_creation'].dt.strftime('%b-%Y')

        monthly_customer_count = customer_df.groupby(['Month_Year', 'Customer_Status'])[
            'customer_count'].sum().reset_index()
        ordered_months = sorted(monthly_customer_count['Month_Year'].unique(),
                                key=lambda x: datetime.strptime(x, '%b-%Y'))
        monthly_customer_count['Month_Year'] = pd.Categorical(monthly_customer_count['Month_Year'],
                                                              categories=ordered_months, ordered=True)
        monthly_customer_count.sort_values('Month_Year', inplace=True)

        status_colors = {1: '#1f77b4', 2: '#ff7f0e'}
        status_names = {1: 'Customer', 2: 'Prospect'}
        max_count = monthly_customer_count['customer_count'].max()  # Find the maximum campaign count

        for status in customer_df['Customer_Status'].unique():
            status_data = monthly_customer_count[monthly_customer_count['Customer_Status'] == status]
            customer_fig.add_trace(go.Bar(
                x=status_data['Month_Year'],
                y=status_data['customer_count'],
                name=status_names.get(status),
                text=status_data['customer_count'],
                textposition='inside',
                marker_color=status_colors.get(status),
            ))

        if np.isnan(max_count):
            tick_interval = 1
        else:
            tick_interval = max(1, math.ceil(max_count / 10))
        customer_fig.update_layout(
            title='Customer Count by Month',
            xaxis_title='Month',
            yaxis_title='Customer Count',
            barmode='stack',
            xaxis=dict(categoryorder='array', categoryarray=ordered_months),
            yaxis=dict(
                tickformat='d',
                tickmode='linear',
                tick0=0,
                dtick=tick_interval,
            ),
            dragmode=False,
            showlegend=True,
        )
    else:
        customer_fig.update_layout(title='Customer Count by Month', xaxis_title='Month', yaxis_title='Customer Count')

    customer_fig.update_traces(marker_line_width=1.5)
    customer_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    customer_html = customer_fig.to_html(full_html=False, include_plotlyjs='cdn', config={'displayModeBar': False})

    # Campaign Graph
    campaign_data = campaign_customer.objects.filter(client_id=request.user.id).values('vailo_record_last_update',
                                                                                       'campaign_info_id',
                                                                                       'campaign_info__Campaign_Name').annotate(
        campaign_count=Count('id'))
    campaign_df = pd.DataFrame.from_records(campaign_data)
    campaign_fig = go.Figure()

    if not campaign_df.empty:
        campaign_df['vailo_record_last_update'] = pd.to_datetime(campaign_df['vailo_record_last_update'])
        campaign_df['Month_Year'] = campaign_df['vailo_record_last_update'].dt.strftime('%b-%Y')

        monthly_campaign_count = \
        campaign_df.groupby(['Month_Year', 'campaign_info_id', 'campaign_info__Campaign_Name'])[
            'campaign_count'].sum().reset_index()

        ordered_months = sorted(monthly_campaign_count['Month_Year'].unique(),
                                key=lambda x: datetime.strptime(x, '%b-%Y'))
        monthly_campaign_count['Month_Year'] = pd.Categorical(monthly_campaign_count['Month_Year'],
                                                              categories=ordered_months, ordered=True)
        monthly_campaign_count.sort_values('Month_Year', inplace=True)

        unique_campaign_ids = campaign_df['campaign_info_id'].unique()
        num_campaign_ids = len(unique_campaign_ids)
        colors = px.colors.qualitative.Set1[:num_campaign_ids]
        max_count = monthly_campaign_count['campaign_count'].max()

        for i, campaign_id in enumerate(unique_campaign_ids):
            status_data = monthly_campaign_count[monthly_campaign_count['campaign_info_id'] == campaign_id]

            campaign_fig.add_trace(go.Bar(
                x=status_data['Month_Year'],
                y=status_data['campaign_count'],
                name=status_data['campaign_info__Campaign_Name'].iloc[0],
                text=status_data['campaign_count'],
                textposition='inside',
                marker_color=colors[i],
            ))

        tick_interval = max(1, math.ceil(max_count / 10))

        campaign_fig.update_layout(
            title='Campaign Count by Month',
            xaxis_title='Month',
            yaxis_title='Campaign Count',
            barmode='stack',
            xaxis=dict(categoryorder='array', categoryarray=ordered_months),
            yaxis=dict(
                tickformat='d',
                tickmode='linear',
                tick0=0,
                dtick=tick_interval,
            ),
            dragmode=False,
            showlegend=True,
        )

    else:
        campaign_fig.update_layout(title='Campaign Count by Month', xaxis_title='Month', yaxis_title='Campaign Count')

    campaign_fig.update_traces(marker_line_width=1.5)
    campaign_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    campaign_html = campaign_fig.to_html(full_html=False, include_plotlyjs='cdn', config={'displayModeBar': False})



    # status graph
    ticket_data = ticket_information.objects.values('event_master_id', 'event_slots_id',
                                                    'event_ticket_category_id', 'ticket_status').annotate(
        ticket_count=Count('id'))

    ticket_df = pd.DataFrame.from_records(ticket_data)
    fig = go.Figure()
    legend_added = {'Sold': False, 'Balance': False, 'Used': False}

    for _, group_df in ticket_df.groupby(['event_master_id', 'event_slots_id', 'event_ticket_category_id']):
        event_master_name = event_master.objects.get(id=group_df['event_master_id'].iloc[0]).Event_Name
        event_slot_name = event_slots.objects.get(id=group_df['event_slots_id'].iloc[0]).Slot_Name
        event_ticket_category_name = event_ticket_category.objects.get(id=group_df['event_ticket_category_id'].iloc[0]).Category_Name

        label = f"{event_master_name} - {event_slot_name} - {event_ticket_category_name}"

        if any(group_df['ticket_status'].isin([0, 10])):
            count_balance = group_df[group_df['ticket_status'].isin([0, 10])]['ticket_count'].sum()
            fig.add_trace(go.Bar(
                x=[label],
                y=[count_balance],
                name='Balance',
                text=[count_balance],
                textposition='inside',
                marker_color='blue',
                showlegend=not legend_added['Balance']
            ))
            legend_added['Balance'] = True




        if any(group_df['ticket_status'].isin([20, 30, 40])):
            count_sold = group_df[group_df['ticket_status'].isin([20, 30, 40])]['ticket_count'].sum()
            fig.add_trace(go.Bar(
                x=[label],
                y=[count_sold],
                name='Sold',
                text=[count_sold],
                textposition='inside',
                marker_color='green',
                showlegend=not legend_added['Sold']
            ))
            legend_added['Sold'] = True


        if any(group_df['ticket_status'].isin([80, 90])):
            count_used = group_df[group_df['ticket_status'].isin([80, 90])]['ticket_count'].sum()
            fig.add_trace(go.Bar(
                x=[label],
                y=[count_used],
                name='Others',
                text=[count_used],
                textposition='inside',
                marker_color='red',
                showlegend=not legend_added['Used']
            ))
            legend_added['Used'] = True

    fig.update_layout(
        barmode='stack',
        title='Ticket Count',
        xaxis_title='Tickets',
        yaxis_title='Ticket Count',
        yaxis=dict(showticklabels=False),
        dragmode=False,
    )

    status_html = fig.to_html(full_html=False, include_plotlyjs='cdn', config={'displayModeBar': False})

    return render(request, 'K_Ticket/EventDashboard.html', {'ticket_html': ticket_html, 'customer_html': customer_html,
                                                            'campaign_html': campaign_html,"status_html":status_html, 'data': data,
                                                            'selected_event': selected_event})


from django.http import HttpResponseRedirect


# #new implument
# def eventmaster(request):
#     skip_levels = request.GET.get('skip_levels')
    
#     if skip_levels == 'level1':
#         eventmaster = event_master.objects.filter(client_id=request.user.id)
#     elif skip_levels == 'level2':
#         eventmaster = event_master.objects.filter(client_id=request.user.id)
#         return HttpResponseRedirect(reverse('slotOFcategory', args=[eventmaster[0].id]))
#     else:
#         status_param = request.GET.get('status')
#         if status_param == 'inactive':
#             eventmaster = event_master.objects.filter(client_id=request.user.id, status=2)
#         elif status_param == 'all':
#             eventmaster = event_master.objects.filter(client_id=request.user.id)
#         else:
#             eventmaster = event_master.objects.filter(client_id=request.user.id, status=1)

#     return render(request, 'K_Ticket/EventMaster.html', {'eventmaster': eventmaster})

# def eventmaster(request):
#     client_id = request.user.id

#     try:
#         event_setting = event_settings.objects.get(client_id=client_id)
#         selected_level_settings = event_setting.level_settings
#     except event_settings.DoesNotExist:
#         selected_level_settings = 'none'

#     eventId = 0  # Initialize 'eventId' variable with a default value of 0
#     slotId = None  # Initialize 'slotId' variable with None

#     if selected_level_settings == 'skiplevel1':
#         # Check if there is an existing event master for the client
#         existing_event_master = event_master.objects.filter(client_id=client_id).first()
#         if existing_event_master:
#             eventId = existing_event_master.id
#         else:
#             # Create a new event master if it doesn't exist
#             new_event_master = event_master(client_id=client_id)
#             new_event_master.save()
#             eventId = new_event_master.id

#         # Check if there is an existing event slot for the client and event master
#         existing_event_slot = event_slots.objects.filter(client_id=client_id, event_master_id=eventId).first()
#         if existing_event_slot:
#             slotId = existing_event_slot.id
#         else:
#             # Create a new event slot if it doesn't exist
#             new_event_slot = event_slots(client_id=client_id, event_master_id=eventId)
#             new_event_slot.save()
#             slotId = new_event_slot.id

#         eventslot = event_slots.objects.filter(client_id=request.user.id)
#         return render(request, 'K_Ticket/eventOFslot.html', {'eventslot': eventslot, 'eventId': eventId})

#     elif selected_level_settings == 'skiplevel1and2':
#         # Handle the logic for 'skiplevel1and2' case
#         # Your code logic here

#         return render(request, 'K_Ticket/slotOFcategory.html', {'slotId': slotId, 'eventId': eventId})

#     else:
#         eventmaster = event_master.objects.filter(client_id=client_id, status=1)  # Filter only active records by default
#         return render(request, 'K_Ticket/EventMaster.html', {'eventmaster': eventmaster, 'eventId': eventId})


def eventmaster(request):
    client_id = request.user.id

    try:
        event_setting = event_settings.objects.get(client_id=client_id)
        selected_level_settings = event_setting.level_settings
    except event_settings.DoesNotExist:
        selected_level_settings = 'none'

    eventId = 0  # Initialize 'eventId' variable with a default value of 0
    slotId = None  # Initialize 'slotId' variable with None

    if selected_level_settings == 'skiplevel1':
        # Check if there is an existing event master for the client
        existing_event_master = event_master.objects.filter(client_id=client_id).first()
        if existing_event_master:
            eventId = existing_event_master.id
        else:
            # Create a new event master if it doesn't exist
            new_event_master = event_master(client_id=client_id)
            new_event_master.save()
            eventId = new_event_master.id

        # Check if there is an existing event slot for the client and event master
        existing_event_slot = event_slots.objects.filter(client_id=client_id, event_master_id=eventId).first()
        if existing_event_slot:
            slotId = existing_event_slot.id
        else:
            # Create a new event slot if it doesn't exist
            new_event_slot = event_slots(client_id=client_id, event_master_id=eventId)
            new_event_slot.save()
            slotId = new_event_slot.id

        eventslot = event_slots.objects.filter(client_id=request.user.id)
        return render(request, 'K_Ticket/eventOFslot.html', {'eventslot': eventslot, 'eventId': eventId})

    elif selected_level_settings == 'skiplevel1and2':
        # Handle the logic for 'skiplevel1and2' case
        # Your code logic here
        existing_event_master = event_master.objects.filter(client_id=client_id).first()
        if existing_event_master:
            eventId = existing_event_master.id
        else:
            # Create a new event master if it doesn't exist
            new_event_master = event_master(client_id=client_id)
            new_event_master.save()
            eventId = new_event_master.id

        # Check if there is an existing event slot for the client and event master
        existing_event_slot = event_slots.objects.filter(client_id=client_id, event_master_id=eventId).first()
        if existing_event_slot:
            slotId = existing_event_slot.id
        else:
            # Create a new event slot if it doesn't exist
            new_event_slot = event_slots(client_id=client_id, event_master_id=eventId)
            new_event_slot.save()
            slotId = new_event_slot.id   
        slotOFcategory = event_ticket_category.objects.filter(client_id=request.user.id)    
        return render(request, 'K_Ticket/slotOFcategory.html', {'slotId': slotId, 'eventId': eventId,'slotOFcategory':slotOFcategory})

    else:
        eventmaster = event_master.objects.filter(client_id=client_id, status=1)  # Filter only active records by default
        return render(request, 'K_Ticket/EventMaster.html', {'eventmaster': eventmaster, 'eventId': eventId})

# def eventmaster(request):
#     status_param = request.GET.get('status')
#     if status_param == 'inactive':
#         eventmaster = event_master.objects.filter(
#             client_id=request.user.id, status=2)  # Filter only inactive records
#     elif status_param == 'all':
#         eventmaster = event_master.objects.filter(
#             client_id=request.user.id)  # Return all records
#     else:
#         # Filter only active records by default
#         eventmaster = event_master.objects.filter(
#             client_id=request.user.id, status=1)

#     return render(request, 'K_Ticket/EventMaster.html', {'eventmaster': eventmaster})


@csrf_exempt
def updateEventStatus(request, event_id):
    print("scsd")
    print('Event ID:', event_id)
    print(request.method)
    if request.method == 'POST' and request.headers.get('Accept') == 'application/json':

        body = json.loads(request.body)
        status = body.get('status')
        print('Event ID:', event_id)
        print('Status:', status)

        try:
            event = event_master.objects.get(id=event_id)
            event.status = int(status)
            event.save()
            print('Event status updated successfully.')
            return JsonResponse({'status': 'success'})

        except event_master.DoesNotExist:
            print('Event not found.')
            return JsonResponse({'status': 'error', 'message': 'Event not found.'}, status=404)

        except Exception as e:
            print('An error occurred:', str(e))
            return JsonResponse({'status': 'error', 'message': 'An error occurred.', 'error': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)


def addevents(request):
    return render(request, 'K_Ticket/addevents.html')


def deleteevents(request, id):
    deleteevents = event_master.objects.get(client_id=request.user.id, pk=id)
    deleteevents.delete()
    return redirect('eventmaster')

from datetime import datetime
print(type(datetime))  # Add this line before the problematic code

#26-07
# def submitevent(request):
#     if request.method == "POST":
#         submitevents = event_master()
#         submitevents.Event_Name = request.POST.get('EventName')
#         submitevents.Event_Description = request.POST.get('EventDescription')
        
#         start_date_str = request.POST.get('StartDate')
#         if start_date_str:
#             try:
#                 start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
#                 submitevents.Start_Date = start_date
#             except ValueError:
#                 # Handle the case when the date is in an invalid format
#                 # For example, set a default date or handle the error as needed.
#                 submitevents.Start_Date = ''  # Set a default value (None)

#         end_date_str = request.POST.get('EndDate')
#         if end_date_str:
#             try:
#                 end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
#                 submitevents.End_Date = end_date
#             except ValueError:
#                 # Handle the case when the date is in an invalid format
#                 # For example, set a default date or handle the error as needed.
#                 submitevents.End_Date = ''  # Set a default value (None)
        
#         if 'EvenHeaderImage' in request.FILES:
#             submitevents.Event_Message_Header_Image = request.FILES['EvenHeaderImage']
        
#         # ... Continue with other fields ...

#         # Get the selected status value from the form
#         status_value = int(request.POST.get('status', 1))
#         submitevents.status = status_value

#         # Save the object to the database
#         submitevents.client_id = request.user.id
#         submitevents.save()
#         return redirect("eventmaster")

#     return render(request, 'K_Ticket/addevents.html')
def submitevent(request):
    if request.method == "POST":
        submitevents = event_master()
        submitevents.Event_Name = request.POST.get('EventName')
        submitevents.Event_Description = request.POST.get('EventDescription')
        submitevents.Start_Date = request.POST.get('StartDate')
        # submitevents.Event_Message_Header = request.POST.get('eventmessageheader')
        # submitevents.Event_Body = request.POST.get('eventbody')
        # submitevents.Event_Footer = request.POST.get('eventfooter')
        submitevents.End_Date = request.POST.get('EndDate')
        # submitevents.Event_Logo = request.FILES['Eventlogo']
        # submitevents.Event_ticket_image = request.FILES['Eventticketimg']
        submitevents.Event_Message_Header_Image = request.FILES['EvenHeaderImage']
        submitevents.Event_Message_Header_Text = request.POST.get(
            'eventheadertext')
        submitevents.Event_Message_Body_Text = request.POST.get(
            'eventbodytext')
        submitevents.Event_Message_Footer_Text = request.POST.get(
            'eventfootertext')
        submitevents.Event_slots_button_name = request.POST.get(
            'eventslotbuttonname')
        submitevents.client_id = request.user.id

        # Get the selected status value from the form
        status_value = int(request.POST.get('status', 1))
        submitevents.status = status_value
        submitevents.save()
        return redirect("eventmaster")
    return render(request, 'K_Ticket/addevents.html')

def updateevent(request, id):
    updateevent = event_master.objects.filter(client_id=request.user.id, id=id)
    if request.method == 'POST':
        for i in updateevent:
            updateevent = event_master.objects.filter(
                client_id=request.user.id, id=id)
            if request.method == 'POST':
                for i in updateevent:
                    updateeventEdit = event_master.objects.get(id=i.id)
                    updateeventEdit.Event_Name = request.POST.get(
                        'reeventname')
                    updateeventEdit.Event_Description = request.POST.get(
                        'reeventdesc')
                    updateeventEdit.Event_Message_Header = request.POST.get(
                        'reeventmessageheader')
                    updateeventEdit.Event_Body = request.POST.get(
                        'reeventbody')
                    updateeventEdit.Event_Footer = request.POST.get(
                        'reeventfooter')
                    if request.POST.get('restartdate'):
                        updateeventEdit.Start_Date = request.POST.get(
                            'restartdate')
                    if request.POST.get('reenddate'):
                        updateeventEdit.End_Date = request.POST.get(
                            'reenddate')
                    if 'relogo' in request.FILES and len(request.FILES['relogo']) != 0:
                        updateeventEdit.Event_Logo = request.FILES['relogo']
                    else:
                        updateeventEdit.Event_Logo = i.Event_Logo
                    if 'reticket' in request.FILES and len(request.FILES['reticket']) != 0:
                        updateeventEdit.Event_ticket_image = request.FILES['reticket']
                    else:
                        updateeventEdit.Event_ticket_image = i.Event_ticket_image
                    if 'reEventMessageHeaderImage' in request.FILES and len(request.FILES['reEventMessageHeaderImage']) != 0:
                        updateeventEdit.Event_Message_Header_Image = request.FILES[
                            'reEventMessageHeaderImage']
                    else:
                        updateeventEdit.Event_Message_Header_Image = i.Event_Message_Header_Image
                    updateeventEdit.Event_Message_Header_Text = request.POST.get(
                        'reeventmessageheadertext')
                    updateeventEdit.Event_Message_Body_Text = request.POST.get(
                        'reeventmessagebodytext')
                    updateeventEdit.Event_Message_Footer_Text = request.POST.get(
                        'reeventmessagefootertext')
                    updateeventEdit.Event_slots_button_name = request.POST.get(
                        'reeventslotbuttonname')

                    # Get the selected status value from the form
                    status_value = int(request.POST.get('status', i.status))
                    updateeventEdit.status = status_value

                    updateeventEdit.save()
                return redirect('eventmaster')
            return render(request, 'K_Ticket/EventMaster.html', {'modifyevents': updateevent})

# ------------------------------------------- Slot -------------------------------------------------


def addslotINevent(request):
    status_param = request.GET.get('status')
    if status_param == 'inactive':
        eventslots = event_slots.objects.filter(
            client_id=request.user.id, status=2)  # Filter only inactive records
    elif status_param == 'all':
        eventslots = event_slots.objects.filter(
            client_id=request.user.id)  # Return all records
    else:
        # Filter only active records by default
        eventslots = event_slots.objects.filter(
            client_id=request.user.id, status=1)

    return render(request, 'K_ticket/addslots.html', {'eventslots': eventslots})


# def addslotINevent(request):
#     eventslots = event_slots.objects.filter(client_id=request.user.id)
#     return render(request, 'K_ticket/addslots.html', {'surya': eventslots})


def submitslot(request, id):
    if request.method == "POST":
        submitslot = event_slots(client_id=request.user.id, event_master_id=id)
        submitslot.Slot_Name = request.POST.get('SlotName')
        submitslot.Slot_Description = request.POST.get('SlotDescription')
        if 'SlotHeaderImage' in request.FILES:
            submitslot.Slot_message_Header_Image = request.FILES['SlotHeaderImage']
            # info_creation.cancel_ticket_header_image = request.FILES['cancelticketheaderimage']

        submitslot.Slot_Message_Header_Text = request.POST.get('slotheadertext')
        submitslot.Slot_Message_Body_Text = request.POST.get('slotbodytext')
        submitslot.Slot_Message_Footer_Text = request.POST.get('slotfootertext')
        submitslot.slot_category_button_name = request.POST.get('slotcategorybuttonname')
        submitslot.client_id = request.user.id
        submitslot.event_master_id = id
        submitslot.save()
        return redirect('/Eventmaster/eventOFslot/' + str(id) + '/')

    return render(request, 'K_Ticket/addslots.html', {'eventId': id})

def submitcattickets(request, id):
    return render(request, 'K_ticket/addtickets.html', {'id': id, 'tid': id, 'ticketID': id})


# # new implumentaion
# def eventOFslot(request, id):
#     skip_levels = request.GET.get('skip_levels')

#     if skip_levels == 'level1':
#         eventslot = event_slots.objects.filter(client_id=request.user.id)
#         return HttpResponseRedirect(reverse('slotOFcategory', args=[eventslot[0].id]))
#     else:
#         modifyevents = event_master.objects.filter(client_id=request.user.id, id=id)
#         eventslot = event_slots.objects.filter(client_id=request.user.id, event_master_id=id)

#         if len(eventslot) == 1:
#             for s in eventslot:
#                 print(s.Slot_Name)
        
#         return render(request, 'K_ticket/eventOFslot.html', {'modifyevents': modifyevents, 'eventslot': eventslot, 'eventId': id})

# def slotOFcategory(request, id):
#     skip_levels = request.GET.get('skip_levels')

#     if skip_levels == 'level2':
#         slotOFcategory = event_ticket_category.objects.filter(client_id=request.user.id)
#     else:
#         modifyslot = event_slots.objects.filter(client_id=request.user.id, id=id)
#         slotOFcategory = event_ticket_category.objects.filter(client_id=request.user.id, event_slots_id=id)

#         if len(slotOFcategory):
#             for i in slotOFcategory:
#                 pass
    
#     return render(request, 'K_Ticket/slotOFcategory.html', {'slotOFcategory': slotOFcategory, 'modifyslot': modifyslot, 'eventId': id})


def eventOFslot(request, id):
    client_id = request.user.id

    try:
        event_setting = event_settings.objects.get(client_id=client_id)
        selected_level_settings = event_setting.level_settings
    except event_settings.DoesNotExist:
        selected_level_settings = 'none'

    if selected_level_settings == 'skiplevel1' or selected_level_settings == 'skiplevel1and2':
        eventslot = event_slots.objects.all()
        return render(request, 'K_ticket/eventOFslot.html', {'eventslot': eventslot, 'eventId': id})

    modifyevents = event_master.objects.filter(client_id=client_id, id=id)
    eventslot = event_slots.objects.filter(client_id=client_id, event_master_id=id)

    if len(eventslot) == 1:
        for s in eventslot:
            print(s.Slot_Name)

    return render(request, 'K_ticket/eventOFslot.html',
                  {'modifyevents': modifyevents, 'eventslot': eventslot, 'eventId': id})



def slotOFcategory(request, id):
    modifyslot = event_slots.objects.filter(client_id=request.user.id, id=id)
    slotOFcategory = event_ticket_category.objects.filter(
        client_id=request.user.id, event_slots_id=id)
    if len(slotOFcategory):
        for i in slotOFcategory:
            pass
    return render(request, 'K_Ticket/slotOFcategory.html',
                  {'slotOFcategory': slotOFcategory, 'modifyslot': modifyslot, 'eventId': id})


def deleteslot(request, id):
    deleteslot = event_slots.objects.filter(client_id=request.user.id, id=id)
    delete_id = ''
    for del_i in deleteslot:
        delete_id = del_i.event_master_id
    deleteslot.delete()
    return redirect('/Eventmaster/eventOFslot/' + str(delete_id) + '/')


def updateslot(request, id):
    updateslot = event_slots.objects.filter(client_id=request.user.id, id=id)

    if request.method == 'POST':
        event_id = ''
        for i in updateslot:
            event_id = i.event_master_id
            updateeventEdit = event_slots.objects.get(id=i.id)
            updateeventEdit.Slot_Name = request.POST.get('reslotname')
            updateeventEdit.Slot_Description = request.POST.get('reslotdesc')
            if 'reSlotmessageHeaderImage' in request.FILES and len(request.FILES['reSlotmessageHeaderImage']) != 0:
                updateeventEdit.Slot_message_Header_Image = request.FILES['reSlotmessageHeaderImage']
            else:
                updateeventEdit.Slot_message_Header_Image = i.Slot_message_Header_Image
            updateeventEdit.Slot_Message_Header_Text = request.POST.get(
                'reslotmessageheadertext')
            updateeventEdit.Slot_Message_Body_Text = request.POST.get(
                'reslotmessagebodytext')
            updateeventEdit.Slot_Message_Footer_Text = request.POST.get(
                'reslotmessagefootertext')
            updateeventEdit.slot_category_button_name = request.POST.get(
                'reslotcategorybuttonname')
            updateeventEdit.save()
            return redirect('/Eventmaster/eventOFslot/' + str(event_id) + '/')
    return render(request, 'K_Ticket/eventOFslot.html', {'modifyslot': updateslot})


# -------------------------------------- Category -----------------------------------------


def modifycategory(request, id):
    modifycategory = event_ticket_category.objects.filter(
        client_id=request.user.id, id=id)
    ticketscategory = ticket_information.objects.filter(
        client_id=request.user.id, event_ticket_category_id=id)
    if len(ticketscategory) == 1:
        for i in ticketscategory:
            pass
    return render(request, 'K_Ticket/modifycategory.html',
                  {'modifycategory': modifycategory, 'ticketscategory': ticketscategory, 'catId': id})


def modifyticket(request, id):
    modifyticket = ticket_information.objects.filter(
        client_id=request.user.id, id=id)
    return render(request, 'K_Ticket/modifytickets.html', {'modifyticket': modifyticket, 'modify': id})


def deleteticket(request, id):
    deleteticket = ticket_information.objects.filter(
        client_id=request.user.id, id=id)
    deltick_id = ''
    for i in deleteticket:
        deltick_id = i.event_ticket_category_id
    deleteticket.delete()
    return redirect('/Eventmaster/modifycategory/' + str(deltick_id) + '/')


def deletecategory(request, id):
    deletecategory = event_ticket_category.objects.filter(
        client_id=request.user.id, id=id)
    deletecat_id=''
    for catg_i in deletecategory:
        deletecat_id = catg_i.event_slots_id

    deletecategory.delete()
    return redirect('/Eventmaster/slotOFcategory/' + str(deletecat_id) + '/')




def addcateINslot(request, slotID):
    return render(request, 'K_ticket/addcategory.html', {'slotID': slotID})

# def addcateINslot(request, slotID=None):
#     if slotID is None:
#         # Handle the logic for 'skiplevel1' and 'skiplevel1and2' cases where event master and event slot IDs are not available
#         # For example, you can create a new event master and event slot
#         new_event_master = event_master(client_id=request.user.id)
#         new_event_master.save()
#         new_event_slot = event_slots(client_id=request.user.id, event_master_id=new_event_master.id)
#         new_event_slot.save()
#         slotID = new_event_slot.id
    
#     # Handle the normal case where event master and event slot IDs are available
#     # Add your code logic here
    
#     return render(request, 'K_Ticket/addcateINslot.html', {'slotID': slotID})


from django.shortcuts import get_object_or_404

def submitcategory(request, id):
    event_slot = get_object_or_404(event_slots, id=id)  # Retrieve the event_slots object or return a 404 error if not found

    if request.method == "POST":
        submitcategory = event_ticket_category(
            client_id=request.user.id, event_slots_id=id)
        submitcategory = event_ticket_category()
        submitcategory.Category_Name = request.POST.get('CategoryName')
        submitcategory.Category_Description = request.POST.get(
            'CategoryDescription')
        submitcategory.Category_Price = request.POST.get('CategoryPrice')
        if 'Categoryticketimage' in request.FILES:
            submitcategory.category_ticket_image = request.FILES['Categoryticketimage']

        if 'CategoryHeaderImage' in request.FILES:    
            submitcategory.Category_Message_Header_Image = request.FILES['CategoryHeaderImage']
        submitcategory.Category_Message_Header_Text = request.POST.get(
            'CategoryHeaderText')
        submitcategory.Category_Message_Body_Text = request.POST.get(
            'CategoryBodyText')
        submitcategory.Category_Message_Footer_Text = request.POST.get(
            'CategoryFooterText')
        submitcategory.Number_Of_Ticket_Button_Name = request.POST.get(
            'numberbuttonname')
        submitcategory.client_id = request.user.id
        event_master = event_slot.event_master
        submitcategory.event_master_id = event_master.id
        submitcategory.event_slots_id = id
        submitcategory.save()
        print(submitcategory.event_slots_id)
        return redirect('/Eventmaster/slotOFcategory/' + str(id) + '/')
    
    return render(request, 'K_Ticket/addcategory.html', {'catID': id})

# def submitticket(request,id):


#     if request.method == "POST":
#         submitticket = ticket_information(client_id=request.user.id,event_ticket_category_id= id)
#         submitticket = ticket_information()
#         submitticket.ticket_number = request.POST.get('TicketNumber')
#         submitticket.expiry_date = request.POST.get('expirydate')
#         submitticket.client_id = request.user.id
#         event_master = event_ticket_category.objects.get(id=id).event_master
#         submitticket.event_master_id = event_master.id
#         event_slots = event_ticket_category.objects.get(id=id).event_slots
#         submitticket.event_slots_id = event_slots.id
#         submitticket.event_ticket_category_id = id
#         submitticket.ticket_status = 00
#         submitticket.save()
#         return redirect('/Eventmaster/modifycategory/' + str(id) + '/')
#     return render(request,'K_ticket/addtickets.html',{'tid':id})
# with validation

def submitticket(request, id):
    if request.method == "POST":
        ticket_number = request.POST.get('TicketNumber')
        category_id = id
        print("category_id : ", category_id)
        existing_ticket = ticket_information.objects.filter(
            ticket_number=ticket_number,
            event_ticket_category_id=category_id
        ).first()
        if existing_ticket:
            # TicketNumber is already in use for this category
            error_message = 'TicketNumber is already in use for this category'
            return render(request, 'K_ticket/addtickets.html', {'tid': id, 'ticketID': id, 'error_message': error_message})
        submitticket = ticket_information(
            client_id=request.user.id, event_ticket_category_id=category_id)
        submitticket.ticket_number = ticket_number
        submitticket.expiry_date = request.POST.get('expirydate')
        submitticket.client_id = request.user.id
        event_master = event_ticket_category.objects.get(
            id=category_id).event_master
        submitticket.event_master_id = event_master.id
        event_slots = event_ticket_category.objects.get(
            id=category_id).event_slots
        submitticket.event_slots_id = event_slots.id
        submitticket.event_ticket_category_id = category_id
        print("aaa")
        submitticket.ticket_status = 00
        submitticket.save()
        return redirect('/Eventmaster/modifycategory/' + str(category_id) + '/')
    return render(request, 'K_ticket/addtickets.html', {'tid': id, 'ticketID': id})


def saveTickets(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        tickets = data.get('tickets', [])
        expiry_date = data.get('expiryDate', '')

        # Save the tickets to the database
        saved_tickets = []
        duplicate_tickets = []

        for ticket_string in tickets:
            existing_ticket = ticket_information.objects.filter(
                ticket_number=ticket_string,
                event_ticket_category_id=id
            ).first()

            if existing_ticket:
                duplicate_tickets.append(ticket_string)
            else:
                category = event_ticket_category.objects.get(id=id)
                event_master_id = category.event_master.id
                event_slots_id = category.event_slots.id

                ticket = ticket_information(
                    client_id=request.user.id,
                    ticket_number=ticket_string,
                    event_ticket_category_id=id,
                    event_master_id=event_master_id,
                    event_slots_id=event_slots_id,
                    expiry_date=expiry_date,  # Assign the expiry date to the ticket
                    ticket_status=00
                    # Set other fields accordingly
                )
                ticket.save()
                saved_tickets.append(ticket_string)

                # Print the IDs
                print("Client ID:", ticket.client_id)
                print("Event Master ID:", ticket.event_master_id)
                print("Event Slots ID:", ticket.event_slots_id)
                print("Event Ticket Category ID:",
                      ticket.event_ticket_category_id)

        response_data = {
            "saved_tickets": saved_tickets,
            "duplicate_tickets": duplicate_tickets
        }

        return JsonResponse(response_data)

    return JsonResponse({"error": "Invalid request method."})


def excel_tickets(request, id):
    if request.method == 'POST':
        file = request.FILES['file']  # Get the uploaded file
        wb = openpyxl.load_workbook(file)  # Load the Excel workbook
        print('id', id)
        # Assuming the ticket numbers and expiry dates are in the first sheet, starting from the second row
        sheet = wb.active
        updated_tickets = set()  # Track updated ticket numbers to check for duplicates
        duplicate_tickets = []
        print(sheet)
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Assuming ticket number is in the first column
            ticket_number = row[0]
            # Assuming expiry date is in the second column
            expiry_date = row[1]
            print(
                f"Ticket Number: {ticket_number}, Expiry Date: {expiry_date}")
            # Check for duplicates
            if ticket_number in updated_tickets:
                duplicate_tickets.append(ticket_number)
                print("Skipping duplicate ticket:", ticket_number)
                continue

            print("ticket_number", ticket_number)
            print('event_ticket_category_id', id)

            try:
                # Retrieve the corresponding ticket
                ticket = ticket_information.objects.get(ticket_number=ticket_number,
                                                        event_ticket_category_id=id)
                print("Updating existing ticket:", ticket_number)
            except ObjectDoesNotExist:
                # Create a new ticket if it doesn't exist
                ticket = ticket_information(ticket_number=ticket_number,
                                            event_ticket_category_id=id)
                print("Creating new ticket:", ticket_number)

            # Update ticket information
            ticket.expiry_date = expiry_date
            # Set the client_id based on the logged-in user
            ticket.client_id = request.user.id
            ticket.ticket_status = 00

            # Retrieve the associated event master and slot
            event_category = event_ticket_category.objects.get(id=id)
            ticket.event_master_id = event_category.event_master_id
            ticket.event_slots_id = event_category.event_slots_id

            ticket.save()

            updated_tickets.add(ticket_number)

            print("event_master_id:", ticket.event_master_id)
            print("client_id:", ticket.client_id)
            print("category_id:", ticket.event_ticket_category_id)
            print("slot_id:", ticket.event_slots_id)

        if duplicate_tickets:
            return HttpResponse(f"The following ticket numbers are duplicates: {', '.join(duplicate_tickets)}")
        else:
            return redirect('/Eventmaster/modifycategory/' + str(id) + '/')

    return render(request, 'K_ticket/addtickets.html', {'id': id})


def generateqr(request, id):
    ticketinformation = ticket_information.objects.filter(
        client_id=request.user.id, event_ticket_category_id=id)
    eventinformation = event_ticket_category.objects.filter(
        client_id=request.user.id, id=id)
    categoryname = ""
    eventname = ""
    slotname = ""
    startdate = ""
    enddate = ""
    description = ""
    categoryticketimage = ''
    for z in eventinformation:
        categoryname = categoryname + z.Category_Name
        categoryticketimage = z.category_ticket_image
        # print(categoryticketimage)

        if categoryticketimage:
            for t in ticketinformation:
                ticket_number = ''
                if t.ticket_status == 0:
                    # print(t.ticket_number)

                    qr = qrcode.QRCode(version=1, box_size=20, border=4)
                    data = str(id) + "_" + str(t.ticket_number)
                    qr.add_data(data)
                    # print(f"{id}_{t.ticket_number}")
                    qr.make(fit=True)
                    qrimg = qr.make_image(
                        fill_color="black", back_color='white')
                    # print(qrimg)
                    qrimg.show()
                    # print("rrrr")
                    response = requests.get(
                        'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(z.category_ticket_image))
                    # print("111")
                    if response.status_code == 200:
                        # print("1111")
                        img = Image.open(BytesIO(response.content))
                        font1 = ImageFont.truetype('arial.ttf', 22)
                        imagepath = 'static/img/blankwhiteimage.jpg'
                        # size = (300, 300)
                        # crop_image = qrimg.copy()
                        # crop_image.thumbnail(size)
                        # copied_image = img.copy()

                        # copied_image.paste(crop_image, (715, 11))
                        # copied_image.show()

                        blankimg = Image.open(imagepath)
                        main_size=(882,371)
                        # size = (300, 300)
                        new_width = 170
                        new_height = 50
                        qr_width = 250
                        qr_height = 352
                        blank_resized_thumbnail = blankimg.resize((new_width,new_height))
                        qr_resized_thumbnail = qrimg.resize((qr_width,qr_height))
                        crop_main_image = img.copy()
                        crop_main_image.thumbnail(main_size)
                        # crop_image = qrimg.copy()
                        # crop_image.thumbnail(size)
                        copied_image = crop_main_image.copy()

                        copied_image.paste(qr_resized_thumbnail, (645, 9))
                        copied_image.paste(blank_resized_thumbnail, (65, 27))
                        copied_image.paste(blank_resized_thumbnail, (470, 27))
                        # copied_image.show()

                        draw = ImageDraw.Draw(copied_image)
                        TicketNo = "TNo:"
                        TNumber = f"{t.ticket_number}"
                        TicketPrice = "Price:"
                        TicketPrice1 = "₹" + f"{z.Category_Price}"

                        draw.text((69, 41), TicketNo, (0, 0, 0), font=font1)
                        draw.text((122, 41), TNumber, (0, 0, 0), font=font1)
                        draw.text((487, 41), TicketPrice,
                                  (0, 0, 0), font=font1)
                        draw.text((554, 41), TicketPrice1,
                                  (0, 0, 0), font=font1)
                        # plt.imshow(copied_image)
                        # plt.show()
                        # copied_image.show()
                        image_bytes = io.BytesIO()
                        copied_image.save(image_bytes, format='PNG')
                        image_bytes.seek(0)
                        image_data = image_bytes.getvalue()
                        filename = f" tickets_{id}_{t.ticket_number}.png"
                        t.ticket_QR.save(filename, ContentFile(image_data))
                        t.ticket_status = 10
                        t.save()
                        # copied_image.show()

                # else:
                    # print("status is updated")

        else:
            event = event_master.objects.filter(
                client_id=request.user.id, id=z.event_master_id)
            slot = event_slots.objects.filter(
                client_id=request.user.id, id=z.event_slots_id)
            for y in event:
                eventname = eventname + y.Event_Name
                startdate = y.Start_Date
                enddate = y.End_Date
                description = description + y.Event_Description
                # print(startdate)
                # print(enddate)

                startdate_string = startdate.strftime('%d-%m-%Y')
                enddate_sring = enddate.strftime('%d-%m-%Y')

                for s in slot:
                    slotname = slotname + s.Slot_Name
                print(ticketinformation)
                for t in ticketinformation:
                    if t.ticket_status == 0:
                        qr = qrcode.QRCode(version=1, box_size=20, border=4)
                        qr.add_data(t.ticket_number)
                        qr.make(fit=True)
                        qrimg = qr.make_image(
                            fill_color="black", back_color='white')
                        # qrimg.show()
                        response = requests.get(
                            'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(y.Event_ticket_image))
                        logoresponse = requests.get(
                            'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(y.Event_Logo))
                        if response.status_code == 200:

                            if logoresponse.status_code == 200:

                                # Open the image using Pillow
                                img = Image.open(BytesIO(response.content))
                                logoimage = Image.open(
                                    BytesIO(logoresponse.content))
                                # print("pppp")
                                # print("rr")

                                # Display the image
                                # img.show()
                                # logoimage.show()
                                # img.show()
                                font = ImageFont.truetype('arial.ttf', 35)
                                font1 = ImageFont.truetype('arial.ttf', 25)
                                font2 = ImageFont.truetype('arial.ttf', 24)
                                font3 = ImageFont.truetype('arial.ttf', 20)
                                font4 = ImageFont.truetype('arial.ttf', 23)
                                # img1 = Image.open(qrimg)
                                size = (300, 300)
                                size1 = (60, 60)
                                crop_image = qrimg.copy()
                                crop_logo = logoimage.copy()
                                crop_image.thumbnail(size)
                                crop_logo.thumbnail(size1)
                                copied_image = img.copy()

                                copied_image.paste(crop_image, (670, 75))
                                copied_image.paste(crop_logo, (90, 45))

                                # copied_image.show()
                                draw = ImageDraw.Draw(copied_image)
                                EventName = eventname
                                SlotName = slotname
                                CategoryName = categoryname

                                start_Date = startdate_string
                                end_date = enddate_sring

                                Description = description
                                SDisplay = "Slots"
                                CDispaly = "Category"
                                Place = "Bangalore Chinna Swamy Stadium"
                                text = "to"

                                draw.text((80, 110), EventName,
                                          (0, 0, 0), font=font)
                                draw.text((80, 190), start_Date,
                                          (0, 0, 0), font=font1)
                                draw.text((228, 190), text,
                                          (0, 0, 0), font=font1)
                                draw.text((265, 190), end_date,
                                          (0, 0, 0), font=font1)
                                draw.text((80, 230), Place,
                                          (0, 0, 0), font=font1)
                                draw.text((80, 153), Description,
                                          (0, 0, 0), font=font1)
                                draw.text((80, 280), SDisplay,
                                          (0, 0, 0), font=font1)
                                draw.text((240, 280), CDispaly,
                                          (0, 0, 0), font=font1)
                                draw.text((80, 320), SlotName,
                                          (0, 0, 0), font=font1)
                                draw.text((245, 323), CategoryName,
                                          (0, 0, 0), font=font1)
                                # copied_image.show()
                                image_bytes = io.BytesIO()
                                copied_image.save(image_bytes, format='PNG')
                                image_bytes.seek(0)
                                image_data = image_bytes.getvalue()
                                filename = f" tickets_{id}_{t.ticket_number}.png"
                                t.ticket_QR.save(
                                    filename, ContentFile(image_data))
                                t.ticket_status = 10
                                t.save()
                                # copied_image.show()
                                # plt.imshow(copied_image)
                                # plt.show()

                            else:
                                print('image not generating')

                        # else:
                        #     print("Request failed with status code:",
                        #           response.status_code)
                    else:
                        print('status is already 1')
    return render(request, 'K_Ticket/generateqr.html')


def updatecategory(request, id):
    updatecategory = event_ticket_category.objects.filter(
        client_id=request.user.id, id=id)
    if request.method == 'POST':
        slotid = ""
        for i in updatecategory:
            slotid = i.event_slots_id
            updatecategoryEdit = event_ticket_category.objects.get(id=i.id)
            updatecategoryEdit.Category_Name = request.POST.get(
                'recategoryname')
            updatecategoryEdit.Category_Description = request.POST.get(
                'recategorydesc')
            updatecategoryEdit.Category_Price = request.POST.get(
                'recategoryprice')
            if 'reCategoryTicketImage' in request.FILES and len(request.FILES['reCategoryTicketImage']) != 0:
                updatecategoryEdit.category_ticket_image = request.FILES['reCategoryTicketImage']
            else:
                updatecategoryEdit.category_ticket_image = i.category_ticket_image
            if 'reCategoryMessageHeaderImage' in request.FILES and len(request.FILES['reCategoryMessageHeaderImage']) != 0:
                updatecategoryEdit.Category_Message_Header_Image = request.FILES[
                    'reCategoryMessageHeaderImage']
            else:
                updatecategoryEdit.Category_Message_Header_Image = i.Category_Message_Header_Image
            updatecategoryEdit.Category_Message_Header_Text = request.POST.get(
                'reCategoryMessageHeaderText')
            updatecategoryEdit.Category_Message_Body_Text = request.POST.get(
                'reCategoryMessageBodyText')
            updatecategoryEdit.Category_Message_Footer_Text = request.POST.get(
                'reCategoryMessageFooterText')
            updatecategoryEdit.Number_Of_Ticket_Button_Name = request.POST.get(
                'reNumberOfTicketButtonName')
            updatecategoryEdit.save()
        return redirect('/Eventmaster/slotOFcategory/' + str(slotid) + '/')
    return render(request, 'K_Ticket/slotOFcategory.html', {'modifycategory': updatecategory})


def updatetickets(request, id):
    updatetickets = ticket_information.objects.filter(
        client_id=request.user.id, id=id)
    error_message = ""
    if request.method == 'POST':
        categoryid = ""
        for j in updatetickets:
            categoryid = j.event_ticket_category_id
            ticket_number = request.POST.get('reticketnumber')
            expiry_date = request.POST.get('redate')
            # Check if ticket with same number and category ID already exists
            existing_ticket = ticket_information.objects.filter(
                event_ticket_category_id=categoryid, ticket_number=ticket_number).exclude(id=j.id).first()

            if existing_ticket:
                error_message = f"Ticket with number '{ticket_number}' already exists in this category."
            else:
                updateticketEdit = ticket_information.objects.get(id=j.id)
                updateticketEdit.ticket_number = ticket_number
                if expiry_date:
                    updateticketEdit.expiry_date = expiry_date
                updateticketEdit.save()
        if error_message:
            messages.error(request, error_message)
        else:
            messages.success(request, "Tickets updated successfully")
        return redirect('/Eventmaster/modifycategory/' + str(categoryid) + '/')
    return render(request, 'K_Ticket/modifycategory.html', {'modifyticket': updatetickets, 'error_message': error_message})


# ------------------------------------------ Event ticket  ---------------------------------------------

# def ticketviewdisplaydata(request):
#     cursor = connection.cursor()
#     cursor.execute("call ticketviewjointables()")
#     results = cursor.fetchall()
#     return render(request, 'K_Ticket/EventTicket.html', {'results': results})


# ----------------------------------------- Event Dashboard -------------------------------------------

# def dashboard(request):
#     cursor = connection.cursor()
#     cursor.execute("call eventTotal()")
#     results1 = cursor.fetchall()
#     eventMonth = []
#     eventTotalno = []
#     for i in results1:
#         for j in range(len(i)):
#             if j == 0:
#                 eventMonth.append(i[j])
#             elif j == 1:
#                 eventTotalno.append(str(i[j]))
#     cursor = connection.cursor()
#     cursor.execute("call allTimeTotal()")
#     allTimeTotal = cursor.fetchall()
#     list1 = list(allTimeTotal)
#     for lst in list1:
#         total = lst[0]
#     cursor = connection.cursor()
#     cursor.execute("call ticketCount()")
#     results2 = cursor.fetchall()

#     cursor = connection.cursor()
#     cursor.execute("call totalTicketBymonth()")
#     results3 = cursor.fetchall()
#     return render(request, 'K_Ticket/EventDashboard.html', {'a': eventMonth, 'b': eventTotalno, 'total': total, 'results1': results1, 'results2': results2, 'results3': results3})


def eventinfo(request):
    print("222222")
    if request.method == "GET":
        eventdash = event_settings.objects.filter(client_id=request.user.id)
        print(eventdash)
        
        if len(eventdash) == 0:
            return render(request, 'K_Ticket/Eventinfo.html')
        else:
            return render(request, 'K_Ticket/Eventinfo1.html', {'eventdash': eventdash})


def eventCustomer(request):
    return render(request, 'K_Ticket/eventCustomer.html')



def billingTicket(request):
    billing = ticket_billing.objects.filter(client_id=request.user.id).order_by('-vailo_record_creation')
    billingRate = admin_permission.objects.filter(client_id = request.user.id)

    return render(request, 'K_Ticket/billingTicket.html', {'billing': billing, 'billingRate':billingRate })

def levelSeting_page(request):
    if request.method == "POST":
        level_settings = request.POST.get('level_settings')
        client_id = request.user.id

        try:
            event_setting = event_settings.objects.get(client_id=client_id)
        except event_settings.DoesNotExist:
            event_setting = event_settings(client_id=client_id)

        event_setting.level_settings = level_settings
        event_setting.save()

        return redirect('eventinfo')

    # Get the existing level_settings value for the current user
    client_id = request.user.id
    try:
        event_setting = event_settings.objects.get(client_id=client_id)
        selected_level_settings = event_setting.level_settings
    except event_settings.DoesNotExist:
        selected_level_settings = None

    context = {
        'selected_level_settings': selected_level_settings
    }

    return render(request, 'K_Ticket/levelSeting_page.html', context)

def viewDetail(request,id):
    viewDetail = ticket_billing_details.objects.filter(client_id=request.user.id,ticket_billing_id=id)

    return render(request, 'K_Ticket/viewDetail.html', {'viewDetail': viewDetail, 'id':id})

def generalinfo(request):
    

    if request.method == "POST":
        info_creation = event_settings()
        # info_creation.event_welcome = request.POST.get('txtwelcomename')
        # info_creation.event_list_selection = request.POST.get('txteventname')
        # info_creation.event_slot_selection = request.POST.get('txtslotname')
        # info_creation.customer_name_selection = request.POST.get('txtcustomer')
        if 'welcomeheaderimage' in request.FILES:
            info_creation.welcome_header_image = request.FILES['welcomeheaderimage']

        # Handle the booking header image if uploaded
        if 'bookingheaderimage' in request.FILES:
            info_creation.booking_header_image = request.FILES['bookingheaderimage']

        # Handle the cancel ticket header image if uploaded
        if 'cancelticketheaderimage' in request.FILES:
            info_creation.cancel_ticket_header_image = request.FILES['cancelticketheaderimage']
        
        if 'ticketconformationheaderimage' in request.FILES:
             info_creation.ticket_conformation_header_image = request.FILES['ticketconformationheaderimage']    

        if 'paymentfailureheaderimage' in request.FILES:
            info_creation.ticket_payment_failure_image = request.FILES['paymentfailureheaderimage'] 

        if 'notavailableheaderimage' in request.FILES:
            info_creation.tickets_not_availble_header_image = request.FILES['notavailableheaderimage']
        # info_creation.welcome_header_text = request.POST.get(
        #     'welcomeheadertext')
        info_creation.welcome_message_text = request.POST.get('welcomemessagetext')

        info_creation.welcome_message_footer = request.POST.get( 'welcomefootertext')
        # info_creation.welcome_header_type = request.POST.get('mySelect')
        # info_creation.booking_header_image = request.FILES['bookingheaderimage']
        info_creation.booking_header_text = request.POST.get(
            'bookingheadertext')
        info_creation.booking_message_text = request.POST.get(
            'bookingmessagetext')
        info_creation.booking_message_footer = request.POST.get(
            'bookingmessagefooter')
        # info_creation.booking_header_type = request.POST.get('booktype')
        info_creation.booking_button_name = request.POST.get(
            'bookingbuttonname')
        info_creation.booking_myticket_button_name = request.POST.get(
            'bookingmyticketname')
        info_creation.booking_cancel_ticket_button_name = request.POST.get(
            'bookingcancelticketname')
        info_creation.event_list_event_button_name = request.POST.get(
            'eventbuttonname')
        # info_creation.cancel_ticket_header_image = request.FILES['cancelticketheaderimage']
        info_creation.cancel_ticket_message_body = request.POST.get(
            'cancelmessagebody')
        
        info_creation.ticket_conformation_message_body = request.POST.get(
            'ticketconformationmessagebody')
        
        info_creation.ticket_failure_message_body = request.POST.get(
            'paymentfailuremessagebody')
        # info_creation.use_header_image = request.FILES['useheaderimage']
        # info_creation.use_message_text = request.POST.get('usemessagebody')
        # info_creation.use_button_name = request.POST.get('usebuttonname')
        info_creation.transfer_button_name = request.POST.get(
            'transferbuttonname')
        info_creation.tickets_not_available_message_body = request.POST.get(
            'notavailablemessagebody')
        

        if 'contactheaderimage' in request.FILES:
            info_creation.contact_header_image = request.FILES['contactheaderimage']
        # info_creation.welcome_header_text = request.POST.get(
        #     'welcomeheadertext')
        info_creation.contact_message_text = request.POST.get('contactmessagebody')

        info_creation.contact_button_name = request.POST.get('contactbuttonname')

        info_creation.ticketcount1_desc = request.POST.get(
            'ticketcount1_desc')
        info_creation.ticketcount2_desc = request.POST.get(
            'ticketcount2_desc')
        info_creation.ticketcount3_desc = request.POST.get(
            'ticketcount3_desc')
        info_creation.ticketcount4_desc = request.POST.get(
            'ticketcount4_desc')
        info_creation.ticketcount5_desc = request.POST.get(
            'ticketcount5_desc')
        info_creation.ticketcount6_desc = request.POST.get(
            'ticketcount6_desc')
        info_creation.ticketcount7_desc = request.POST.get('ticketcount7_desc')

        info_creation.ticketcount8_desc = request.POST.get('ticketcount8_desc')
       
        info_creation.ticketcount9_desc = request.POST.get('ticketcount9_desc')
        
        ticket_second_number = request.POST.get('ticketsecondnumber', '')
        try:
            info_creation.second_number = int(ticket_second_number)
        except ValueError:
            # Handle the case when the value cannot be converted to an integer
            # For example, set a default value or handle the error as needed.
            info_creation.second_number = 0
        
        info_creation.client_id = request.user.id
        info_creation.save()
        return redirect('eventmaster')


def home1(request):
    return redirect('eventmaster')


def hierarchicalV(request):
    return render(request, 'K_Ticket/hierarchical.html')


from django.contrib.auth.models import User

# def eventCampaign(request, id):
#     if request.user.is_superuser:
#         # User is authenticated through the User table
#         user = User.objects.filter(id=subclient_id).first()
#         eventcampaign = campaign_info.objects.filter(client_id=request.user.id)
#         custmerCampaign = History_campaign_customer.objects.filter(client_id=request.user.id)
#         infoCampaign = History_campaign_infor.objects.filter(client_id=request.user.id)
#         context = {
#             'eventcampaign': eventcampaign, 
#             'custmerCampaign': custmerCampaign,
#             'infoCampaign': infoCampaign, 
#         }
#     else:
#         # User is authenticated through the Subclient table
#         subclient_preferences = SubUserPreference.objects.filter(subclient_id=subclient_id).first()
#         context = {
#             'subclient_preferences': subclient_preferences,
#         }
        
#     return render(request, 'K_Ticket/eventcampaign.html', context)

def eventCampaign(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    eventcampaign = campaign_info.objects.filter(client_id=request.user.id)
    custmerCampaign = History_campaign_customer.objects.filter(client_id=request.user.id)
    infoCampaign = History_campaign_infor.objects.filter(client_id=request.user.id)
    
    context = {
        'subclient_preferences': subclient_preferences,
        'eventcampaign': eventcampaign, 
        'custmerCampaign': custmerCampaign,
        'infoCampaign': infoCampaign, 
    }

    return render(request, 'K_Ticket/eventcampaign.html', context)


def addCampaign(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    context ={
        'subclient_preferences': subclient_preferences
    }
    return render(request, 'K_Ticket/addCampaign.html', context)


def assignCampaign(request, id):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()


    subUpdateCamaign = campaign_info.objects.filter(
        client_id=request.user.id, id=id)
    assignCampaign = ticket_customer_master.objects.filter(
        client_id=request.user.id)
    campaignList = list(campaign_customer.objects.filter(
        client_id=request.user.id, campaign_info_id=id))
    print("campaignList", campaignList)
    selectedItems = {}  # Define an empty list for selected items
    context ={ 
        'assignCampaign': assignCampaign,
        'subUpdateCamaign': subUpdateCamaign,
        'selectedItems': selectedItems,
        'campaignList': campaignList,
        'subclient_preferences' : subclient_preferences,

    }
    return render(request, 'K_Ticket/assignCampaign.html', context )


def sendCampaign(request, id):
    print(id)

    campaign_data = campaign_info.objects.filter(
        client_id=request.user.id, id=id)
    customer_data = campaign_customer.objects.filter(
        client_id=request.user.id, campaign_info_id=id)
    print(campaign_data)
    print(customer_data)
    phonenumber = [
        customer.Customer_Whatsapp_Number for customer in customer_data]
    print(phonenumber)
    access_token = facebook_details.objects.filter(client_id=request.user.id)
    fb_token = ''
    for token_i in access_token:
        fb_token = fb_token + token_i.fb_access_token

    for send_i in campaign_data:
        url = "https://graph.facebook.com/v15.0/102085716156273/messages"

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phonenumber,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "header": {
                    "type": "image",
                    "image": {
                        "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/" + str(
                            send_i.Campaign_Header_Image)
                    }
                },
                "body": {
                    "text": send_i.Campaign_Message_Text
                },
                "footer": {
                    "text": send_i.Campaign_Footer_Text
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "F1",
                                "title": send_i.Campaign_First_Button_Name
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "F2",
                                "title": send_i.Campaign_Second_Button_Name
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "F3",
                                "title": send_i.Campaign_Third_Button_Name
                            }
                        }
                    ]
                }
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer EAAFENj48uKsBAApSbFWZAeffQF5cVuDAOZCzF5U0y73T7vYqzL5mOAUIqLbIjoQZB8jPMAhyjI8UMsLs8ucN9bxkqRtS1xTLMpsPUxe9zHzGSkLtsBeJBH91lBr88NlZAqdsnvcLfNZCCplWZAkWL38jLx2ZCdXbej3r9MuTwAYQcw0cZCFjpHHl6LicYbydRwiH5GZBVKbJSiAZDZD'
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            messages.success(request, "Campaign sent successfully!")

            transaction_count = len(phonenumber)
            ticket_billing_details.objects.create(
                    client_id=request.user.id,
                    transaction_type="Campaign Sent",
                    transaction_name=send_i.Campaign_Name,
                    transaction_count=transaction_count,

                )
        else:
            messages.error(request, "Failed to send the campaign.")

        print(response.text)

    for send_i in campaign_data:
        histroCampaignInfo = History_campaign_infor.objects.create(
            Campaign_Name=send_i.Campaign_Name,
            Campaign_Header_Image=send_i.Campaign_Header_Image,
            Campaign_Message_Text=send_i.Campaign_Message_Text,
            Campaign_Footer_Text=send_i.Campaign_Footer_Text,
            Campaign_First_Button_Name=send_i.Campaign_First_Button_Name,
            Campaign_Second_Button_Name=send_i.Campaign_Second_Button_Name,
            Campaign_Third_Button_Name=send_i.Campaign_Third_Button_Name,
            client_id=request.user.id,
            campaign_info_id=id
        )

        histroCampaignInfo.save()

    for a in customer_data:
        historyCustomer = History_campaign_customer.objects.create(
            Customer_First_Name=a.Customer_First_Name,
            Customer_Whatsapp_Number=a.Customer_Whatsapp_Number,
            Customer_City=a.Customer_City,
            campaign_info_id=id,
            campaign_customer_id=a.id,
            client_id=request.user.id,
            campaign_name=a.campaign_info.Campaign_Name
        )
        print(historyCustomer.campaign_info.Campaign_Name)
        historyCustomer.save()

    return redirect('eventCampaign')


    
def deleteCampaign(request,id):
    deletecampaign = campaign_info.objects.get(
        client_id=request.user.id, pk=id)
    deletecampaign.delete()
    return redirect('eventCampaign')



@transaction.atomic
def moveCampaignList(request, campaign_info_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_items = data.get('selected_items')
        print(selected_items)

        duplicate_entries = []  # List to store duplicate entry messages

        try:
            with transaction.atomic():
                for item in selected_items:
                    ticket_customer_master_id = item.get(
                        'ticket_customer_master_id')
                    if ticket_customer_master_id is None:
                        print("Ticket Customer Master ID is missing.")
                        continue

                    try:
                        ticket_customer = ticket_customer_master.objects.get(
                            id=ticket_customer_master_id)
                        print(ticket_customer)
                    except ObjectDoesNotExist:
                        print(
                            f"Ticket Customer Master with ID {ticket_customer_master_id} does not exist.")
                        continue

                    try:
                        campaign = campaign_customer.objects.get(
                            ticket_customer_master=ticket_customer,
                            client=request.user,
                            campaign_info_id=campaign_info_id
                        )
                        duplicate_entries.append(
                            f"Duplicate entry: Campaign with the combination of ticket_customer_master, client, and campaign_info_id already exists for {ticket_customer}.")
                    except campaign_customer.DoesNotExist:
                        try:
                            campaign = campaign_customer.objects.create(
                                ticket_customer_master=ticket_customer,
                                client=request.user,
                                campaign_info_id=campaign_info_id,
                                Customer_First_Name=item['name'],
                                Customer_Whatsapp_Number=item['whatsappNumber'],
                                Customer_City=item['city']
                            )
                            print(f"Campaign created successfully: {campaign}")
                        except IntegrityError:
                            print(
                                "Duplicate entry: The combination of ticket_customer_master, client, and campaign_info_id must be unique.")

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})

        # Check if there are any duplicate entries
        if duplicate_entries:
            return JsonResponse({'success': False, 'duplicate_entries': duplicate_entries})
        else:
            return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def deleteCampaignList(request, id):
    campaign_customer_obj = campaign_customer.objects.get(
        client_id=request.user.id, pk=id)
    campaign_info_id = campaign_customer_obj.campaign_info_id
    campaign_customer_obj.delete()
    return redirect('assignCampaign', id=campaign_info_id)


def addCampaignSubmit(request):
    if request.method == 'POST':
        submitAddCampaign = campaign_info()
        submitAddCampaign.Campaign_Name = request.POST.get('campaignName')
        submitAddCampaign.Campaign_Description = request.POST.get(
            'campaignDescription')
        if 'campaignHeaderImg' in request.FILES:
            submitAddCampaign.Campaign_Header_Image = request.FILES['campaignHeaderImg']
        submitAddCampaign.Campaign_Message_Text = request.POST.get(
            'campaignMessageText')
        submitAddCampaign.Campaign_Footer_Text = request.POST.get(
            'campaignFooterText')
        submitAddCampaign.Campaign_First_Button_Name = request.POST.get(
            'campaignButton1')
        submitAddCampaign.Campaign_Second_Button_Name = request.POST.get(
            'campaignButton2')
        submitAddCampaign.Campaign_Third_Button_Name = request.POST.get(
            'campaignButton3')
        if 'campaignStatus' in request.POST:
             submitAddCampaign.Campaign_Status = request.POST.get('campaignStatus')
        submitAddCampaign.client_id = request.user.id
        submitAddCampaign.save()
        return redirect("eventCampaign")
    return render(request, 'K_Ticket/addcampaign.html')


def updateCamaign(request, id):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    updateCampaign = campaign_info.objects.filter(
        client_id=request.user.id, id=id)
    
    context ={
        "updateCampaign": updateCampaign,
        'subclient_preferences': subclient_preferences
    }
    return render(request, 'K_Ticket/editCampaign.html', context)


def subUpdateCamaign(request, id):
    subUpdateCamaign = campaign_info.objects.filter(
        client_id=request.user.id, id=id)
    if request.method == 'POST':
        for i in subUpdateCamaign:
            # Update the campaign fields based on the form data
            editinfo = campaign_info.objects.get(id=i.id)
            if request.POST.get('reCampaignName'):
                editinfo.Campaign_Name = request.POST.get('reCampaignName')
            if request.POST.get('reCampaignDescription'):
                editinfo.Campaign_Description = request.POST.get(
                    'reCampaignDescription')
            if request.POST.get('reCampaignMessageText'):
                editinfo.Campaign_Message_Text = request.POST.get(
                    'reCampaignMessageText')
            if request.POST.get('reCampaignFooterText'):
                editinfo.Campaign_Footer_Text = request.POST.get(
                    'reCampaignFooterText')
            if request.POST.get('reCampaignButton1'):
                editinfo.Campaign_First_Button_Name = request.POST.get(
                    'reCampaignButton1')
            if request.POST.get('reCampaignButton2'):
                editinfo.Campaign_Second_Button_Name = request.POST.get(
                    'reCampaignButton2')
            if request.POST.get('reCampaignButton3'):
                editinfo.Campaign_Third_Button_Name = request.POST.get(
                    'reCampaignButton3')

            campaign_status = request.POST.get('reCampaignStatus')
            if campaign_status is not None and campaign_status != '':
                editinfo.Campaign_Status = int(campaign_status)

            # Update the campaign header image if provided
            if 'reCampaignHeaderImg' in request.FILES and len(request.FILES['reCampaignHeaderImg']) != 0:
                editinfo.Campaign_Header_Image = request.FILES['reCampaignHeaderImg']

            editinfo.save()

        return redirect('eventCampaign')

    # When the request method is not POST, render the form with the existing campaign data
    return render(request, 'K_Ticket/editCampaign.html', {'updateCampaign': subUpdateCamaign})

    # return render(request, 'K_Ticket/addCampaign.html')
    # eventmaster = event_master.objects.filter(client_id=request.user.id)
    # if len(eventmaster) == 1:
    #     for s in eventmaster:
    #         pass
    # return render(request, 'K_Ticket/EventMaster.html', {'eventmaster': eventmaster})


def editsettingsinfo(request):
    editsettings = event_settings.objects.filter(client_id=request.user.id)
    for info_creations in editsettings:
        if request.method == "POST":
            # info_creation = event_settings()

            if 'rewelcomeImage' in request.FILES and len(request.FILES['rewelcomeImage']) != 0:
                info_creations.welcome_header_image = request.FILES['rewelcomeImage']
            else:
                info_creations.welcome_header_image = info_creations.welcome_header_image
            # info_creation.welcome_header_text = request.POST.get('rewelcomemessagetext')
            info_creations.welcome_message_text = request.POST.get(
                'rewelcomemessagetext')
            info_creations.welcome_message_footer = request.POST.get(
                'rewelcomefootertext')
            # info_creation.welcome_header_type = request.POST.get('mySelect')
            if 'rewelcomebookImage' in request.FILES and len(request.FILES['rewelcomebookImage']) != 0:
                info_creations.booking_header_image = request.FILES['rewelcomebookImage']
            else:
                info_creations.booking_header_image = info_creations.booking_header_image
            info_creations.booking_header_text = request.POST.get(
                'rebookingheadertext')
            info_creations.booking_message_text = request.POST.get(
                'rebookingmessagetext')
            info_creations.booking_message_footer = request.POST.get(
                'rebookingmessagefooter')
            # info_creation.booking_header_type = request.POST.get('booktype')
            info_creations.booking_button_name = request.POST.get(
                'rebookingbuttonname')
            info_creations.booking_myticket_button_name = request.POST.get(
                'rebookingmyticketname')
            info_creations.booking_cancel_ticket_button_name = request.POST.get(
                'rebookingcancelticketname')
            info_creations.event_list_event_button_name = request.POST.get(
                'reeventbuttonname')
            if 'reCancelImage' in request.FILES and len(request.FILES['reCancelImage']) != 0:
                info_creations.cancel_ticket_header_image = request.FILES['reCancelImage']
            else:
                info_creations.cancel_ticket_header_image = info_creations.cancel_ticket_header_image
            info_creations.cancel_ticket_message_body = request.POST.get(
                'recancelmessagebody')
            if 'reConformationImage' in request.FILES and len(request.FILES['reConformationImage']) != 0:
                info_creations.ticket_conformation_header_image = request.FILES[
                    'reConformationImage']
            else:
                info_creations.ticket_conformation_header_image = info_creations.ticket_conformation_header_image
            info_creations.ticket_conformation_message_body = request.POST.get(
                'reticketconformationmessagebody')
            if 'refailureImage' in request.FILES and len(request.FILES['refailureImage']) != 0:
                info_creations.ticket_payment_failure_image = request.FILES['refailureImage']
            else:
                info_creations.ticket_payment_failure_image = info_creations.ticket_payment_failure_image
            info_creations.ticket_failure_message_body = request.POST.get(
                'repaymentfailuremessagebody')
            # if 'reUseImage' in request.FILES and len(request.FILES['reUseImage']) != 0:
            #     info_creations.use_header_image = request.FILES['reUseImage']
            # else:
            #     info_creations.use_header_image = info_creations.use_header_image
            # info_creations.use_message_text = request.POST.get(
            #     'reusemessagebody')
            # info_creations.use_button_name = request.POST.get(
            #     'reusebuttonname')
            info_creations.transfer_button_name = request.POST.get(
                'retransferbuttonname')
            if 'renotavailableImage' in request.FILES and len(request.FILES['renotavailableImage']) != 0:
                info_creations.tickets_not_availble_header_image = request.FILES[
                    'renotavailableImage']
            else:
                info_creations.tickets_not_availble_header_image = info_creations.tickets_not_availble_header_image
            info_creations.tickets_not_available_message_body = request.POST.get(
                'renotavailablemessagebody')
            


            if 'reContactImage' in request.FILES and len(request.FILES['reContactImage']) != 0:
                info_creations.contact_header_image = request.FILES[
                    'reContactImage']
            else:
                info_creations.contact_header_image = info_creations.contact_header_image

            info_creations.contact_message_text = request.POST.get(
                'recontactmessagebody')
            info_creations.contact_button_name = request.POST.get(
               'recontactbuttonname')

            info_creations.ticketcount1_desc = request.POST.get(
               'reticketcount1_desc')
            info_creations.ticketcount2_desc = request.POST.get(
                    'reticketcount2_desc')
            info_creations.ticketcount3_desc = request.POST.get(
                 'reticketcount3_desc')
            info_creations.ticketcount4_desc = request.POST.get(
                   'reticketcount4_desc')
            info_creations.ticketcount5_desc = request.POST.get(
                 'reticketcount5_desc')
            info_creations.ticketcount6_desc = request.POST.get(
                    'reticketcount6_desc')
            info_creations.ticketcount7_desc = request.POST.get(
                 'reticketcount7_desc')
            info_creations.ticketcount8_desc = request.POST.get(
                 'reticketcount8_desc')
            info_creations.ticketcount9_desc = request.POST.get(
                 'reticketcount9_desc')
            info_creations.second_number = int(
                request.POST.get('reticketsecondnumber'))
            info_creations.client_id = request.user.id
            info_creations.save()
            print("ee")
            return redirect('eventmaster')


def event_treedata(request):
    data = []
    status_param = request.GET.get('status')

    if status_param == 'inactive':
        events = event_master.objects.filter(
            client_id=request.user.id, status=2)  # Filter only inactive records
    elif status_param == 'all':
        events = event_master.objects.filter(
            client_id=request.user.id)  # Return all records
    else:
        # Filter only active records by default
        events = event_master.objects.filter(
            client_id=request.user.id, status=1)

    for event in events:
        event_data = {
            'event': event,
            'text': f"{event.Event_Name} - ",
            'texts': f"({event.Event_Description}) - start:{event.Start_Date} - end:{event.End_Date}",
            'children': [],
            'url': reverse('eventOFslot', kwargs={'id': event.id}),
            'uss': reverse('submitslot', kwargs={'id': event.id}),

        }
        print(event.id, "sadfd")
        slots = event_slots.objects.filter(event_master_id=event.id)
        for slot in slots:
            slot_data = {
                'slot': slot,
                'text1': f"{slot.Slot_Name} - ",
                'texts': f"({slot.Slot_Description})",
                'children': [],
                'url': reverse('slotOFcategory', kwargs={'id': slot.id}),
                'uss': reverse('addcateINslot', kwargs={'slotID': slot.id})
            }
            print(slot.status)
            print(slot_data)
            tickets = event_ticket_category.objects.filter(
                event_slots_id=slot.id)
            for ticket in tickets:
                ticket_data = {
                    'ticket': ticket,
                    'text2': f"{ticket.Category_Name} - ",
                    'texts': f"({ticket.Category_Description}) - RS:{ticket.Category_Price}",
                    'children': [],
                    'url': reverse('modifycategory', kwargs={'id': ticket.id})
                }
                print(ticket.status)
                print(ticket_data)
                slot_data['children'].append(ticket_data)
            event_data['children'].append(slot_data)
        data.append(event_data)
    return render(request, 'K_ticket/hierarchical.html', {'data': data})


# import sys
# print(sys.path)
# import plotly
# import pandas as pd
# print(plotly.__version__)
# print(px.__version__)
# import sys
# print(sys.path)

import pandas as pd
import plotly.express as px

def sunburst_chart(request):
    events = event_master.objects.filter(client_id=request.user.id)
    slots = event_slots.objects.filter(client_id=request.user.id)
    categories = event_ticket_category.objects.filter(client_id=request.user.id)

    data = []

    for event in events:
        eventslots = slots.filter(event_master_id=event.id)

        if not eventslots:
            data.append({'path_0': event.Event_Name})
        else:
            for slot in eventslots:
                categories_slot = categories.filter(event_slots_id=slot.id)

                if not categories_slot:
                    data.append({'path_0': event.Event_Name, 'path_1': slot.Slot_Name})
                else:
                    for category in categories_slot:
                        data.append({'path_0': event.Event_Name, 'path_1': slot.Slot_Name, 'path_2': category.Category_Name})

    try:
        df = pd.DataFrame(data)

        if df['path_0'].duplicated().any():
            print("Please wait, event names are duplicated.")

        fig = px.sunburst(df, path=['path_0', 'path_1', 'path_2'])
    except ValueError as e:
        print("An error occurred:", str(e))
        return HttpResponse("Please wait, an error occurred...")

    plot_html = fig.to_html(full_html=True)
    context = {'plot_html': plot_html}
    return render(request, 'K_ticket/sunburstChat.html', context)



# // ticket 
# def ticketviewdisplaydata(request):
#     subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
#     subclient = Subclient.objects.filter(id=subclient_id).first()
#     subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()


#     events = event_master.objects.filter(client_id =request.user.id)
#     data = []
#     for event in events:
#         event_data = {
#             'text': {
#                 'name': event.Event_Name,
#                 'start_date': event.Start_Date,
#                 'end_date': event.End_Date
#             },
#             'id': event.id,
#         }
#         data.append(event_data)
#     context = {
#         'data': data,
#         'subclient_preferences':subclient_preferences,
#                }
#     return render(request, 'K_ticket/EventTicket.html', context)


# def fetch_slots(request):
#     event_id = request.GET.get('event_id')
#     slots = event_slots.objects.filter(event_master_id=event_id).distinct()

#     slot_data = []
#     for slot in slots:
#         slot_data.append({
#             'id': slot.id,
#             'text1': f"{slot.Slot_Name}"
#         })

#     return JsonResponse(slot_data, safe=False)


# def fetch_categories(request):
#     slot_id = request.GET.get('slot_id')
#     categories = event_ticket_category.objects.filter(event_slots_id=slot_id).distinct()

#     category_data = []
#     for category in categories:
#         category_data.append({
#             'id': category.id,
#             'text2': f"{category.Category_Name}  - {category.Category_Price}"
#         })

#     return JsonResponse(category_data, safe=False)

# def fetch_ticket(request):
#     event_id = request.GET.get('event_id')
#     slot_id = request.GET.get('slot_id')
#     ticket_id = request.GET.get('ticket_id')

#     ticket_filter = {}

#     if event_id is not None:
#         ticket_filter['event_master_id'] = event_id
#     if slot_id is not None:
#         ticket_filter['event_slots_id'] = slot_id
#     if ticket_id is not None:
#         ticket_filter['event_ticket_category_id'] = ticket_id

#     tickets = ticket_information.objects.filter(**ticket_filter)

#     ss_data = []
#     for ticket in tickets:
#         event_name = ticket.event_master.Event_Name
#         start_date = ticket.event_master.Start_Date
#         end_date = ticket.event_master.End_Date

#         ss_data.append({
#             'id': ticket.id,
#             'text': {
#                 'name': event_name,
#                 'start_date': start_date,
#                 'end_date': end_date,
#                 'ticket_number': ticket.ticket_number,
#                 'expiry_date': ticket.expiry_date,
#                 'ticket_status': ticket.ticket_status,
#                 'event_master_id': ticket.event_master_id,
#                 'event_slots_id': ticket.event_slots_id,
#                 'event_ticket_category_id': ticket.event_ticket_category_id
#             },
#             'text3': f"T.No:{ticket.ticket_number} ‎ ‎  Ex-Date: {ticket.expiry_date} ‎ ‎  status: {ticket.ticket_status}",
#             'text4': f"T.No:{ticket.ticket_number} ‎ ‎  Ex-Date: {ticket.expiry_date} ‎ ‎  status: {ticket.ticket_status}‎ ‎  EventId: {ticket.event_master_id} ‎ ‎ SlotId:{ticket.event_slots_id} ‎ ‎ CategoryId:{ticket.event_ticket_category_id } ",
#             'text5': f"T.No:{ticket.ticket_number} ‎ ‎  Ex-Date: {ticket.expiry_date} ‎ ‎  status: {ticket.ticket_status} ‎ ‎ SlotId:{ticket.event_slots_id}‎ ‎  CategoryId:{ticket.event_ticket_category_id} "
#         })

#     return JsonResponse(ss_data, safe=False)

from django.http import FileResponse
from django.conf import settings
import os

def download_excel(request):
    # Assuming the Excel file is named "your_excel_sheet.xlsx"
    file_path = os.path.join(settings.STATIC_ROOT, 'sample_Ticket.xlsx')
    return FileResponse(open(file_path, 'rb'), as_attachment=True)


def ticketviewdisplaydata(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    # print('subclient_id',subclient_id) 
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    events = event_master.objects.filter(client_id =request.user.id)
    data = []
    for event in events:
        event_data = {
            'text': {
                'name': event.Event_Name,
                'start_date': event.Start_Date,
                'end_date': event.End_Date,
                'subclient_preferences' : subclient_preferences,
            },
            'id': event.id,
        }
        data.append(event_data)
    context = {'data': data, 'subclient_preferences':subclient_preferences}
    return render(request, 'K_ticket/EventTicket.html', context)


def fetch_slots(request):
    event_id = request.GET.get('event_id')
    slots = event_slots.objects.filter(event_master_id=event_id).distinct()

    slot_data = []
    for slot in slots:
        slot_data.append({
            'id': slot.id,
            'text1': f"{slot.Slot_Name}"
        })

    return JsonResponse(slot_data, safe=False)


def fetch_categories(request):
    slot_id = request.GET.get('slot_id')
    categories = event_ticket_category.objects.filter(event_slots_id=slot_id).distinct()

    category_data = []
    for category in categories:
        category_data.append({
            'id': category.id,
            'text2': f"{category.Category_Name}  - {category.Category_Price}"
        })

    return JsonResponse(category_data, safe=False)

def fetch_ticket(request):

    event_id = request.GET.get('event_id')
    slot_id = request.GET.get('slot_id')
    ticket_id = request.GET.get('ticket_id')

    ticket_filter = {}

    if event_id is not None:
        ticket_filter['event_master_id'] = event_id
    if slot_id is not None:
        ticket_filter['event_slots_id'] = slot_id
    if ticket_id is not None:
        ticket_filter['event_ticket_category_id'] = ticket_id

    tickets = ticket_information.objects.filter(**ticket_filter)

    ss_data = []
    for ticket in tickets:
        event_name = ticket.event_master.Event_Name
        start_date = ticket.event_master.Start_Date
        end_date = ticket.event_master.End_Date

        ss_data.append({
            'id': ticket.id,
            'text': {
                'name': event_name,
                'start_date': start_date,
                'end_date': end_date,
                'ticket_number': ticket.ticket_number,
                'expiry_date': ticket.expiry_date,
                'ticket_status': ticket.ticket_status,
                'event_master_id': ticket.event_master_id,
                'event_slots_id': ticket.event_slots_id,
                'event_ticket_category_id': ticket.event_ticket_category_id
            },
            'text3': f"T.No:{ticket.ticket_number}    Ex-Date: {ticket.expiry_date}    status: {ticket.ticket_status}",
            'text4': f"T.No:{ticket.ticket_number}    Ex-Date: {ticket.expiry_date}    status: {ticket.ticket_status}   EventId: {ticket.event_master_id}   SlotId:{ticket.event_slots_id}   CategoryId:{ticket.event_ticket_category_id } ",
            'text5': f"T.No:{ticket.ticket_number}    Ex-Date: {ticket.expiry_date}    status: {ticket.ticket_status}   SlotId:{ticket.event_slots_id}   CategoryId:{ticket.event_ticket_category_id} "
        })

    return JsonResponse(ss_data, safe=False)


def update_ticket_status(request):
    print('jvdv')
    if request.method == "POST":
        data = json.loads(request.body)
        ticket_id = data.get("ticket_id")  # Change "id" to "ticket_id"
        new_status = data.get("new_status")
        try:
            ticket = ticket_information.objects.get(id=ticket_id)
            ticket.ticket_status = new_status
            ticket.save()
            return JsonResponse({"success": True})
        except ticket_information.DoesNotExist:
            return JsonResponse({"success": False, "error": "Ticket not found"})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})

def delete_ticket(request):
    print('uycuvil')
    if request.method == "DELETE":
        data = json.loads(request.body)
        ticket_id = data.get("ticket_id")
        try:
            ticket = ticket_information.objects.get(id=ticket_id)
            ticket.delete()
            print('jijiji')
            return JsonResponse({"success": True})
        except ticket_information.DoesNotExist:
            print("jingalaka")
            return JsonResponse({"success": False, "error": "Ticket not found"})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})
    


def ticket_dashboard(request):
    ticket_data = ticket_information.objects.values('event_master_id', 'event_slots_id',
                                                    'event_ticket_category_id', 'ticket_status').annotate(
        ticket_count=Count('id'))

    ticket_df = pd.DataFrame.from_records(ticket_data)
    fig = go.Figure()
    legend_added = {'Sold': False, 'Balance': False, 'Used': False}

    for _, group_df in ticket_df.groupby(['event_master_id', 'event_slots_id', 'event_ticket_category_id']):
        event_master_name = event_master.objects.get(id=group_df['event_master_id'].iloc[0]).Event_Name
        event_slot_name = event_slots.objects.get(id=group_df['event_slots_id'].iloc[0]).Slot_Name
        event_ticket_category_name = event_ticket_category.objects.get(id=group_df['event_ticket_category_id'].iloc[0]).Category_Name

        label = f"{event_master_name} - {event_slot_name} - {event_ticket_category_name}"

        if any(group_df['ticket_status'].isin([0, 10])):
            count_balance = group_df[group_df['ticket_status'].isin([0, 10])]['ticket_count'].sum()
            fig.add_trace(go.Bar(
                x=[label],
                y=[count_balance],
                name='Balance',
                text=[count_balance],
                textposition='inside',
                marker_color='blue',
                showlegend=not legend_added['Balance']
            ))
            legend_added['Balance'] = True




        if any(group_df['ticket_status'].isin([20, 30, 40])):
            count_sold = group_df[group_df['ticket_status'].isin([20, 30, 40])]['ticket_count'].sum()
            fig.add_trace(go.Bar(
                x=[label],
                y=[count_sold],
                name='Sold',
                text=[count_sold],
                textposition='inside',
                marker_color='green',
                showlegend=not legend_added['Sold']
            ))
            legend_added['Sold'] = True


        if any(group_df['ticket_status'].isin([80, 90])):
            count_used = group_df[group_df['ticket_status'].isin([80, 90])]['ticket_count'].sum()
            fig.add_trace(go.Bar(
                x=[label],
                y=[count_used],
                name='Others',
                text=[count_used],
                textposition='inside',
                marker_color='red',
                showlegend=not legend_added['Used']
            ))
            legend_added['Used'] = True

    fig.update_layout(
        barmode='stack',
        title='Ticket Count',
        xaxis_title='Tickets',
        yaxis_title='Ticket Count',
        yaxis=dict(showticklabels=False),
        dragmode=False,
    )

    ticket_html = fig.to_html(full_html=False, include_plotlyjs='cdn', config={'displayModeBar': False})
    return render(request, 'K_Ticket/ticketSummery.html', {'ticket_html': ticket_html})
    