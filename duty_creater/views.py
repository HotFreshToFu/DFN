from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.forms import formset_factory
import datetime
from .models import Event
from .forms import EventForm, EventFormSet
from .make_schedule import make_monthly_schedule
from pprint import pprint


def index(request):
    context = {
    }
    return render(request, 'dfn/index.html', context)


def new_main(request):
    example_nurse_info = {
        1: [1, 0, 0, 0, 0, 0, 2, 0],
        2: [2, 0, 0, 0, 0, 0, 2, 0],
        3: [3, 0, 0, 0, 0, 0, 2, 0],
        4: [4, 0, 0, 0, 0, 0, 2, 0],
        5: [5, 0, 0, 0, 0, 0, 2, 0],
        6: [6, 0, 0, 0, 0, 0, 2, 0],
        # 7: [7, 0, 0, 0, 0, 0, 2, 0],
        # 8: [8, 0, 0, 0, 0, 0, 2, 0],
        # 9: [9, 0, 0, 0, 0, 0, 0, 0],
        # 10:[10, 0, 0, 0, 0, 0, 2, 0],
        # 11: [11, 0, 0, 0, 0, 0, 2, 0],
        # 12: [12, 0, 0, 0, 0, 0, 2, 0],
        # 13: [13, 0, 0, 0, 0, 0, 2, 0],
        # 14: [13, 0, 0, 0, 0, 0, 2, 0],
        # 15: [13, 0, 0, 0, 0, 0, 2, 0],
        # 16: [13, 0, 0, 0, 0, 0, 2, 0],
    }

    example_nurse_pk_list = [1, 2, 3, 4, 5, 6]

    result, modified_nurse_info = make_monthly_schedule(
        nurse_pk_list=example_nurse_pk_list,
        nurse_info=example_nurse_info,
        number_of_nurses=6,
        needed_nurses_per_shift=1,
        vacation_info=[],
        current_month=10,
        current_day=1,    
        )
    pprint(result)
    pprint(modified_nurse_info)
    
    return render(request, 'dfn/new_main.html') 


def new(request):
    # 듀티 생성 알고리즘을 통해 이번 달의 듀티 목록을 받아옴
    duties = [
        [1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3], 
        [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0], 
        [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0], 
        [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2], 
        [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1], 
        [0, 0, 3, 0, 1, 0, 0, 0, 1, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
    ]
    # 만약 듀티가 딕셔너리로 주어진다면
    dict_duties = {
        'nurse1': [1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3], 
        'nurse2': [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0], 
        'nurse3': [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0], 
        'nurse4': [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2], 
        'nurse5': [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1], 
        'nurse6': [0, 0, 3, 0, 1, 0, 0, 0, 1, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
    }


    # 간호사를 username으로 저장한 리스트
    nurses = []
    for id in range(2, 8):
        nurses.append(get_user_model().objects.filter(pk=id).values('username')[0]['username'])
    print(nurses)


    if request.method == 'POST':
        start_date = request.POST.get('start')  # 사용자가 선택한 날짜
        print(start_date)
        month = start_date[5: 7] 

        Event.objects.all().delete()  # new 함수를 실행할때마다 db에 추가되서 임시로 매번 다 삭제


        # 근무 기록 생성
        for nurse_id in range(2, 8):  # range()는 이후 간호사 id를 담은 리스트로 변경
            date = datetime.datetime.strptime(start_date, '%Y-%m')  # datetime 객체로 변환
            for duty in duties[nurse_id - 2]:  # 2차원 리스트로는 현재 리스트가 어떤 간호사에 해당하는지 구분 안됨
                Event.objects.create(date=date, duty=duty, nurse_id=nurse_id)  # Event 생성
                date = date + datetime.timedelta(days=1)  # 하루 추가
        

        # 하루 단위로 각 듀티를 맡은 간호사의 username 저장(OFF는 제외)
        date = datetime.datetime.strptime(start_date, '%Y-%m')  # datetime 객체로 변환
        duties_of_day = [[0] * 3 for _ in range(31)]
        for day in range(31):
            wanted_date = str(date + datetime.timedelta(days=day))[:10]
            duties_of_wanted_date = Event.objects.filter(date=wanted_date).all()
            for duty in [1, 2, 3]:
                wanted_nurse_id = duties_of_wanted_date.filter(duty=duty).values('nurse_id')[0]['nurse_id']
                duties_of_day[day][duty - 1] = get_user_model().objects.filter(pk=wanted_nurse_id).values('username')[0]['username']


        duties_of_month = Event.objects.filter(date__startswith='2020-01').all()
        

        context = {
            'duties_of_month': duties_of_month,
            'duties_of_day': duties_of_day,
            'month': month,
            'start_date': start_date,

            'nurses': nurses,
            'duties': duties,
            'dict_duties': dict_duties
        }
        return render(request, 'dfn/new.html', context)



def myduty(request, nurse_pk):
    pass


def update(request, date):
    wanted_events = Event.objects.filter(date__startswith=date).all().order_by('date')
    
    if request.method == 'POST':
        formset = EventFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('dfn:new_main')  # 임시

    else:
        formset = EventFormSet(queryset=wanted_events)
    context = {
        'formset': formset,
        'date': date
    }
    return render(request, 'dfn/update.html', context)