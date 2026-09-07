from django.conf import settings
from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


class Todo(models.Model):

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="todos"
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    due_date = models.DateField(
        blank=True,
        null=True
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    is_completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["is_completed", "-created_at"]

    def __str__(self):
        return self.title

# =========================================================
# STUDENT
# =========================================================

class Student(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("completed", "Completed"),
    ]

    LEARNING_MODE_CHOICES = [
        ("online", "Online"),
        ("offline", "Offline"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("partial", "Partially Paid"),
        ("paid", "Paid"),
    ]

    # -----------------------------------------------------
    # PERSONAL DETAILS
    # -----------------------------------------------------

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # STUDENT DOCUMENTS
    # -----------------------------------------------------

    photo = models.ImageField(
        upload_to="students/photos/",
        blank=True,
        null=True
    )

    aadhaar_card = models.FileField(
        upload_to="students/aadhaar/",
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # COURSE DETAILS
    # -----------------------------------------------------

    course = models.CharField(
        max_length=150,
        blank=True
    )

    batch = models.CharField(
        max_length=100,
        blank=True
    )

    joining_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    # -----------------------------------------------------
    # ASSIGNED EMPLOYEE
    # -----------------------------------------------------

    assigned_employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_students",
        limit_choices_to={
            "role": "employee"
        }
    )

    # -----------------------------------------------------
    # LEARNING MODE
    # -----------------------------------------------------

    learning_mode = models.CharField(
        max_length=20,
        choices=LEARNING_MODE_CHOICES,
        default="online"
    )

    # -----------------------------------------------------
    # COURSE DURATION
    # -----------------------------------------------------

    course_duration_months = models.PositiveIntegerField(
        default=0,
        blank=True
    )

    course_duration_days = models.PositiveIntegerField(
        default=0,
        blank=True
    )

    # -----------------------------------------------------
    # FEE DETAILS
    # -----------------------------------------------------

    total_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # IMPORTANT:
    # Monthly fee belongs to Student.
    # It is the regular monthly course fee.
    monthly_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # Automatically calculated from StudentFeePayment
    fee_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    # -----------------------------------------------------
    # CERTIFICATE
    # -----------------------------------------------------

    certificate_status = models.CharField(
        max_length=20,
        choices=[
            ("not_issued", "Not Issued"),
            ("issued", "Certificate Issued"),
        ],
        default="not_issued"
    )

    # -----------------------------------------------------
    # ADDITIONAL DETAILS
    # -----------------------------------------------------

    notes = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # TIMESTAMPS
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # -----------------------------------------------------
    # REMAINING FEE
    # -----------------------------------------------------

    @property
    def remaining_fee(self):

        remaining = (
            self.total_fee -
            self.fee_paid
        )

        if remaining < Decimal("0.00"):
            return Decimal("0.00")

        return remaining

    # -----------------------------------------------------
    # AUTO PAYMENT STATUS
    # -----------------------------------------------------

    def update_payment_status(self):

        if self.fee_paid <= Decimal("0.00"):

            self.payment_status = "pending"

        elif self.fee_paid >= self.total_fee:

            self.payment_status = "paid"

        else:

            self.payment_status = "partial"

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    def save(self, *args, **kwargs):

        self.update_payment_status()

        super().save(*args, **kwargs)

    # -----------------------------------------------------
    # STRING
    # -----------------------------------------------------

    def __str__(self):

        return (
            f"{self.first_name} "
            f"{self.last_name}"
        ).strip()


# =========================================================
# STUDENT FEE PAYMENT
# =========================================================

class StudentFeePayment(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ("paid", "Paid"),
        ("pending", "Pending"),
    ]

    # -----------------------------------------------------
    # STUDENT
    # -----------------------------------------------------

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="monthly_payments"
    )

    # -----------------------------------------------------
    # PAYMENT MONTH
    # -----------------------------------------------------

    payment_month = models.DateField()

    # -----------------------------------------------------
    # PAYMENT AMOUNT
    # -----------------------------------------------------

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # -----------------------------------------------------
    # PAYMENT DATE
    # -----------------------------------------------------

    payment_date = models.DateField(
        null=True,
        blank=True
    )

    # -----------------------------------------------------
    # PAYMENT STATUS
    # -----------------------------------------------------

    status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default="paid"
    )

    # -----------------------------------------------------
    # TIMESTAMP
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

    class Meta:

        ordering = [
            "payment_month"
        ]

        indexes = [

            models.Index(
                fields=[
                    "student",
                    "payment_month"
                ]
            ),

            models.Index(
                fields=[
                    "student",
                    "status"
                ]
            ),

        ]

        verbose_name = "Student Fee Payment"

        verbose_name_plural = "Student Fee Payments"

    # -----------------------------------------------------
    # STRING
    # -----------------------------------------------------

    def __str__(self):

        return (
            f"{self.student} - "
            f"{self.payment_month} - "
            f"₹{self.amount}"
        )


