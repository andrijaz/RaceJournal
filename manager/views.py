from django.shortcuts import render, redirect, get_object_or_404
from manager.models import Member, Group, Staff, MonthPlan, MonthTrainingPlan, MemberGroup
from manager.forms import MemberForm, MonthPlanForm
from django.http import HttpResponse
from datetime import datetime

# Create your views here.


def index(request):
    all_people = Member.objects.all()
    groups = Group.objects.all()
    return render(request, 'manager/index.html', {"members": all_people, "group": groups})


def member(request, pk=None):
    member = Member.objects.get(pk=pk)
    return render(request, 'manager/member_detail.html', {"member": member})


def edit_member(request, pk=None):
    member = get_object_or_404(Member, pk=pk) if pk else Member(profile_id=pk)

    form = MemberForm(request.POST or None, instance=member)

    if request.POST and form.is_valid():
        form.save()
        return redirect('manager-index')
    return render(request, 'manager/edit_member.html', {"form": form})


def group(request, pk=None):
    group_to_show = Group.objects.get(pk=pk)
    return render(request, 'manager/edit_group_members.html', {"group": group_to_show})


def staff(request, pk=None):
    staff_to_show = Staff.objects.get(pk=pk)

    return render(request, 'manager/staff_detail.html', {"staff": staff_to_show})


# @login_required
def profile(request):
    profile = request.user.profile
    # all_races = Race.objects.filter(userraces__profile_id=request.user.profile)
    # staff_info = Staff.objects.get(profile_id=profile)
    # context = {'all_races': all_races, 'profile': profile}
    return render(request, 'manager/profile.html', {})


def group_edit_members(request, pk=None):
    group = Group.objects.get(pk=pk)
    members = Member.objects.all().exclude(membergroup__group=group)
    if request.POST and request.POST.get('option') == 'delete':
        x=2
        # for m in requst.post MG(group_id=group, member=bla).delete()
        # delete runner
    elif request.POST and request.POST.get('option') == 'add':
        x=3
        # new_mg = MemberGroup(group_id=group, member=members)
        # new_mg = save()
        # add new member
    else:
        # show info
        pass
    return render(request, 'manager/edit_group_members.html', {"group": group, 'members': members})

def group_edit_plan_training(request, pk=None):

    mp_to_show = MonthPlan.objects.filter(group=pk, month=datetime.now().month, year=datetime.now().year)
    return render(request, 'manager/edit_group_month_training_plan.html', {"training_list": mp_to_show})


def month_plan_detail(request, pk=None):
    plan = MonthPlan.objects.get(pk=pk)
    trainings = MonthTrainingPlan.objects.filter(month_plan=plan)
    return render(request, 'manager/month_plan/month_plan_detail.html', {"plan": plan, "training_list": trainings})


def month_plan_edit(request, pk=None):
    plan = get_object_or_404(MonthPlan, pk=pk) if pk else MonthPlan(group_id=pk)

    form = MonthPlanForm(request.POST, instance=plan)
    if request.POST and form.is_valid():
        # form = MonthPlanForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = MonthPlanForm()

    return render(request, 'manager/edit_plan.html', {'form': form})


from django.views.generic import DetailView, CreateView, UpdateView
from manager.models import Training, OneTrainingPlan


class MemberDetail(DetailView):
    model = Member
    # queryset = Book.objects.order_by('-publication_date')
    template_name = 'manager/member/member_detail.html'


class MemberCreate(CreateView):
    # opcija da se kreira profil odavde, pa tek onda member!!!
    model = Member
    fields = '__all__'
    template_name = "manager/member/member_form.html"


class MemberUpdate(UpdateView):
    fields = '__all__'
    model = Member

    template_name = "manager/member/member_update.html"


class GroupDetail(DetailView):
    model = Group
    # queryset = Book.objects.order_by('-publication_date')
    template_name = 'manager/group/group_detail.html'


class GroupCreate(CreateView):
    # opcija da se kreira profil odavde, pa tek onda member!!!
    model = Group
    fields = '__all__'
    template_name = "manager/group/group_form.html"


class GroupUpdate(UpdateView):
    fields = '__all__'
    model = Group

    template_name = "manager/group/group_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        # MonthTrainingPlan.objects.get(pk=kwargs.get('pk'))
        return HttpResponse(request)


class StaffDetail(DetailView):
    model = Staff
    # queryset = Book.objects.order_by('-publication_date')
    template_name = 'manager/staff/staff_detail.html'


class StaffCreate(CreateView):
    # opcija da se kreira profil odavde, pa tek onda member!!!
    model = Staff
    fields = '__all__'
    template_name = "manager/staff/staff_form.html"


class StaffUpdate(UpdateView):
    fields = '__all__'
    model = Staff

    template_name = "manager/staff/staff_update.html"


class TrainingDetail(DetailView):
    model = Training
    # queryset = Book.objects.order_by('-publication_date')
    template_name = 'manager/training/training_detail.html'


class TrainingCreate(CreateView):
    model = Training
    fields = '__all__'
    template_name = "manager/training/training_form.html"


class TrainingUpdate(UpdateView):
    fields = '__all__'
    model = Training

    template_name = "manager/training/training_update.html"


class OneTrainingPlanDetail(DetailView):
    model = OneTrainingPlan
    # queryset = Book.objects.order_by('-publication_date')
    template_name = 'manager/training_plan/one_training_plan_detail.html'


class OneTrainingPlanCreate(CreateView):
    model = OneTrainingPlan
    fields = '__all__'
    template_name = "manager/training_plan/one_training_plan_form.html"


class OneTrainingPlanUpdate(UpdateView):
    fields = '__all__'
    model = OneTrainingPlan

    template_name = "manager/training_plan/one_training_plan_update.html"


class MonthPlanDetail(DetailView):
    model = MonthPlan
    # queryset = Book.objects.order_by('-publication_date')
    template_name = 'manager/month_plan/month_plan_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class MonthPlanCreate(CreateView):
    model = MonthPlan
    fields = '__all__'
    template_name = "manager/month_plan/month_plan_form.html"


class MonthPlanUpdate(UpdateView):
    fields = '__all__'
    model = MonthPlan

    template_name = "manager/month_plan/month_plan_update.html"

class MonthTrainingPlanDetail(DetailView):
    model = MonthTrainingPlan
    # queryset = Book.objects.order_by('-publication_date')
    template_name = 'manager/month_plan/month_plan_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['bla'] = 2
    #     return context


class MonthTrainingPlanCreate(CreateView):
    model = MonthTrainingPlan
    fields = '__all__'
    template_name = "manager/month_plan/month_plan_form.html"


class MonthTrainingPlanUpdate(UpdateView):
    fields = '__all__'
    model = MonthTrainingPlan

    template_name = "manager/month_plan/month_plan_update.html"
    template_name = 'manager/edit_group_month_training_plan.html'



