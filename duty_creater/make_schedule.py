import os, sys, django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DFN.settings') 	# settings.py가 있는곳
django.setup()

from .schedule_maker_module import (
    make_daily_schedule,
    make_ideal_counter,
)

from .validation_checker_module import (
    check_validation
)

from pprint import pprint
import time

MONTHS_LAST_DAY = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
NUMBER_OF_NURSES = 32


def make_monthly_schedule(
    nurse_pk_list,  # 0. 간호사 PK 정보. 
    nurse_info,     # 1. 간호사 정보. pk가 key, value가 아래와 같은 딕셔너리.  
    number_of_nurses,       # 2. 간호사 인원 수 
    needed_nurses_per_shift,    # 3. shift당 필요한 간호사 수. 3의 배수로 기입 필수. 
    vacation_info,          # 4.연차 신청 정보. [딕셔너리. nurse_pk : set(날짜 묶음)]
    current_month,          # 5. 현재 월
    current_day,            # 6. 현재 날짜
):

    whole_schedule = []
    # 추가 예정 - recursion을 위한 당시.. dict 추가. 
    temporary_dicts = [dict() for _ in range(MONTHS_LAST_DAY[current_month] + 1)]
    recursion_time = 0
    ideal_schedule = make_ideal_counter(needed_nurses_per_shift)

    # 1. 종료 조건
    # 정상 종료
    while current_day != MONTHS_LAST_DAY[current_month] + 1:

        # 2. 스케쥴 생성
        temporary_schedule = make_daily_schedule(
            nurse_pk_list = nurse_pk_list,
            nurse_info = nurse_info,
            ideal_schedule = ideal_schedule,
            current_day = current_day
            )

        # 3. 스케쥴 검증(미구현)

        # 4. 스케쥴 업데이트
        nurse_info = update_nurse_info(nurse_info, temporary_schedule)
        whole_schedule.append(temporary_schedule)

        current_day += 1

        if recursion_time >= 15:
            print('설정 변경 필요')
            return 

    return whole_schedule, nurse_info

# 3. 스케쥴 검증
        # is_validate = check_validation(temporary_schedule)

        # 1) 검증 실패
        # 재작성. 
        # need_to_go_back = False
        # for _ in range(100):
        #     temporary_schedule = make_daily_schedule(nurse_info, ideal_schedule)
        #     is_validate = check_validation(temporary_schedule)    
        #     if is_validate:
        #         break
        # else:
        #     need_to_go_back = True

        # 4. 재귀
        # if need_to_go_back:
        #     recursion_time += 1
        #     return make_monthly_schedule()        



"""
0 NURSE_NUMBER 간호사 일련번호
1 SHIFTS, 이번 다 근무 일수 
2 SHIFT_STREAKS, 연속 근무일 수 
3 OFFS, 그.. 마크다운에 있는 'OFF' 참조.
4 MONTHLY_NIGHT_SHIFTS, 한 달에 night 근무한 횟수
5 VACATION_INFO,   휴가 정보(딕셔너리로 수정 예정)
6 OFF_STREAKS,         연속 휴무 
7 LAST_SHIFT,           마지막 근무 정보
"""
def update_nurse_info(nurse_info, temporary_schedule):
    
    # 모든 4개의 시프트를 순회하며    
    for shift in range(4):

        # 모든 간호사들 순회.
        for nurse in temporary_schedule[shift]:
            
            # 가장 최근 근무 기록 갱신. 
            nurse_info[nurse][7] = shift

            # 만약 오늘 쉬었다면 
            # 연속 근무일수 초기화
            if not shift:
                nurse_info[nurse][2] = 0
                nurse_info[nurse][6] += 1
                
            # 일을 한 것. 
            elif shift == 1:
                nurse_info[nurse][1] += 1
                nurse_info[nurse][2] += 1
                nurse_info[nurse][6] = 0

            elif shift == 2:
                nurse_info[nurse][1] += 1
                nurse_info[nurse][2] += 1
                nurse_info[nurse][6] = 0

            elif shift == 3:
                nurse_info[nurse][1] += 1
                nurse_info[nurse][2] += 1
                nurse_info[nurse][4] += 1
                nurse_info[nurse][6] = 0
            
    return nurse_info


"""
테스트용 -- 리스트의 각 열이 의미하는 바는 아래와 같습니다.
0 NURSE_NUMBER 간호사 일련번호
1 SHIFTS, 이번 달 근무 일수 
2 SHIFT_STREAKS, 연속 근무일 수 
3 OFFS, 그.. 마크다운에 있는 'OFF' 참조.
4 MONTHLY_NIGHT_SHIFTS, 한 달에 night 근무한 횟수
5 VACATION_INFO,   휴가 정보(외부 딕셔너리로 수정 예정)
6 OFF_STREAKS,         연속 휴무 
7 LAST_SHIFT,           마지막 근무 정보
"""

example_nurse_info = {
    1: [1, 0, 0, 0, 0, 0, 2, 0],
    2: [2, 0, 0, 0, 0, 0, 2, 0],
    3: [3, 0, 0, 0, 0, 0, 2, 0],
    4: [4, 0, 0, 0, 0, 0, 2, 0],
    5: [5, 0, 0, 0, 0, 0, 2, 0],
    6: [6, 0, 0, 0, 0, 0, 2, 0],
    7: [7, 0, 0, 0, 0, 0, 2, 0],
    8: [8, 0, 0, 0, 0, 0, 2, 0],
    9: [9, 0, 0, 0, 0, 0, 0, 0],
    10:[10, 0, 0, 0, 0, 0, 2, 0],
    11: [11, 0, 0, 0, 0, 0, 2, 0],
    12: [12, 0, 0, 0, 0, 0, 2, 0],
    13: [13, 0, 0, 0, 0, 0, 2, 0]
}

# example_nurse_pk_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

# start_time = time.time()
# result, modified_nurse_info = make_monthly_schedule(
#     nurse_pk_list=example_nurse_pk_list,
#     nurse_info=example_nurse_info,
#     number_of_nurses=13,
#     needed_nurses_per_shift=3,
#     vacation_info=[],
#     current_month=10,
#     current_day=1,    
#     )
# print('디버깅용 딕셔너리')
# pprint(modified_nurse_info)

# print()
# i = 1
# for daily in result:
#     print(i, end=' ')
#     i += 1
#     for j in range(4):
#         aaa = daily[j]
#         aaa.sort()
#         print(f'근무 타입:"{j} 근무자: {aaa}', end=' ')
#     print()

# end_time = time.time()
# print('실행 시간')
# print(end_time - start_time)