# =========================================================
# CLIENT
# =========================================================

class Client(models.Model):

    CLIENT_TYPE_CHOICES = [
        ("indian", "Indian"),
        ("foreigner", "Foreigner"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    # -----------------------------------------------------
    # BASIC DETAILS
    # -----------------------------------------------------

    name = models.CharField(
        max_length=150
    )

    company_name = models.CharField(
        max_length=200,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    country = models.CharField(
        max_length=100,
        default="India"
    )

    client_type = models.CharField(
        max_length=20,
        choices=CLIENT_TYPE_CHOICES,
        default="indian"
    )

    address = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    # -----------------------------------------------------
    # ADDITIONAL DETAILS
    # -----------------------------------------------------

    notes = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # TIMESTAMPS
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # -----------------------------------------------------
    # STRING
    # -----------------------------------------------------

    def __str__(self):

        if self.company_name:

            return (
                f"{self.name} - "
                f"{self.company_name}"
            )

        return self.name

    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = "Client"

        verbose_name_plural = "Clients"


# =========================================================
# PROJECT
# =========================================================

class Project(models.Model):

    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("in_progress", "In Progress"),
        ("testing", "Testing"),
        ("on_hold", "On Hold"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    PROJECT_TYPE_CHOICES = [
        ("website", "Website"),
        ("web_application", "Web Application"),
        ("mobile_application", "Mobile Application"),
        ("software", "Software"),
        ("ecommerce", "E-Commerce"),
        ("api", "API / Integration"),
        ("maintenance", "Maintenance"),
        ("other", "Other"),
    ]

    # -----------------------------------------------------
    # BASIC PROJECT DETAILS
    # -----------------------------------------------------

    project_name = models.CharField(
        max_length=200
    )

    project_code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # CLIENT
    # -----------------------------------------------------

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    # -----------------------------------------------------
    # PROJECT TYPE
    # -----------------------------------------------------

    project_type = models.CharField(
        max_length=50,
        choices=PROJECT_TYPE_CHOICES,
        default="website"
    )

    # -----------------------------------------------------
    # DESCRIPTION
    # -----------------------------------------------------

    description = models.TextField(
        blank=True
    )

    requirements = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # TECHNOLOGIES / TOOLS
    # -----------------------------------------------------

    technology_stack = models.TextField(
        blank=True,
        help_text=(
            "Example: Django, Python, MySQL, "
            "HTML, CSS, JavaScript"
        )
    )

    # -----------------------------------------------------
    # TEAM MEMBERS
    # -----------------------------------------------------

    project_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_projects",
        limit_choices_to={
            "role": "employee"
        }
    )

    designer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="designed_projects",
        limit_choices_to={
            "role": "employee"
        }
    )

    developer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="developed_projects",
        limit_choices_to={
            "role": "employee"
        }
    )

    tester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tested_projects",
        limit_choices_to={
            "role": "employee"
        }
    )

    # -----------------------------------------------------
    # PROJECT COST
    # -----------------------------------------------------

    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    development_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    paid_development_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    development_payment_date = models.DateField(
        null=True,
        blank=True
    )

    designer_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    tester_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # -----------------------------------------------------
    # TIMELINE
    # -----------------------------------------------------

    start_date = models.DateField(
        null=True,
        blank=True
    )

    expected_end_date = models.DateField(
        null=True,
        blank=True
    )

    estimated_days = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Estimated project duration in days"
    )

    actual_end_date = models.DateField(
        null=True,
        blank=True
    )

    # -----------------------------------------------------
    # STATUS & PRIORITY
    # -----------------------------------------------------

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="planning"
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    # -----------------------------------------------------
    # PROGRESS
    # -----------------------------------------------------

    progress = models.PositiveIntegerField(
        default=0,
        help_text="Project completion percentage"
    )

    # -----------------------------------------------------
    # ADDITIONAL DETAILS
    # -----------------------------------------------------

    notes = models.TextField(
        blank=True
    )

    # -----------------------------------------------------
    # TIMESTAMPS
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    def save(self, *args, **kwargs):

        if self.progress < 0:
            self.progress = 0

        if self.progress > 100:
            self.progress = 100

        if self.total_cost < Decimal("0.00"):
            self.total_cost = Decimal("0.00")

        if self.development_cost < Decimal("0.00"):
            self.development_cost = Decimal("0.00")

        if self.paid_development_cost < Decimal("0.00"):
            self.paid_development_cost = Decimal("0.00")

        if self.designer_cost < Decimal("0.00"):
            self.designer_cost = Decimal("0.00")

        if self.tester_cost < Decimal("0.00"):
            self.tester_cost = Decimal("0.00")

        super().save(*args, **kwargs)

    # -----------------------------------------------------
    # STRING
    # -----------------------------------------------------

    def __str__(self):

        return self.project_name

    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = "Project"

        verbose_name_plural = "Projects"


