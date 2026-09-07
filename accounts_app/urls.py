from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        "",
        views.home,
        name="home"
    ),


    # =====================================================
    # LOGIN / LOGOUT
    # =====================================================

    path(
        "login/",
        views.login_page,
        name="login"
    ),

    path(
        "logout/",
        views.logout_page,
        name="logout"
    ),


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),


    # =====================================================
    # EMPLOYEES
    # =====================================================

    path(
        "employees/",
        views.employees,
        name="employees"
    ),

    path(
        "employees/add/",
        views.add_employee,
        name="add_employee"
    ),

    path(
        "employees/edit/<int:employee_id>/",
        views.edit_employee,
        name="edit_employee"
    ),

    path(
        "employees/delete/<int:employee_id>/",
        views.delete_employee,
        name="delete_employee"
    ),


    # =====================================================
    # STUDENTS
    # =====================================================

    path(
        "students/",
        views.students,
        name="students"
    ),

    path(
        "students/add/",
        views.add_student,
        name="add_student"
    ),

    path(
        "students/edit/<int:student_id>/",
        views.edit_student,
        name="edit_student"
    ),

    path(
        "students/delete/<int:student_id>/",
        views.delete_student,
        name="delete_student"
    ),

    path(
        "students/<int:student_id>/",
        views.student_detail,
        name="student_detail"
    ),


    # =====================================================
    # CLIENTS
    # =====================================================

    path(
        "clients/",
        views.clients,
        name="clients"
    ),

    path(
        "clients/add/",
        views.add_client,
        name="add_client"
    ),

    path(
        "clients/edit/<int:client_id>/",
        views.edit_client,
        name="edit_client"
    ),

    path(
        "clients/delete/<int:client_id>/",
        views.delete_client,
        name="delete_client"
    ),

    path(
        "clients/<int:client_id>/",
        views.client_detail,
        name="client_detail"
    ),


    # =====================================================
    # PROJECTS
    # =====================================================

    path(
        "projects/",
        views.projects,
        name="projects"
    ),

    path(
        "projects/add/",
        views.add_project,
        name="add_project"
    ),

    path(
        "projects/edit/<int:project_id>/",
        views.edit_project,
        name="edit_project"
    ),

    path(
        "projects/delete/<int:project_id>/",
        views.delete_project,
        name="delete_project"
    ),

    path(
        "projects/<int:project_id>/",
        views.project_detail,
        name="project_detail"
    ),


    # =====================================================
    # PROJECT TASKS
    # =====================================================

    path(
        "projects/<int:project_id>/tasks/",
        views.project_tasks,
        name="project_tasks"
    ),

    path(
        "projects/<int:project_id>/tasks/add/",
        views.add_project_tasks,
        name="add_project_tasks"
    ),

    path(
        "project-task/<int:task_id>/",
        views.project_task_details,
        name="project_task_details"
    ),

    path(
        "project-task/<int:task_id>/edit/",
        views.edit_project_task,
        name="edit_project_task"
    ),

    path(
        "project-task/<int:task_id>/admin-comment/",
        views.project_task_admin_comment,
        name="project_task_admin_comment"
    ),
    # =========================================================
# DELETE PROJECT TASK
# =========================================================

path(
    "projects/tasks/delete/<int:task_id>/",
    views.delete_project_task,
    name="delete_project_task"
),

    # =====================================================
    # TASKS - ADMIN
    # =====================================================

    path(
        "tasks/",
        views.tasks,
        name="tasks"
    ),

    path(
        "tasks/add/",
        views.add_task,
        name="add_task"
    ),

    path(
        "tasks/edit/<int:task_id>/",
        views.edit_task,
        name="edit_task"
    ),

    path(
        "tasks/delete/<int:task_id>/",
        views.delete_task,
        name="delete_task"
    ),

    path(
        "tasks/comment/<int:task_id>/",
        views.admin_task_comment,
        name="admin_task_comment"
    ),

    path(
        "tasks/view/<int:task_id>/",
        views.task_detail,
        name="task_detail"
    ),


    # =====================================================
    # EMPLOYEE DASHBOARD
    # =====================================================

    path(
        "employee-dashboard/",
        views.employee_dashboard,
        name="employee_dashboard"
    ),


    # =====================================================
    # EMPLOYEE TASK STATUS
    # =====================================================

    path(
        "tasks/update/<int:task_id>/",
        views.update_task_status,
        name="update_task_status"
    ),

    path(
        "employee/tasks/",
        views.employee_tasks,
        name="employee_tasks"
    ),

    path(
        "employee/task/<int:task_id>/update/",
        views.employee_task_update,
        name="employee_task_update"
    ),

    path(
        "employee/project/<int:project_id>/",
        views.employee_project_details,
        name="employee_project_details"
    ),


    # =====================================================
    # EMPLOYEE LEAVE
    # =====================================================

    path(
        "employee/leave/apply/",
        views.apply_leave,
        name="apply_leave"
    ),


    # =====================================================
    # EMPLOYEE ATTENDANCE
    # =====================================================

    path(
        "attendance/",
        views.attendance,
        name="attendance"
    ),


    # =====================================================
    # ADMIN ATTENDANCE REPORTS
    # =====================================================

    path(
        "attendance-reports/",
        views.attendance_reports,
        name="attendance_reports"
    ),


    # =====================================================
    # ADMIN ATTENDANCE HISTORY
    # =====================================================

    path(
        "attendance-history/",
        views.attendance_history,
        name="attendance_history"
    ),
    
    path(
    "todo/",
    views.todo_list,
    name="todo_list"
),
    
    path(
    "holidays/",
    views.manage_holidays,
    name="manage_holidays"
),
    # =========================================================
# CHAT
# =========================================================

path(
    "chat/users/",
    views.chat_users,
    name="chat_users"
),

path(
    "chat/messages/<int:user_id>/",
    views.chat_messages,
    name="chat_messages"
),

path(
    "chat/send/<int:user_id>/",
    views.chat_send_message,
    name="chat_send_message"
),

path(
    "chat/status/",
    views.chat_update_status,
    name="chat_update_status"
),

# =========================================================
# INVOICE ROUTES
# =========================================================

path(
    "invoices/",
    views.invoice_list,
    name="invoice_list"
),

path(
    "invoices/create/",
    views.create_invoice,
    name="create_invoice"
),

path(
    "invoices/<int:invoice_id>/",
    views.invoice_detail,
    name="invoice_detail"
),

path(
    "invoices/<int:invoice_id>/delete/",
    views.delete_invoice,
    name="delete_invoice"
),
]