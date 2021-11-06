import heapq
import random
from pprint import pprint
# 카운터 리스트 제작 함수 
def make_ideal_counter(needed_nurses_per_shift):
    """
    매개변수: 한 근무당 한 팀에서 필요한 간호사의 인원 수 N
    출력: 리스트 == [0, N, N, N]
    """
    counter_list = [0] + [needed_nurses_per_shift] * 3
    return counter_list

# 메인 함수  - 스케쥴 제작.
def make_daily_schedule(
    nurse_pk_list,
    nurse_info,
    ideal_schedule, 
    current_date
    ):
    """
    매개 변수 : 
    1. 현재 근무중인 간호사들의 pk_list 
    2. 간호사 정보 dict
    3. make_ideal_counter 함수의 실행 결과값.
    4. current_date : 오늘. 

    반환값:
    1. 제작 성공시 - 일간 스케쥴
    2. 실패시 - None

    """
    

    # 1. 종료조건 설정
    IDEAL_SCHEDULE = ideal_schedule
    
    # 총 10회 반복. 
    for _ in range(10):
        # 2. 큐 제작
        priority_que = make_priority_que(
            nurse_pk_list,
            nurse_info,
            current_date
            )

        # 3. 큐를 활용해 스케쥴 제작
        daily_schedule, grade_checker = place_shifts(priority_que, IDEAL_SCHEDULE)

        # 4. 검증
        # if is_validate(daily_schedule):
        # 추후 
        if True:
            return daily_schedule, grade_checker

    return None


# 우선순위 큐 제작 함수.
def make_priority_que(nurse_pk_list, nurse_info, current_date):

    shift_que = []

    for nurse_pk in nurse_pk_list:
        nurse_detail = nurse_info[nurse_pk]
        for shift in range(4):
            
            priority = check_priority(nurse_detail, current_date, shift)

            if priority is not None:
                nurse_grade = nurse_detail[1]
                heapq.heappush(shift_que, (priority, nurse_pk, nurse_grade, shift)) 

    return shift_que


def check_priority(
    nurse_detail,
    current_date,
    shift
):

    NURSE_NUMBER,\
    NURSE_GRADE,\
    TEAM_NUMBER,\
    SHIFTS,\
    SHIFT_STREAKS,\
    OFFS,\
    MONTHLY_NIGHT_SHIFTS,\
    VACATION_INFO,\
    OFF_STREAKS,\
    LAST_SHIFT,\
        = nurse_detail

    CURRENT_DAY = current_date
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
        priority_token = random.randrange(1, 40)
        return priority_token

    # 2) 5연속 근무 이후 휴무
    if SHIFT_STREAKS >= 5 and not CURRENT_SHIFT:
        priority_token = random.randrange(1, 40)
        return priority_token

    # 3) 휴가 신청일일 경우. 
    if VACATION_INFO == CURRENT_DAY:
        priority_token = 0
        return priority_token

    
    # 3. 기타 연속 근무
    if CURRENT_SHIFT and LAST_SHIFT == CURRENT_SHIFT:
        priority_token = random.randrange(100, 500)
        return priority_token

    # 4. 그 외의 근무
    # 원래는 1000~ 1200. 수정해보자.. 
    if CURRENT_SHIFT:
        priority_token = random.randrange(150, 600)
        return priority_token

    else:   # 조건 없는 off. 원래는 1000 상수로 리턴했음. 
        priority_token = 700
        return priority_token


def place_shifts(
    priority_que,
    ideal_schedule,
):
    """
    매개변수:
    1. priority_que : 우선순위 큐
    2. ideal_schedule: 한 shift당 한 팀에서 제공해야 하는 간호사 수.
    
    반환값:
    1. schedule_table : 스케쥴 테이블
    2. grade_counter_bit : 저연차 간호사만 근무하는 것을 방지하기 위한 비트값. 
    """
    IDEAL_SCHEDULE = ideal_schedule
    schedule_table = [[] for _ in range(4)] # 각각 off, day, evening, night.
    current_schedule_counter = [0] * 4
    # 비트마스킹을 활용, day, evening, night 에 근무자가 있는지 체크. 
    grade_counter_bit = 0
    placed_nurse_set = set()

    while priority_que:
        current_priority, nurse_number, nurse_grade, shift = heapq.heappop(priority_que)
        
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

        # 간호사 grade가 1 이상이라면
        # 비트에 1번...  
        if nurse_grade > 0:
            grade_counter_bit |= (1 << shift)
        
    return schedule_table, grade_counter_bit