# =========================================================
# TASK
# =========================================================

class Task(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    # -----------------------------------------------------
    # TASK DETAILS
    # -----------------------------------------------------

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # PROJECT
    # -----------------------------------------------------

    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks"
    )

    # -----------------------------------------------------
    # ASSIGNED EMPLOYEE
    # -----------------------------------------------------

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_tasks",
        limit_choices_to={
            "role": "employee"
        }
    )

    # -----------------------------------------------------
    # DATE / TIME
    # -----------------------------------------------------

    task_date = models.DateField()

    due_time = models.TimeField(
        null=True,
        blank=True
    )

    # -----------------------------------------------------
    # PRIORITY
    # -----------------------------------------------------

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # -----------------------------------------------------
    # EMPLOYEE UPDATE
    # -----------------------------------------------------

    employee_comment = models.TextField(
        blank=True,
        default="",
        help_text=(
            "Comment/update provided by "
            "the assigned employee"
        )
    )

    # -----------------------------------------------------
    # REMAINING DAYS
    # -----------------------------------------------------

    remaining_days = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=(
            "Approximate number of days remaining "
            "to complete the task"
        )
    )

    # -----------------------------------------------------
    # TIMESTAMPS
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # -----------------------------------------------------
    # STRING
    # -----------------------------------------------------

    def __str__(self):

        return self.title

    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

    class Meta:

        ordering = [
            "-created_at"
        ]

        indexes = [

            models.Index(
                fields=[
                    "assigned_to"
                ]
            ),

            models.Index(
                fields=[
                    "assigned_to",
                    "status"
                ]
            ),

            models.Index(
                fields=[
                    "task_date"
                ]
            ),

        ]

        verbose_name = "Task"

        verbose_name_plural = "Tasks"


# =========================================================
# TASK COMMENTS
# =========================================================

class TaskComment(models.Model):

    # -----------------------------------------------------
    # TASK
    # -----------------------------------------------------

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    # -----------------------------------------------------
    # COMMENT AUTHOR
    # -----------------------------------------------------

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_comments"
    )

    # -----------------------------------------------------
    # COMMENT
    # -----------------------------------------------------

    comment = models.TextField()

    # -----------------------------------------------------
    # TIMESTAMP
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # -----------------------------------------------------
    # STRING
    # -----------------------------------------------------

    def __str__(self):

        return (
            f"{self.task.title} - "
            f"{self.user.get_full_name() or self.user.username}"
        )

    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

    class Meta:

        ordering = [
            "created_at"
        ]

        indexes = [

            models.Index(
                fields=[
                    "task"
                ]
            ),

            models.Index(
                fields=[
                    "user"
                ]
            ),

            models.Index(
                fields=[
                    "task",
                    "created_at"
                ]
            ),

        ]

        verbose_name = "Task Comment"

        verbose_name_plural = "Task Comments"


# =========================================================
# ATTENDANCE
# =========================================================

