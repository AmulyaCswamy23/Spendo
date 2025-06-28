from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense
import re

# Show the combined login/signup page
def index_view(request):
    return render(request, 'tracker/index.html')

# Login handler (POST from sign-in form)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect("index")
    else:
        return redirect("index")

# Signup handler (POST from sign-up form)
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("index")

        user = User.objects.create_user(username=username, password=password)
        auth_login(request, user)
        return redirect("dashboard")
    else:
        return redirect("index")

# Dashboard view: enter expense and view all
@login_required
def dashboard_view(request):
    if request.method == "POST" and request.POST.get("add_expense_btn")=="1":
        voice_text = request.POST.get("voice_text", "")
        amount_match = re.search(r'\d+', voice_text)
        category_match = re.search(r'on (\w+)', voice_text)

        if amount_match and category_match:
            amount = float(amount_match.group())
            category = category_match.group(1)

            Expense.objects.create(
                user=request.user,
                amount=amount,
                category=category,
                description=voice_text
            )
            messages.success(request, "Expense added successfully!")
        else:
            messages.error(request, "Could not understand the expense format. Try: 'Spent 500 on food'")
        return redirect("dashboard")
    expenses = Expense.objects.filter(user=request.user).order_by("-date")
    return render(request, 'tracker/dashboard.html', {"expenses": expenses})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense

def logout_view(request):
    logout(request)
    return redirect('index')

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Expense

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Remove this line if not using token auth
def add_expense_api(request):
    text = request.data.get("voice_text", "")
    
    try:
        # Basic NLP: Extract amount and category
        parts = text.lower().replace("rupees", "").split("on")
        amount_part = parts[0].replace("spent", "").strip()
        category_part = parts[1].strip()

        amount = int(''.join(filter(str.isdigit, amount_part)))
        category = category_part.capitalize()

        Expense.objects.create(
            user=request.user,
            amount=amount,
            category=category,
            description=text
        )

        return Response({"success": True, "msg": f"Added ₹{amount} to {category}"})
    except Exception as e:
        return Response({"success": False, "error": "Could not parse voice input"})

from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Sum
from datetime import datetime
from .models import Expense
@login_required
def export_monthly_spending(request):
    # Filter: current user's expenses from this month
    now = datetime.now()
    expenses = Expense.objects.filter(
        user=request.user,
        date__month=now.month,
        date__year=now.year
    )

    # Group by category
    category_totals = expenses.values('category').annotate(total=Sum('amount'))

    # Total
    grand_total = expenses.aggregate(total=Sum('amount'))['total'] or 0

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Monthly Spending"

    # Header
    ws.append(["Category", "Amount Spent"])

    # Data
    for entry in category_totals:
        ws.append([entry['category'], entry['total']])

    # Total row
    ws.append(["Total", grand_total])

    # Prepare response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"Monthly_Spending_{now.strftime('%Y_%m')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    wb.save(response)
    return response