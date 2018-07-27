from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, TimeSheetFormSet, TimeSheetForm
from .models import Profile, TimeSheet
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db import transaction


class RequestFormKwargsMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormKwargsMixin, self).get_form_kwargs()
        # Update the existing form kwargs dict with the request's user.
        kwargs.update({"request": self.request})
        return kwargs


class UserList(ListView):
    model = User


class UserCreate(CreateView):
    model = User
    fields = ['project', 'week', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


class UserTimeSheetCreate(CreateView):
    model = User
#    fields = ['project', 'week', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    fields = []
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        data = super(UserTimeSheetCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['timesheets'] = TimeSheetFormSet(self.request.POST)
        else:
            data['timesheets'] = TimeSheetFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        timesheets = context['timesheets']
        with transaction.atomic():
            self.object = form.save()

            if timesheets.is_valid():
                timesheets.instance = self.object
                timesheets.save()
        return super(UserTimeSheetCreate, self).form_valid(form)


class UserTimeSheetUpdate(UpdateView):
    model = User
    fields = []
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        data = super(UserTimeSheetUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['timesheets'] = TimeSheetFormSet(self.request.POST, instance=self.object)
        else:
            data['timesheets'] = TimeSheetFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        timesheets = context['timesheets']
#        timesheet = form.save(commit=False)
#        timesheet.person = User.objects.get(username=self.request.user)
#        timesheet.save()
        with transaction.atomic():
            self.object = form.save()
            if timesheets.is_valid():
                timesheets.instance = self.object
                timesheets.save()
        return super(UserTimeSheetUpdate, self).form_valid(form)


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('profile-list')


class TimeSheetListView(ListView):
    model = TimeSheet

    def get_queryset(self):
        return TimeSheet.objects.filter(person=self.request.user)


class TimeSheetCreate(RequestFormKwargsMixin, CreateView):
    model = TimeSheet
    form_class = TimeSheetForm

    def form_valid(self, form):
        timesheet = form.save(commit=False)
        timesheet.person = User.objects.get(username=self.request.user)
        timesheet.save()
        return HttpResponseRedirect('http://127.0.0.1:8000/account/timesheet/')


class TimeSheetUpdate(RequestFormKwargsMixin, UpdateView):
    model = TimeSheet
    fields = '__all__'
    form_class = TimeSheetForm


@login_required
def dashboard(request):
    return render(request, 'people/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = Profile.objects.create(user=new_user)
            return render(request,
                          'people/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'people/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'people/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})