from django.shortcuts import render
import datetime
from .models import Event


# Create your views here.
def index(request):
    context = {

    }
    return render(request, 'dfn/index.html', context)


def new(request):
    duties = [
        [1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3], 
        [2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0], 
        [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0], 
        [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2], 
        [3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1], 
        [0, 0, 3, 0, 1, 0, 0, 0, 1, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
    ]
    
    start_date = '20-01-01'  # 시작 날, 이후 사용자에게 달을 입력받는 것으로 수정

    Event.objects.all().delete()  # new 함수를 실행할때마다 db에 추가되서 임시로 매번 다 삭제

    for nurse_id in range(2, 8):  # range()는 이후 간호사 id를 담은 리스트로 변경
        date = datetime.datetime.strptime(start_date, '%y-%m-%d')  # datetime 객체로 변환
        for duty in duties[nurse_id - 2]:  # 2차원 리스트로는 현재 리스트가 어떤 간호사에 해당하는지 구분 안됨
            Event.objects.create(date=date, duty=duty, nurse_id=nurse_id)  # Event 생성
            date = date + datetime.timedelta(days=1)  # 하루 추가
    
    

    # print(Event.objects.filter(date='2020-01-09').all())
    date = datetime.datetime.strptime(start_date, '%y-%m-%d')  # datetime 객체로 변환
    duties_of_day = [[0] * 3 for _ in range(31)]
    for day in range(31):
        wanted_date = str(date + datetime.timedelta(days=day))[:10]
        # print(wanted_date)
        duties_of_wanted_date = Event.objects.filter(date=wanted_date).all()
        for duty in [1, 2, 3]:
            duties_of_day[day][duty - 1] = duties_of_wanted_date.filter(duty=duty).values('nurse_id')
        # print(Event.objects.filter(date=wanted_date).all())
    # print(duties_of_day)
    # print(type(duties_of_day[0][0]))
        
    duties_of_month = Event.objects.filter(date__startswith='2020-01').all()
    context = {
        'duties_of_month': duties_of_month,
        'duties_of_day': duties_of_day,
    }
    return render(request, 'dfn/new.html', context)


def myduty(request, nurse_pk):
    pass