import random
from datetime import date
"""
number_of_nurses: 간호사 총 인원 수

last_duties: 이전 근무 기록을 담은 리스트.
인덱스는 간호사 번호, 값은 스케쥴을 의미함.

today_schedule: 현재 근무 기록을 담은 리스트.


"""


def generate_random_token(last_duties, number_of_nurses):
    # print(number_of_nurses)

    nurse_generator_token = [0] * number_of_nurses
    
    for nurse in range(number_of_nurses):
        token = last_duties[nurse] + random.random() + random.random()
        nurse_generator_token[nurse] = token

    return nurse_generator_token


def check_ascendance(today_schedule, last_duties, number_of_nurses):
    # print('checking ascendance')
    # print(today_schedule)

    for nurse in range(number_of_nurses):
        if today_schedule[nurse] != 0\
                and today_schedule[nurse] < last_duties[nurse]:

            # print(f'{nurse}의 오름차순 근무 불가')
            return False

    # print()
    return True


def ascend_shift(schedule_token_list):

    for i in range(len(schedule_token_list)):
        schedule_token_list[i] += 1

    return schedule_token_list


def make_daily_schedule(random_token_list, number_of_nurses):
    # 이후 구현할 것 = day_off_list 받아서..

    daily_schedule = [-1] * number_of_nurses

    for nurse in range(number_of_nurses):
        daily_schedule[nurse] = int(random_token_list[nurse] % 4)

    # print(daily_schedule)
    return daily_schedule


def check_enough_nurse(
    today_schedule,
    nurse_grade,
    needed_nurse,
    number_of_nurses,
    exceptions=0
    ):
    
    # print('checking enough nurses....')
    # 아침 1, 점심1, 저녁 1, 
    # 수간호사 1, 중간 간호사 1, 약체 간호사 1.
    # 이렇게 최소한 9명이 있어야 함

    # nurses_sorted 에는 아침, 점심, 저녁별
    
    # 빈 리스트를 만든 뒤
    nurses_counter = [[0] * 3 for _ in range(3)]

    # 모든 간호사들을 조회.
    for nurse in range(number_of_nurses):
        shift_type = today_schedule[nurse] - 1  # 근무 타입(주간 / 오후 / 심야)
        grade = nurse_grade[nurse]  # 간호사 등급을 조회한 뒤 

        nurses_counter[shift_type][grade] += 1  # nurse_counter에 정렬한다.

    # print(nurses_counter)

    for shift in nurses_counter:
        if 0 in shift:
            return False


    return True
