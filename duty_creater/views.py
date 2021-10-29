from django.contrib.auth import get_user_model
from django.db.models import Q
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from accounts.models import Profile
from .make_schedule import make_monthly_schedule
from .models import Event
from .forms import EventForm, EventFormSet
from pprint import pprint
import json
import datetime


def index(request):
    context = {
    }
    return render(request, 'schedule/index.html', context)


def create(request):
    if request.method == "POST":
        start_date = request.POST.get('start')  # 사용자가 선택한 날짜(YY-MM 형식에 str type)
        return redirect('schedule:create_monthly', start_date)
    
    return render(request, 'schedule/create.html') 


def create_monthly(request, date):
    # date: 사용자가 선택한 날짜(YY-MM 형식. str)
    month = date[5: 7]  # 사용자가 선택한 달(MM 형식)
    year = date[: 4]  # 사용자가 선택한 연(YY 형식)

    weekdays = []  # date-01 부터 date-31까지 요일 저장 리스트
    start_date = date + '-01'  # 시작일
    weekday = datetime.datetime.strptime(start_date, '%Y-%m-%d')  # datetime 객체로 변환
    for _ in range(31):
        weekdays.append(weekday.strftime('%a'))
        weekday = weekday + datetime.timedelta(days=1)  # 하루 추가


    if request.method == "POST":
        # 사용자가 생성하기로 했다면 json 파일을 불러와 이를 DB에 저장
        with open('temp_schedule.json') as json_file:
            dict_duties = json.load(json_file)

        Event.objects.all().delete()  # create_monthly 함수를 실행할때마다 db에 추가되서 임시로 매번 다 삭제


        # 근무 기록 생성
        for nurse_pk, duties in dict_duties.items():  
            start_date = datetime.datetime.strptime(date, '%Y-%m')  # datetime 객체로 변환
            nurse_profile = Profile.objects.get(pk=nurse_pk)  # 간호사 프로필 객체
            nurse_profile.OFF = 0  # 임시로 OFF 초기화

            weekdays_idx = 0  # 현재 날짜(int)
            for duty in duties:
                # OFF 갱신
                if duty > 0 and (weekdays[weekdays_idx] == 'Sun' or weekdays[weekdays_idx] == 'Sat'):
                    nurse_profile.OFF += 1
                    nurse_profile.save()
                weekdays_idx += 1

                # Event 생성
                Event.objects.create(date=start_date, duty=duty, nurse_id=nurse_pk) 
                start_date = start_date + datetime.timedelta(days=1)  # 하루 추가

        return redirect('schedule:index')

    # 한달 일정 생성
    example_nurse_info = {
        7: [7, 0, 0, 0, 0, 0, 2, 0],
        2: [2, 0, 0, 0, 0, 0, 2, 0],
        3: [3, 0, 0, 0, 0, 0, 2, 0],
        4: [4, 0, 0, 0, 0, 0, 2, 0],
        5: [5, 0, 0, 0, 0, 0, 2, 0],
        6: [6, 0, 0, 0, 0, 0, 2, 0],
    }

    example_nurse_pk_list = []
    nurse_pk_list = get_user_model().objects.filter(~Q(username='admin')).values('id')
    for i in range(len(nurse_pk_list)):
        example_nurse_pk_list.append(nurse_pk_list[i]['id'])

    result, modified_nurse_info = make_monthly_schedule(
        nurse_pk_list=example_nurse_pk_list,
        nurse_info=example_nurse_info,
        number_of_nurses=6,
        needed_nurses_per_shift=1,
        vacation_info=[],
        current_month=10,
        current_day=1,    
        )
    # pprint(result)
    # pprint(modified_nurse_info)

    dict_duties = {
        2: [1, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3], 
        3: [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0], 
        4: [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0], 
        5: [0, 1, 0, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2], 
        6: [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1], 
        7: [0, 0, 3, 0, 1, 0, 0, 0, 1, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
    }

    # 한달 일정을 json 파일로 임시 저장
    with open('temp_schedule.json', 'w') as json_file:
        json.dump(dict_duties, json_file)

    nurse_names = []  # 간호사 이름 저장 [(pk, 이름), ...]
    for nurse_pk in dict_duties:
        nurse_profile = Profile.objects.get(user_id=nurse_pk)  # 간호사 프로필 객체
        nurse_names.append((nurse_pk, nurse_profile.name))

    context = {
        'month': month,
        'year': year,
        'start_date': date,
        'weekdays': weekdays,
        'nurse_names': nurse_names,
        'dict_duties': dict_duties,
    }
    return render(request, 'schedule/create_monthly.html', context)


def update(request, date):
    wanted_events = Event.objects.filter(date__startswith=date).all().order_by('date')
    
    if request.method == 'POST':
        formset = EventFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('schedule:create', '2020-01')  # 임시

    else:
        formset = EventFormSet(queryset=wanted_events)
    context = {
        'formset': formset,
        'date': date
    }
    return render(request, 'schedule/update.html', context)


today = datetime.datetime.today().strftime('%Y-%m')  # 현재 달

def personal(request, nurse_pk, date=today):
    # date의 기본값은 현재 달
    month = date[5: 7]  # 사용자가 선택한 달(MM 형식)
    year = date[: 4]  # 사용자가 선택한 연(YY 형식)
    nurse_name = Profile.objects.filter(user_id=nurse_pk).values('name')[0]['name']
    duties = list(Event.objects.filter(date__startswith=date).filter(nurse_id=nurse_pk).values_list('duty', flat=True))

    start_date = date + '-01'  # 시작일
    start_weekday = datetime.datetime.strptime(start_date, '%Y-%m-%d').weekday() + 1  # 시작 요일
    weeks = [[-1] * (start_weekday) + duties[: (7 - start_weekday)]]
    day_idx = 7 - start_weekday
    while day_idx < 31:
        if 31 - day_idx <= 7:
            weeks.append(duties[day_idx: ])
            break
        weeks.append(duties[day_idx: day_idx + 7 ])
        day_idx += 7
    
    weekdays = ['일', '월', '화', '수', '목', '금', '토']

    context = {
        'month': month,
        'year': year,
        'nurse_name': nurse_name,
        'date': date,
        'weeks': weeks,
        'weekdays': weekdays,
    }
    return render(request, 'schedule/personal.html', context)


def team(request, team_id, date=today):
    # date의 기본값은 현재 달
    month = date[5: 7]  # 사용자가 선택한 달(MM 형식)
    year = date[: 4]  # 사용자가 선택한 연(YY 형식)

    nurse_pks = Profile.objects.filter(team=team_id).values_list('user_id', flat=True)
    dict_duties = {}
    for nurse_pk in nurse_pks:
        duties = list(Event.objects.filter(date__startswith=date).filter(nurse_id=nurse_pk).values_list('duty', flat=True))
        dict_duties[nurse_pk] = duties
    
    weekdays = []  # date-01 부터 date-31까지 요일 저장 리스트
    start_date = date + '-01'  # 시작일
    weekday = datetime.datetime.strptime(start_date, '%Y-%m-%d')  # datetime 객체로 변환
    for _ in range(31):
        weekdays.append(weekday.strftime('%a'))
        weekday = weekday + datetime.timedelta(days=1)  # 하루 추가

    nurse_names = []  # 간호사 이름 저장 [(pk, 이름), ...]
    for nurse_pk in dict_duties:
        nurse_profile = Profile.objects.get(user_id=nurse_pk)  # 간호사 프로필 객체
        nurse_names.append((nurse_pk, nurse_profile.name))

    context = {
        'month': month,
        'year': year,
        'team_id': team_id,
        'nurse_names': nurse_names,
        'date': date,
        'weekdays': weekdays,
        'dict_duties': dict_duties,
    }
    return render(request, 'schedule/team.html', context)