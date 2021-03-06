import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import DetailView, RedirectView, UpdateView, DeleteView, CreateView, ListView
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse

from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.template import RequestContext

from .models import Employee, EmergencyContact, Salary, Department, Designation, Vacation
from .forms import EmployeeUpdateForm, EmergencyContactCreateForm, VacationCreateForm, VacationUpdateForm

# Create your views here.

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    """
    Lists employees for a given user
    """
    login_url = "/login/"

    def get_object(self):
        
        user = self.request.user
        profile_user = User.objects.filter(username=self.kwargs.get("username"))[:1].get()

        if user.userprofile.role == "MANAGER":
        
            if profile_user is None:
                raise Http404
            return get_object_or_404(Employee, owner=profile_user)

        else:

            if user != profile_user:
                raise Http404
            
            return get_object_or_404(Employee, owner=user)


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    """
    View to update employee's personal imformation
    """
    form_class = EmployeeUpdateForm
    template_name = "user/profile_info.html"
    success_url = "/"

    def get_object(self):
        username = self.request.user
        return get_object_or_404(Employee, owner=username)

class ProfileRedirectView(RedirectView):
    """
    Redirect to the main profile page for the user
    """
    permanent = False

    def get_redirect_url(self, *args, **kwards):
        username = self.request.user

        if username is None:
            raise Http404
        elif str(username) == "AnonymousUser":
            return "/vacations"
            
        return "/profile/{}".format(username)

class EmergencyContactDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to delete emergency contact
    """
    form_class = EmergencyContact
    template_name = "user/emergencycontact_confirm_delete.html"
    success_url = "/"
    
    def get_object(self, queryset=None):
        return get_object_or_404(EmergencyContact, id=self.kwargs.get("contact"))

class EmergencyContactCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new emergency contact
    """
    form_class = EmergencyContactCreateForm
    template_name = 'user/emergencycontact_create.html'
    success_url = "/"

    def form_valid(self, form):
        form.instance.employee = Employee.objects.filter(owner=self.request.user)[:1].get()
        return super(EmergencyContactCreateView, self).form_valid(form)

class SalaryListView(LoginRequiredMixin, ListView):
    """
    Provides a list of holidays
    """
    login_url = "/login/"
    template_name = "user/salary_list.html"

    def get_queryset(self):
        user = self.request.user
        
        if user.userprofile.role == "MANAGER":
            return Salary.objects.all()
        else:
            return Salary.objects.filter(employee=user.employee)

class EmployeeListView(LoginRequiredMixin, ListView):
    """
    Provides a list of employees
    """
    login_url = "/login/"
    template_name = "user/employees_list.html"

    def get_queryset(self):
        user = self.request.user

        if user.userprofile.role == "MANAGER":
            return Employee.objects.all()
        else:
            return Employee.objects.filter(owner=user)

class DepartmentListView(LoginRequiredMixin, ListView):
    """
    Provides a list of departments
    """
    login_url = "/login/"
    template_name = "user/departments_list.html"

    def get_queryset(self):
        return Department.objects.all()

class DesignationListView(LoginRequiredMixin, ListView):
    """
    Provides a list of designations
    """
    login_url = "/login/"
    template_name = "user/designations_list.html"

    def get_queryset(self):
        return Designation.objects.all()

class VacationListView(LoginRequiredMixin, ListView):
    """
    Provides a list of vacation requests
    """
    login_url = "/login/"
    template_name = "user/vacation_list.html"

    def get_queryset(self):
        
        user = self.request.user
        
        if user.userprofile.role == "MANAGER":
            return Vacation.objects.all()
        else:
            return Vacation.objects.filter(employee=user.employee)

class VacationCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new vacation request
    """
    form_class = VacationCreateForm
    template_name = 'user/vacation_list.html'
    success_url = "/vacation"

    def form_valid(self, form):
        form.instance.employee = Employee.objects.filter(owner=self.request.user)[:1].get()
        form.instance.status = "new"
        return super(VacationCreateView, self).form_valid(form)

class VacationDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to delete emergency contact
    """
    form_class = EmergencyContact
    template_name = 'user/vacation_delete.html'
    success_url = "/vacation"
    
    def get_object(self, queryset=None):
        return get_object_or_404(Vacation, id=self.kwargs.get("vacation"))

class VacationUpdateView(LoginRequiredMixin, UpdateView):
    """
    View to update a status of a vacation request
    """
    form_class = VacationUpdateForm
    template_name = "user/vacation_update.html"
    success_url = "/vacation"
    
    def form_valid(self, form):
        form.instance.status = self.request.POST["status"]
        return super(VacationUpdateView, self).form_valid(form)

    def get_object(self):
        return get_object_or_404(Vacation, id=self.kwargs.get("vacation"))

# View functions for custom error handlers

def handler404(request, exception):
    return render(request, 'error-404.html', status=404)

def handler500(request):
    return render(request, 'error-500.html', status=500)