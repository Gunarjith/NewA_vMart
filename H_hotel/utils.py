from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from vailodb_h.models import Hotel_settings, Hotel_services,Food, Nearby_place, Hotel_facilities, Hotel_rooms,Selfhelp, Information, Hotel_marketplace, Hotel_marketplace_settings ,Hotel_rooms_type, Room_list, Food_Category,Food_catalogue, Food_catalogue_items, Hotel_services_settings,Food_order_header, Food_order_details, Service_order, Guest_info,Hotel_Room_Guest_info, Checkout_questions,\
Checkout_response_header, Checkout_responses, Complaint_settings, Complaint_info

import matplotlib.pyplot as plt
import base64
from io import BytesIO
import calendar
from django.db.models import F

# For Monthly Ratings:

def get_monthly_ratings(hotel_name=None, year=None):
    # Create a base queryset
    queryset = Checkout_responses.objects.all()

    # Filter by hotel name if provided
    if hotel_name:
        queryset = queryset.filter(Checkout_response_header__Hotel_details__hotel_name=hotel_name)
        # print(queryset)

    # Filter by year if provided
    if year:
        queryset = queryset.filter(vailo_record_creation__year=year)
        # print(queryset)

    # Annotate and aggregate ratings data
    rating_data = queryset.annotate(
        month=TruncMonth('vailo_record_creation')
    ).values('month').annotate(
        rating_1=Count('pk', filter=Q(Checkout_response=1)),
        rating_2=Count('pk', filter=Q(Checkout_response=2)),
        rating_3=Count('pk', filter=Q(Checkout_response=3)),
        rating_4=Count('pk', filter=Q(Checkout_response=4)),
        rating_5=Count('pk', filter=Q(Checkout_response=5)),
    ).order_by('month')
    # print(rating_data)
    return list(rating_data)

    
# For Plotting Monthly ratings Graph:    
def plot_monthly_ratings_base64(data):
    all_month_names = [calendar.month_abbr[i] for i in range(1, 13)]

    # Initialize ratings for all months to 0
    ratings_dict = {f'rating_{i}': [0] * 12 for i in range(1, 6)}

    # Update ratings with actual data
    for item in data:
        month_index = item['month'].month - 1  # month index starts from 0
        for i in range(1, 6):
            ratings_dict[f'rating_{i}'][month_index] = item.get(f'rating_{i}', 0)

    plt.figure(figsize=(8, 6))

    bottom = [0] * 12
    for i in range(5):
        plt.bar(range(12), ratings_dict[f'rating_{i+1}'], bottom=bottom, label=f'Rating {i+1}')
        bottom = [sum(x) for x in zip(bottom, ratings_dict[f'rating_{i+1}'])]

    plt.xlabel('Months')
    plt.ylabel('Number of Customers')
    plt.title('Monthly Customer Ratings')
    plt.xticks(range(12), all_month_names, rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.subplots_adjust(right=0.75)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches="tight")
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph

# Monthly ratings Percentage of customers:
def plot_monthly_ratings_cusper(data):
    all_month_names = [calendar.month_abbr[i] for i in range(1, 13)]

    # Initialize ratings for all months to 0
    ratings_dict = {f'rating_{i}': [0] * 12 for i in range(1, 6)}

    # Count total customers for each month
    total_customers = [0] * 12

    # Update ratings with actual data and count total customers for each month
    for item in data:
        month_index = item['month'].month - 1  # month index starts from 0
        for i in range(1, 6):
            rating = item.get(f'rating_{i}', 0)
            ratings_dict[f'rating_{i}'][month_index] += rating
            total_customers[month_index] += rating

    plt.figure(figsize=(8, 6))

    bottom = [0] * 12
    for i in range(5):
        # Calculate percentage for each rating in each month
        percentages = [rating / total_customers[j] * 100 if total_customers[j] != 0 else 0 for j, rating in enumerate(ratings_dict[f'rating_{i+1}'])]
        plt.bar(range(12), percentages, bottom=bottom, label=f'Rating {i+1}')
        bottom = [sum(x) for x in zip(bottom, percentages)]
        # print(percentages)

    plt.xlabel('Months')
    plt.ylabel('Percentage of Customers')
    plt.title('Monthly Customer Ratings')
    plt.xticks(range(12), all_month_names, rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.subplots_adjust(right=0.75)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches="tight")
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph

# For Monthly Complaints:

def get_monthly_complaints(year=None, hotel_name=None):
    # Create a base queryset
    queryset = Complaint_info.objects.all()

    # Filter by year if provided
    if year:
        queryset = queryset.filter(vailo_record_creation__year=year)

    # Filter by hotel name if provided
    if hotel_name:
        queryset = queryset.filter(Hotel_details__hotel_name=hotel_name)

    # Annotate and aggregate complaints data
    complaint_data = queryset.annotate(
        month=TruncMonth('vailo_record_creation'),
        hotel_name=F('Hotel_details__hotel_name')  # Include hotel_name from Hotel_details
    ).values('month', 'hotel_name', 'Complaint_category__Complaint_category').annotate(
        total_complaints=Count('pk')
    ).order_by('month', 'hotel_name', 'Complaint_category__Complaint_category')
    # print(complaint_data)
    return list(complaint_data)


# For Plotting Monthly Complaints graph:
def plot_monthly_complaints(complaint_data):
    all_month_names = [calendar.month_abbr[i] for i in range(1, 13)]

    # Initialize complaints count for all months to 0 for each category
    complaints_dict = {}
    categories = set(item['Complaint_category__Complaint_category'] for item in complaint_data)
    
    # Define decent colors
    decent_colors = ['SteelBlue', 'Maroon', 'Gold', 'SlateGray',
                     'Lavender', 'Coral', 'SkyBlue', 'SandyBrown', 'MintGreen',
                     'Salmon', 'DarkCyan', 'Teal', 'Indigo', 'Sienna']
    
    # Assign decent colors to categories
    category_colors = dict(zip(categories, decent_colors))

    for category in categories:
        complaints_dict[category] = [0] * 12

    # Update complaints count with actual data
    for item in complaint_data:
        month_index = item['month'].month - 1  # month index starts from 0
        category = item['Complaint_category__Complaint_category']
        complaints_dict[category][month_index] = item['total_complaints']

    plt.figure(figsize=(8, 6))

    bottom = [0] * 12
    for category in categories:
        plt.bar(range(12), complaints_dict[category], bottom=bottom, label=category, color=category_colors[category])
        bottom = [sum(x) for x in zip(bottom, complaints_dict[category])]

    plt.xlabel('Months')
    plt.ylabel('Number of Complaints')
    plt.title('Monthly Complaints by Category')
    plt.xticks(range(12), all_month_names, rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.subplots_adjust(right=0.75)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches="tight")
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph

# For Monthly Percentage of Complaints:
def plot_monthly_complaint_percentage(data):
    all_month_names = [calendar.month_abbr[i] for i in range(1, 13)]

    # Initialize complaints count for all months to 0 for each category
    complaints_dict = {}
    categories = set(item['Complaint_category__Complaint_category'] for item in data)
    
    # Define decent colors
    decent_colors = ['SteelBlue', 'Salmon', 'Teal', 'SlateGray',
                     'Lavender', 'Coral', 'SkyBlue', 'SandyBrown', 'MintGreen',
                     'Maroon', 'DarkCyan', 'Indigo', 'Gold', 'Sienna']
    
    # Assign decent colors to categories
    category_colors = dict(zip(categories, decent_colors))

    for category in categories:
        complaints_dict[category] = [0] * 12

    # Update complaints count with actual data
    for item in data:
        month_index = item['month'].month - 1  # month index starts from 0
        category = item['Complaint_category__Complaint_category']
        complaints_dict[category][month_index] = item['total_complaints']

    # Calculate total complaints for each month
    total_complaints_per_month = [sum(complaints_dict[category][i] for category in categories) for i in range(12)]

    plt.figure(figsize=(8, 6))

    bottom = [0] * 12
    for category in categories:
        percentages = [complaints_dict[category][i] / total_complaints_per_month[i] * 100 if total_complaints_per_month[i] != 0 else 0 for i in range(12)]
        plt.bar(range(12), percentages, bottom=bottom, label=category, color=category_colors[category])
        bottom = [sum(x) for x in zip(bottom, percentages)]

    plt.xlabel('Months')
    plt.ylabel('Percentage of Complaints')
    plt.title('Percentage of Monthly Complaints by Category')
    plt.xticks(range(12), all_month_names, rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.subplots_adjust(right=0.75)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches="tight")
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph

