from datetime import date, datetime, time, timedelta
from calendar import monthrange
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.templatetags.static import static
from email.mime.image import MIMEImage

from django.http import request
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
)

from django.views.decorators.http import require_GET, require_POST
from core.models import ChatMessage, UserStatus
from django.http import JsonResponse
from accounts_app import models
from core.models import Todo
from core.models import Task, TaskComment
from django.contrib.auth.models import User
from django.db import transaction
from core.models import Student, StudentFeePayment
from core.models import Project, Task
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Q, Avg

from decimal import (
    Decimal,
    InvalidOperation,
)

from core.models import (
    Student,
    Client,
    Project,
    Task,
    TaskComment,
    Attendance,
    Leave,
    Holiday,
    ChatMessage,
    UserStatus,
    Invoice,
    InvoiceItem,
)


User = get_user_model()


# =========================================================
# ATTENDANCE / LEAVE TIME RULES
# =========================================================

CHECK_IN_START = time(9, 0)
CHECK_IN_END = time(11, 0)

CHECK_OUT_START = time(16, 0)
CHECK_OUT_END = time(18, 0)

LEAVE_TODAY_DEADLINE = time(9, 0)


# =========================================================
# HOME
# =========================================================

def home(request):

    return render(
        request,
        "home/index.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login_page(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not user.is_active:

                messages.error(
                    request,
                    "Your account is inactive. Please contact the administrator."
                )

                return redirect("login")

            login(request, user)

            if user.role == "admin":

                return redirect(
                    "admin_dashboard"
                )

            elif user.role == "employee":

                return redirect(
                    "employee_dashboard"
                )

            logout(request)

            messages.error(
                request,
                "Your account role is not configured."
            )

            return redirect("login")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_page(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("login")
# =========================================================
# ADMIN DASHBOARD
# =========================================================

@login_required(login_url="login")
def admin_dashboard(request):

    # =====================================================
    # ADMIN ACCESS CHECK
    # =====================================================

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to access the Admin Dashboard."
        )

        return redirect("employee_dashboard")

    # =====================================================
    # EMPLOYEES
    # =====================================================

    employees = User.objects.filter(
        role="employee"
    ).order_by(
        "-created_at"
    )

    employee_count = employees.count()

    # =====================================================
    # STUDENTS
    # =====================================================

    student_count = Student.objects.count()

    active_student_count = Student.objects.filter(
        status="active"
    ).count()

    # =====================================================
    # STUDENT FEES
    # =====================================================

    fee_data = Student.objects.aggregate(
        total_fee=Sum("total_fee"),
        fee_paid=Sum("fee_paid")
    )

    total_fee = (
        fee_data["total_fee"]
        or Decimal("0.00")
    )

    fee_collected = (
        fee_data["fee_paid"]
        or Decimal("0.00")
    )

    fee_remaining = (
        total_fee
        - fee_collected
    )

    if fee_remaining < Decimal("0.00"):

        fee_remaining = Decimal("0.00")

    # =====================================================
    # FEE PAYMENT STATUS
    # =====================================================

    pending_fee_students = Student.objects.filter(
        payment_status="pending"
    ).count()

    partial_fee_students = Student.objects.filter(
        payment_status="partial"
    ).count()

    paid_fee_students = Student.objects.filter(
        payment_status="paid"
    ).count()

    # =====================================================
    # CLIENTS
    # =====================================================

    total_clients = Client.objects.count()

    indian_clients = Client.objects.filter(
        client_type="indian"
    ).count()

    foreign_clients = Client.objects.filter(
        client_type="foreigner"
    ).count()

    active_clients = Client.objects.filter(
        status="active"
    ).count()

    inactive_clients = Client.objects.filter(
        status="inactive"
    ).count()

    # =====================================================
    # PROJECTS
    # =====================================================

    total_projects = Project.objects.count()

    # -----------------------------------------------------
    # ACTIVE PROJECTS
    # Planning + In Progress + Testing
    # -----------------------------------------------------

    active_projects = Project.objects.filter(
        status__in=[
            "planning",
            "in_progress",
            "testing",
        ]
    ).count()

    # -----------------------------------------------------
    # COMPLETED PROJECTS
    # -----------------------------------------------------

    completed_projects = Project.objects.filter(
        status="completed"
    ).count()

    # =====================================================
    # PROJECT STATUS
    # ALL PROJECTS
    # =====================================================

    planning_projects = Project.objects.filter(
        status="planning"
    ).count()

    in_progress_projects = Project.objects.filter(
        status="in_progress"
    ).count()

    completed_projects = Project.objects.filter(
        status="completed"
    ).count()

    testing_projects = Project.objects.filter(
        status="testing"
    ).count()

    on_hold_projects = Project.objects.filter(
        status="on_hold"
    ).count()

    cancelled_projects = Project.objects.filter(
        status="cancelled"
    ).count()

    # =====================================================
    # PROJECT COSTS
    # =====================================================

    project_cost_data = Project.objects.aggregate(

        total_project_cost=Sum(
            "total_cost"
        ),

        total_development_cost=Sum(
            "development_cost"
        ),

        total_paid_development_cost=Sum(
            "paid_development_cost"
        ),
    )

    total_project_cost = (
        project_cost_data[
            "total_project_cost"
        ]
        or Decimal("0.00")
    )

    total_development_cost = (
        project_cost_data[
            "total_development_cost"
        ]
        or Decimal("0.00")
    )

    total_paid_development_cost = (
        project_cost_data[
            "total_paid_development_cost"
        ]
        or Decimal("0.00")
    )

    # =====================================================
    # PENDING DEVELOPMENT COST
    # =====================================================

    pending_development_cost = (
        total_development_cost
        - total_paid_development_cost
    )

    if pending_development_cost < Decimal("0.00"):

        pending_development_cost = Decimal("0.00")

    # =====================================================
    # PROJECT PROGRESS
    # =====================================================
    # IMPORTANT:
    # This must be a queryset because dashboard.html
    # loops through project_progress.
    # =====================================================

    project_progress = Project.objects.values(
        "project_name",
        "progress"
    ).order_by(
        "-progress"
    )

    # =====================================================
    # TODAY'S TASKS
    # =====================================================

    today = timezone.localdate()

    today_tasks = Task.objects.filter(
        task_date=today
    )

    # -----------------------------------------------------
    # TOTAL TODAY'S TASKS
    # -----------------------------------------------------

    total_task_count = today_tasks.count()

    # -----------------------------------------------------
    # PENDING TODAY'S TASKS
    # -----------------------------------------------------

    pending_task_count = today_tasks.filter(
        status="pending"
    ).count()

    # -----------------------------------------------------
    # IN PROGRESS TODAY'S TASKS
    # -----------------------------------------------------

    in_progress_task_count = today_tasks.filter(
        status="in_progress"
    ).count()

    # -----------------------------------------------------
    # COMPLETED TODAY'S TASKS
    # -----------------------------------------------------

    completed_task_count = today_tasks.filter(
        status="completed"
    ).count()

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        # =================================================
        # EMPLOYEES
        # =================================================

        "employee_count": employee_count,

        "employees": employees,


        # =================================================
        # STUDENTS
        # =================================================

        "student_count": student_count,

        "active_student_count": (
            active_student_count
        ),

        "total_fee": total_fee,

        "fee_collected": fee_collected,

        "fee_remaining": fee_remaining,

        "pending_fee_students": (
            pending_fee_students
        ),

        "partial_fee_students": (
            partial_fee_students
        ),

        "paid_fee_students": (
            paid_fee_students
        ),


        # =================================================
        # CLIENTS
        # =================================================

        "client_count": total_clients,

        "total_clients": total_clients,

        "indian_client_count": (
            indian_clients
        ),

        "indian_clients": indian_clients,

        "foreign_client_count": (
            foreign_clients
        ),

        "foreign_clients": foreign_clients,

        "active_client_count": (
            active_clients
        ),

        "active_clients": active_clients,

        "inactive_client_count": (
            inactive_clients
        ),

        "inactive_clients": inactive_clients,


        # =================================================
        # PROJECTS
        # =================================================

        "project_count": total_projects,

        "total_projects": total_projects,

        "active_project_count": (
            active_projects
        ),

        "active_projects": active_projects,

        "completed_project_count": (
            completed_projects
        ),

        "completed_projects": completed_projects,


        # =================================================
        # PROJECT STATUS
        # =================================================

        "planning_projects": (
            planning_projects
        ),

        "in_progress_projects": (
            in_progress_projects
        ),

        "completed_projects": (
            completed_projects
        ),

        "testing_projects": (
            testing_projects
        ),

        "on_hold_projects": (
            on_hold_projects
        ),

        "cancelled_projects": (
            cancelled_projects
        ),


        # =================================================
        # PROJECT COSTS
        # =================================================

        "total_project_cost": (
            total_project_cost
        ),

        "total_development_cost": (
            total_development_cost
        ),

        "total_paid_development_cost": (
            total_paid_development_cost
        ),

        "pending_development_cost": (
            pending_development_cost
        ),


        # =================================================
        # TASKS
        # TODAY'S TASKS
        # =================================================

        "total_task_count": (
            total_task_count
        ),

        "pending_task_count": (
            pending_task_count
        ),

        "in_progress_task_count": (
            in_progress_task_count
        ),

        "completed_task_count": (
            completed_task_count
        ),


        # =================================================
        # PROJECT PROGRESS
        # =================================================

        "project_progress": (
            project_progress
        ),

    }

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "admin/dashboard.html",
        context
    )

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "admin/dashboard.html",
        context
    )
# =========================================================
# EMPLOYEES
# =========================================================

@login_required(login_url="login")
def employees(request):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to access Employees."
        )

        return redirect("employee_dashboard")

    employee_list = User.objects.filter(
        role="employee"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "admin/employees.html",
        {
            "employees": employee_list,
        }
    )


# =========================================================
# ADD EMPLOYEE
# =========================================================

@login_required(login_url="login")
def add_employee(request):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to add employees."
        )

        return redirect("employee_dashboard")

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        department = request.POST.get(
            "department",
            ""
        ).strip()

        designation = request.POST.get(
            "designation",
            ""
        ).strip()

        joining_date = request.POST.get(
            "joining_date",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        if not first_name:

            messages.error(
                request,
                "First name is required."
            )

            return redirect("add_employee")

        if not username:

            messages.error(
                request,
                "Username is required."
            )

            return redirect("add_employee")

        if not email:

            messages.error(
                request,
                "Email is required."
            )

            return redirect("add_employee")

        if not password:

            messages.error(
                request,
                "Password is required."
            )

            return redirect("add_employee")

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("add_employee")

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email already exists."
            )

            return redirect("add_employee")

        employee = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role="employee"
        )

        employee.phone = phone
        employee.department = department
        employee.designation = designation

        if joining_date:
            employee.joining_date = joining_date

        employee.save()

        messages.success(
            request,
            f"Employee {first_name} {last_name} created successfully."
        )

        return redirect("employees")

    return render(
        request,
        "admin/add_employee.html"
    )


# =========================================================
# EDIT EMPLOYEE
# =========================================================

@login_required(login_url="login")
def edit_employee(
    request,
    employee_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to edit employees."
        )

        return redirect("employee_dashboard")

    employee = get_object_or_404(
        User,
        id=employee_id,
        role="employee"
    )

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        department = request.POST.get(
            "department",
            ""
        ).strip()

        designation = request.POST.get(
            "designation",
            ""
        ).strip()

        joining_date = request.POST.get(
            "joining_date",
            ""
        ).strip()

        if not first_name or not username or not email:

            messages.error(
                request,
                "First name, username and email are required."
            )

            return redirect(
                "edit_employee",
                employee_id=employee.id
            )

        if User.objects.filter(
            username=username
        ).exclude(
            id=employee.id
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect(
                "edit_employee",
                employee_id=employee.id
            )

        if User.objects.filter(
            email=email
        ).exclude(
            id=employee.id
        ).exists():

            messages.error(
                request,
                "Email already exists."
            )

            return redirect(
                "edit_employee",
                employee_id=employee.id
            )

        employee.first_name = first_name
        employee.last_name = last_name
        employee.username = username
        employee.email = email
        employee.phone = phone
        employee.department = department
        employee.designation = designation

        employee.joining_date = (
            joining_date
            if joining_date
            else None
        )

        employee.save()

        messages.success(
            request,
            "Employee details updated successfully."
        )

        return redirect("employees")

    return render(
        request,
        "admin/edit_employee.html",
        {
            "employee": employee
        }
    )


# =========================================================
# DELETE EMPLOYEE
# =========================================================

@login_required(login_url="login")
def delete_employee(
    request,
    employee_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to delete employees."
        )

        return redirect("employee_dashboard")

    employee = get_object_or_404(
        User,
        id=employee_id,
        role="employee"
    )

    if request.method == "POST":

        employee_name = (
            f"{employee.first_name} "
            f"{employee.last_name}"
        ).strip()

        if not employee_name:
            employee_name = employee.username

        employee.delete()

        messages.success(
            request,
            f"Employee {employee_name} deleted successfully."
        )

        return redirect("employees")

    return redirect("employees")


# =========================================================
# STUDENTS
# =========================================================

@login_required(login_url="login")
def students(request):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to access Students."
        )

        return redirect("employee_dashboard")

    student_list = Student.objects.select_related(
        "assigned_employee"
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        student_list = student_list.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
            | Q(course__icontains=search)
            | Q(batch__icontains=search)
        )

    selected_status = request.GET.get(
        "status",
        ""
    ).strip()

    if selected_status in [
        "active",
        "inactive",
        "completed"
    ]:

        student_list = student_list.filter(
            status=selected_status
        )

    selected_mode = request.GET.get(
        "mode",
        ""
    ).strip()

    if selected_mode in [
        "online",
        "offline"
    ]:

        student_list = student_list.filter(
            learning_mode=selected_mode
        )

    student_list = student_list.order_by(
        "-created_at"
    )

    total_students = Student.objects.count()

    active_students = Student.objects.filter(
        status="active"
    ).count()

    inactive_students = Student.objects.filter(
        status="inactive"
    ).count()

    completed_students = Student.objects.filter(
        status="completed"
    ).count()

    fee_data = Student.objects.aggregate(
        total_fee_amount=Sum("total_fee"),
        fee_paid_amount=Sum("fee_paid")
    )

    total_fee = (
        fee_data["total_fee_amount"]
        or Decimal("0.00")
    )

    fee_collected = (
        fee_data["fee_paid_amount"]
        or Decimal("0.00")
    )

    fee_remaining = total_fee - fee_collected

    if fee_remaining < Decimal("0.00"):
        fee_remaining = Decimal("0.00")

    pending_fee_students = Student.objects.filter(
        payment_status="pending"
    ).count()

    partial_fee_students = Student.objects.filter(
        payment_status="partial"
    ).count()

    paid_fee_students = Student.objects.filter(
        payment_status="paid"
    ).count()

    context = {

        "students": student_list,

        "total_students": total_students,

        "active_students": active_students,

        "inactive_students": inactive_students,

        "completed_students": completed_students,

        "active_count": active_students,

        "inactive_count": inactive_students,

        "completed_count": completed_students,

        "total_fee": total_fee,

        "fee_collected": fee_collected,

        "fee_remaining": fee_remaining,

        "total_fees": total_fee,

        "fees_paid": fee_collected,

        "remaining_fees": fee_remaining,

        "pending_fee_students": pending_fee_students,

        "partial_fee_students": partial_fee_students,

        "paid_fee_students": paid_fee_students,

        "filtered_student_count": student_list.count(),

        "search": search,

        "selected_status": selected_status,

        "selected_mode": selected_mode,
    }

    return render(
        request,
        "admin/students.html",
        context
    )


# =========================================================
# STUDENT DETAIL
# =========================================================

@login_required(login_url="login")
def student_detail(
    request,
    student_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to view student details."
        )

        return redirect("employee_dashboard")

    student = get_object_or_404(
        Student.objects.select_related(
            "assigned_employee"
        ),
        id=student_id
    )

    return render(
        request,
        "admin/student_detail.html",
        {
            "student": student
        }
    )




# =========================================================
# ADD STUDENT
# =========================================================

@login_required(login_url="login")
def add_student(request):

    # =====================================================
    # ADMIN ACCESS CHECK
    # =====================================================

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to add students."
        )

        return redirect("employee_dashboard")

    # =====================================================
    # EMPLOYEE LIST
    # =====================================================

    employee_list = User.objects.filter(
        role="employee",
        is_active=True
    ).order_by(
        "first_name",
        "last_name"
    )

    # =====================================================
    # POST REQUEST
    # =====================================================

    if request.method == "POST":

        # =================================================
        # PERSONAL INFORMATION
        # =================================================

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        # =================================================
        # COURSE INFORMATION
        # =================================================

        course = request.POST.get(
            "course",
            ""
        ).strip()

        batch = request.POST.get(
            "batch",
            ""
        ).strip()

        learning_mode = request.POST.get(
            "learning_mode",
            "online"
        ).strip()

        assigned_employee_id = request.POST.get(
            "assigned_employee",
            ""
        ).strip()

        # =================================================
        # COURSE DURATION
        # =================================================

        duration_months_input = request.POST.get(
            "course_duration_months",
            "0"
        ).strip()

        # =================================================
        # ENROLLMENT
        # =================================================

        joining_date = request.POST.get(
            "joining_date",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            "active"
        ).strip()

        # =================================================
        # FEE DETAILS
        # =================================================

        total_fee_input = request.POST.get(
            "total_fee",
            "0"
        ).strip()

        # =================================================
        # NOTES
        # =================================================

        notes = request.POST.get(
            "notes",
            ""
        ).strip()

        # =================================================
        # BASIC VALIDATION
        # =================================================

        if not first_name:

            messages.error(
                request,
                "First name is required."
            )

            return redirect("add_student")

        if not email:

            messages.error(
                request,
                "Email is required."
            )

            return redirect("add_student")

        # =================================================
        # DUPLICATE EMAIL CHECK
        # =================================================

        if Student.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "A student with this email already exists."
            )

            return redirect("add_student")

        # =================================================
        # STATUS VALIDATION
        # =================================================

        if status not in [
            "active",
            "inactive",
            "completed"
        ]:

            status = "active"

        # =================================================
        # LEARNING MODE VALIDATION
        # =================================================

        if learning_mode not in [
            "online",
            "offline"
        ]:

            learning_mode = "online"

        # =================================================
        # ASSIGNED EMPLOYEE
        # =================================================

        assigned_employee = None

        if assigned_employee_id:

            assigned_employee = get_object_or_404(
                User,
                id=assigned_employee_id,
                role="employee",
                is_active=True
            )

        # =================================================
        # COURSE DURATION
        # =================================================

        try:

            course_duration_months = int(
                duration_months_input or 0
            )

        except (
            ValueError,
            TypeError
        ):

            messages.error(
                request,
                "Please enter a valid course duration."
            )

            return redirect("add_student")

        if course_duration_months < 0:

            messages.error(
                request,
                "Course duration cannot be negative."
            )

            return redirect("add_student")

        # =================================================
        # FEE CONVERSION
        # =================================================

        try:

            total_fee = Decimal(
                total_fee_input or "0"
            )

        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):

            messages.error(
                request,
                "Please enter a valid total fee."
            )

            return redirect("add_student")

        # =================================================
        # FEE VALIDATION
        # =================================================

        if total_fee < Decimal("0.00"):

            messages.error(
                request,
                "Total fee cannot be negative."
            )

            return redirect("add_student")

        # =================================================
        # MONTHLY PAYMENT DATA
        # =================================================

        payment_months = request.POST.getlist(
            "payment_month[]"
        )

        payment_amounts = request.POST.getlist(
            "payment_amount[]"
        )

        payment_dates = request.POST.getlist(
            "payment_date[]"
        )

        payment_statuses = request.POST.getlist(
            "payment_status[]"
        )

        # =================================================
        # CALCULATE TOTAL PAID
        # =================================================

        total_paid = Decimal("0.00")

        for index, payment_month in enumerate(
            payment_months
        ):

            if not payment_month:
                continue

            # ---------------------------------------------
            # PAYMENT AMOUNT
            # ---------------------------------------------

            amount_input = "0"

            if index < len(payment_amounts):

                amount_input = (
                    payment_amounts[index]
                    or "0"
                )

            try:

                amount = Decimal(
                    amount_input
                )

            except (
                InvalidOperation,
                ValueError,
                TypeError
            ):

                messages.error(
                    request,
                    "Please enter valid monthly payment amounts."
                )

                return redirect("add_student")

            if amount < Decimal("0.00"):

                messages.error(
                    request,
                    "Monthly payment cannot be negative."
                )

                return redirect("add_student")

            # ---------------------------------------------
            # PAYMENT STATUS
            # ---------------------------------------------

            payment_status = "paid"

            if index < len(payment_statuses):

                payment_status = (
                    payment_statuses[index]
                    or "paid"
                )

            if payment_status not in [
                "paid",
                "pending"
            ]:

                payment_status = "paid"

            # ---------------------------------------------
            # CALCULATE PAID AMOUNT
            # ---------------------------------------------

            if payment_status == "paid":

                total_paid += amount

        # =================================================
        # PAID CANNOT EXCEED TOTAL FEE
        # =================================================

        if total_paid > total_fee:

            messages.error(
                request,
                "Total paid fee cannot be greater than total course fee."
            )

            return redirect("add_student")

        # =================================================
        # CREATE STUDENT
        # =================================================
        #
        # IMPORTANT:
        # Only fields that currently exist in Student model
        # are used here.
        #
        # Removed:
        # monthly_fee
        # course_duration_days
        # certificate_status
        #
        # =================================================

        student = Student.objects.create(

            first_name=first_name,

            last_name=last_name,

            email=email,

            phone=phone,

            address=address,

            course=course,

            batch=batch,

            joining_date=(
                joining_date
                if joining_date
                else None
            ),

            status=status,

            assigned_employee=assigned_employee,

            learning_mode=learning_mode,

            total_fee=total_fee,

            fee_paid=total_paid,

            course_duration_months=course_duration_months,

            notes=notes
        )

        # =================================================
        # SAVE MONTHLY FEE RECORDS
        # =================================================

        for index, payment_month in enumerate(
            payment_months
        ):

            if not payment_month:
                continue

            # ---------------------------------------------
            # PAYMENT AMOUNT
            # ---------------------------------------------

            amount_input = "0"

            if index < len(payment_amounts):

                amount_input = (
                    payment_amounts[index]
                    or "0"
                )

            try:

                amount = Decimal(
                    amount_input
                )

            except (
                InvalidOperation,
                ValueError,
                TypeError
            ):

                messages.error(
                    request,
                    "Please enter a valid payment amount."
                )

                return redirect("add_student")

            # ---------------------------------------------
            # PAYMENT DATE
            # ---------------------------------------------

            payment_date = None

            if (
                index < len(payment_dates)
                and payment_dates[index]
            ):

                try:

                    payment_date = datetime.strptime(
                        payment_dates[index],
                        "%Y-%m-%d"
                    ).date()

                except ValueError:

                    messages.error(
                        request,
                        "Please enter a valid payment date."
                    )

                    return redirect("add_student")

            # ---------------------------------------------
            # PAYMENT STATUS
            # ---------------------------------------------

            payment_status = "paid"

            if index < len(payment_statuses):

                payment_status = (
                    payment_statuses[index]
                    or "paid"
                )

            if payment_status not in [
                "paid",
                "pending"
            ]:

                payment_status = "paid"

            # ---------------------------------------------
            # PAYMENT MONTH
            # ---------------------------------------------

            try:

                payment_month_date = datetime.strptime(
                    payment_month,
                    "%Y-%m"
                ).date()

            except ValueError:

                messages.error(
                    request,
                    "Please enter a valid payment month."
                )

                return redirect("add_student")

            # ---------------------------------------------
            # CREATE FEE PAYMENT
            # ---------------------------------------------

            StudentFeePayment.objects.create(

                student=student,

                payment_month=payment_month_date,

                amount=amount,

                payment_date=payment_date,

                status=payment_status
            )

        # =================================================
        # SUCCESS
        # =================================================

        messages.success(
            request,
            f"Student {student.first_name} {student.last_name} added successfully."
        )

        return redirect("students")

    # =====================================================
    # GET REQUEST
    # =====================================================

    return render(
        request,
        "admin/add_student.html",
        {
            "employees": employee_list
        }
    )


# =========================================================
# EDIT STUDENT
# =========================================================

@login_required(login_url="login")
def edit_student(request, student_id):

    # =====================================================
    # ADMIN ACCESS CHECK
    # =====================================================

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to edit students."
        )

        return redirect("employee_dashboard")


    # =====================================================
    # GET STUDENT
    # =====================================================

    student = get_object_or_404(
        Student,
        id=student_id
    )


    # =====================================================
    # EMPLOYEES
    # =====================================================

    employees = User.objects.filter(
        role="employee"
    ).order_by(
        "first_name",
        "last_name"
    )


    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        # =================================================
        # PERSONAL INFORMATION
        # =================================================

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()


        # =================================================
        # REQUIRED VALIDATION
        # =================================================

        if not first_name:

            messages.error(
                request,
                "First name is required."
            )

            return redirect(
                "edit_student",
                student_id=student.id
            )


        if not email:

            messages.error(
                request,
                "Email is required."
            )

            return redirect(
                "edit_student",
                student_id=student.id
            )


        # =================================================
        # EMAIL DUPLICATE CHECK
        # =================================================

        email_exists = Student.objects.filter(
            email__iexact=email
        ).exclude(
            id=student.id
        ).exists()


        if email_exists:

            messages.error(
                request,
                "A student with this email already exists."
            )

            return redirect(
                "edit_student",
                student_id=student.id
            )


        # =================================================
        # ACADEMIC INFORMATION
        # =================================================

        course = request.POST.get(
            "course",
            ""
        ).strip()

        batch = request.POST.get(
            "batch",
            ""
        ).strip()

        learning_mode = request.POST.get(
            "learning_mode",
            "online"
        )

        status = request.POST.get(
            "status",
            "active"
        )

        joining_date = request.POST.get(
            "joining_date",
            ""
        ).strip()


        # =================================================
        # ASSIGNED EMPLOYEE
        # =================================================

        assigned_employee_id = request.POST.get(
            "assigned_employee",
            ""
        ).strip()


        assigned_employee = None


        if assigned_employee_id:

            try:

                assigned_employee = User.objects.get(
                    id=assigned_employee_id,
                    role="employee"
                )

            except User.DoesNotExist:

                messages.error(
                    request,
                    "Selected employee does not exist."
                )

                return redirect(
                    "edit_student",
                    student_id=student.id
                )


        # =================================================
        # COURSE DURATION
        # =================================================

        course_duration_months = request.POST.get(
            "course_duration_months",
            "0"
        ).strip()

        course_duration_days = request.POST.get(
            "course_duration_days",
            "0"
        ).strip()


        try:

            course_duration_months = int(
                course_duration_months or 0
            )

            course_duration_days = int(
                course_duration_days or 0
            )

        except ValueError:

            messages.error(
                request,
                "Course duration must contain valid numbers."
            )

            return redirect(
                "edit_student",
                student_id=student.id
            )


        if course_duration_months < 0:

            course_duration_months = 0


        if course_duration_days < 0:

            course_duration_days = 0


        # =================================================
        # FEE INFORMATION
        # =================================================

        total_fee = request.POST.get(
            "total_fee",
            "0"
        ).strip()

        monthly_fee = request.POST.get(
            "monthly_fee",
            "0"
        ).strip()


        try:

            total_fee = Decimal(
                total_fee or "0"
            )

            monthly_fee = Decimal(
                monthly_fee or "0"
            )

        except Exception:

            messages.error(
                request,
                "Fee amount must contain valid numbers."
            )

            return redirect(
                "edit_student",
                student_id=student.id
            )


        if total_fee < Decimal("0.00"):

            total_fee = Decimal("0.00")


        if monthly_fee < Decimal("0.00"):

            monthly_fee = Decimal("0.00")


        # =================================================
        # CERTIFICATE
        # =================================================

        certificate_status = request.POST.get(
            "certificate_status",
            "not_issued"
        )


        if certificate_status not in [
            "not_issued",
            "issued"
        ]:

            certificate_status = "not_issued"


        # =================================================
        # NOTES
        # =================================================

        notes = request.POST.get(
            "notes",
            ""
        ).strip()


        # =================================================
        # UPDATE STUDENT
        # =================================================

        student.first_name = first_name

        student.last_name = last_name

        student.email = email

        student.phone = phone

        student.address = address

        student.course = course

        student.batch = batch

        student.learning_mode = learning_mode

        student.status = status

        student.assigned_employee = assigned_employee

        student.course_duration_months = (
            course_duration_months
        )

        student.course_duration_days = (
            course_duration_days
        )

        student.total_fee = total_fee

        student.monthly_fee = monthly_fee

        student.certificate_status = (
            certificate_status
        )

        student.notes = notes


        # =================================================
        # JOINING DATE
        # =================================================

        if joining_date:

            try:

                student.joining_date = (
                    datetime.strptime(
                        joining_date,
                        "%Y-%m-%d"
                    ).date()
                )

            except ValueError:

                messages.error(
                    request,
                    "Invalid joining date."
                )

                return redirect(
                    "edit_student",
                    student_id=student.id
                )

        else:

            student.joining_date = None


        # =================================================
        # SAVE STUDENT
        # =================================================

        student.save()


        # =================================================
        # MONTHLY PAYMENT DATA
        # =================================================

        payment_ids = request.POST.getlist(
            "payment_id[]"
        )

        payment_months = request.POST.getlist(
            "payment_month[]"
        )

        payment_amounts = request.POST.getlist(
            "payment_amount[]"
        )

        payment_dates = request.POST.getlist(
            "payment_date[]"
        )

        payment_statuses = request.POST.getlist(
            "payment_status[]"
        )


        # =================================================
        # UPDATE / CREATE PAYMENTS
        # =================================================

        calculated_paid = Decimal("0.00")


        for index, month_value in enumerate(
            payment_months
        ):

            month_value = month_value.strip()


            if not month_value:
                continue


            # =============================================
            # FIX MONTH INPUT
            #
            # HTML type="month" sends:
            #
            # 2026-08
            #
            # Django DateField requires:
            #
            # 2026-08-01
            # =============================================

            try:

                if len(month_value) == 7:

                    payment_month = datetime.strptime(
                        month_value,
                        "%Y-%m"
                    ).date().replace(
                        day=1
                    )

                else:

                    payment_month = datetime.strptime(
                        month_value,
                        "%Y-%m-%d"
                    ).date()

            except ValueError:

                messages.error(
                    request,
                    f"Invalid payment month: {month_value}"
                )

                return redirect(
                    "edit_student",
                    student_id=student.id
                )


            # =============================================
            # AMOUNT
            # =============================================

            amount_value = (
                payment_amounts[index]
                if index < len(payment_amounts)
                else "0"
            )


            try:

                amount = Decimal(
                    amount_value or "0"
                )

            except Exception:

                messages.error(
                    request,
                    "Invalid payment amount."
                )

                return redirect(
                    "edit_student",
                    student_id=student.id
                )


            if amount < Decimal("0.00"):

                amount = Decimal("0.00")


            # =============================================
            # PAYMENT DATE
            # =============================================

            payment_date_value = (
                payment_dates[index]
                if index < len(payment_dates)
                else ""
            )


            payment_date = None


            if payment_date_value:

                try:

                    payment_date = datetime.strptime(
                        payment_date_value,
                        "%Y-%m-%d"
                    ).date()

                except ValueError:

                    messages.error(
                        request,
                        "Invalid payment date."
                    )

                    return redirect(
                        "edit_student",
                        student_id=student.id
                    )


            # =============================================
            # PAYMENT STATUS
            # =============================================

            status_value = (
                payment_statuses[index]
                if index < len(payment_statuses)
                else "paid"
            )


            if status_value not in [
                "paid",
                "pending"
            ]:

                status_value = "pending"


            # =============================================
            # EXISTING PAYMENT
            # =============================================

            payment_id = (
                payment_ids[index]
                if index < len(payment_ids)
                else ""
            )


            if payment_id:

                try:

                    payment = StudentFeePayment.objects.get(
                        id=payment_id,
                        student=student
                    )

                except StudentFeePayment.DoesNotExist:

                    messages.error(
                        request,
                        "One of the payment records could not be found."
                    )

                    return redirect(
                        "edit_student",
                        student_id=student.id
                    )


                payment.payment_month = payment_month

                payment.amount = amount

                payment.payment_date = payment_date

                payment.status = status_value

                payment.save()


            # =============================================
            # NEW PAYMENT
            # =============================================

            else:

                payment = StudentFeePayment.objects.create(

                    student=student,

                    payment_month=payment_month,

                    amount=amount,

                    payment_date=payment_date,

                    status=status_value

                )


            # =============================================
            # CALCULATE PAID
            # =============================================

            if status_value == "paid":

                calculated_paid += amount


        # =================================================
        # UPDATE STUDENT FEE PAID
        # =================================================

        student.fee_paid = calculated_paid

        student.update_payment_status()

        student.save(
            update_fields=[
                "fee_paid",
                "payment_status",
                "updated_at"
            ]
        )


        # =================================================
        # SUCCESS
        # =================================================

        messages.success(
            request,
            "Student updated successfully."
        )


        return redirect(
            "students"
        )


    # =====================================================
    # GET
    # =====================================================

    return render(
        request,
        "admin/edit_student.html",
        {
            "student": student,
            "employees": employees,
        }
    )

# =========================================================
# DELETE STUDENT
# =========================================================

@login_required(login_url="login")
def delete_student(
    request,
    student_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to delete students."
        )

        return redirect("employee_dashboard")

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":

        student_name = str(student)

        student.delete()

        messages.success(
            request,
            f"Student {student_name} deleted successfully."
        )

        return redirect("students")

    return redirect("students")


# =========================================================
# CLIENTS
# =========================================================

@login_required(login_url="login")
def clients(request):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to access Clients."
        )

        return redirect("employee_dashboard")

    client_list = Client.objects.all().order_by(
        "-created_at"
    )

    total_clients = Client.objects.count()

    indian_clients = Client.objects.filter(
        client_type="indian"
    ).count()

    foreign_clients = Client.objects.filter(
        client_type="foreigner"
    ).count()

    active_clients = Client.objects.filter(
        status="active"
    ).count()

    inactive_clients = Client.objects.filter(
        status="inactive"
    ).count()

    context = {

        "clients": client_list,

        "total_clients": total_clients,

        "indian_clients": indian_clients,

        "foreign_clients": foreign_clients,

        "active_clients": active_clients,

        "inactive_clients": inactive_clients,

        "filtered_client_count": client_list.count(),
    }

    return render(
        request,
        "admin/clients.html",
        context
    )


# =========================================================
# ADD CLIENT
# =========================================================

@login_required(login_url="login")
def add_client(request):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to add clients."
        )

        return redirect("employee_dashboard")

    if request.method == "POST":

        client_name = request.POST.get(
            "client_name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone_no = request.POST.get(
            "phone_no",
            ""
        ).strip()

        location = request.POST.get(
            "location",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            "active"
        ).strip().lower()

        if not client_name:

            messages.error(
                request,
                "Client name is required."
            )

            return redirect("add_client")

        if not email:

            messages.error(
                request,
                "Client email is required."
            )

            return redirect("add_client")

        if not phone_no:

            messages.error(
                request,
                "Phone number is required."
            )

            return redirect("add_client")

        if location not in [
            "India",
            "Foreign"
        ]:

            messages.error(
                request,
                "Please select a valid location."
            )

            return redirect("add_client")

        if Client.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "A client with this email already exists."
            )

            return redirect("add_client")

        if status not in [
            "active",
            "inactive"
        ]:

            status = "active"

        if location == "India":

            client_type = "indian"
            country = "India"

        else:

            client_type = "foreigner"
            country = "Foreign"

        Client.objects.create(

            name=client_name,

            email=email,

            phone=phone_no,

            client_type=client_type,

            country=country,

            status=status,
        )

        messages.success(
            request,
            f"Client {client_name} added successfully."
        )

        return redirect("clients")

    return render(
        request,
        "admin/add_client.html"
    )


# =========================================================
# CLIENT DETAIL
# =========================================================

@login_required(login_url="login")
def client_detail(
    request,
    client_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to view client details."
        )

        return redirect("employee_dashboard")

    client = get_object_or_404(
        Client,
        id=client_id
    )

    return render(
        request,
        "admin/client_detail.html",
        {
            "client": client
        }
    )


# =========================================================
# EDIT CLIENT
# =========================================================

@login_required(login_url="login")
def edit_client(
    request,
    client_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to edit clients."
        )

        return redirect("employee_dashboard")

    client = get_object_or_404(
        Client,
        id=client_id
    )

    if request.method == "POST":

        client_name = request.POST.get(
            "client_name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone_no = request.POST.get(
            "phone_no",
            ""
        ).strip()

        location = request.POST.get(
            "location",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            "active"
        ).strip().lower()

        if not client_name:

            messages.error(
                request,
                "Client name is required."
            )

            return redirect(
                "edit_client",
                client_id=client.id
            )

        if not email:

            messages.error(
                request,
                "Client email is required."
            )

            return redirect(
                "edit_client",
                client_id=client.id
            )

        if not phone_no:

            messages.error(
                request,
                "Phone number is required."
            )

            return redirect(
                "edit_client",
                client_id=client.id
            )

        if location not in [
            "India",
            "Foreign"
        ]:

            messages.error(
                request,
                "Please select a valid location."
            )

            return redirect(
                "edit_client",
                client_id=client.id
            )

        if Client.objects.filter(
            email__iexact=email
        ).exclude(
            id=client.id
        ).exists():

            messages.error(
                request,
                "Another client with this email already exists."
            )

            return redirect(
                "edit_client",
                client_id=client.id
            )

        if status not in [
            "active",
            "inactive"
        ]:

            status = "active"

        if location == "India":

            client.client_type = "indian"
            client.country = "India"

        else:

            client.client_type = "foreigner"
            client.country = "Foreign"

        client.name = client_name
        client.email = email
        client.phone = phone_no
        client.status = status

        client.save()

        messages.success(
            request,
            "Client details updated successfully."
        )

        return redirect("clients")

    return render(
        request,
        "admin/edit_client.html",
        {
            "client": client
        }
    )


# =========================================================
# DELETE CLIENT
# =========================================================

@login_required(login_url="login")
def delete_client(
    request,
    client_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to delete clients."
        )

        return redirect("employee_dashboard")

    client = get_object_or_404(
        Client,
        id=client_id
    )

    if request.method == "POST":

        client_name = client.name

        client.delete()

        messages.success(
            request,
            f"Client {client_name} deleted successfully."
        )

        return redirect("clients")

    return redirect("clients")


# =========================================================
# PROJECTS
# =========================================================

@login_required(login_url="login")
def projects(request):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to access Projects."
        )

        return redirect("employee_dashboard")

    # -----------------------------------------------------
    # PROJECT LIST
    # -----------------------------------------------------

    project_list = Project.objects.select_related(
        "client",
        "project_manager",
        "designer",
        "developer",
        "tester",
    ).order_by(
        "-created_at"
    )

    # -----------------------------------------------------
    # PROJECT COUNTS
    # -----------------------------------------------------

    total_projects = Project.objects.count()

    planning_projects = Project.objects.filter(
        status="planning"
    ).count()

    in_progress_projects = Project.objects.filter(
        status="in_progress"
    ).count()

    testing_projects = Project.objects.filter(
        status="testing"
    ).count()

    completed_projects = Project.objects.filter(
        status="completed"
    ).count()

    on_hold_projects = Project.objects.filter(
        status="on_hold"
    ).count()

    cancelled_projects = Project.objects.filter(
        status="cancelled"
    ).count()

    active_projects = Project.objects.filter(
        status__in=[
            "planning",
            "in_progress",
            "testing",
        ]
    ).count()

    # -----------------------------------------------------
    # TOTAL PROJECT COST
    # -----------------------------------------------------

    total_project_cost = (
        Project.objects.aggregate(
            total=Sum("total_cost")
        )["total"]
        or Decimal("0.00")
    )

    # -----------------------------------------------------
    # TOTAL DEVELOPMENT COST
    # -----------------------------------------------------

    total_development_cost = (
        Project.objects.aggregate(
            total=Sum("development_cost")
        )["total"]
        or Decimal("0.00")
    )

    # -----------------------------------------------------
    # TOTAL PAID DEVELOPMENT COST
    # -----------------------------------------------------

    total_paid_development_cost = (
        Project.objects.aggregate(
            total=Sum("paid_development_cost")
        )["total"]
        or Decimal("0.00")
    )

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {

        "projects": project_list,

        "total_projects": total_projects,

        "planning_projects": planning_projects,

        "in_progress_projects": in_progress_projects,

        "testing_projects": testing_projects,

        "completed_projects": completed_projects,

        "on_hold_projects": on_hold_projects,

        "cancelled_projects": cancelled_projects,

        "active_projects": active_projects,

        "total_project_cost": total_project_cost,

        "total_development_cost": total_development_cost,

        "total_paid_development_cost": (
            total_paid_development_cost
        ),
    }

    return render(
        request,
        "admin/projects.html",
        context
    )


# =========================================================
# PROJECT DETAIL
# =========================================================

@login_required(login_url="login")
def project_detail(
    request,
    project_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to view project details."
        )

        return redirect("employee_dashboard")

    project = get_object_or_404(
        Project.objects.select_related(
            "client",
            "project_manager",
            "designer",
            "developer",
            "tester",
        ),
        id=project_id
    )

    return render(
        request,
        "admin/project_detail.html",
        {
            "project": project
        }
    )


# =========================================================
# ADD PROJECT
# =========================================================

@login_required(login_url="login")
def add_project(request):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to add projects."
        )

        return redirect("employee_dashboard")

    clients = Client.objects.filter(
        status="active"
    ).order_by(
        "name"
    )

    employees = User.objects.filter(
        role="employee",
        is_active=True
    ).order_by(
        "first_name",
        "last_name"
    )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    if request.method == "GET":

        return render(
            request,
            "admin/add_project.html",
            {
                "clients": clients,

                "employees": employees,

                "status_choices": Project.STATUS_CHOICES,

                "priority_choices": Project.PRIORITY_CHOICES,

                "project_type_choices": (
                    Project.PROJECT_TYPE_CHOICES
                ),
            }
        )

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    if request.method == "POST":

        try:

            # -------------------------------------------------
            # BASIC PROJECT INFORMATION
            # -------------------------------------------------

            project_name = request.POST.get(
                "name",
                ""
            ).strip()

            client_id = request.POST.get(
                "client",
                ""
            ).strip()

            project_type = request.POST.get(
                "category",
                "website"
            ).strip()

            technology_stack = request.POST.get(
                "technology",
                ""
            ).strip()

            description = request.POST.get(
                "description",
                ""
            ).strip()

            requirements = request.POST.get(
                "requirements",
                ""
            ).strip()

            # -------------------------------------------------
            # VALIDATE BASIC INFORMATION
            # -------------------------------------------------

            if not project_name:

                messages.error(
                    request,
                    "Project name is required."
                )

                return redirect("add_project")

            if not client_id:

                messages.error(
                    request,
                    "Please select a client."
                )

                return redirect("add_project")

            client = get_object_or_404(
                Client,
                id=client_id,
                status="active"
            )

            # -------------------------------------------------
            # TEAM MEMBERS
            # -------------------------------------------------

            project_manager_id = request.POST.get(
                "project_manager",
                ""
            ).strip()

            designer_id = request.POST.get(
                "designer",
                ""
            ).strip()

            developer_id = request.POST.get(
                "developer",
                ""
            ).strip()

            tester_id = request.POST.get(
                "tester",
                ""
            ).strip()

            project_manager = None
            designer = None
            developer = None
            tester = None

            if project_manager_id:

                project_manager = get_object_or_404(
                    User,
                    id=project_manager_id,
                    role="employee",
                    is_active=True
                )

            if designer_id:

                designer = get_object_or_404(
                    User,
                    id=designer_id,
                    role="employee",
                    is_active=True
                )

            if developer_id:

                developer = get_object_or_404(
                    User,
                    id=developer_id,
                    role="employee",
                    is_active=True
                )

            if tester_id:

                tester = get_object_or_404(
                    User,
                    id=tester_id,
                    role="employee",
                    is_active=True
                )

            # -------------------------------------------------
            # PROJECT COSTS
            # -------------------------------------------------

            total_cost = Decimal(
                request.POST.get(
                    "total_cost",
                    "0"
                ) or "0"
            )

            designer_cost = Decimal(
                request.POST.get(
                    "designer_cost",
                    "0"
                ) or "0"
            )

            development_cost = Decimal(
                request.POST.get(
                    "development_cost",
                    "0"
                ) or "0"
            )

            # NEW: PAID DEVELOPMENT COST
            paid_development_cost = Decimal(
                request.POST.get(
                    "paid_development_cost",
                    "0"
                ) or "0"
            )

            tester_cost = Decimal(
                request.POST.get(
                    "tester_cost",
                    "0"
                ) or "0"
            )

            other_cost = Decimal(
                request.POST.get(
                    "other_cost",
                    "0"
                ) or "0"
            )

            # -------------------------------------------------
            # COST VALIDATION
            # -------------------------------------------------

            if (
                total_cost < Decimal("0.00")
                or designer_cost < Decimal("0.00")
                or development_cost < Decimal("0.00")
                or paid_development_cost < Decimal("0.00")
                or tester_cost < Decimal("0.00")
                or other_cost < Decimal("0.00")
            ):

                messages.error(
                    request,
                    "Project costs cannot be negative."
                )

                return redirect("add_project")

            # -------------------------------------------------
            # PAID DEVELOPMENT COST VALIDATION
            # -------------------------------------------------

            if paid_development_cost > development_cost:

                messages.error(
                    request,
                    "Paid development cost cannot be greater than development cost."
                )

                return redirect("add_project")

            # -------------------------------------------------
            # DATES
            # -------------------------------------------------

            start_date = request.POST.get(
                "start_date"
            ) or None

            expected_end_date = request.POST.get(
                "end_date"
            ) or None

            # -------------------------------------------------
            # DURATION
            # -------------------------------------------------

            duration_raw = request.POST.get(
                "duration",
                ""
            ).strip()

            estimated_days = None

            if duration_raw:

                import re

                duration_match = re.search(
                    r"\d+",
                    duration_raw
                )

                if duration_match:

                    estimated_days = int(
                        duration_match.group()
                    )

            # -------------------------------------------------
            # STATUS
            # -------------------------------------------------

            status = request.POST.get(
                "status",
                "planning"
            ).strip()

            valid_statuses = [
                "planning",
                "in_progress",
                "testing",
                "on_hold",
                "completed",
                "cancelled",
            ]

            if status not in valid_statuses:

                status = "planning"

            # -------------------------------------------------
            # PRIORITY
            # -------------------------------------------------

            priority = request.POST.get(
                "priority",
                "medium"
            ).strip()

            valid_priorities = [
                "low",
                "medium",
                "high",
                "urgent",
            ]

            if priority not in valid_priorities:

                priority = "medium"

            # -------------------------------------------------
            # PROJECT TYPE
            # -------------------------------------------------

            valid_project_types = [
                "website",
                "web_application",
                "mobile_application",
                "software",
                "ecommerce",
                "api",
                "maintenance",
                "other",
            ]

            if project_type not in valid_project_types:

                project_type = "website"

            # -------------------------------------------------
            # NOTES
            # -------------------------------------------------

            notes = request.POST.get(
                "notes",
                ""
            ).strip()

            # -------------------------------------------------
            # PROJECT DATA
            # -------------------------------------------------

            project_data = {

                "project_name": project_name,

                "client": client,

                "project_type": project_type,

                "description": description,

                "requirements": requirements,

                "technology_stack": technology_stack,

                "project_manager": project_manager,

                "designer": designer,

                "developer": developer,

                "tester": tester,

                "total_cost": total_cost,

                "designer_cost": designer_cost,

                "development_cost": development_cost,

                # NEW
                "paid_development_cost": (
                    paid_development_cost
                ),

                "tester_cost": tester_cost,

                "start_date": start_date,

                "expected_end_date": expected_end_date,

                "estimated_days": estimated_days,

                "status": status,

                "priority": priority,

                "notes": notes,
            }

            # -------------------------------------------------
            # OTHER COST
            # -------------------------------------------------

            if hasattr(
                Project,
                "other_cost"
            ):

                project_data["other_cost"] = other_cost

            # -------------------------------------------------
            # CREATE PROJECT
            # -------------------------------------------------

            Project.objects.create(
                **project_data
            )

            messages.success(
                request,
                f"Project '{project_name}' created successfully."
            )

            return redirect("projects")

        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):

            messages.error(
                request,
                "Please enter valid numeric values for project costs."
            )

            return redirect("add_project")

        except Exception as e:

            messages.error(
                request,
                f"Unable to create project: {str(e)}"
            )

            return redirect("add_project")

    return redirect("add_project")


# =========================================================
# EDIT PROJECT
# =========================================================

@login_required(login_url="login")
def edit_project(
    request,
    project_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to edit projects."
        )

        return redirect("employee_dashboard")

    project = get_object_or_404(
        Project,
        id=project_id
    )

    clients = Client.objects.filter(
        status="active"
    ).order_by(
        "name"
    )

    employees = User.objects.filter(
        role="employee",
        is_active=True
    ).order_by(
        "first_name",
        "last_name"
    )

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    if request.method == "POST":

        project_name = request.POST.get(
            "project_name",
            ""
        ).strip()

        project_code = request.POST.get(
            "project_code",
            ""
        ).strip()

        client_id = request.POST.get(
            "client",
            ""
        ).strip()

        # -------------------------------------------------
        # BASIC VALIDATION
        # -------------------------------------------------

        if not project_name:

            messages.error(
                request,
                "Project name is required."
            )

            return redirect(
                "edit_project",
                project_id=project.id
            )

        if not client_id:

            messages.error(
                request,
                "Client is required."
            )

            return redirect(
                "edit_project",
                project_id=project.id
            )

        # -------------------------------------------------
        # PROJECT CODE
        # -------------------------------------------------

        if project_code and Project.objects.filter(
            project_code=project_code
        ).exclude(
            id=project.id
        ).exists():

            messages.error(
                request,
                "Project code already exists."
            )

            return redirect(
                "edit_project",
                project_id=project.id
            )

        client = get_object_or_404(
            Client,
            id=client_id,
            status="active"
        )

        # -------------------------------------------------
        # TEAM MEMBERS
        # -------------------------------------------------

        project_manager_id = request.POST.get(
            "project_manager",
            ""
        ).strip()

        designer_id = request.POST.get(
            "designer",
            ""
        ).strip()

        developer_id = request.POST.get(
            "developer",
            ""
        ).strip()

        tester_id = request.POST.get(
            "tester",
            ""
        ).strip()

        project_manager = None
        designer = None
        developer = None
        tester = None

        if project_manager_id:

            project_manager = get_object_or_404(
                User,
                id=project_manager_id,
                role="employee",
                is_active=True
            )

        if designer_id:

            designer = get_object_or_404(
                User,
                id=designer_id,
                role="employee",
                is_active=True
            )

        if developer_id:

            developer = get_object_or_404(
                User,
                id=developer_id,
                role="employee",
                is_active=True
            )

        if tester_id:

            tester = get_object_or_404(
                User,
                id=tester_id,
                role="employee",
                is_active=True
            )

        # -------------------------------------------------
        # COSTS
        # -------------------------------------------------

        try:

            total_cost = Decimal(
                request.POST.get(
                    "total_cost",
                    "0"
                ) or "0"
            )

            designer_cost = Decimal(
                request.POST.get(
                    "designer_cost",
                    "0"
                ) or "0"
            )

            development_cost = Decimal(
                request.POST.get(
                    "development_cost",
                    "0"
                ) or "0"
            )

            # NEW
            paid_development_cost = Decimal(
                request.POST.get(
                    "paid_development_cost",
                    "0"
                ) or "0"
            )

            tester_cost = Decimal(
                request.POST.get(
                    "tester_cost",
                    "0"
                ) or "0"
            )

            other_cost = Decimal(
                request.POST.get(
                    "other_cost",
                    "0"
                ) or "0"
            )

        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):

            messages.error(
                request,
                "Please enter valid project cost amounts."
            )

            return redirect(
                "edit_project",
                project_id=project.id
            )

        # -------------------------------------------------
        # NEGATIVE COST VALIDATION
        # -------------------------------------------------

        if (
            total_cost < Decimal("0.00")
            or designer_cost < Decimal("0.00")
            or development_cost < Decimal("0.00")
            or paid_development_cost < Decimal("0.00")
            or tester_cost < Decimal("0.00")
            or other_cost < Decimal("0.00")
        ):

            messages.error(
                request,
                "Project costs cannot be negative."
            )

            return redirect(
                "edit_project",
                project_id=project.id
            )

        # -------------------------------------------------
        # PAID DEVELOPMENT COST VALIDATION
        # -----------------------------------------------------

        if paid_development_cost > development_cost:

            messages.error(
                request,
                "Paid development cost cannot be greater than development cost."
            )

            return redirect(
                "edit_project",
                project_id=project.id
            )

        # -------------------------------------------------
        # PROGRESS
        # -------------------------------------------------

        try:

            progress = int(
                request.POST.get(
                    "progress",
                    "0"
                ) or "0"
            )

        except (
            ValueError,
            TypeError
        ):

            progress = 0

        progress = max(
            0,
            min(progress, 100)
        )

        # -------------------------------------------------
        # ESTIMATED DAYS
        # -------------------------------------------------

        estimated_days_input = request.POST.get(
            "estimated_days",
            ""
        ).strip()

        estimated_days = None

        if estimated_days_input:

            try:

                estimated_days = int(
                    estimated_days_input
                )

                if estimated_days < 0:

                    estimated_days = None

            except (
                ValueError,
                TypeError
            ):

                messages.error(
                    request,
                    "Estimated days must be a valid number."
                )

                return redirect(
                    "edit_project",
                    project_id=project.id
                )

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        valid_statuses = [
            "planning",
            "in_progress",
            "testing",
            "on_hold",
            "completed",
            "cancelled",
        ]

        status = request.POST.get(
            "status",
            "planning"
        ).strip()

        if status not in valid_statuses:

            status = "planning"

        # -------------------------------------------------
        # PRIORITY
        # -------------------------------------------------

        valid_priorities = [
            "low",
            "medium",
            "high",
            "urgent",
        ]

        priority = request.POST.get(
            "priority",
            "medium"
        ).strip()

        if priority not in valid_priorities:

            priority = "medium"

        # -------------------------------------------------
        # PROJECT TYPE
        # -------------------------------------------------

        valid_project_types = [
            "website",
            "web_application",
            "mobile_application",
            "software",
            "ecommerce",
            "api",
            "maintenance",
            "other",
        ]

        project_type = request.POST.get(
            "project_type",
            "website"
        ).strip()

        if project_type not in valid_project_types:

            project_type = "website"

        # -------------------------------------------------
        # UPDATE PROJECT
        # -------------------------------------------------

        project.project_name = project_name

        project.project_code = (
            project_code
            if project_code
            else None
        )

        project.client = client

        project.project_type = project_type

        project.description = request.POST.get(
            "description",
            ""
        ).strip()

        project.requirements = request.POST.get(
            "requirements",
            ""
        ).strip()

        project.technology_stack = request.POST.get(
            "technology_stack",
            ""
        ).strip()

        # -------------------------------------------------
        # TEAM
        # -------------------------------------------------

        if hasattr(
            project,
            "project_manager"
        ):

            project.project_manager = project_manager

        project.designer = designer

        project.developer = developer

        project.tester = tester

        # -------------------------------------------------
        # COSTS
        # -------------------------------------------------

        project.total_cost = total_cost

        project.designer_cost = designer_cost

        project.development_cost = development_cost

        # NEW
        project.paid_development_cost = (
            paid_development_cost
        )

        project.tester_cost = tester_cost

        if hasattr(
            project,
            "other_cost"
        ):

            project.other_cost = other_cost

        # -------------------------------------------------
        # DATES
        # -------------------------------------------------

        project.start_date = (
            request.POST.get(
                "start_date"
            )
            or None
        )

        project.expected_end_date = (
            request.POST.get(
                "expected_end_date"
            )
            or None
        )

        if hasattr(
            project,
            "estimated_days"
        ):

            project.estimated_days = estimated_days

        project.actual_end_date = (
            request.POST.get(
                "actual_end_date"
            )
            or None
        )

        # -------------------------------------------------
        # STATUS / PRIORITY / PROGRESS
        # -------------------------------------------------

        project.status = status

        project.priority = priority

        project.progress = progress

        # -------------------------------------------------
        # NOTES
        # -------------------------------------------------

        project.notes = request.POST.get(
            "notes",
            ""
        ).strip()

        # -------------------------------------------------
        # DURATION
        # -------------------------------------------------

        if hasattr(
            project,
            "duration"
        ):

            project.duration = request.POST.get(
                "duration",
                ""
            ).strip()

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        project.save()

        messages.success(
            request,
            "Project details updated successfully."
        )

        return redirect("projects")

    # -----------------------------------------------------
    # GET / EDIT PAGE
    # -----------------------------------------------------

    return render(
        request,
        "admin/edit_project.html",
        {
            "project": project,

            "clients": clients,

            "employees": employees,

            "status_choices": (
                Project.STATUS_CHOICES
            ),

            "priority_choices": (
                Project.PRIORITY_CHOICES
            ),

            "project_type_choices": (
                Project.PROJECT_TYPE_CHOICES
            ),
        }
    )


# =========================================================
# DELETE PROJECT
# =========================================================

@login_required(login_url="login")
def delete_project(
    request,
    project_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to delete projects."
        )

        return redirect("employee_dashboard")

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == "POST":

        project_name = project.project_name

        project.delete()

        messages.success(
            request,
            f"Project {project_name} deleted successfully."
        )

        return redirect("projects")

    return redirect("projects")
# =========================================================
# ADMIN TASKS
# =========================================================

@login_required(login_url="login")
def tasks(request):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to access tasks."
        )

        return redirect("employee_dashboard")

    task_list = Task.objects.select_related(
        "assigned_to",
        "project",
        "project__client"
    ).prefetch_related(
        "comments__user"
    ).order_by(
        "-task_date",
        "-created_at"
    )

    # =====================================================
    # SEARCH
    # =====================================================

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        task_list = task_list.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(assigned_to__first_name__icontains=search)
            | Q(assigned_to__last_name__icontains=search)
            | Q(project__project_name__icontains=search)
        )

    # =====================================================
    # STATUS FILTER
    # =====================================================

    selected_status = request.GET.get(
        "status",
        ""
    ).strip()

    if selected_status in [
        "pending",
        "in_progress",
        "completed"
    ]:

        task_list = task_list.filter(
            status=selected_status
        )

    # =====================================================
    # STATISTICS
    # =====================================================

    all_tasks = Task.objects.all()

    total_tasks = all_tasks.count()

    pending_tasks = all_tasks.filter(
        status="pending"
    ).count()

    in_progress_tasks = all_tasks.filter(
        status="in_progress"
    ).count()

    completed_tasks = all_tasks.filter(
        status="completed"
    ).count()

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "tasks": task_list,

        "total_tasks": total_tasks,

        "pending_tasks": pending_tasks,

        "in_progress_tasks": in_progress_tasks,

        "completed_tasks": completed_tasks,

        "filtered_task_count": task_list.count(),

        "search": search,

        "selected_status": selected_status,
    }

    return render(
        request,
        "admin/tasks.html",
        context
    )

# =========================================================
# ADMIN TASKS ALIAS
# =========================================================

@login_required(login_url="login")
def admin_tasks(request):

    return tasks(request)

# =========================================================
# PROJECT TASK DETAILS
# =========================================================

@login_required(login_url="login")
def project_task_details(request, task_id):

    # Admin only
    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to view task details."
        )

        return redirect("employee_dashboard")

    task = get_object_or_404(
        Task.objects.select_related(
            "project",
            "assigned_to",
            "project__client"
        ).prefetch_related(
            "comments__user"
        ),
        id=task_id
    )

    return render(
        request,
        "admin/project_task_details.html",
        {
            "task": task,
        }
    )
    
    # =========================================================
# DELETE PROJECT TASK
# =========================================================

@login_required(login_url="login")
def delete_project_task(request, task_id):

    # =====================================================
    # ADMIN ACCESS CHECK
    # =====================================================

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to delete tasks."
        )

        return redirect("employee_dashboard")

    # =====================================================
    # GET TASK
    # =====================================================

    task = get_object_or_404(
        Task,
        id=task_id
    )

    # =====================================================
    # SAVE PROJECT ID
    # =====================================================

    project_id = task.project.id

    # =====================================================
    # DELETE TASK
    # =====================================================

    task.delete()

    messages.success(
        request,
        "Task deleted successfully."
    )

    # =====================================================
    # REDIRECT TO SAME PROJECT TASKS PAGE
    # =====================================================

    return redirect(
        "project_tasks",
        project_id=project_id
    )
    # =========================================================
# PROJECT TASK ADMIN COMMENT
# =========================================================

@login_required(login_url="login")
def project_task_admin_comment(request, task_id):

    # =====================================================
    # ADMIN ACCESS CHECK
    # =====================================================

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to add admin comments."
        )

        return redirect("admin_dashboard")

    # =====================================================
    # ONLY POST ALLOWED
    # =====================================================

    if request.method != "POST":

        return redirect("admin_dashboard")

    # =====================================================
    # GET TASK
    # =====================================================

    task = get_object_or_404(
        Task,
        id=task_id
    )

    # =====================================================
    # GET COMMENT
    # =====================================================

    comment_text = request.POST.get(
        "comment",
        ""
    ).strip()

    # =====================================================
    # EMPTY COMMENT CHECK
    # =====================================================

    if not comment_text:

        messages.error(
            request,
            "Comment cannot be empty."
        )

        return redirect(
            "project_tasks",
            project_id=task.project.id
        )

    # =====================================================
    # CREATE ADMIN COMMENT
    # =====================================================

    TaskComment.objects.create(
        task=task,
        user=request.user,
        comment=comment_text
    )

    # =====================================================
    # SUCCESS MESSAGE
    # =====================================================

    messages.success(
        request,
        "Admin comment added successfully."
    )

    # =====================================================
    # STAY ON PROJECT TASKS PAGE
    # =====================================================

    return redirect(
        "project_tasks",
        project_id=task.project.id
    )
    
    # =========================================================
# EDIT PROJECT TASK
# =========================================================

@login_required(login_url="login")
def edit_project_task(request, task_id):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to edit tasks."
        )

        return redirect("employee_dashboard")

    task = get_object_or_404(
        Task.objects.select_related(
            "project",
            "assigned_to"
        ),
        id=task_id
    )

    projects = Project.objects.all().order_by(
        "project_name"
    )

    employees = User.objects.filter(
        role="employee"
    ).order_by(
        "first_name",
        "last_name"
    )

    # =====================================================
    # UPDATE TASK
    # =====================================================

    if request.method == "POST":

        task.title = request.POST.get(
            "title",
            ""
        ).strip()

        task.description = request.POST.get(
            "description",
            ""
        ).strip()

        project_id = request.POST.get(
            "project"
        )

        assigned_to_id = request.POST.get(
            "assigned_to"
        )

        task_date = request.POST.get(
            "task_date"
        )

        due_time = request.POST.get(
            "due_time"
        )

        task.priority = request.POST.get(
            "priority",
            "medium"
        )

        task.status = request.POST.get(
            "status",
            "pending"
        )

        # =================================================
        # PROJECT
        # =================================================

        if project_id:

            task.project = get_object_or_404(
                Project,
                id=project_id
            )

        else:

            task.project = None

        # =================================================
        # EMPLOYEE
        # =================================================

        if assigned_to_id:

            task.assigned_to = get_object_or_404(
                User,
                id=assigned_to_id,
                role="employee"
            )

        else:

            task.assigned_to = None

        # =================================================
        # DATE / TIME
        # =================================================

        task.task_date = task_date or None

        task.due_time = due_time or None

        # =================================================
        # SAVE
        # =================================================

        task.save()

        messages.success(
            request,
            "Task updated successfully."
        )

        # =================================================
        # BACK TO PROJECT TASKS
        # =================================================

        if task.project:

            return redirect(
                "project_tasks",
                project_id=task.project.id
            )

        return redirect("tasks")

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "task": task,

        "projects": projects,

        "employees": employees,

        "project": task.project,

    }

    return render(
        request,
        "admin/edit_project_task.html",
        context
    )
# =========================================================
# ADD PROJECT TASK
# =========================================================

@login_required(login_url="login")
def add_project_tasks(request, project_id):

    # =====================================================
    # ADMIN ACCESS CHECK
    # =====================================================

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to add project tasks."
        )

        return redirect(
            "employee_dashboard"
        )

    # =====================================================
    # GET PROJECT
    # =====================================================

    project = get_object_or_404(
        Project,
        id=project_id
    )

    # =====================================================
    # GET EMPLOYEES
    # =====================================================

    employees = User.objects.filter(
        role="employee",
        is_active=True
    ).order_by(
        "first_name",
        "last_name"
    )

    # =====================================================
    # HANDLE FORM SUBMISSION
    # =====================================================

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        assigned_to_id = request.POST.get(
            "assigned_to",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        task_date = request.POST.get(
            "task_date",
            ""
        ).strip()

        due_time = request.POST.get(
            "due_time",
            ""
        ).strip()

        priority = request.POST.get(
            "priority",
            "medium"
        ).strip()

        # =================================================
        # VALIDATION
        # =================================================

        if not title:

            messages.error(
                request,
                "Task title is required."
            )

            return render(
                request,
                "admin/add_project_tasks.html",
                {
                    "project": project,
                    "employees": employees,
                }
            )

        if not assigned_to_id:

            messages.error(
                request,
                "Please select an employee."
            )

            return render(
                request,
                "admin/add_project_tasks.html",
                {
                    "project": project,
                    "employees": employees,
                }
            )

        if not task_date:

            messages.error(
                request,
                "Task date is required."
            )

            return render(
                request,
                "admin/add_project_tasks.html",
                {
                    "project": project,
                    "employees": employees,
                }
            )

        # =================================================
        # GET EMPLOYEE
        # =================================================

        employee = get_object_or_404(
            User,
            id=assigned_to_id,
            role="employee",
            is_active=True
        )

        # =================================================
        # CREATE TASK
        # =================================================

        task = Task.objects.create(

            title=title,

            description=description,

            project=project,

            assigned_to=employee,

            task_date=task_date,

            due_time=due_time or None,

            priority=priority,

            status="pending",
        )

        # =================================================
        # SEND EMAIL TO EMPLOYEE
        # =================================================

        if employee.email:

            employee_name = (
                employee.get_full_name()
                or employee.username
            )

            assigned_by = (
                request.user.get_full_name()
                or request.user.username
            )

            # =================================================
            # PLAIN TEXT EMAIL
            # =================================================

            email_message = f"""
Hello {employee_name},

A new task has been assigned to you in E-Office Webcodeft Tech.

Task Details
----------------------------------------

Task: {task.title}

Project: {project.project_name}

Description:
{task.description or "No description provided."}

Task Date: {task.task_date}

Due Time: {task.due_time or "Not specified"}

Priority: {task.priority.replace("_", " ").title()}

Status: {task.status.replace("_", " ").title()}

Assigned By: {assigned_by}

----------------------------------------

Please log in to E-Office Webcodeft Tech to view and manage this task.

Regards,
Sandeep Sharma
E-Office Webcodeft Tech

Global Contracts For Digital Services & Software Consulting
"""

            # =================================================
            # HTML EMAIL
            # =================================================

            html_message = f"""
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>New Task Assigned - E-Office Webcodeft Tech</title>

</head>


<body style="
    margin:0;
    padding:0;
    background-color:#f4f5f7;
    font-family:Arial, Helvetica, sans-serif;
">


<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        background-color:#f4f5f7;
    "
>

    <tr>

        <td
            align="center"
            style="
                padding:30px 15px;
            "
        >


            <!-- =================================================
                 EMAIL CARD
            ================================================== -->

            <table
                width="650"
                cellpadding="0"
                cellspacing="0"
                border="0"
                style="
                    max-width:650px;
                    width:100%;
                    background:#ffffff;
                    border-radius:12px;
                    overflow:hidden;
                "
            >


                <!-- =================================================
                     HEADER
                     NO LOGO
                ================================================== -->

                <tr>

                    <td
                        align="center"
                        style="
                            padding:24px 20px;
                            background:#111111;
                            color:#ffffff;
                        "
                    >

                        <h2
                            style="
                                margin:0;
                                font-size:24px;
                                line-height:1.3;
                                font-weight:600;
                            "
                        >
                            New Task Assigned
                        </h2>

                        <p
                            style="
                                margin:7px 0 0 0;
                                color:#cccccc;
                                font-size:12px;
                                line-height:1.5;
                            "
                        >
                            E-Office Webcodeft Tech
                        </p>

                    </td>

                </tr>


                <!-- =================================================
                     CONTENT
                ================================================== -->

                <tr>

                    <td
                        style="
                            padding:30px;
                            color:#333333;
                        "
                    >


                        <!-- GREETING -->

                        <p
                            style="
                                margin:0 0 15px 0;
                                font-size:15px;
                                line-height:1.6;
                            "
                        >

                            Hello
                            <strong>
                                {employee_name}
                            </strong>,

                        </p>


                        <!-- MESSAGE -->

                        <p
                            style="
                                margin:0 0 25px 0;
                                font-size:15px;
                                line-height:1.6;
                                color:#444444;
                            "
                        >

                            A new task has been assigned to you
                            in <strong>E-Office Webcodeft Tech</strong>.

                        </p>


                        <!-- =================================================
                             TASK DETAILS
                        ================================================== -->

                        <table
                            width="100%"
                            cellpadding="0"
                            cellspacing="0"
                            border="0"
                            style="
                                border-collapse:collapse;
                                width:100%;
                            "
                        >


                            <!-- TASK -->

                            <tr>

                                <td
                                    style="
                                        padding:12px;
                                        background:#f7f7f7;
                                        font-weight:bold;
                                        width:35%;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                    "
                                >
                                    Task
                                </td>

                                <td
                                    style="
                                        padding:12px;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                        color:#333333;
                                    "
                                >
                                    {task.title}
                                </td>

                            </tr>


                            <!-- PROJECT -->

                            <tr>

                                <td
                                    style="
                                        padding:12px;
                                        background:#f7f7f7;
                                        font-weight:bold;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                    "
                                >
                                    Project
                                </td>

                                <td
                                    style="
                                        padding:12px;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                        color:#333333;
                                    "
                                >
                                    {project.project_name}
                                </td>

                            </tr>


                            <!-- TASK DATE -->

                            <tr>

                                <td
                                    style="
                                        padding:12px;
                                        background:#f7f7f7;
                                        font-weight:bold;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                    "
                                >
                                    Task Date
                                </td>

                                <td
                                    style="
                                        padding:12px;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                        color:#333333;
                                    "
                                >
                                    {task.task_date}
                                </td>

                            </tr>


                            <!-- DUE TIME -->

                            <tr>

                                <td
                                    style="
                                        padding:12px;
                                        background:#f7f7f7;
                                        font-weight:bold;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                    "
                                >
                                    Due Time
                                </td>

                                <td
                                    style="
                                        padding:12px;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                        color:#333333;
                                    "
                                >
                                    {task.due_time or "Not specified"}
                                </td>

                            </tr>


                            <!-- PRIORITY -->

                            <tr>

                                <td
                                    style="
                                        padding:12px;
                                        background:#f7f7f7;
                                        font-weight:bold;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                    "
                                >
                                    Priority
                                </td>

                                <td
                                    style="
                                        padding:12px;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                        color:#333333;
                                    "
                                >
                                    {task.priority.replace("_", " ").title()}
                                </td>

                            </tr>


                            <!-- STATUS -->

                            <tr>

                                <td
                                    style="
                                        padding:12px;
                                        background:#f7f7f7;
                                        font-weight:bold;
                                        font-size:14px;
                                    "
                                >
                                    Status
                                </td>

                                <td
                                    style="
                                        padding:12px;
                                        font-size:14px;
                                        color:#333333;
                                    "
                                >
                                    {task.status.replace("_", " ").title()}
                                </td>

                            </tr>


                        </table>


                        <!-- =================================================
                             DESCRIPTION
                        ================================================== -->

                        <div
                            style="
                                background:#f7f7f7;
                                padding:18px;
                                border-radius:8px;
                                margin-top:20px;
                            "
                        >

                            <p
                                style="
                                    margin:0 0 8px 0;
                                    font-weight:bold;
                                    font-size:15px;
                                    color:#222222;
                                "
                            >
                                Description
                            </p>


                            <p
                                style="
                                    margin:0;
                                    font-size:14px;
                                    line-height:1.6;
                                    color:#555555;
                                "
                            >

                                {task.description or "No description provided."}

                            </p>

                        </div>


                        <!-- =================================================
                             LOGIN MESSAGE
                        ================================================== -->

                        <p
                            style="
                                margin:25px 0 0 0;
                                font-size:14px;
                                line-height:1.6;
                                color:#555555;
                            "
                        >

                            Please log in to
                            <strong>
                                E-Office Webcodeft Tech
                            </strong>
                            to view and manage this task.

                        </p>


                        <!-- =================================================
                             SIGNATURE
                        ================================================== -->

                        <p
                            style="
                                margin:25px 0 0 0;
                                font-size:14px;
                                line-height:1.7;
                                color:#333333;
                            "
                        >

                            Thanks &amp; Regards..!!<br><br>

                            <strong
                                style="
                                    font-size:16px;
                                "
                            >
                                Sandeep Sharma
                            </strong>

                            <br>

                            E-Office Webcodeft Tech

                        </p>


                    </td>

                </tr>


                <!-- =================================================
                     SIGNATURE LOGO SECTION
                     LOGO LIKE EMAIL SIGNATURE
                ================================================== -->

                <tr>

                    <td
                        align="left"
                        style="
                            background:#ffffff;
                            padding:0 30px 28px 30px;
                        "
                    >


                        <!-- LOGO -->

                        <img
                            src="cid:webcodeft_logo"
                            alt="Webcodeft Technologies"
                            style="
                                display:block;
                                width:180px;
                                max-width:180px;
                                height:auto;
                                margin:0;
                                border:0;
                                outline:none;
                                text-decoration:none;
                            "
                        >


                        <!-- TAGLINE -->

                        <p
                            style="
                                margin:12px 0 0 0;
                                font-size:15px;
                                line-height:1.5;
                                color:#333333;
                            "
                        >

                            Global Contracts For Digital Services
                            <br>
                            &amp; Software Consulting

                        </p>


                    </td>

                </tr>


                <!-- =================================================
                     FOOTER
                ================================================== -->

                <tr>

                    <td
                        align="center"
                        style="
                            padding:18px 20px;
                            background:#111111;
                        "
                    >

                        <p
                            style="
                                margin:0;
                                color:#ffffff;
                                font-size:12px;
                                line-height:1.5;
                            "
                        >

                            E-Office Webcodeft Tech

                        </p>

                    </td>

                </tr>


            </table>

        </td>

    </tr>

</table>


</body>

</html>
"""


            # =================================================
            # CREATE EMAIL
            # =================================================

            email = EmailMultiAlternatives(

                subject=f"New Task Assigned: {task.title}",

                body=email_message,

                from_email=settings.DEFAULT_FROM_EMAIL,

                to=[employee.email],
            )


            # =================================================
            # ADD HTML VERSION
            # =================================================

            email.attach_alternative(
                html_message,
                "text/html"
            )


            # =================================================
            # ADD LOGO INLINE
            # =================================================

            logo_path = (
                r"C:\Projects\OfficeManagementSystem"
                r"\static\images\Webcodeft-logo-Copy.png"
            )

            try:

                with open(
                    logo_path,
                    "rb"
                ) as logo_file:

                    logo = MIMEImage(
                        logo_file.read(),
                        _subtype="png"
                    )

                    logo.add_header(
                        "Content-ID",
                        "<webcodeft_logo>"
                    )

                    logo.add_header(
                        "Content-Disposition",
                        "inline",
                        filename="Webcodeft-logo-Copy.png"
                    )

                    email.attach(
                        logo
                    )

            except FileNotFoundError:

                pass


            # =================================================
            # SEND EMAIL
            # =================================================

            email.send(
                fail_silently=False
            )


        # =====================================================
        # SUCCESS MESSAGE
        # =====================================================

        messages.success(
            request,
            f"Task '{title}' has been assigned successfully."
        )

        return redirect(
            "project_tasks",
            project_id=project.id
        )


    # =====================================================
    # GET REQUEST
    # =====================================================

    context = {
        "project": project,
        "employees": employees,
    }

    return render(
        request,
        "admin/add_project_tasks.html",
        context
    )



# =========================================================
# ADD TASK
# =========================================================

@login_required(login_url="login")
def add_task(request):

    # =====================================================
    # ADMIN ACCESS CHECK
    # =====================================================

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to add tasks."
        )

        return redirect(
            "employee_dashboard"
        )

    # =====================================================
    # GET EMPLOYEES
    # =====================================================

    employee_list = User.objects.filter(
        role="employee",
        is_active=True
    ).order_by(
        "first_name",
        "last_name"
    )

    # =====================================================
    # GET PROJECTS
    # =====================================================

    project_list = Project.objects.select_related(
        "client"
    ).order_by(
        "project_name"
    )

    # =====================================================
    # HANDLE FORM SUBMISSION
    # =====================================================

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        assigned_to_id = request.POST.get(
            "assigned_to",
            ""
        ).strip()

        project_id = request.POST.get(
            "project",
            ""
        ).strip()

        task_date = request.POST.get(
            "task_date",
            ""
        ).strip()

        due_time = request.POST.get(
            "due_time",
            ""
        ).strip()

        priority = request.POST.get(
            "priority",
            "medium"
        ).strip()

        status = request.POST.get(
            "status",
            "pending"
        ).strip()


        # =================================================
        # VALIDATION
        # =================================================

        if not title:

            messages.error(
                request,
                "Task title is required."
            )

            return redirect(
                "add_task"
            )


        if not assigned_to_id:

            messages.error(
                request,
                "Please select an employee."
            )

            return redirect(
                "add_task"
            )


        if not project_id:

            messages.error(
                request,
                "Please select a project."
            )

            return redirect(
                "add_task"
            )


        if not task_date:

            messages.error(
                request,
                "Task date is required."
            )

            return redirect(
                "add_task"
            )


        # =================================================
        # GET EMPLOYEE
        # =================================================

        employee = get_object_or_404(
            User,
            id=assigned_to_id,
            role="employee",
            is_active=True
        )


        # =================================================
        # GET PROJECT
        # =================================================

        project = get_object_or_404(
            Project,
            id=project_id
        )


        # =================================================
        # VALID PRIORITY
        # =================================================

        valid_priorities = [
            "low",
            "medium",
            "high",
            "urgent"
        ]

        if priority not in valid_priorities:

            priority = "medium"


        # =================================================
        # VALID STATUS
        # =================================================

        valid_statuses = [
            "pending",
            "in_progress",
            "completed"
        ]

        if status not in valid_statuses:

            status = "pending"


        # =================================================
        # CREATE TASK
        # =================================================

        task = Task.objects.create(

            title=title,

            description=description,

            assigned_to=employee,

            project=project,

            task_date=task_date,

            due_time=due_time or None,

            priority=priority,

            status=status
        )


        # =================================================
        # SEND EMAIL TO EMPLOYEE
        # =================================================

        if employee.email:

            employee_name = (
                employee.get_full_name()
                or employee.username
            )

            assigned_by = (
                request.user.get_full_name()
                or request.user.username
            )


            # =================================================
            # PLAIN TEXT EMAIL
            # =================================================

            email_message = f"""
Hello {employee_name},

A new task has been assigned to you in E-Office Webcodeft Tech.

Task Details
----------------------------------------

Task: {task.title}

Project: {project.project_name}

Description:
{task.description or "No description provided."}

Task Date: {task.task_date}

Due Time: {task.due_time or "Not specified"}

Priority: {task.priority.replace("_", " ").title()}

Status: {task.status.replace("_", " ").title()}

Assigned By: {assigned_by}

----------------------------------------

Please log in to E-Office Webcodeft Tech to view and manage this task.

Regards,
Sandeep Sharma
E-Office Webcodeft Tech

Global Contracts For Digital Services & Software Consulting
"""


            # =================================================
            # HTML EMAIL
            # =================================================

            html_message = f"""
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>New Task Assigned - E-Office Webcodeft Tech</title>

</head>


<body style="
    margin:0;
    padding:0;
    background-color:#f4f5f7;
    font-family:Arial, Helvetica, sans-serif;
">


<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        background-color:#f4f5f7;
    "
>

    <tr>

        <td
            align="center"
            style="
                padding:30px 15px;
            "
        >


            <!-- =================================================
                 EMAIL CARD
            ================================================== -->

            <table
                width="650"
                cellpadding="0"
                cellspacing="0"
                border="0"
                style="
                    max-width:650px;
                    width:100%;
                    background:#ffffff;
                    border-radius:12px;
                    overflow:hidden;
                "
            >


                <!-- =================================================
                     HEADER
                     NO LOGO
                ================================================== -->

                <tr>

                    <td
                        align="center"
                        style="
                            padding:24px 20px;
                            background:#111111;
                            color:#ffffff;
                        "
                    >

                        <h2
                            style="
                                margin:0;
                                font-size:24px;
                                line-height:1.3;
                                font-weight:600;
                            "
                        >
                            New Task Assigned
                        </h2>

                        <p
                            style="
                                margin:7px 0 0 0;
                                color:#cccccc;
                                font-size:12px;
                                line-height:1.5;
                            "
                        >
                            E-Office Webcodeft Tech
                        </p>

                    </td>

                </tr>


                <!-- =================================================
                     CONTENT
                ================================================== -->

                <tr>

                    <td
                        style="
                            padding:30px;
                            color:#333333;
                        "
                    >


                        <!-- GREETING -->

                        <p
                            style="
                                margin:0 0 15px 0;
                                font-size:15px;
                                line-height:1.6;
                            "
                        >

                            Hello
                            <strong>
                                {employee_name}
                            </strong>,

                        </p>


                        <!-- MESSAGE -->

                        <p
                            style="
                                margin:0 0 25px 0;
                                font-size:15px;
                                line-height:1.6;
                                color:#444444;
                            "
                        >

                            A new task has been assigned to you
                            in <strong>E-Office Webcodeft Tech</strong>.

                        </p>


                        <!-- =================================================
                             TASK DETAILS
                        ================================================== -->

                        <table
                            width="100%"
                            cellpadding="0"
                            cellspacing="0"
                            border="0"
                            style="
                                border-collapse:collapse;
                                width:100%;
                            "
                        >


                            <!-- TASK -->

                            <tr>

                                <td
                                    style="
                                        padding:12px;
                                        background:#f7f7f7;
                                        font-weight:bold;
                                        width:35%;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                    "
                                >
                                    Task
                                </td>

                                <td
                                    style="
                                        padding:12px;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                        color:#333333;
                                    "
                                >
                                    {task.title}
                                </td>

                            </tr>


                            <!-- PROJECT -->

                            <tr>

                                <td
                                    style="
                                        padding:12px;
                                        background:#f7f7f7;
                                        font-weight:bold;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                    "
                                >
                                    Project
                                </td>

                                <td
                                    style="
                                        padding:12px;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                        color:#333333;
                                    "
                                >
                                    {project.project_name}
                                </td>

                            </tr>


                            <!-- TASK DATE -->

                            <tr>

                                <td
                                    style="
                                        padding:12px;
                                        background:#f7f7f7;
                                        font-weight:bold;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                    "
                                >
                                    Task Date
                                </td>

                                <td
                                    style="
                                        padding:12px;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                        color:#333333;
                                    "
                                >
                                    {task.task_date}
                                </td>

                            </tr>


                            <!-- DUE TIME -->

                            <tr>

                                <td
                                    style="
                                        padding:12px;
                                        background:#f7f7f7;
                                        font-weight:bold;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                    "
                                >
                                    Due Time
                                </td>

                                <td
                                    style="
                                        padding:12px;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                        color:#333333;
                                    "
                                >
                                    {task.due_time or "Not specified"}
                                </td>

                            </tr>


                            <!-- PRIORITY -->

                            <tr>

                                <td
                                    style="
                                        padding:12px;
                                        background:#f7f7f7;
                                        font-weight:bold;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                    "
                                >
                                    Priority
                                </td>

                                <td
                                    style="
                                        padding:12px;
                                        border-bottom:1px solid #e5e5e5;
                                        font-size:14px;
                                        color:#333333;
                                    "
                                >
                                    {task.priority.replace("_", " ").title()}
                                </td>

                            </tr>


                            <!-- STATUS -->

                            <tr>

                                <td
                                    style="
                                        padding:12px;
                                        background:#f7f7f7;
                                        font-weight:bold;
                                        font-size:14px;
                                    "
                                >
                                    Status
                                </td>

                                <td
                                    style="
                                        padding:12px;
                                        font-size:14px;
                                        color:#333333;
                                    "
                                >
                                    {task.status.replace("_", " ").title()}
                                </td>

                            </tr>


                        </table>


                        <!-- =================================================
                             DESCRIPTION
                        ================================================== -->

                        <div
                            style="
                                background:#f7f7f7;
                                padding:18px;
                                border-radius:8px;
                                margin-top:20px;
                            "
                        >

                            <p
                                style="
                                    margin:0 0 8px 0;
                                    font-weight:bold;
                                    font-size:15px;
                                    color:#222222;
                                "
                            >
                                Description
                            </p>


                            <p
                                style="
                                    margin:0;
                                    font-size:14px;
                                    line-height:1.6;
                                    color:#555555;
                                "
                            >

                                {task.description or "No description provided."}

                            </p>

                        </div>


                        <!-- =================================================
                             LOGIN MESSAGE
                        ================================================== -->

                        <p
                            style="
                                margin:25px 0 0 0;
                                font-size:14px;
                                line-height:1.6;
                                color:#555555;
                            "
                        >

                            Please log in to
                            <strong>
                                E-Office Webcodeft Tech
                            </strong>
                            to view and manage this task.

                        </p>


                        <!-- =================================================
                             SIGNATURE
                        ================================================== -->

                        <p
                            style="
                                margin:25px 0 0 0;
                                font-size:14px;
                                line-height:1.7;
                                color:#333333;
                            "
                        >

                            Thanks &amp; Regards..!!<br><br>

                            <strong
                                style="
                                    font-size:16px;
                                "
                            >
                                Sandeep Sharma
                            </strong>

                            <br>

                            E-Office Webcodeft Tech

                        </p>


                    </td>

                </tr>


                <!-- =================================================
                     SIGNATURE LOGO
                ================================================== -->

                <tr>

                    <td
                        align="left"
                        style="
                            background:#ffffff;
                            padding:0 30px 28px 30px;
                        "
                    >


                        <!-- LOGO -->

                        <img
                            src="cid:webcodeft_logo"
                            alt="Webcodeft Technologies"
                            style="
                                display:block;
                                width:80px;
                                max-width:180px;
                                height:auto;
                                margin:0;
                                border:0;
                                outline:none;
                                text-decoration:none;
                            "
                        >


                        <!-- TAGLINE -->

                        <p
                            style="
                                margin:12px 0 0 0;
                                font-size:15px;
                                line-height:1.5;
                                color:#333333;
                            "
                        >

                            Global Contracts For Digital Services
                            <br>
                            &amp; Software Consulting

                        </p>


                    </td>

                </tr>


                <!-- =================================================
                     FOOTER
                ================================================== -->

                <tr>

                    <td
                        align="center"
                        style="
                            padding:18px 20px;
                            background:#111111;
                        "
                    >

                        <p
                            style="
                                margin:0;
                                color:#ffffff;
                                font-size:12px;
                                line-height:1.5;
                            "
                        >

                            E-Office Webcodeft Tech

                        </p>

                    </td>

                </tr>


            </table>

        </td>

    </tr>

</table>


</body>

</html>
"""


            # =================================================
            # CREATE EMAIL
            # =================================================

            email = EmailMultiAlternatives(

                subject=f"New Task Assigned: {task.title}",

                body=email_message,

                from_email=settings.DEFAULT_FROM_EMAIL,

                to=[employee.email],
            )


            # =================================================
            # ADD HTML VERSION
            # =================================================

            email.attach_alternative(
                html_message,
                "text/html"
            )


            # =================================================
            # ADD LOGO INLINE
            # =================================================

            logo_path = (
                r"C:\Projects\OfficeManagementSystem"
                r"\static\images\Webcodeft-logo-Copy.png"
            )

            try:

                with open(
                    logo_path,
                    "rb"
                ) as logo_file:

                    logo = MIMEImage(
                        logo_file.read(),
                        _subtype="png"
                    )

                    logo.add_header(
                        "Content-ID",
                        "<webcodeft_logo>"
                    )

                    logo.add_header(
                        "Content-Disposition",
                        "inline",
                        filename="Webcodeft-logo-Copy.png"
                    )

                    email.attach(
                        logo
                    )

            except FileNotFoundError:

                pass


            # =================================================
            # SEND EMAIL
            # =================================================

            email.send(
                fail_silently=False
            )


        # =====================================================
        # SUCCESS MESSAGE
        # =====================================================

        messages.success(
            request,
            "Task assigned successfully."
        )

        return redirect(
            "tasks"
        )


    # =====================================================
    # GET REQUEST
    # =====================================================

    return render(
        request,
        "admin/add_task.html",
        {
            "employees": employee_list,
            "projects": project_list,
            "today": timezone.localdate()
        }
    )
def project_tasks(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    # Only tasks belonging to this project
    tasks = Task.objects.filter(
        project=project
    ).order_by('-id')

    # Project-wise task statistics
    total_tasks = tasks.count()

    pending_tasks = tasks.filter(
        status='pending'
    ).count()

    in_progress_tasks = tasks.filter(
        status='in_progress'
    ).count()

    completed_tasks = tasks.filter(
        status='completed'
    ).count()

    return render(
        request,
        'admin/project_tasks.html',
        {
            'project': project,
            'tasks': tasks,

            'total_tasks': total_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'completed_tasks': completed_tasks,
        }
    )
# =========================================================
# TASK DETAIL
# =========================================================

@login_required(login_url="login")
def task_detail(
    request,
    task_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to view task details."
        )

        return redirect("employee_dashboard")

    task = get_object_or_404(
        Task.objects.select_related(
            "assigned_to",
            "project",
            "project__client"
        ),
        id=task_id
    )

    return render(
        request,
        "admin/task_detail.html",
        {
            "task": task
        }
    )


# =========================================================
# ADMIN TASK COMMENT
# =========================================================

@login_required(login_url="login")
def admin_task_comment(request, task_id):

    # =====================================================
    # ADMIN ONLY
    # =====================================================

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to comment on tasks."
        )

        return redirect("employee_dashboard")

    # =====================================================
    # GET TASK
    # =====================================================

    task = get_object_or_404(
        Task,
        id=task_id
    )

    # =====================================================
    # SAVE COMMENT
    # =====================================================

    if request.method == "POST":

        comment_text = request.POST.get(
            "comment",
            ""
        ).strip()

        # ---------------------------------------------
        # EMPTY COMMENT CHECK
        # ---------------------------------------------

        if not comment_text:

            messages.error(
                request,
                "Comment cannot be empty."
            )

            return redirect("tasks")

        # ---------------------------------------------
        # SAVE ADMIN COMMENT
        # ---------------------------------------------

        TaskComment.objects.create(

            task=task,

            user=request.user,

            comment=comment_text

        )

        messages.success(
            request,
            "Admin comment added successfully."
        )

    # =====================================================
    # REDIRECT BACK TO TASKS
    # =====================================================

    return redirect("tasks")
# =========================================================
# EDIT TASK
# =========================================================

@login_required(login_url="login")
def edit_task(
    request,
    task_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to edit tasks."
        )

        return redirect("employee_dashboard")

    task = get_object_or_404(
        Task.objects.select_related(
            "assigned_to",
            "project",
            "project__client"
        ),
        id=task_id
    )

    employee_list = User.objects.filter(
        role="employee",
        is_active=True
    ).order_by(
        "first_name",
        "last_name"
    )

    project_list = Project.objects.select_related(
        "client"
    ).order_by(
        "project_name"
    )

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        assigned_to_id = request.POST.get(
            "assigned_to",
            ""
        ).strip()

        project_id = request.POST.get(
            "project",
            ""
        ).strip()

        task_date = request.POST.get(
            "task_date",
            ""
        ).strip()

        due_time = request.POST.get(
            "due_time",
            ""
        ).strip()

        priority = request.POST.get(
            "priority",
            "medium"
        ).strip()

        status = request.POST.get(
            "status",
            "pending"
        ).strip()

        if not title:

            messages.error(
                request,
                "Task title is required."
            )

            return redirect(
                "edit_task",
                task_id=task.id
            )

        if not assigned_to_id:

            messages.error(
                request,
                "Please select an employee."
            )

            return redirect(
                "edit_task",
                task_id=task.id
            )

        if not project_id:

            messages.error(
                request,
                "Please select a project."
            )

            return redirect(
                "edit_task",
                task_id=task.id
            )

        if not task_date:

            messages.error(
                request,
                "Task date is required."
            )

            return redirect(
                "edit_task",
                task_id=task.id
            )

        employee = get_object_or_404(
            User,
            id=assigned_to_id,
            role="employee",
            is_active=True
        )

        project = get_object_or_404(
            Project,
            id=project_id
        )

        valid_priorities = [
            "low",
            "medium",
            "high",
            "urgent"
        ]

        if priority not in valid_priorities:

            priority = "medium"

        valid_statuses = [
            "pending",
            "in_progress",
            "completed"
        ]

        if status not in valid_statuses:

            status = "pending"

        task.title = title

        task.description = description

        task.assigned_to = employee

        task.project = project

        task.task_date = task_date

        task.due_time = (
            due_time
            if due_time
            else None
        )

        task.priority = priority

        task.status = status

        task.save()

        messages.success(
            request,
            "Task details updated successfully."
        )

        return redirect("tasks")

    return render(
        request,
        "admin/edit_task.html",
        {
            "task": task,

            "employees": employee_list,

            "projects": project_list,

            "today": timezone.localdate()
        }
    )


# =========================================================
# DELETE TASK
# =========================================================

@login_required(login_url="login")
def delete_task(
    request,
    task_id
):

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to delete tasks."
        )

        return redirect("employee_dashboard")

    task = get_object_or_404(
        Task,
        id=task_id
    )

    if request.method == "POST":

        task.delete()

        messages.success(
            request,
            "Task deleted successfully."
        )

        return redirect("tasks")

    return redirect("tasks")


# =========================================================
# EMPLOYEE DASHBOARD
# =========================================================

@login_required(login_url="login")
def employee_dashboard(request):

    if request.user.role != "employee":

        messages.error(
            request,
            "You are not authorized to access the Employee Dashboard."
        )

        return redirect("admin_dashboard")

    today = timezone.localdate()

    today_tasks = Task.objects.select_related(
        "project",
        "project__client"
    ).filter(
        assigned_to=request.user,
        task_date=today
    ).order_by(
        "due_time",
        "-created_at"
    )

    context = {

        "today": today,

        "today_tasks": today_tasks,

        "total_tasks": today_tasks.count(),

        "completed_tasks": today_tasks.filter(
            status="completed"
        ).count(),

        "pending_tasks": today_tasks.filter(
            status="pending"
        ).count(),

        "in_progress_tasks": today_tasks.filter(
            status="in_progress"
        ).count(),
    }

    return render(
        request,
        "employee/emp_dashboard.html",
        context
    )


# =========================================================
# EMPLOYEE ALL TASKS
# =========================================================

@login_required(login_url="login")
def employee_tasks(request):

    if request.user.role != "employee":

        messages.error(
            request,
            "You are not authorized to access your tasks."
        )

        return redirect("admin_dashboard")

    employee_all_tasks = Task.objects.filter(
        assigned_to_id=request.user.id
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    selected_status = request.GET.get(
        "status",
        ""
    ).strip()

    all_tasks = employee_all_tasks.select_related(
        "project",
        "project__client"
    ).order_by(
        "-task_date",
        "due_time",
        "-created_at"
    )

    if search:

        all_tasks = all_tasks.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(project__project_name__icontains=search)
        )

    if selected_status in [
        "pending",
        "in_progress",
        "completed"
    ]:

        all_tasks = all_tasks.filter(
            status=selected_status
        )

    total_tasks = employee_all_tasks.count()

    pending_tasks = employee_all_tasks.filter(
        status="pending"
    ).count()

    in_progress_tasks = employee_all_tasks.filter(
        status="in_progress"
    ).count()

    completed_tasks = employee_all_tasks.filter(
        status="completed"
    ).count()

    context = {

        "all_tasks": all_tasks,

        "total_tasks": total_tasks,

        "pending_tasks": pending_tasks,

        "in_progress_tasks": in_progress_tasks,

        "completed_tasks": completed_tasks,

        "filtered_task_count": all_tasks.count(),

        "search": search,

        "selected_status": selected_status,
    }

    return render(
        request,
        "employee/employee_tasks.html",
        context
    )


# =========================================================
# EMPLOYEE PROJECT DETAILS
# =========================================================

@login_required(login_url="login")
def employee_project_details(
    request,
    project_id
):

    if request.user.role != "employee":

        messages.error(
            request,
            "You are not authorized to access project details."
        )

        return redirect("admin_dashboard")

    project = get_object_or_404(
        Project,
        id=project_id
    )

    assigned_task = Task.objects.filter(
        project=project,
        assigned_to=request.user
    ).first()

    if not assigned_task:

        messages.error(
            request,
            "You are not authorized to view this project."
        )

        return redirect("employee_tasks")

    employee_tasks = Task.objects.filter(
        project=project,
        assigned_to=request.user
    )

    return render(
        request,
        "employee/project_details.html",
        {
            "project": project,
            "employee_tasks": employee_tasks,
        }
    )


# =========================================================
# EMPLOYEE TASK UPDATE
# =========================================================

@login_required(login_url="login")
def employee_task_update(
    request,
    task_id
):

    if request.user.role != "employee":

        messages.error(
            request,
            "You are not authorized to update this task."
        )

        return redirect("admin_dashboard")

    task = get_object_or_404(
        Task,
        id=task_id,
        assigned_to=request.user
    )

    if request.method == "POST":

        employee_comment = request.POST.get(
            "employee_comment",
            ""
        ).strip()

        remaining_days = request.POST.get(
            "remaining_days",
            ""
        ).strip()

        task.employee_comment = employee_comment

        if remaining_days:

            try:

                remaining_days = int(
                    remaining_days
                )

                if remaining_days < 0:

                    messages.error(
                        request,
                        "Remaining days cannot be negative."
                    )

                    return redirect("employee_tasks")

                task.remaining_days = remaining_days

            except ValueError:

                messages.error(
                    request,
                    "Please enter a valid number of remaining days."
                )

                return redirect("employee_tasks")

        else:

            task.remaining_days = None

        task.save()

        messages.success(
            request,
            "Task update saved successfully."
        )

        return redirect("employee_tasks")

    return redirect("employee_tasks")


# =========================================================
# UPDATE TASK STATUS
# =========================================================

@login_required(login_url="login")
def update_task_status(
    request,
    task_id
):

    if request.user.role != "employee":

        messages.error(
            request,
            "You are not authorized to update tasks."
        )

        return redirect("admin_dashboard")

    task = get_object_or_404(
        Task,
        id=task_id,
        assigned_to_id=request.user.id
    )

    if request.method == "POST":

        status = request.POST.get(
            "status",
            ""
        ).strip()

        if status in [
            "pending",
            "in_progress",
            "completed"
        ]:

            task.status = status

            task.save(
                update_fields=[
                    "status",
                    "updated_at"
                ]
            )

            messages.success(
                request,
                "Task status updated successfully."
            )

        else:

            messages.error(
                request,
                "Invalid task status."
            )

    return redirect("employee_tasks")


# =========================================================
# AUTOMATIC ABSENT AFTER 11:00 AM
# =========================================================

def mark_automatic_absent():

    # =====================================================
    # CURRENT DATE / TIME
    # =====================================================

    today = timezone.localdate()

    current_time = timezone.localtime().time().replace(
        second=0,
        microsecond=0
    )

    # =====================================================
    # ONLY RUN AFTER 11:00 AM
    # =====================================================

    if current_time <= CHECK_IN_END:
        return

    # =====================================================
    # ALL ACTIVE EMPLOYEES
    # =====================================================

    employees = User.objects.filter(
        role="employee",
        is_active=True
    )

    # =====================================================
    # PROCESS EACH EMPLOYEE
    # =====================================================

    for employee in employees:

        # -------------------------------------------------
        # CHECK TODAY'S ATTENDANCE
        # -------------------------------------------------

        attendance_exists = Attendance.objects.filter(
            employee=employee,
            date=today
        ).exists()

        # -------------------------------------------------
        # ATTENDANCE ALREADY EXISTS
        # -------------------------------------------------

        if attendance_exists:
            continue

        # -------------------------------------------------
        # CHECK APPROVED LEAVE
        # -------------------------------------------------

        approved_leave = Leave.objects.filter(
            employee=employee,
            leave_date=today,
            status="approved"
        ).exists()

        # -------------------------------------------------
        # APPROVED LEAVE
        # -------------------------------------------------

        if approved_leave:

            Attendance.objects.create(
                employee=employee,
                date=today,
                status="leave",
                check_in=None,
                check_out=None,
                remarks="Automatically marked Leave."
            )

            continue

        # -------------------------------------------------
        # NO ATTENDANCE + NO APPROVED LEAVE
        # = ABSENT
        # -------------------------------------------------

        Attendance.objects.create(
            employee=employee,
            date=today,
            status="absent",
            check_in=None,
            check_out=None,
            remarks="Automatically marked Absent after 11:00 AM."
        )

# =========================================================
# AUTOMATIC ABSENT AFTER 11:00 AM
# =========================================================

def mark_automatic_absent():

    # =====================================================
    # CURRENT DATE / TIME
    # =====================================================

    today = timezone.localdate()

    current_time = timezone.localtime().time().replace(
        second=0,
        microsecond=0
    )

    # =====================================================
    # DO NOTHING BEFORE / AT 11:00 AM
    # =====================================================

    if current_time <= CHECK_IN_END:
        return

    # =====================================================
    # ALL ACTIVE EMPLOYEES
    # =====================================================

    employees = User.objects.filter(
        role="employee",
        is_active=True
    )

    # =====================================================
    # PROCESS EACH EMPLOYEE
    # =====================================================

    for employee in employees:

        # -------------------------------------------------
        # CHECK WHETHER ATTENDANCE ALREADY EXISTS
        # -------------------------------------------------

        attendance_exists = Attendance.objects.filter(
            employee=employee,
            date=today
        ).exists()

        if attendance_exists:
            continue

        # -------------------------------------------------
        # CHECK APPROVED LEAVE
        # -------------------------------------------------

        approved_leave = Leave.objects.filter(
            employee=employee,
            leave_date=today,
            status="approved"
        ).exists()

        # -------------------------------------------------
        # MARK LEAVE
        # -------------------------------------------------

        if approved_leave:

            Attendance.objects.get_or_create(
                employee=employee,
                date=today,
                defaults={
                    "status": "leave",
                    "check_in": None,
                    "check_out": None,
                    "remarks": "Automatically marked Leave."
                }
            )

            continue

        # -------------------------------------------------
        # MARK ABSENT
        # -------------------------------------------------

        Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={
                "status": "absent",
                "check_in": None,
                "check_out": None,
                "remarks": (
                    "Automatically marked Absent "
                    "after 11:00 AM."
                )
            }
        )


# =========================================================
# EMPLOYEE ATTENDANCE
# =========================================================

@login_required(login_url="login")
def attendance(request):

    # =====================================================
    # EMPLOYEE ONLY
    # =====================================================

    if request.user.role != "employee":

        messages.error(
            request,
            "You are not authorized to access Attendance."
        )

        return redirect("admin_dashboard")

    # =====================================================
    # CURRENT DATE / TIME
    # =====================================================

    today = timezone.localdate()

    current_datetime = timezone.localtime()

    current_time = current_datetime.time().replace(
        second=0,
        microsecond=0
    )

    # =====================================================
    # AUTOMATIC ABSENT AFTER 11:00 AM
    # =====================================================

    mark_automatic_absent()

    # =====================================================
    # TODAY'S ATTENDANCE
    # =====================================================

    attendance_record = Attendance.objects.filter(
        employee=request.user,
        date=today
    ).first()

    # =====================================================
    # TODAY'S LEAVE
    # =====================================================

    leave_record = Leave.objects.filter(
        employee=request.user,
        leave_date=today
    ).exclude(
        status="rejected"
    ).first()

    # =====================================================
    # POST ACTION
    # =====================================================

    if request.method == "POST":

        action = request.POST.get(
            "action",
            ""
        ).strip()

        # =================================================
        # CHECK IN
        # =================================================

        if action == "check_in":

            # ---------------------------------------------
            # ATTENDANCE LEAVE CHECK
            # ---------------------------------------------

            if (
                attendance_record
                and attendance_record.status == "leave"
            ):

                messages.error(
                    request,
                    "You are on leave today. Check-in is not allowed."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # APPROVED LEAVE CHECK
            # ---------------------------------------------

            if (
                leave_record
                and leave_record.status == "approved"
            ):

                messages.error(
                    request,
                    "You are on leave today. Check-in is not allowed."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # ALREADY CHECKED IN
            # ---------------------------------------------

            if (
                attendance_record
                and attendance_record.check_in
            ):

                messages.warning(
                    request,
                    "You have already checked in today."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # ALREADY ABSENT
            # ---------------------------------------------

            if (
                attendance_record
                and attendance_record.status == "absent"
            ):

                messages.error(
                    request,
                    "Check-in is closed. You were marked Absent after 11:00 AM."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # BEFORE 9 AM
            # ---------------------------------------------

            if current_time < CHECK_IN_START:

                messages.error(
                    request,
                    "Check-in will be available from 9:00 AM to 11:00 AM."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # AFTER 11 AM
            # ---------------------------------------------

            if current_time > CHECK_IN_END:

                messages.error(
                    request,
                    "Check-in is closed. Check-in is allowed only from 9:00 AM to 11:00 AM."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # CREATE / UPDATE ATTENDANCE
            # ---------------------------------------------

            attendance_record, created = (
                Attendance.objects.update_or_create(

                    employee=request.user,

                    date=today,

                    defaults={
                        "status": "present",
                        "check_in": current_time,
                        "check_out": None,
                        "remarks": "Checked in.",
                    }
                )
            )

            messages.success(
                request,
                f"Check-in recorded successfully at "
                f"{current_time.strftime('%I:%M %p')}."
            )

            return redirect("attendance")

        # =================================================
        # CHECK OUT
        # =================================================

        elif action == "check_out":

            # ---------------------------------------------
            # NO ATTENDANCE
            # ---------------------------------------------

            if not attendance_record:

                messages.error(
                    request,
                    "Please check in first."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # ABSENT
            # ---------------------------------------------

            if attendance_record.status == "absent":

                messages.error(
                    request,
                    "You are marked Absent today. Checkout is not allowed."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # LEAVE
            # ---------------------------------------------

            if attendance_record.status == "leave":

                messages.error(
                    request,
                    "You are on leave today. Checkout is not allowed."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # NO CHECK-IN
            # ---------------------------------------------

            if not attendance_record.check_in:

                messages.error(
                    request,
                    "Please check in first."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # ALREADY CHECKED OUT
            # ---------------------------------------------

            if attendance_record.check_out:

                messages.warning(
                    request,
                    "You have already checked out today."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # AFTER 6 PM
            # ---------------------------------------------

            if current_time > CHECK_OUT_END:

                messages.error(
                    request,
                    "Normal checkout is closed after 6:00 PM."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # SAVE CHECK-OUT TIME
            # ---------------------------------------------

            attendance_record.check_out = current_time

            # ---------------------------------------------
            # BEFORE 4 PM = HALF DAY
            # ---------------------------------------------

            if current_time < CHECK_OUT_START:

                attendance_record.status = "half_day"

                attendance_record.remarks = (
                    "Checked out before 4:00 PM."
                )

                attendance_record.save(
                    update_fields=[
                        "check_out",
                        "status",
                        "remarks",
                        "updated_at"
                    ]
                )

                messages.warning(
                    request,
                    "Checkout recorded. Your attendance is marked as Half Day because you checked out before 4:00 PM."
                )

                return redirect("attendance")

            # ---------------------------------------------
            # 4 PM - 6 PM = PRESENT
            # ---------------------------------------------

            attendance_record.status = "present"

            attendance_record.remarks = (
                "Checked out during normal checkout hours."
            )

            attendance_record.save(
                update_fields=[
                    "check_out",
                    "status",
                    "remarks",
                    "updated_at"
                ]
            )

            messages.success(
                request,
                f"Check-out recorded successfully at "
                f"{current_time.strftime('%I:%M %p')}. "
                f"Attendance marked Present."
            )

            return redirect("attendance")

        # =================================================
        # APPLY LEAVE
        # =================================================

        elif action == "apply_leave":

            return redirect("apply_leave")

        # =================================================
        # INVALID ACTION
        # =================================================

        else:

            messages.error(
                request,
                "Invalid attendance action."
            )

            return redirect("attendance")

    # =====================================================
    # RECENT ATTENDANCE
    # =====================================================

    recent_attendance = Attendance.objects.filter(
        employee=request.user
    ).order_by(
        "-date"
    )[:20]

    # =====================================================
    # RECENT LEAVES
    # =====================================================

    recent_leaves = Leave.objects.filter(
        employee=request.user
    ).order_by(
        "-leave_date",
        "-applied_at"
    )[:20]

    # =====================================================
    # ATTENDANCE STATISTICS
    # =====================================================

    present_days = Attendance.objects.filter(
        employee=request.user,
        status="present"
    ).count()

    absent_days = Attendance.objects.filter(
        employee=request.user,
        status="absent"
    ).count()

    half_day_days = Attendance.objects.filter(
        employee=request.user,
        status="half_day"
    ).count()

    leave_days = Attendance.objects.filter(
        employee=request.user,
        status="leave"
    ).count()

    # =====================================================
    # WORKING HOURS
    # =====================================================

    total_working_seconds = 0

    attendance_records = Attendance.objects.filter(
        employee=request.user,
        check_in__isnull=False
    )

    for record in attendance_records:

        try:

            # ---------------------------------------------
            # CHECK-IN DATETIME
            # ---------------------------------------------

            check_in_datetime = timezone.make_aware(
                datetime.combine(
                    record.date,
                    record.check_in
                )
            )

            # ---------------------------------------------
            # CHECKED OUT
            # ---------------------------------------------

            if record.check_out:

                check_out_datetime = timezone.make_aware(
                    datetime.combine(
                        record.date,
                        record.check_out
                    )
                )

            # ---------------------------------------------
            # STILL WORKING TODAY
            # ---------------------------------------------

            elif record.date == today:

                check_out_datetime = current_datetime

            # ---------------------------------------------
            # OLD RECORD WITHOUT CHECKOUT
            # ---------------------------------------------

            else:

                continue

            # ---------------------------------------------
            # CALCULATE DURATION
            # ---------------------------------------------

            duration = (
                check_out_datetime
                - check_in_datetime
            )

            seconds = duration.total_seconds()

            if seconds > 0:

                total_working_seconds += seconds

        except Exception:

            continue

    # =====================================================
    # CONVERT TO HOURS + MINUTES
    # =====================================================

    total_working_hours = int(
        total_working_seconds // 3600
    )

    total_working_minutes = int(
        (total_working_seconds % 3600) // 60
    )

    if total_working_hours > 0:

        working_hours = (
            f"{total_working_hours}h "
            f"{total_working_minutes}m"
        )

    else:

        working_hours = (
            f"{total_working_minutes}m"
        )

    # =====================================================
    # CHECK-IN AVAILABILITY
    # =====================================================

    check_in_available = (
        CHECK_IN_START
        <= current_time
        <= CHECK_IN_END
    )

    check_in_not_started = (
        current_time < CHECK_IN_START
    )

    check_in_closed = (
        current_time > CHECK_IN_END
    )

    # =====================================================
    # CHECK-OUT AVAILABILITY
    # =====================================================

    check_out_available = (
        CHECK_OUT_START
        <= current_time
        <= CHECK_OUT_END
    )

    check_out_half_day = (
        current_time < CHECK_OUT_START
    )

    check_out_closed = (
        current_time > CHECK_OUT_END
    )

    # =====================================================
    # TODAY LEAVE AVAILABILITY
    # =====================================================

    today_leave_available = (
        current_time < LEAVE_TODAY_DEADLINE
    )

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "employee/attendance.html",
        {

            "today": today,

            "current_time": current_time,

            "attendance_record": attendance_record,

            "attendance": attendance_record,

            "recent_attendance": recent_attendance,

            "attendance_history": recent_attendance,

            "leave_record": leave_record,

            "recent_leaves": recent_leaves,

            # -----------------------------
            # STATISTICS
            # -----------------------------

            "present_days": present_days,

            "absent_days": absent_days,

            "half_day_days": half_day_days,

            "leave_days": leave_days,

            "working_hours": working_hours,

            # -----------------------------
            # CHECK-IN / CHECK-OUT
            # -----------------------------

            "check_in_available": check_in_available,

            "check_in_not_started": check_in_not_started,

            "check_in_closed": check_in_closed,

            "check_out_available": check_out_available,

            "check_out_half_day": check_out_half_day,

            "check_out_closed": check_out_closed,

            # -----------------------------
            # LEAVE
            # -----------------------------

            "today_leave_available": today_leave_available,

            # -----------------------------
            # TIME CONSTANTS
            # -----------------------------

            "check_in_start": CHECK_IN_START,

            "check_in_end": CHECK_IN_END,

            "check_out_start": CHECK_OUT_START,

            "check_out_end": CHECK_OUT_END,

            "leave_today_deadline": LEAVE_TODAY_DEADLINE,

        }
    )


# =========================================================
# EMPLOYEE LEAVE APPLICATION
# =========================================================
#
# Rules:
#
# 1. Past dates -> NOT allowed
# 2. Today's leave -> before 9 AM only
# 3. Tomorrow's leave -> before 9 AM today
# 4. Day after tomorrow / future -> anytime
# 5. Leave immediately approved
# 6. Attendance immediately marked "leave"
#
# =========================================================

@login_required(login_url="login")
def apply_leave(request):

    # =====================================================
    # EMPLOYEE ONLY
    # =====================================================

    if request.user.role != "employee":

        messages.error(
            request,
            "You are not authorized to apply for leave."
        )

        return redirect("employee_dashboard")

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        leave_date_str = (
            request.POST.get(
                "leave_date",
                ""
            )
            .strip()
        )

        # -----------------------------------------------
        # DATE REQUIRED
        # -----------------------------------------------

        if not leave_date_str:

            messages.error(
                request,
                "Please select a leave date."
            )

            return redirect("apply_leave")

        # -----------------------------------------------
        # DATE VALIDATION
        # -----------------------------------------------

        try:

            leave_date = datetime.strptime(
                leave_date_str,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            messages.error(
                request,
                "Please select a valid leave date."
            )

            return redirect("apply_leave")

        # =================================================
        # CURRENT DATE / TIME
        # =================================================

        today = timezone.localdate()

        current_time = (
            timezone.localtime()
            .time()
            .replace(
                second=0,
                microsecond=0
            )
        )

        # =================================================
        # PAST DATE
        # =================================================

        if leave_date < today:

            messages.error(
                request,
                "You cannot apply leave for a past date."
            )

            return redirect("apply_leave")

        # =================================================
        # TODAY
        # =================================================

        if leave_date == today:

            if current_time >= LEAVE_TODAY_DEADLINE:

                messages.error(
                    request,
                    "Today's leave can only be applied before 9:00 AM."
                )

                return redirect("apply_leave")

        # =================================================
        # TOMORROW
        # =================================================

        tomorrow = today + timezone.timedelta(days=1)

        if leave_date == tomorrow:

            if current_time >= time(9, 0):

                messages.error(
                    request,
                    "Tomorrow's leave can only be applied before 9:00 AM."
                )

                return redirect("apply_leave")

        # =================================================
        # CHECK EXISTING ATTENDANCE
        # =================================================

        existing_attendance = Attendance.objects.filter(
            employee=request.user,
            date=leave_date
        ).first()

        # =================================================
        # ALREADY PRESENT / HALF DAY
        # =================================================

        if (
            existing_attendance
            and existing_attendance.status in [
                "present",
                "half_day"
            ]
        ):

            messages.error(
                request,
                "Attendance already exists for this date. Leave cannot be applied."
            )

            return redirect("apply_leave")

        # =================================================
        # EXISTING LEAVE
        # =================================================

        existing_leave = Leave.objects.filter(
            employee=request.user,
            leave_date=leave_date
        ).exclude(
            status="rejected"
        ).first()

        if existing_leave:

            messages.warning(
                request,
                f"Leave is already applied for "
                f"{leave_date.strftime('%d %B %Y')}."
            )

            return redirect("attendance")

        # =================================================
        # CREATE / UPDATE ATTENDANCE
        # =================================================

        attendance_record, created = (
            Attendance.objects.update_or_create(

                employee=request.user,

                date=leave_date,

                defaults={
                    "status": "leave",
                    "check_in": None,
                    "check_out": None,
                    "remarks": "Leave applied by employee.",
                }

            )
        )

        # =================================================
        # CREATE LEAVE RECORD
        # =================================================

        Leave.objects.create(

            employee=request.user,

            leave_date=leave_date,

            reason="Leave applied by employee.",

            status="approved"

        )

        # =================================================
        # SUCCESS
        # =================================================

        messages.success(
            request,
            f"Leave applied successfully for "
            f"{leave_date.strftime('%d %B %Y')}."
        )

        return redirect("attendance")

    # =====================================================
    # GET
    # =====================================================

    return render(
        request,
        "employee/apply_leave.html"
    )


# =========================================================
# ADMIN - TODAY'S ATTENDANCE REPORT
# =========================================================

@login_required(login_url="login")
def attendance_reports(request):

    # =====================================================
    # ADMIN ONLY
    # =====================================================

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to access Attendance Reports."
        )

        return redirect("employee_dashboard")

    # =====================================================
    # CURRENT DATE / TIME
    # =====================================================

    today = timezone.localdate()

    current_datetime = timezone.localtime()

    current_time = current_datetime.time().replace(
        second=0,
        microsecond=0
    )

    # =====================================================
    # AUTOMATIC ABSENT AFTER 11:00 AM
    # =====================================================

    mark_automatic_absent()

    # =====================================================
    # ALL ACTIVE EMPLOYEES
    # =====================================================

    employees = User.objects.filter(
        role="employee",
        is_active=True
    ).order_by(
        "first_name",
        "last_name"
    )

    # =====================================================
    # TODAY'S ATTENDANCE
    # =====================================================

    attendance_records = Attendance.objects.filter(
        date=today
    ).select_related(
        "employee"
    ).order_by(
        "employee__first_name",
        "employee__last_name"
    )

    # =====================================================
    # EMPLOYEE FILTER
    # =====================================================

    employee_id = request.GET.get(
        "employee",
        ""
    ).strip()

    if employee_id:

        attendance_records = attendance_records.filter(
            employee_id=employee_id
        )

    # =====================================================
    # STATUS FILTER
    # =====================================================

    selected_status = request.GET.get(
        "status",
        ""
    ).strip()

    if selected_status:

        attendance_records = attendance_records.filter(
            status=selected_status
        )

    # =====================================================
    # FROM DATE
    # =====================================================

    from_date = request.GET.get(
        "from_date",
        ""
    ).strip()

    # =====================================================
    # TO DATE
    # =====================================================

    to_date = request.GET.get(
        "to_date",
        ""
    ).strip()

    # =====================================================
    # DATE FILTER
    # =====================================================

    if from_date:

        try:

            from_date_value = datetime.strptime(
                from_date,
                "%Y-%m-%d"
            ).date()

            attendance_records = attendance_records.filter(
                date__gte=from_date_value
            )

        except ValueError:

            pass

    if to_date:

        try:

            to_date_value = datetime.strptime(
                to_date,
                "%Y-%m-%d"
            ).date()

            attendance_records = attendance_records.filter(
                date__lte=to_date_value
            )

        except ValueError:

            pass

    # =====================================================
    # SUMMARY
    # =====================================================

    total_records = attendance_records.count()

    present_count = attendance_records.filter(
        status="present"
    ).count()

    absent_count = attendance_records.filter(
        status="absent"
    ).count()

    leave_count = attendance_records.filter(
        status="leave"
    ).count()

    half_day_count = attendance_records.filter(
        status="half_day"
    ).count()

    # =====================================================
    # WORKING HOURS FOR EACH RECORD
    # =====================================================

    for record in attendance_records:

        # -----------------------------------------------
        # DEFAULT
        # -----------------------------------------------

        record.working_hours = "—"

        # -----------------------------------------------
        # NO CHECK-IN
        # -----------------------------------------------

        if not record.check_in:

            continue

        try:

            # -------------------------------------------
            # CHECK-IN DATETIME
            # -------------------------------------------

            check_in_datetime = datetime.combine(
                record.date,
                record.check_in
            )

            # -------------------------------------------
            # CHECKED OUT
            # -------------------------------------------

            if record.check_out:

                end_datetime = datetime.combine(
                    record.date,
                    record.check_out
                )

            # -------------------------------------------
            # STILL WORKING TODAY
            # -------------------------------------------

            elif record.date == today:

                end_datetime = datetime.combine(
                    record.date,
                    current_time
                )

            # -------------------------------------------
            # OLD RECORD WITHOUT CHECKOUT
            # -------------------------------------------

            else:

                continue

            # -------------------------------------------
            # CALCULATE DURATION
            # -------------------------------------------

            duration = (
                end_datetime
                - check_in_datetime
            )

            total_seconds = int(
                duration.total_seconds()
            )

            # -------------------------------------------
            # NEGATIVE DURATION PROTECTION
            # -------------------------------------------

            if total_seconds < 0:

                continue

            # -------------------------------------------
            # HOURS + MINUTES
            # -------------------------------------------

            hours = total_seconds // 3600

            minutes = (
                total_seconds % 3600
            ) // 60

            if hours > 0:

                record.working_hours = (
                    f"{hours}h {minutes}m"
                )

            else:

                record.working_hours = (
                    f"{minutes}m"
                )

        except Exception:

            record.working_hours = "—"

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "admin/attendance_reports.html",
        {

            "today": today,

            "employees": employees,

            "attendance_records": attendance_records,

            # -----------------------------
            # FILTER VALUES
            # -----------------------------

            "selected_employee": employee_id,

            "selected_status": selected_status,

            "from_date": from_date,

            "to_date": to_date,

            # -----------------------------
            # SUMMARY
            # -----------------------------

            "total_records": total_records,

            "present_count": present_count,

            "absent_count": absent_count,

            "leave_count": leave_count,

            "half_day_count": half_day_count,

        }
    )# =========================================================
# ADMIN - COMPLETE ATTENDANCE HISTORY
# =========================================================

@login_required(login_url="login")
def attendance_history(request):

    # =====================================================
    # ADMIN ONLY
    # =====================================================

    if request.user.role != "admin":

        messages.error(
            request,
            "You are not authorized to access Attendance History."
        )

        return redirect("employee_dashboard")

    # =====================================================
    # EMPLOYEES
    # =====================================================

    employees = User.objects.filter(
        role="employee",
        is_active=True
    ).order_by(
        "first_name",
        "last_name"
    )

    # =====================================================
    # FILTER VALUES
    # =====================================================

    selected_employee = request.GET.get(
        "employee",
        ""
    ).strip()

    selected_month = request.GET.get(
        "month",
        ""
    ).strip()

    selected_status = request.GET.get(
        "status",
        ""
    ).strip()

    # =====================================================
    # PARSE SELECTED MONTH
    # =====================================================

    selected_year = None
    selected_month_number = None

    if selected_month:

        try:

            selected_year, selected_month_number = (
                selected_month.split("-")
            )

            selected_year = int(
                selected_year
            )

            selected_month_number = int(
                selected_month_number
            )

        except (
            ValueError,
            TypeError
        ):

            selected_year = None
            selected_month_number = None

    # =====================================================
    # MAIN ATTENDANCE RECORDS
    # =====================================================

    attendance_records = (
        Attendance.objects
        .all()
        .select_related("employee")
        .order_by(
            "-date",
            "employee__first_name",
            "employee__last_name"
        )
    )

    # =====================================================
    # EMPLOYEE FILTER
    # =====================================================

    if selected_employee:

        attendance_records = attendance_records.filter(
            employee_id=selected_employee
        )

    # =====================================================
    # MONTH FILTER
    # =====================================================

    if selected_year and selected_month_number:

        attendance_records = attendance_records.filter(
            date__year=selected_year,
            date__month=selected_month_number
        )

    # =====================================================
    # STATUS FILTER
    # =====================================================

    if selected_status:

        attendance_records = attendance_records.filter(
            status=selected_status
        )

    # =====================================================
    # WORKING HOURS FOR DISPLAYED RECORDS
    # =====================================================

    total_working_seconds = 0

    for record in attendance_records:

        record.working_hours = "—"

        if not record.check_in or not record.check_out:

            continue

        try:

            check_in_datetime = datetime.combine(
                record.date,
                record.check_in
            )

            check_out_datetime = datetime.combine(
                record.date,
                record.check_out
            )

            duration = (
                check_out_datetime
                - check_in_datetime
            )

            working_seconds = int(
                duration.total_seconds()
            )

            if working_seconds < 0:

                continue

            total_working_seconds += (
                working_seconds
            )

            hours = (
                working_seconds // 3600
            )

            minutes = (
                working_seconds % 3600
            ) // 60

            if hours > 0:

                record.working_hours = (
                    f"{hours}h {minutes}m"
                )

            else:

                record.working_hours = (
                    f"{minutes}m"
                )

        except Exception:

            record.working_hours = "—"

    # =====================================================
    # EMPLOYEE-WISE MONTHLY SUMMARY
    # =====================================================

    summary_records = Attendance.objects.all()

    if selected_employee:

        summary_records = summary_records.filter(
            employee_id=selected_employee
        )

    if selected_year and selected_month_number:

        summary_records = summary_records.filter(
            date__year=selected_year,
            date__month=selected_month_number
        )

    # =====================================================
    # EMPLOYEES TO SHOW IN SUMMARY
    # =====================================================

    summary_employees = employees

    if selected_employee:

        summary_employees = employees.filter(
            id=selected_employee
        )

    # =====================================================
    # EMPLOYEE MONTHLY DATA
    # =====================================================

    employee_monthly_hours = []

    for employee in summary_employees:

        employee_records = summary_records.filter(
            employee_id=employee.id
        )

        present_count = employee_records.filter(
            status="present"
        ).count()

        half_day_count = employee_records.filter(
            status="half_day"
        ).count()

        absent_count = employee_records.filter(
            status="absent"
        ).count()

        leave_count = employee_records.filter(
            status="leave"
        ).count()

        employee_total_seconds = 0

        for record in employee_records:

            if not record.check_in:
                continue

            if not record.check_out:
                continue

            try:

                check_in_datetime = datetime.combine(
                    record.date,
                    record.check_in
                )

                check_out_datetime = datetime.combine(
                    record.date,
                    record.check_out
                )

                duration = (
                    check_out_datetime
                    - check_in_datetime
                )

                seconds = int(
                    duration.total_seconds()
                )

                if seconds > 0:

                    employee_total_seconds += (
                        seconds
                    )

            except Exception:

                continue

        employee_hours = (
            employee_total_seconds // 3600
        )

        employee_minutes = (
            employee_total_seconds % 3600
        ) // 60

        if employee_hours > 0:

            monthly_working_hours = (
                f"{employee_hours}h "
                f"{employee_minutes}m"
            )

        else:

            monthly_working_hours = (
                f"{employee_minutes}m"
            )

        employee_monthly_hours.append({

            "employee": employee,

            "present_count": present_count,

            "half_day_count": half_day_count,

            "absent_count": absent_count,

            "leave_count": leave_count,

            "hours": int(
                employee_hours
            ),

            "minutes": int(
                employee_minutes
            ),

            "total_seconds": int(
                employee_total_seconds
            ),

            "monthly_working_hours": (
                monthly_working_hours
            ),

        })

    # =====================================================
    # OVERALL WORKING HOURS
    # =====================================================

    overall_working_seconds = 0

    for record in summary_records:

        if not record.check_in:
            continue

        if not record.check_out:
            continue

        try:

            check_in_datetime = datetime.combine(
                record.date,
                record.check_in
            )

            check_out_datetime = datetime.combine(
                record.date,
                record.check_out
            )

            duration = (
                check_out_datetime
                - check_in_datetime
            )

            seconds = int(
                duration.total_seconds()
            )

            if seconds > 0:

                overall_working_seconds += (
                    seconds
                )

        except Exception:

            continue

    overall_hours = (
        overall_working_seconds // 3600
    )

    overall_minutes = (
        overall_working_seconds % 3600
    ) // 60

    if overall_hours > 0:

        total_working_hours = (
            f"{overall_hours}h "
            f"{overall_minutes}m"
        )

    else:

        total_working_hours = (
            f"{overall_minutes}m"
        )

    # =====================================================
    # MAIN TABLE SUMMARY
    # =====================================================

    total_records = attendance_records.count()

    present_count = attendance_records.filter(
        status="present"
    ).count()

    absent_count = attendance_records.filter(
        status="absent"
    ).count()

    leave_count = attendance_records.filter(
        status="leave"
    ).count()

    half_day_count = attendance_records.filter(
        status="half_day"
    ).count()

    # =====================================================
    # MANUAL COMPANY HOLIDAYS
    # =====================================================

    holidays = Holiday.objects.none()

    holiday_count = 0

    if selected_year and selected_month_number:

        holidays = Holiday.objects.filter(
            date__year=selected_year,
            date__month=selected_month_number
        ).order_by(
            "date"
        )

        holiday_count = holidays.count()

    # =====================================================
    # HOLIDAY DATE SET
    #
    # Used to avoid duplicate Sunday + manual holiday.
    # =====================================================

    manual_holiday_dates = set(
        holidays.values_list(
            "date",
            flat=True
        )
    )

    # =====================================================
    # COMBINED MONTHLY ITEMS
    #
    # Attendance + Manual Holidays + Sundays
    # =====================================================

    monthly_items = []

    # =====================================================
    # ADD ATTENDANCE
    # =====================================================

    for record in attendance_records:

        monthly_items.append({

            "type": "attendance",

            "date": record.date,

            "record": record,

        })

    # =====================================================
    # ADD MANUAL HOLIDAYS
    # =====================================================

    for holiday in holidays:

        monthly_items.append({

            "type": "holiday",

            "date": holiday.date,

            "holiday_name": holiday.name,

            "holiday_description": (
                holiday.description
            ),

        })

    # =====================================================
    # ADD AUTOMATIC SUNDAYS
    # =====================================================

    if selected_year and selected_month_number:

        first_day = date(
            selected_year,
            selected_month_number,
            1
        )

        # -------------------------------------------------
        # NEXT MONTH
        # -------------------------------------------------

        if selected_month_number == 12:

            next_month = date(
                selected_year + 1,
                1,
                1
            )

        else:

            next_month = date(
                selected_year,
                selected_month_number + 1,
                1
            )

        # -------------------------------------------------
        # LOOP THROUGH MONTH
        # -------------------------------------------------

        current_day = first_day

        while current_day < next_month:

            # Sunday
            if current_day.weekday() == 6:

                # -------------------------------------------------
                # ONLY ADD IF NOT ALREADY MANUAL HOLIDAY
                # -------------------------------------------------

                if current_day not in manual_holiday_dates:

                    monthly_items.append({

                        "type": "holiday",

                        "date": current_day,

                        "holiday_name": "Sunday",

                        "holiday_description": (
                            "Weekly Holiday"
                        ),

                    })

            current_day += timedelta(
                days=1
            )

    # =====================================================
    # SORT BY DATE
    # =====================================================

    monthly_items.sort(
        key=lambda item: item["date"],
        reverse=True
    )

    # =====================================================
    # MONTHLY HOLIDAY COUNT
    #
    # Manual Holidays + Sundays
    # =====================================================

    monthly_holiday_count = sum(
        1
        for item in monthly_items
        if item["type"] == "holiday"
    )

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "admin/attendance_history.html",
        {

            "employees": employees,

            "attendance_records": attendance_records,

            "monthly_items": monthly_items,

            "selected_employee": selected_employee,

            "selected_month": selected_month,

            "selected_status": selected_status,

            "total_records": total_records,

            "present_count": present_count,

            "absent_count": absent_count,

            "leave_count": leave_count,

            "half_day_count": half_day_count,

            "total_working_hours": total_working_hours,

            "overall_working_seconds": (
                overall_working_seconds
            ),

            "employee_monthly_hours": (
                employee_monthly_hours
            ),

            "holidays": holidays,

            "holiday_count": holiday_count,

            "monthly_holiday_count": (
                monthly_holiday_count
            ),

        }
    )
    # =========================================================
# TODO LIST
# =========================================================

@login_required(login_url="login")
def todo_list(request):

    # -----------------------------------------------------
    # CURRENT USER'S TODOS
    # -----------------------------------------------------

    todos = Todo.objects.filter(
        user=request.user
    ).order_by(
        "is_completed",
        "-created_at"
    )


    # -----------------------------------------------------
    # ADD TODO
    # -----------------------------------------------------

    if request.method == "POST":

        action = request.POST.get("action")


        # =================================================
        # ADD
        # =================================================

        if action == "add":

            title = request.POST.get(
                "title",
                ""
            ).strip()

            description = request.POST.get(
                "description",
                ""
            ).strip()

            due_date = request.POST.get(
                "due_date"
            )

            priority = request.POST.get(
                "priority",
                "medium"
            )

            category = request.POST.get(
                "category",
                ""
            ).strip()


            if not title:

                messages.error(
                    request,
                    "Please enter a To-Do title."
                )

                return redirect("todo_list")


            Todo.objects.create(

                user=request.user,

                title=title,

                description=description,

                due_date=due_date
                    if due_date
                    else None,

                priority=priority,

                category=category

            )


            messages.success(
                request,
                "To-Do added successfully."
            )

            return redirect("todo_list")


        # =================================================
        # COMPLETE / UNCOMPLETE
        # =================================================

        elif action == "toggle":

            todo_id = request.POST.get(
                "todo_id"
            )


            todo = get_object_or_404(

                Todo,

                id=todo_id,

                user=request.user

            )


            todo.is_completed = not todo.is_completed

            todo.save(
                update_fields=[
                    "is_completed",
                    "updated_at"
                ]
            )


            return redirect("todo_list")


        # =================================================
        # EDIT
        # =================================================

        elif action == "edit":

            todo_id = request.POST.get(
                "todo_id"
            )


            todo = get_object_or_404(

                Todo,

                id=todo_id,

                user=request.user

            )


            title = request.POST.get(
                "title",
                ""
            ).strip()

            description = request.POST.get(
                "description",
                ""
            ).strip()

            due_date = request.POST.get(
                "due_date"
            )

            priority = request.POST.get(
                "priority",
                "medium"
            )

            category = request.POST.get(
                "category",
                ""
            ).strip()


            if not title:

                messages.error(
                    request,
                    "To-Do title cannot be empty."
                )

                return redirect("todo_list")


            todo.title = title

            todo.description = description

            todo.due_date = (
                due_date
                if due_date
                else None
            )

            todo.priority = priority

            todo.category = category

            todo.save()


            messages.success(
                request,
                "To-Do updated successfully."
            )

            return redirect("todo_list")


        # =================================================
        # DELETE
        # =================================================

        elif action == "delete":

            todo_id = request.POST.get(
                "todo_id"
            )


            todo = get_object_or_404(

                Todo,

                id=todo_id,

                user=request.user

            )


            todo.delete()


            messages.success(
                request,
                "To-Do deleted successfully."
            )

            return redirect("todo_list")


    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    total_todos = todos.count()


    completed_todos = todos.filter(
        is_completed=True
    ).count()


    pending_todos = todos.filter(
        is_completed=False
    ).count()


    today = timezone.localdate()


    overdue_todos = todos.filter(
        is_completed=False,
        due_date__lt=today
    ).count()


    today_todos = todos.filter(
        due_date=today
    ).count()


    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {

        "todos": todos,

        "total_todos": total_todos,

        "completed_todos": completed_todos,

        "pending_todos": pending_todos,

        "overdue_todos": overdue_todos,

        "today_todos": today_todos,

    }


    return render(
        request,
        "todo/todo.html",
        context
    )
    
# =========================================================
# AUTOMATIC ABSENT AFTER 11:00 AM
# =========================================================

def mark_automatic_absent():

    today = timezone.localdate()

    current_time = timezone.localtime().time().replace(
        second=0,
        microsecond=0
    )

    # -----------------------------------------------------
    # BEFORE / AT 11 AM
    # -----------------------------------------------------

    if current_time <= CHECK_IN_END:
        return

    # -----------------------------------------------------
    # COMPANY HOLIDAY
    # -----------------------------------------------------

    if Holiday.objects.filter(
        date=today
    ).exists():

        return

    # -----------------------------------------------------
    # ACTIVE EMPLOYEES
    # -----------------------------------------------------

    employees = User.objects.filter(
        role="employee",
        is_active=True
    )

    # -----------------------------------------------------
    # PROCESS EMPLOYEES
    # -----------------------------------------------------

    for employee in employees:

        # -------------------------------------------------
        # ALREADY HAS ATTENDANCE
        # -------------------------------------------------

        attendance_exists = Attendance.objects.filter(
            employee=employee,
            date=today
        ).exists()

        if attendance_exists:
            continue

        # -------------------------------------------------
        # APPROVED LEAVE
        # -------------------------------------------------

        approved_leave = Leave.objects.filter(
            employee=employee,
            leave_date=today,
            status="approved"
        ).exists()

        if approved_leave:

            Attendance.objects.get_or_create(
                employee=employee,
                date=today,
                defaults={
                    "status": "leave",
                    "check_in": None,
                    "check_out": None,
                    "remarks": "Automatically marked Leave."
                }
            )

            continue

        # -------------------------------------------------
        # ABSENT
        # -------------------------------------------------

        Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={
                "status": "absent",
                "check_in": None,
                "check_out": None,
                "remarks": (
                    "Automatically marked Absent "
                    "after 11:00 AM."
                )
            }
        )
  
def manage_holidays(request):

    if request.user.role != "admin":
        messages.error(
            request,
            "You are not authorized to manage holidays."
        )
        return redirect("employee_dashboard")

    if request.method == "POST":

        holiday_date = request.POST.get("date", "").strip()
        holiday_name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        if not holiday_date:
            messages.error(
                request,
                "Please select a holiday date."
            )
            return redirect("manage_holidays")

        if not holiday_name:
            messages.error(
                request,
                "Please enter a holiday name."
            )
            return redirect("manage_holidays")

        try:
            holiday_date_value = datetime.strptime(
                holiday_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            messages.error(
                request,
                "Please enter a valid holiday date."
            )
            return redirect("manage_holidays")

        if Holiday.objects.filter(
            date=holiday_date_value
        ).exists():

            messages.error(
                request,
                "A holiday already exists for this date."
            )
            return redirect("manage_holidays")

        Holiday.objects.create(
            date=holiday_date_value,
            name=holiday_name,
            description=description
        )

        messages.success(
            request,
            f"Holiday '{holiday_name}' added successfully."
        )

        return redirect("manage_holidays")

    holidays = Holiday.objects.all().order_by("date")

    return render(
        request,
        "admin/holiday.html",
        {
            "holidays": holidays
        }
    )
    
    # =========================================================
# CHAT - CONTACT LIST
# =========================================================

@login_required(login_url="login")
@require_GET
def chat_users(request):

    current_user = request.user

    # -----------------------------------------------------
    # ADMIN
    # Admin can see all employees
    # -----------------------------------------------------

    if getattr(current_user, "role", "") == "admin":

        users = User.objects.filter(
            role="employee",
            is_active=True
        ).order_by(
            "first_name",
            "last_name",
            "username"
        )

    # -----------------------------------------------------
    # EMPLOYEE
    # Employee can see admin users
    # -----------------------------------------------------

    elif getattr(current_user, "role", "") == "employee":

        users = User.objects.filter(
            role="admin",
            is_active=True
        ).order_by(
            "first_name",
            "last_name",
            "username"
        )

    else:

        users = User.objects.none()


    result = []


    for user in users:

        full_name = user.get_full_name().strip()

        if not full_name:

            full_name = user.username


        # -----------------------------------------------
        # ONLINE STATUS
        # -----------------------------------------------

        try:

            status = user.chat_status

            is_online = status.is_online

            last_seen = (
                status.last_seen.isoformat()
                if status.last_seen
                else None
            )

        except UserStatus.DoesNotExist:

            is_online = False

            last_seen = None


        # -----------------------------------------------
        # UNREAD MESSAGES
        # -----------------------------------------------

        unread_count = ChatMessage.objects.filter(
            sender=user,
            receiver=current_user,
            is_read=False
        ).count()


        result.append({

            "id": user.id,

            "name": full_name,

            "username": user.username,

            "email": user.email,

            "role": getattr(
                user,
                "role",
                ""
            ),

            "is_online": is_online,

            "last_seen": last_seen,

            "unread": unread_count,

        })


    return JsonResponse({

        "success": True,

        "users": result,

    })


# =========================================================
# CHAT - LOAD MESSAGES
# =========================================================

@login_required(login_url="login")
@require_GET
def chat_messages(request, user_id):

    current_user = request.user


    try:

        other_user = User.objects.get(
            id=user_id,
            is_active=True
        )

    except User.DoesNotExist:

        return JsonResponse(
            {
                "success": False,
                "error": "User not found."
            },
            status=404
        )


    # -----------------------------------------------------
    # SECURITY
    # -----------------------------------------------------

    allowed = False


    if getattr(current_user, "role", "") == "admin":

        allowed = (
            getattr(
                other_user,
                "role",
                ""
            ) == "employee"
        )


    elif getattr(current_user, "role", "") == "employee":

        allowed = (
            getattr(
                other_user,
                "role",
                ""
            ) == "admin"
        )


    if not allowed:

        return JsonResponse(
            {
                "success": False,
                "error": "You are not allowed to chat with this user."
            },
            status=403
        )


    # -----------------------------------------------------
    # GET CONVERSATION
    # -----------------------------------------------------

    messages_list = ChatMessage.objects.filter(

        sender__in=[
            current_user,
            other_user
        ],

        receiver__in=[
            current_user,
            other_user
        ]

    ).order_by(
        "timestamp"
    )


    # -----------------------------------------------------
    # MARK RECEIVED MESSAGES AS READ
    # -----------------------------------------------------

    ChatMessage.objects.filter(
        sender=other_user,
        receiver=current_user,
        is_read=False
    ).update(
        is_read=True
    )


    data = []


    for msg in messages_list:

        data.append({

            "id": msg.id,

            "sender_id": msg.sender_id,

            "receiver_id": msg.receiver_id,

            "message": msg.message,

            "timestamp": (
                timezone.localtime(
                    msg.timestamp
                ).strftime("%I:%M %p")
            ),

        })


    return JsonResponse({

        "success": True,

        "messages": data,

    })


# =========================================================
# CHAT - SEND MESSAGE
# =========================================================

@login_required(login_url="login")
@require_POST
def chat_send_message(request, user_id):

    current_user = request.user


    try:

        other_user = User.objects.get(
            id=user_id,
            is_active=True
        )

    except User.DoesNotExist:

        return JsonResponse(
            {
                "success": False,
                "error": "User not found."
            },
            status=404
        )


    # -----------------------------------------------------
    # SECURITY
    # -----------------------------------------------------

    allowed = False


    if getattr(current_user, "role", "") == "admin":

        allowed = (
            getattr(
                other_user,
                "role",
                ""
            ) == "employee"
        )


    elif getattr(current_user, "role", "") == "employee":

        allowed = (
            getattr(
                other_user,
                "role",
                ""
            ) == "admin"
        )


    if not allowed:

        return JsonResponse(
            {
                "success": False,
                "error": "You are not allowed to chat with this user."
            },
            status=403
        )


    # -----------------------------------------------------
    # MESSAGE
    # -----------------------------------------------------

    import json

    try:

        body = json.loads(
            request.body
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "success": False,
                "error": "Invalid request."
            },
            status=400
        )


    message_text = str(
        body.get(
            "message",
            ""
        )
    ).strip()


    if not message_text:

        return JsonResponse(
            {
                "success": False,
                "error": "Message cannot be empty."
            },
            status=400
        )


    if len(message_text) > 2000:

        return JsonResponse(
            {
                "success": False,
                "error": "Message is too long."
            },
            status=400
        )


    message = ChatMessage.objects.create(

        sender=current_user,

        receiver=other_user,

        message=message_text

    )


    return JsonResponse({

        "success": True,

        "message": {

            "id": message.id,

            "sender_id": message.sender_id,

            "receiver_id": message.receiver_id,

            "message": message.message,

            "timestamp": timezone.localtime(
                message.timestamp
            ).strftime("%I:%M %p"),

        }

    })


# =========================================================
# CHAT - USER STATUS
# =========================================================

@login_required(login_url="login")
@require_POST
def chat_update_status(request):

    status, created = UserStatus.objects.get_or_create(

        user=request.user

    )


    status.is_online = True

    status.last_seen = timezone.now()

    status.save(
        update_fields=[
            "is_online",
            "last_seen"
        ]
    )


    return JsonResponse({

        "success": True

    })
    
    # =========================================================
# INVOICE MODULE
# =========================================================


@login_required(login_url="login")
def invoice_list(request):

    if request.user.role != "admin":
        messages.error(
            request,
            "You are not authorized to access invoices."
        )
        return redirect("employee-dashboard")

    invoices = (
        Invoice.objects
        .select_related("client", "project")
        .prefetch_related("items")
        .order_by("-created_at")
    )

    return render(
        request,
        "admin/invoices.html",
        {
            "invoices": invoices,
        }
    )


# =========================================================
# CREATE INVOICE
# =========================================================

@login_required(login_url="login")
def create_invoice(request):

    if request.user.role != "admin":
        messages.error(
            request,
            "You are not authorized to create invoices."
        )
        return redirect("employee-dashboard")

    clients = Client.objects.all().order_by("name")

    projects = (
        Project.objects
        .select_related("client")
        .order_by("-created_at")
    )

    if request.method == "POST":

        try:

            with transaction.atomic():

                # =================================================
                # BASIC DETAILS
                # =================================================

                client_id = request.POST.get("client")

                if not client_id:
                    raise ValueError("Please select a client.")

                project_id = request.POST.get("project") or None

                invoice_date = (
                    request.POST.get("invoice_date")
                    or timezone.localdate()
                )

                due_date = request.POST.get("due_date") or None

                currency = (
                    request.POST.get("currency")
                    or "INR"
                )

                tax_type = (
                    request.POST.get("tax_type")
                    or "gst"
                )

                client_gstin = (
                    request.POST.get("client_gstin")
                    or ""
                ).strip()

                reference_number = (
                    request.POST.get("reference_number")
                    or ""
                ).strip()

                payment_terms = (
                    request.POST.get("payment_terms")
                    or "Payment due within 30 days."
                ).strip()

                notes = (
                    request.POST.get("notes")
                    or ""
                ).strip()

                terms = (
                    request.POST.get("terms")
                    or ""
                ).strip()

                payment_method = (
                    request.POST.get("payment_method")
                    or ""
                ).strip()

                payment_reference = (
                    request.POST.get("payment_reference")
                    or ""
                ).strip()

                # =================================================
                # AMOUNT PAID
                # =================================================

                amount_paid_raw = (
                    request.POST.get("amount_paid")
                    or "0"
                ).strip()

                try:
                    amount_paid = Decimal(amount_paid_raw)
                except (ValueError, TypeError, InvalidOperation):
                    amount_paid = Decimal("0.00")

                if amount_paid < Decimal("0.00"):
                    amount_paid = Decimal("0.00")

                # =================================================
                # CLIENT
                # =================================================

                client = get_object_or_404(
                    Client,
                    id=client_id
                )

                # =================================================
                # PROJECT
                # =================================================

                project = None

                if project_id:
                    project = get_object_or_404(
                        Project,
                        id=project_id
                    )

                    # Optional safety:
                    # Project should belong to selected client
                    if project.client_id != client.id:
                        raise ValueError(
                            "Selected project does not belong to the selected client."
                        )

                # =================================================
                # CREATE INVOICE
                # =================================================

                invoice = Invoice.objects.create(

                    client=client,

                    project=project,

                    invoice_date=invoice_date,

                    due_date=due_date,

                    currency=currency,

                    tax_type=tax_type,

                    client_gstin=client_gstin,

                    reference_number=reference_number,

                    payment_terms=payment_terms,

                    amount_paid=amount_paid,

                    notes=notes,

                    terms=terms,

                    payment_method=payment_method,

                    payment_reference=payment_reference,
                )

                # =================================================
                # GET ITEM DATA
                # =================================================

                descriptions = request.POST.getlist(
                    "item_description[]"
                )

                hsn_sacs = request.POST.getlist(
                    "item_hsn_sac[]"
                )

                quantities = request.POST.getlist(
                    "item_quantity[]"
                )

                units = request.POST.getlist(
                    "item_unit[]"
                )

                unit_prices = request.POST.getlist(
                    "item_unit_price[]"
                )

                discount_percents = request.POST.getlist(
                    "item_discount_percent[]"
                )

                tax_percents = request.POST.getlist(
                    "item_tax_percent[]"
                )

                # =================================================
                # CHECK ITEMS
                # =================================================

                valid_item_found = False

                # =================================================
                # SAVE ITEMS
                # =================================================

                for index, description in enumerate(descriptions):

                    description = (
                        description or ""
                    ).strip()

                    if not description:
                        continue

                    valid_item_found = True

                    # ---------------------------------------------
                    # HSN / SAC
                    # ---------------------------------------------

                    hsn_sac = (
                        hsn_sacs[index]
                        if index < len(hsn_sacs)
                        else ""
                    )

                    hsn_sac = (
                        hsn_sac or ""
                    ).strip()

                    # ---------------------------------------------
                    # QUANTITY
                    # ---------------------------------------------

                    quantity_raw = (
                        quantities[index]
                        if index < len(quantities)
                        else "1"
                    )

                    try:
                        quantity = Decimal(
                            quantity_raw or "1"
                        )
                    except (ValueError, TypeError, InvalidOperation):
                        quantity = Decimal("1.00")

                    if quantity <= Decimal("0"):
                        quantity = Decimal("1.00")

                    # ---------------------------------------------
                    # UNIT
                    # ---------------------------------------------

                    unit = (
                        units[index]
                        if index < len(units)
                        else "Unit"
                    )

                    unit = (
                        unit or "Unit"
                    ).strip()

                    # ---------------------------------------------
                    # UNIT PRICE
                    # ---------------------------------------------

                    unit_price_raw = (
                        unit_prices[index]
                        if index < len(unit_prices)
                        else "0"
                    )

                    try:
                        unit_price = Decimal(
                            unit_price_raw or "0"
                        )
                    except (ValueError, TypeError, InvalidOperation):
                        unit_price = Decimal("0.00")

                    if unit_price < Decimal("0"):
                        unit_price = Decimal("0.00")

                    # ---------------------------------------------
                    # DISCOUNT %
                    # ---------------------------------------------

                    discount_raw = (
                        discount_percents[index]
                        if index < len(discount_percents)
                        else "0"
                    )

                    try:
                        discount_percent = Decimal(
                            discount_raw or "0"
                        )
                    except (ValueError, TypeError, InvalidOperation):
                        discount_percent = Decimal("0.00")

                    if discount_percent < Decimal("0"):
                        discount_percent = Decimal("0.00")

                    if discount_percent > Decimal("100"):
                        discount_percent = Decimal("100.00")

                    # ---------------------------------------------
                    # TAX %
                    # ---------------------------------------------

                    tax_raw = (
                        tax_percents[index]
                        if index < len(tax_percents)
                        else "0"
                    )

                    try:
                        tax_percent = Decimal(
                            tax_raw or "0"
                        )
                    except (ValueError, TypeError, InvalidOperation):
                        tax_percent = Decimal("0.00")

                    if tax_percent < Decimal("0"):
                        tax_percent = Decimal("0.00")

                    if tax_percent > Decimal("100"):
                        tax_percent = Decimal("100.00")

                    # ---------------------------------------------
                    # CREATE ITEM
                    # ---------------------------------------------

                    InvoiceItem.objects.create(

                        invoice=invoice,

                        description=description,

                        hsn_sac=hsn_sac,

                        quantity=quantity,

                        unit=unit,

                        unit_price=unit_price,

                        discount_percent=discount_percent,

                        tax_percent=tax_percent,

                        order=index,
                    )

                # =================================================
                # REQUIRE AT LEAST ONE ITEM
                # =================================================

                if not valid_item_found:

                    raise ValueError(
                        "Please add at least one invoice item."
                    )

                # =================================================
                # FINAL TOTAL CALCULATION
                # =================================================

                invoice.calculate_totals()

                invoice.save()

            # =====================================================
            # SUCCESS
            # =====================================================

            messages.success(
                request,
                f"Invoice {invoice.invoice_number} created successfully."
            )

            return redirect(
                "invoice_detail",
                invoice_id=invoice.id
            )

        except Exception as e:

            # ---------------------------------------------
            # PRINT EXACT ERROR IN TERMINAL
            # ---------------------------------------------

            print("\n")
            print("=" * 70)
            print("INVOICE CREATION ERROR")
            print("=" * 70)
            print(type(e).__name__)
            print(str(e))
            print("=" * 70)
            print("\n")

            messages.error(
                request,
                f"Unable to create invoice: {type(e).__name__}: {str(e)}"
            )

    return render(
        request,
        "admin/create_invoice.html",
        {
            "clients": clients,
            "projects": projects,
            "today": timezone.localdate(),
        }
    )


# =========================================================
# INVOICE DETAIL
# =========================================================

@login_required(login_url="login")
def invoice_detail(request, invoice_id):

    if request.user.role != "admin":
        messages.error(
            request,
            "You are not authorized to view invoices."
        )
        return redirect("employee-dashboard")

    invoice = get_object_or_404(
        Invoice.objects
        .select_related("client", "project")
        .prefetch_related("items"),
        id=invoice_id
    )

    return render(
        request,
        "admin/invoice_detail.html",
        {
            "invoice": invoice,
            "items": invoice.items.all(),
        }
    )


# =========================================================
# DELETE INVOICE
# =========================================================

@login_required(login_url="login")
def delete_invoice(request, invoice_id):

    if request.user.role != "admin":
        messages.error(
            request,
            "You are not authorized to delete invoices."
        )
        return redirect("employee-dashboard")

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )

    if request.method == "POST":

        invoice_number = invoice.invoice_number

        invoice.delete()

        messages.success(
            request,
            f"Invoice {invoice_number} deleted successfully."
        )

    return redirect("invoice_list")