def update_nurse_info(nurse_info, temporary_schedule):
    """
    0 NURSE_NUMBER 간호사 일련번호
    1 NURSE_GRADE 간호사 grade
    2 TEAM_NUMBER 팀넘버
    3 SHIFTS, 이번 달 근무 일수 
    4 SHIFT_STREAKS, 연속 근무일 수 
    5 OFFS, 그.. 마크다운에 있는 'OFF' 참조.
    6 MONTHLY_NIGHT_SHIFTS, 한 달에 night 근무한 횟수
    7 VACATION_INFO,   휴가 정보(외부 딕셔너리로 수정 예정)
    8 OFF_STREAKS,         연속 휴무 
    9 LAST_SHIFT,           마지막 근무 정보
    """

    # 모든 4개의 시프트를 순회하며    
    for shift in range(4):

        # 모든 간호사들 순회.
        for nurse in temporary_schedule[shift]:
            
            # 1. 가장 최근 근무 기록 갱신 
            nurse_info[nurse][9] = shift

            # 1) 휴무 
            # 만약 오늘 쉬었다면 
            # 연속 근무일수 초기화
            if not shift:
                nurse_info[nurse][4] = 0
                nurse_info[nurse][8] += 1
                
            # 2) 근무
            # (1) DAY 근무 
            elif shift == 1:
                # a. 한 달 전체 근무일 1 가산
                nurse_info[nurse][3] += 1
                # b. 연속 근무일 수 1 가산
                nurse_info[nurse][4] += 1
                # c. 연속 휴무일 수 0으로 수정
                nurse_info[nurse][8] = 0

            # (2) EVENING 근무 
            elif shift == 2:
                # a. 한 달 근무일 1 가산
                nurse_info[nurse][3] += 1
                # b. 연속 근무일 수 1 가산
                nurse_info[nurse][4] += 1
                # c. 연속 휴무일 수 0으로 수정. 
                nurse_info[nurse][8] = 0

            # (3) NIGHT 근무
            elif shift == 3:
                # a. 한 달 근무일 수 1 가산
                nurse_info[nurse][3] += 1
                # b. 연속 근무일 수 1 가산
                nurse_info[nurse][4] += 1
                # c. 한 달 전체 나이트 근무 1 가산
                nurse_info[nurse][6] += 1
                # d. 연속 휴무일 수 0으로 조정. 
                nurse_info[nurse][8] = 0
            
    return nurse_info



# counter_sorted_list를 개인별 딕셔너리 형태로 출력물을 전환하는 함수.
def transfer_table_to_dict(team_list, whole_schedule, nurse_pk_list, days_of_month):
    """
    연결리스트 형식으로 정렬된 스케쥴 리스트를 입력받아
    KEY는 간호사의 PK, Value는 개인의 한 달 스케쥴 리스트인 
    dict 개체를 반환하는 함수
    """

    result_dict = dict()
    # 팀 넘버마다 값을 받을 딕셔너리.. 추가. 
    # for team_number in team_list:
    #     result_dict[team_number] = dict()

    for team_number in team_list:
        nurse_pk_by_team = nurse_pk_list[team_number]
        for nurse_pk in nurse_pk_by_team:
            result_dict[nurse_pk] = [0] * (days_of_month)
        # 인덱스 어떻게 맞출건지 협의 필. 

        for date in range(days_of_month):
            daily_schedule = whole_schedule[date][team_number]
            for shift in range(1, 4):
                for nurse in daily_schedule[shift]:
                    result_dict[nurse][date] = shift

    # print(result_dict)
    return result_dict


# 분할 부분. 
def divide_nurse_info_by_team(
    team_list,
    nurse_profile_dict,
    nurse_last_months_schedule_dict
    ):

    """
    매개변수:
    0. team_list: 팀명... 
    1. nurse_profile_dict: view 함수 중 get_nurse_info의 출력값.
    key = pk
    value = [pk, level, team, off_cnt]
    2. nurse_last_months_schedule_dict: get_last_schedule의 출력값.
    key = pk
    value = [한 달 개인 듀티표]

    출력값:

    딕셔너리
    Key: 팀 번호들
    value: 팀에 속하는 간호사들의 info 딕셔너리
    0 NURSE_NUMBER 간호사 일련번호
    1 NURSE_GRADE 간호사 grade
    2 TEAM_NUMBER 팀넘버
    3 SHIFTS, 이번 달 근무 일수 
    4 SHIFT_STREAKS, 연속 근무일 수 
    5 OFFS, 그.. 마크다운에 있는 'OFF' 참조.
    6 MONTHLY_NIGHT_SHIFTS, 한 달에 night 근무한 횟수
    7 VACATION_INFO,   휴가 정보(외부 딕셔너리로 수정 예정)
    8 OFF_STREAKS,         연속 휴무 
    9 LAST_SHIFT,           마지막 근무 정보
    
    """
    # 1. 선언
    # 출력을 위한 dict 선언.
    divided_nurse_info_dict_by_team = dict()
    nurse_pk_by_team = dict()
    for team_number in team_list:
        divided_nurse_info_dict_by_team[team_number] = dict()
        nurse_pk_by_team[team_number] = list()
    
    # 2. 연산
    for nurse_detail in nurse_profile_dict.values():

        # 1) 앞부분에 필요한 값들.
        nurse_pk = nurse_detail[0]
        nurse_grade = nurse_detail[1]
        nurse_team = nurse_detail[2]
        nurse_offs = nurse_detail[3]
        
        # 2) 뒷부분에 필요한 값들. 
        nurse_last_month_schedule = nurse_last_months_schedule_dict[nurse_pk]
        nurse_last_shift = nurse_last_month_schedule[-1]
        nurse_shift_streaks = 0
        if not nurse_last_shift and not nurse_last_month_schedule[-2]:
            nurse_off_streaks = 2
        elif not nurse_last_shift:
            nurse_off_streaks = 1
        else:
            nurse_off_streaks = 0
            for i in range(1, 6):
                if nurse_last_month_schedule[-i]:
                    nurse_shift_streaks += 1
                else:
                    break
        
        # 3) 딕셔너리에 삽입
        nurse_pk_by_team[nurse_team].append(nurse_pk)

        divided_nurse_info_dict_by_team[nurse_team][nurse_pk] = [
            nurse_pk,
            nurse_grade,
            nurse_team,
            0,
            nurse_shift_streaks,
            nurse_offs,
            0,
            0,
            nurse_off_streaks,
            nurse_last_shift
        ]
    # pprint(nurse_pk_by_team)
    return divided_nurse_info_dict_by_team, nurse_pk_by_team





