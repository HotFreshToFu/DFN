import heapq
import random

# 스케쥴 카운터. 
# 추후 더 복잡한 알고리즘이 추가될 수 있음. 
def make_ideal_counter(needed_nurses_per_shift):
    counter_list = [0] + [needed_nurses_per_shift] * 3
    return counter_list


# 메인 함수 - 일간 스케쥴 제작.
def make_daily_schedule(
    nurse_pk_list,
    nurse_info,
    ideal_schedule, 
    current_day
    ):

    # 1. 종료조건 설정
    IDEAL_SCHEDULE = ideal_schedule
    
    # 총 10회 반복. 
    for _ in range(10):
        # 2. 큐 제작
        priority_que = make_priority_que(
            nurse_pk_list,
            nurse_info,
            current_day
            )

        # 3. 큐를 활용해 스케쥴 제작
        daily_schedule = place_shifts(priority_que, IDEAL_SCHEDULE)

        # 4. 검증
        # if is_validate(daily_schedule):
        # 추후 
        if True:
            return daily_schedule

    return None


# 우선순위 큐 제작 함수.
def make_priority_que(nurse_pk_list, nurse_info, current_day):

    shift_que = []

    for nurse_pk in nurse_pk_list:
        nurse_detail = nurse_info[nurse_pk]
        for shift in range(4):
            
            priority = check_priority(nurse_detail, current_day, shift)

            if priority is not None:
                heapq.heappush(shift_que, (priority, nurse_detail[0], shift)) 

    return shift_que


def check_priority(
    nurse_detail,
    current_day,
    shift
):

    NURSE_NUMBER,\
    SHIFTS,\
    SHIFT_STREAKS,\
    OFFS,\
    MONTHLY_NIGHT_SHIFTS,\
    VACATION_INFO,\
    OFF_STREAKS,\
    LAST_SHIFT,\
        = nurse_detail

    CURRENT_DAY = current_day
    CURRENT_SHIFT = shift

    # 1. 예외 처리
    # 1) 주 5회 이상 근무 
    if SHIFT_STREAKS >= 5 and CURRENT_SHIFT:
        return None
    
    # 2) NIGHT 8회 이상 근무 시도.
    # '부득이한 근무.. 조건 추가시 변경 필요.
    if MONTHLY_NIGHT_SHIFTS > 7 and CURRENT_SHIFT == 3:
        return None

    # 3) 비 오름차순 근무
    if CURRENT_SHIFT and LAST_SHIFT > CURRENT_SHIFT:
        return None

    # 4) 휴가 전날 NIGHT 근무
    if VACATION_INFO == CURRENT_DAY + 1:
        return None


    # 2. off가 꼭 필요한 경우.
    # 1) 이틀 연속으로 쉬게 해주기. 
    if OFF_STREAKS == 1 and not CURRENT_SHIFT:
        return 0 + random.randrange(1, 40)

    # 2) 5연속 근무 이후 휴무
    if SHIFT_STREAKS >= 5 and not CURRENT_SHIFT:
        return 0 + random.randrange(1, 40)

    if VACATION_INFO == CURRENT_DAY:
        return 0

    
    # 3. 기타 연속 근무
    if CURRENT_SHIFT and LAST_SHIFT == CURRENT_SHIFT:
        return random.randrange(100, 500)

    
    # 4. 그 외의 근무
    # 원래는 1000~ 1200. 수정해보자.. 
    if CURRENT_SHIFT:
        return random.randrange(250, 600)

    else:   # 조건 없는 off. 원래는 1000 상수로 리턴했음. 
        return 700



def place_shifts(
    priority_que,
    ideal_schedule,
):
    IDEAL_SCHEDULE = ideal_schedule
    schedule_table = [[] for _ in range(4)] # 각각 off, day, evening, night.
    current_schedule_counter = [0] * 4
    placed_nurse_set = set()

    while priority_que:
        current_priority, nurse_number, shift = heapq.heappop(priority_que)
        
        # 휴가 제외, 현재 확인중인 shift 가 꽉 차있으면..
        # 더 이상 근무를 배치하지 않음.
        if shift and current_schedule_counter[shift] >= IDEAL_SCHEDULE[shift]:
            continue
        
        # 이미 배치된 간호사라면
        if nurse_number in placed_nurse_set:
            continue
        
        current_schedule_counter[shift] += 1
        schedule_table[shift].append(nurse_number)
        placed_nurse_set.add(nurse_number)
        
    return schedule_table


def transfer_table_to_dict(whole_schedule, nurse_pk_list, days_of_month):
    """
    연결리스트 형식으로 정렬된 스케쥴 리스트를 입력받아
    KEY는 간호사의 PK, Value는 개인의 한 달 스케쥴 리스트인 
    dict 개체를 반환하는 함수
    """

    result_dict = dict()
    for nurse_pk in nurse_pk_list:
        result_dict[nurse_pk] = [0] * (days_of_month)
    # 인덱스 어떻게 맞출건지 협의 필. 

    for date in range(days_of_month):
        daily_schedule = whole_schedule[date]
        for shift in range(1, 4):
            for nurse in daily_schedule[shift]:
                result_dict[nurse][date] = shift


    return result_dict