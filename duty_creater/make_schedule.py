import os, sys, django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DFN.settings') 	# settings.py가 있는곳
django.setup()


from .schedule_maker_module import (
    make_daily_schedule,
    make_ideal_counter,
    update_nurse_info,
    transfer_table_to_dict,
    divide_nurse_info_by_team
)

from .validation_checker_module import (
    check_validation
)

from pprint import pprint
import time

MONTHS_LAST_DAY = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def make_monthly_schedule(
    team_list, # -1. 팀 정보. 리스트. 
    needed_nurses_shift_by_team,    # 3. shift당 필요한 간호사 수. 3의 배수로 기입 필수. 
    vacation_info,          # 4.연차 신청 정보. [딕셔너리. nurse_pk : set(날짜 묶음)]
    current_month,          # 5. 현재 월
    current_date,            # 6. 현재 날짜
    nurse_profile_dict,         # 간호사 프로필 딕셔너리
    nurse_last_month_schedule_dict, # 지난 달 근무표
):

    """
    매개변수:
    0. team_list. list 형태로 팀 정보를 받는다.
    1. nurse_pk_list. list. 현재 근무중인 간호사의 pk를 리스트 형태로 입력.
    2. number_of_nurses. int. 간호사 인원 수.
    3. needed_nurses_shift_by_team. int. shift당 한 팀에 필요한 간호사 수.
    4. vacation_info. dict. key = 간호사, value = set 혹은 list로 '날짜' 정보
    5. current_month = 생성 시작을 원하는  월
    6. current_date = 생성 시작을 원하는 날짜.  
    """

    # 1. 선언
    # 1) 최종 결과값을 저장할 리스트 .
    whole_schedule = []
    # NUMBER_OF_NURSES = len(nurse_pk_list)
    NUMBER_OF_TEAMS = len(team_list)

    # 2) 예외 처리를 위한 변수들 선언
    # (1) 이전 시점의 nurse_info정보를  저장하는 스택
    nurse_info_stack = [[] for _ in range(NUMBER_OF_TEAMS + 1)]   
    # (2) 무한루프 방지를 위한 변수.
    recursion_time = 0

    # 2. 연산
    # 1) 연산 전 준비
    # nurse_profile_dict 자료형 맞춰야 함. 
    ideal_schedule = make_ideal_counter(needed_nurses_shift_by_team)
    nurse_info, nurse_pk_list = divide_nurse_info_by_team(
        team_list=team_list,
        nurse_profile_dict=nurse_profile_dict,
        nurse_last_months_schedule_dict=nurse_last_month_schedule_dict
    )

    # 1. 종료 조건
    # 정상 종료
    while current_date != MONTHS_LAST_DAY[current_month] + 1:

        # 2. 선언
        # 비트마스킹 형태로 grade의 참여 여부 확인. 
        whole_team_temp_schedule = []

        # 2. 스케쥴 생성
        # 팀별 스케쥴 제작 및 검증 알고리즘 필요함. 제작중. 
        is_enough_grade = False

        while not is_enough_grade and recursion_time < 15:

            teamed_up_schedule = dict()
            whole_team_grade_checker = 1    
            
            # 여기 매개변수로 팀별 인원수가 들어가야 함. 
            for team_number in team_list:           
                temporary_schedule, grade_counter_bit\
                    = make_daily_schedule(
                    nurse_pk_list = nurse_pk_list[team_number],
                    nurse_info = nurse_info[team_number],
                    ideal_schedule = ideal_schedule,
                    current_date = current_date
                    )
                # 팀 
                teamed_up_schedule[team_number] = temporary_schedule
                whole_team_grade_checker |= grade_counter_bit

            if whole_team_grade_checker == 15:
                whole_team_temp_schedule.append(teamed_up_schedule)
                is_enough_grade = True
                
            else:
                recursion_time += 1

        if recursion_time >= 15:
            print('설정 변경 필요')
            return 

        # 4. 스케쥴 업데이트
        for team_number in team_list:
            nurse_info[team_number] = update_nurse_info(nurse_info[team_number], teamed_up_schedule[team_number])
        whole_schedule.append(teamed_up_schedule)
        current_date += 1

    whole_schedule_dict = transfer_table_to_dict(
        team_list=team_list,
        whole_schedule=whole_schedule,
        nurse_pk_list=nurse_pk_list,
        days_of_month = MONTHS_LAST_DAY[current_month]
        )

    return whole_schedule_dict, nurse_info