class Attendance(models.Model):

    STATUS_CHOICES = [

        ("present", "Present"),

        ("absent", "Absent"),

        ("half_day", "Half Day"),

        ("leave", "Leave"),

    ]

    # -----------------------------------------------------
    # EMPLOYEE
    # -----------------------------------------------------

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        limit_choices_to={
            "role": "employee"
        }
    )

    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    date = models.DateField()

    # -----------------------------------------------------
    # CHECK IN
    # -----------------------------------------------------

    check_in = models.TimeField(
        null=True,
        blank=True
    )

    # -----------------------------------------------------
    # CHECK OUT
    # -----------------------------------------------------

    check_out = models.TimeField(
        null=True,
        blank=True
    )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="present"
    )

    # -----------------------------------------------------
    # REMARKS
    # -----------------------------------------------------

    remarks = models.CharField(
        max_length=255,
        blank=True
    )

    # -----------------------------------------------------
    # TIMESTAMPS
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "employee",
                    "date"
                ],
                name="unique_employee_attendance_per_day"
            )

        ]

        ordering = [
            "-date"
        ]

        indexes = [

            models.Index(
                fields=[
                    "employee",
                    "date"
                ]
            ),

            models.Index(
                fields=[
                    "date"
                ]
            ),

            models.Index(
                fields=[
                    "employee",
                    "status"
                ]
            ),

        ]

        verbose_name = "Attendance"

        verbose_name_plural = "Attendance Records"

    # -----------------------------------------------------
    # STRING
    # -----------------------------------------------------

    def __str__(self):

        return (
            f"{self.employee.username} - "
            f"{self.date} - "
            f"{self.get_status_display()}"
        )

# =========================================================
# COMPANY HOLIDAY
# =========================================================

class Holiday(models.Model):

    date = models.DateField(
        unique=True
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.date} - {self.name}"

    class Meta:
        ordering = ["-date"]
        verbose_name = "Holiday"
        verbose_name_plural = "Holidays"



# =========================================================
# LEAVE
# =========================================================

class Leave(models.Model):

    STATUS_CHOICES = [

        ("pending", "Pending"),

        ("approved", "Approved"),

        ("rejected", "Rejected"),

    ]

    # -----------------------------------------------------
    # EMPLOYEE
    # -----------------------------------------------------

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leave_requests",
        limit_choices_to={
            "role": "employee"
        }
    )

    # -----------------------------------------------------
    # LEAVE DATE
    # -----------------------------------------------------

    leave_date = models.DateField()

    # -----------------------------------------------------
    # REASON
    # -----------------------------------------------------

    reason = models.TextField(
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # -----------------------------------------------------
    # ADMIN REMARKS
    # -----------------------------------------------------

    admin_remarks = models.TextField(
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # APPLIED DATE / TIME
    # -----------------------------------------------------

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    # -----------------------------------------------------
    # UPDATED DATE / TIME
    # -----------------------------------------------------

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

    class Meta:

        ordering = [
            "-leave_date",
            "-applied_at"
        ]

        indexes = [

            models.Index(
                fields=[
                    "employee",
                    "leave_date"
                ]
            ),

            models.Index(
                fields=[
                    "leave_date"
                ]
            ),

            models.Index(
                fields=[
                    "employee",
                    "status"
                ]
            ),

        ]

        verbose_name = "Leave"

        verbose_name_plural = "Leave Requests"

    # -----------------------------------------------------
    # STRING
    # -----------------------------------------------------

    def __str__(self):

        return (
            f"{self.employee.username} - "
            f"{self.leave_date} - "
            f"{self.get_status_display()}"
        )

# =========================================================
# CHAT MESSAGE
# =========================================================

class ChatMessage(models.Model):

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_chat_messages"
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_chat_messages"
    )

    message = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender} → {self.receiver}"


# =========================================================
# USER CHAT STATUS
# =========================================================

class UserStatus(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_status"
    )

    is_online = models.BooleanField(
        default=False
    )

    last_seen = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):

        return (
            f"{self.user} - "
            f"{'Online' if self.is_online else 'Offline'}"
        )
        
        # =========================================================
# INVOICE
# =========================================================

class Invoice(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("paid", "Paid"),
        ("partial", "Partially Paid"),
        ("overdue", "Overdue"),
        ("cancelled", "Cancelled"),
    ]

    TAX_TYPE_CHOICES = [
        ("none", "No Tax"),
        ("gst", "GST"),
        ("igst", "IGST"),
    ]

    CURRENCY_CHOICES = [
        ("INR", "Indian Rupee (₹)"),
        ("USD", "US Dollar ($)"),
        ("EUR", "Euro (€)"),
        ("GBP", "British Pound (£)"),
    ]

    # -----------------------------------------------------
    # INVOICE NUMBER
    # -----------------------------------------------------

    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True
    )

    # -----------------------------------------------------
    # CLIENT
    # -----------------------------------------------------

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    # -----------------------------------------------------
    # PROJECT
    # -----------------------------------------------------

    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices"
    )

    # -----------------------------------------------------
    # INVOICE DATE
    # -----------------------------------------------------

    invoice_date = models.DateField()

    # -----------------------------------------------------
    # DUE DATE
    # -----------------------------------------------------

    due_date = models.DateField(
        null=True,
        blank=True
    )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    # -----------------------------------------------------
    # CURRENCY
    # -----------------------------------------------------

    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default="INR"
    )

    # -----------------------------------------------------
    # TAX TYPE
    # -----------------------------------------------------

    tax_type = models.CharField(
        max_length=10,
        choices=TAX_TYPE_CHOICES,
        default="gst"
    )

    # -----------------------------------------------------
    # GSTIN
    # -----------------------------------------------------

    client_gstin = models.CharField(
        max_length=20,
        blank=True
    )

    # -----------------------------------------------------
    # REFERENCE / PO NUMBER
    # -----------------------------------------------------

    reference_number = models.CharField(
        max_length=100,
        blank=True
    )

    # -----------------------------------------------------
    # PAYMENT TERMS
    # -----------------------------------------------------

    payment_terms = models.CharField(
        max_length=255,
        blank=True,
        default="Payment due within 30 days."
    )

    # -----------------------------------------------------
    # FINANCIAL DETAILS
    # -----------------------------------------------------

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    cgst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    sgst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    igst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    balance_due = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # -----------------------------------------------------
    # NOTES
    # -----------------------------------------------------

    notes = models.TextField(
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # TERMS & CONDITIONS
    # -----------------------------------------------------

    terms = models.TextField(
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # PAYMENT INFORMATION
    # -----------------------------------------------------

    payment_method = models.CharField(
        max_length=100,
        blank=True
    )

    payment_reference = models.CharField(
        max_length=150,
        blank=True
    )

    # -----------------------------------------------------
    # TIMESTAMPS
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # -----------------------------------------------------
    # CALCULATE TOTALS
    # -----------------------------------------------------

    def calculate_totals(self):

        items = self.items.all()

        subtotal = Decimal("0.00")
        discount = Decimal("0.00")
        tax_amount = Decimal("0.00")

        for item in items:

            subtotal += item.line_subtotal
            discount += item.discount_amount
            tax_amount += item.tax_amount

        taxable_amount = (
            subtotal - discount
        )

        if taxable_amount < Decimal("0.00"):
            taxable_amount = Decimal("0.00")

        total_amount = (
            taxable_amount + tax_amount
        )

        balance_due = (
            total_amount - self.amount_paid
        )

        if balance_due < Decimal("0.00"):
            balance_due = Decimal("0.00")

        self.subtotal = subtotal
        self.discount = discount
        self.tax_amount = tax_amount
        self.total_amount = total_amount
        self.balance_due = balance_due

        # -------------------------------------------------
        # GST SPLIT
        # -------------------------------------------------

        if self.tax_type == "gst":

            self.cgst_amount = (
                tax_amount / Decimal("2")
            )

            self.sgst_amount = (
                tax_amount / Decimal("2")
            )

            self.igst_amount = Decimal("0.00")

        elif self.tax_type == "igst":

            self.igst_amount = tax_amount

            self.cgst_amount = Decimal("0.00")
            self.sgst_amount = Decimal("0.00")

        else:

            self.cgst_amount = Decimal("0.00")
            self.sgst_amount = Decimal("0.00")
            self.igst_amount = Decimal("0.00")

        # -------------------------------------------------
        # PAYMENT STATUS
        # -------------------------------------------------

        if self.amount_paid <= Decimal("0.00"):

            if self.status != "cancelled":
                self.status = "draft"

        elif self.amount_paid >= total_amount:

            if self.status != "cancelled":
                self.status = "paid"

        else:

            if self.status != "cancelled":
                self.status = "partial"

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    def save(self, *args, **kwargs):

        if not self.invoice_number:

            last_invoice = (
                Invoice.objects
                .order_by("-id")
                .first()
            )

            if last_invoice:

                next_number = last_invoice.id + 1

            else:

                next_number = 1

            self.invoice_number = (
                f"INV-{next_number:04d}"
            )

        if self.amount_paid < Decimal("0.00"):

            self.amount_paid = Decimal("0.00")

        super().save(*args, **kwargs)

    # -----------------------------------------------------
    # STRING
    # -----------------------------------------------------

    def __str__(self):

        return (
            f"{self.invoice_number} - "
            f"{self.client}"
        )

    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

    class Meta:

        ordering = [
            "-created_at"
        ]

        indexes = [

            models.Index(
                fields=[
                    "invoice_number"
                ]
            ),

            models.Index(
                fields=[
                    "client"
                ]
            ),

            models.Index(
                fields=[
                    "project"
                ]
            ),

            models.Index(
                fields=[
                    "status"
                ]
            ),

            models.Index(
                fields=[
                    "invoice_date"
                ]
            ),

            models.Index(
                fields=[
                    "due_date"
                ]
            ),

        ]

        verbose_name = "Invoice"

        verbose_name_plural = "Invoices"


# =========================================================
# INVOICE ITEM
# =========================================================

class InvoiceItem(models.Model):

    # -----------------------------------------------------
    # INVOICE
    # -----------------------------------------------------

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="items"
    )

    # -----------------------------------------------------
    # ITEM DESCRIPTION
    # -----------------------------------------------------

    description = models.CharField(
        max_length=500
    )

    # -----------------------------------------------------
    # HSN / SAC
    # -----------------------------------------------------

    hsn_sac = models.CharField(
        max_length=50,
        blank=True
    )

    # -----------------------------------------------------
    # QUANTITY
    # -----------------------------------------------------

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("1.00")
    )

    # -----------------------------------------------------
    # UNIT
    # -----------------------------------------------------

    unit = models.CharField(
        max_length=50,
        default="Unit",
        blank=True
    )

    # -----------------------------------------------------
    # UNIT PRICE
    # -----------------------------------------------------

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # -----------------------------------------------------
    # DISCOUNT
    # -----------------------------------------------------

    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # -----------------------------------------------------
    # TAX
    # -----------------------------------------------------

    tax_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # -----------------------------------------------------
    # CALCULATED AMOUNTS
    # -----------------------------------------------------

    line_subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    taxable_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # -----------------------------------------------------
    # DISPLAY ORDER
    # -----------------------------------------------------

    order = models.PositiveIntegerField(
        default=0
    )

    # -----------------------------------------------------
    # TIMESTAMP
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # -----------------------------------------------------
    # CALCULATE ITEM
    # -----------------------------------------------------

    def calculate_amounts(self):

        quantity = self.quantity or Decimal("0.00")

        unit_price = (
            self.unit_price or Decimal("0.00")
        )

        discount_percent = (
            self.discount_percent or Decimal("0.00")
        )

        tax_percent = (
            self.tax_percent or Decimal("0.00")
        )

        # -------------------------------------------------
        # SUBTOTAL
        # -------------------------------------------------

        self.line_subtotal = (
            quantity * unit_price
        )

        # -------------------------------------------------
        # DISCOUNT
        # -------------------------------------------------

        self.discount_amount = (
            self.line_subtotal *
            discount_percent /
            Decimal("100")
        )

        # -------------------------------------------------
        # TAXABLE AMOUNT
        # -------------------------------------------------

        self.taxable_amount = (
            self.line_subtotal -
            self.discount_amount
        )

        if self.taxable_amount < Decimal("0.00"):

            self.taxable_amount = Decimal("0.00")

        # -------------------------------------------------
        # TAX
        # -------------------------------------------------

        self.tax_amount = (
            self.taxable_amount *
            tax_percent /
            Decimal("100")
        )

        # -------------------------------------------------
        # FINAL AMOUNT
        # -------------------------------------------------

        self.amount = (
            self.taxable_amount +
            self.tax_amount
        )

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    def save(self, *args, **kwargs):

        self.calculate_amounts()

        super().save(*args, **kwargs)

        # -------------------------------------------------
        # UPDATE INVOICE TOTALS
        # -------------------------------------------------

        self.invoice.calculate_totals()

        self.invoice.save(
            update_fields=[
                "subtotal",
                "discount",
                "tax_amount",
                "cgst_amount",
                "sgst_amount",
                "igst_amount",
                "total_amount",
                "balance_due",
                "status",
                "updated_at",
            ]
        )

    # -----------------------------------------------------
    # STRING
    # -----------------------------------------------------

    def __str__(self):

        return (
            f"{self.invoice.invoice_number} - "
            f"{self.description}"
        )

    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

    class Meta:

        ordering = [
            "order",
            "id"
        ]

        indexes = [

            models.Index(
                fields=[
                    "invoice"
                ]
            ),

        ]

        verbose_name = "Invoice Item"

        verbose_name_plural = "Invoice Items"