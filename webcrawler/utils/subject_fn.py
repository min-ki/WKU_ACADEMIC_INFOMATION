from collections import Counter
from . import subject_variable

def get_major_subject(subject):
    
    """
        전공과목 리스트 반환
    """    
    major_subject = {}

    for title, item in subject.items():
        if item[0] == '기전' or item[0] == '선전' or item[0] == '전선' or item[0] == '전필' or item[0] == '응전' or item[0] == '복수' or item[0] == '교직':
            major_subject[title] = item

    return major_subject

## 교양과목 반환해주는 함수
def get_culture_subject(subject):

    """ 
        교양과목 리스트 반환
    """
    culture_subject = {}

    for title, item in subject.items():
        if item[0] == '교필' or item[0] == '교선' or item[0] == '계필' or item[0] == '학필':
            culture_subject[title] =  item

    return culture_subject

## 전공과목 총 학점, 교양과목 총 학점
def get_sum_of_subject(subject):

    sum = {}

    basic_major_subject_sum = 0
    major_subject_sum = 0
    culture_subject_sum = 0

    select_major_subject_sum = 0 
    apply_major_subject_sum = 0
    multiply_major_subject_sum = 0
    normal_subject = 0
    teach_subject = 0

    for title, arr in subject.items():
        if arr[0] == "기전" or arr[0] == "전필":  # 기전 카운트
            basic_major_subject_sum += float(arr[2])

        if arr[0] == "선전" or arr[0] == "전선": # 선택전공 카운트
            select_major_subject_sum += float(arr[2])
        
        if arr[0] == "응전": # 응용전공 카운트
            apply_major_subject_sum += float(arr[2])

        if arr[0] == "복수": # 복수전공 카운트
            multiply_major_subject_sum += float(arr[2])

        if arr[0] == "일선":  # 일반선택 카운트
            normal_subject += float(arr[2])

        if arr[0] == "교직": # 교직 카운트
            teach_subject += float(arr[2])

        if arr[0] == "교필" or arr[0] == "교선" or arr[0] == "계필":  # or arr[0] == "일선"
            culture_subject_sum = culture_subject_sum + float(arr[2])
        elif arr[0] == "기전" or arr[0] == "전필" or arr[0] == "전선" or arr[0] == "선전" or arr[0] == "복수" or arr[0] == "응전" or arr[0] == '교직':
            major_subject_sum = major_subject_sum + float(arr[2])

    sum['basic_major_subject_sum'] = int(basic_major_subject_sum)
    sum['major_subject_sum'] = int(major_subject_sum)
    sum['culture_subject_sum'] = int(culture_subject_sum)
    sum['select_major_subject_sum'] = int(select_major_subject_sum)
    sum['apply_major_subject_sum'] = int(apply_major_subject_sum)
    sum['multiply_major_subject_sum'] = int(multiply_major_subject_sum)
    sum['normal_subject'] = int(normal_subject)
    sum['teach_subject'] = int(teach_subject)
    
    return sum

### 복수전공 체크
def check_plural_major(subject):
    '''
        복수전공을 한다면은 복수유형의 과목이 존재
    '''
    for item in subject.values():
        if item[0] == "복수":
            return True
    return False

### 교직이수 체크
def check_teach_major(subject):
    '''
        타입중 교직이 존재하면 교직 이수
    '''
    for item in subject.values():
        if item[0] == "교직":
            return True
    return False

def get_major_point(user_number, user_colleage, user_major):
    """
        리턴값 : 전공학점, 기본전공학점
    """
    user_number = int(''.join(list(user_number[2:4])))

    basic_major_point = 0
    major_point = 0
    special_point = 0

    # 교학대학
    if user_colleage == "교학대학":
        basic_major_point = 18
        major_point = 69
    # 인문대학
    elif user_major == "국어국문학과" or user_major == "문예창작학과" or user_major == "영어영문학과" or user_major == "중국학과" or user_major == "역사문화학부" or user_major == "철학과" or user_major == "음악과":
        basic_major_point = 15
        major_point = 66
    # 사범대학
    elif user_major == "국어교육과" or user_major == "영어교육과" or user_major == "일어교육과" or user_major == "한문교육과" or user_major == "역사교육과" or user_major == "교육학과" or user_major == "유아교육과":
        basic_major_point = 15
        major_point = 69
    elif user_major == "가정교육과" or user_major == "수학교육과" or user_major == "체육교육과":
        basic_major_point = 19
        major_point = 69
    elif user_major == "중등특수교육과":
        basic_major_point = 15
        major_point = 80
        special_point = 42 - basic_major_point
    # 조형예술디자인 대학
    elif user_major == "미술과" or user_major == "귀금속보석공예과" or user_major == "디자인학부":
        basic_major_point = 19
        major_point = 66
    elif user_major == "패션디자인산업학과":
        basic_major_point = 19
        major_point = 69
    # 사회과학대학
    elif user_major == "행정언론학부" or user_major == "복지·보건학부" or user_major == "군사학과" or user_major == "경찰행정학과" or user_major == "소방행정학과":
        basic_major_point = 15
        major_point = 66
    elif user_major == "가동아정복지학과":
        basic_major_point = 19
        major_point = 69
    # 자연과학대학
    elif user_major == "응용수학부" or user_major == "빅데이터·금융통계학부" or user_major == "바이오나노화학부" or user_major == "반도체·디스플레이학부" or user_major == "생명과학부" or user_major == "뷰티디자인학부":
        basic_major_point = 19
        major_point = 69
    elif user_major == "스포츠과학부":
        basic_major_point = 19
        major_point = 66
    elif user_colleage == "농식품융합대학":
        basic_major_point = 19
        major_point = 69
    # 창의공과대학
    elif user_colleage == "창의공과대학" and user_major != "건축학과":
        
        # 17학번 부터는 75학점 적용
        if user_number >= 17:
            major_point = 75
        else:
            major_point = 72

        basic_major_point = 19
        

    elif user_major == "건축학과":
        basic_major_point = 0
        major_point = 0
    # 경영대학
    elif user_major == "국제통상학부":
        basic_major_point = 15
        major_point = 66
    elif user_major == "경제학부":
        basic_major_point = 24
        major_point = 66
    elif user_major == "경영학부":
        basic_major_point = 30
        major_point = 66
    # 의과대학, 한의과대학, 치과대학, 한약학과
    elif user_colleage == "의과대학" or user_colleage == "한의과대학" or user_colleage == "치과대학" or user_major == "한약학과":
        basic_major_point = 0
        major_point = 0

        if user_major == "한의예과":
            basic_major_point = 0
            major_point = 0
    # 약학과
    elif user_major == "약학과":
        basic_major_point = 0
        major_point = 160
    elif user_major == "정보·전자상거래학부":
        basic_major_point = 15
        major_point = 66
    

    return major_point, basic_major_point

# 교양 이수 학점 
def get_culture_point(user_number):
    
    user_number = int(''.join(list(user_number[2:4])))
    culture_point = 0

    if user_number >= 10:
        culture_point = 60
    elif 5 <= user_number <= 9:
        culture_point = 70
    elif 2 <= user_number <= 4:
        culture_point = 80
    else:
        culture_point = 100000

    return culture_point

# 학번 user_info[1] , 단과대학명 user_info[4], 학과 user_info[6]
def get_graduated_point(user_number, user_colleage, user_major):

    graduated_point = 0

    user_number = int(''.join(list(user_number[2:4])))

    # 13학번부터 136학점 창의공과대학
    if user_number > 12 and user_colleage == "창의공과대학":
        graduated_point = 136

    elif user_number > 12 and (user_colleage == "교학대학" or user_colleage == "인문대학" or user_colleage == "경영대학" or user_colleage == "농식품융합대학"
                               or user_colleage == "자연과학대학" or user_colleage == "생활과학대학" or user_colleage == "사회과학대학"):
        graduated_point = 130
    elif user_number > 12 and user_major == "봉황인재학과":
        graduated_point = 120
    elif user_number > 5 and (user_colleage == "조형예술디자인대학" or user_colleage == "미술대학"):
        graduated_point = 130
    elif user_colleage == "의과대학" or user_colleage == "한의과대학" or user_colleage == "치과대학":
        if user_major == "한의예과":
            graduated_point = 80
        else:
            graduated_point = 160

    elif user_major == "간호학과" or user_colleage == "사범대학" or user_major == '작업치료학과':
        graduated_point = 140
    else:
        graduated_point = 140

    return graduated_point

## 백분위
def get_percentage(point, grade_point):

    try:
        percentage = (point / grade_point) * 100
    except ZeroDivisionError:
        percentage = 0
    return percentage

## 타입 카운팅
def get_count_type(subject):

    type_count = Counter()

    for title, item in subject.items():
        if item[0] in subject_variable.subject_type:
            type_count[item[0]] += 1

    return type_count

## 점수 카운팅
def get_count_grade_point(subject):

    grade_point = Counter()

    for title, item in subject.items():
        if item[3] in ['A+', 'A0', 'B+', 'B0', 'C+', 'C0', 'D+', 'D0', 'P']:
            grade_point[item[3]] += 1

    return grade_point

## 타입 별 학점 평균
def get_count_grade_average_point(subject):

    basic_major_average_point = 0 # 기본 전공 평균 평점
    select_major_average_point = 0 # 선택 전공 평균 평점
    apply_major_average_point = 0 # 응용 전공 평균 평점
    multiply_major_average_point = 0 # 복수 전공 평균 평점

    necessary_culture_average_point = 0 # 교양 필수 평균 평점
    select_culture_average_point = 0 # 교양 선택 평균 평점
    necessary_line_average_point = 0 # 계열 필수 평균 평점
    normal_select_average_point = 0 # 일반 선택 평균 평점
    teach_major_average_point = 0 # 교직 평균 평점
    major_necessary_average_point = 0 # 학과 필수 평점

    type_count = get_count_type(subject)

    type_count['기전'] -= count_consult(subject)
    type_count['교필'] -= count_uni_subject(subject)

    for title, item in subject.items():
        if item[0] == "기전" or item[0] == "전필":
            basic_major_average_point += calc_average_point(item[3])
        elif item[0] == "선전" or item[0] == "전선":
            select_major_average_point += calc_average_point(item[3])
        elif item[0] == "응전":
            apply_major_average_point += calc_average_point(item[3])
        elif item[0] == "복수":
            multiply_major_average_point += calc_average_point(item[3])
        elif item[0] == "교필":
            necessary_culture_average_point += calc_average_point(item[3])
        elif item[0] == "교선":
            select_culture_average_point += calc_average_point(item[3])
        elif item[0] == "계필":
            necessary_line_average_point += calc_average_point(item[3])
        elif item[0] == "일선":
            normal_select_average_point += calc_average_point(item[3])
        elif item[0] == "교직":
            teach_major_average_point += calc_average_point(item[3])
        elif item[0] == "학필":
            major_necessary_average_point += calc_average_point(item[3])

    type_average_point = {}

    if type_count['기전']:
        type_average_point['basic_major_average_point'] = (basic_major_average_point / type_count['기전']) if type_count['기전'] else 0
    elif type_count['전필']:
        type_average_point['basic_major_average_point'] = (basic_major_average_point / type_count['전필']) if type_count['전필'] else 0
    else:
        type_average_point['basic_major_average_point'] = 0

    if type_count['선전']:
        type_average_point['select_major_average_point'] = (select_major_average_point / type_count['선전']) if type_count['선전'] else 0
    elif type_count['전선']:
        type_average_point['select_major_average_point'] = (select_major_average_point / type_count['전선']) if type_count['전선'] else 0
    else:
        type_average_point['select_major_average_point'] = 0

    type_average_point['apply_major_average_point'] = (apply_major_average_point / type_count['응전']) if type_count['응전'] else 0
    type_average_point['multiply_major_average_point'] = (multiply_major_average_point / type_count['복수']) if type_count['복수'] else 0
    type_average_point['necessary_culture_average_point'] = (necessary_culture_average_point / type_count['교필']) if type_count['교필'] else 0
    type_average_point['select_culture_average_point'] = (select_culture_average_point / type_count['교선']) if type_count['교선'] else 0
    type_average_point['necessary_line_average_point'] = (necessary_line_average_point / type_count['계필']) if type_count['계필'] else 0
    type_average_point['normal_select_average_point'] = (normal_select_average_point / type_count['일선']) if type_count['일선'] else 0
    type_average_point['teach_major_average_point'] = (teach_major_average_point / type_count['교직']) if type_count['교직'] else 0
    type_average_point['major_necessary_average_point'] = (major_necessary_average_point / type_count['학필']) if type_count['학필'] else 0

    return type_average_point

def calc_average_point(type):
    
    return subject_variable.grade_type_value[type]

def get_culutre_necessary_point(subject):

    """
        교양 필수 학점 계산
    """

    culture_necessary_point = 0

    for title, item in subject.items():
        if item[0] == '교필':
            culture_necessary_point += float(item[2])
    
    return int(culture_necessary_point)

def get_culutre_select_point(subject):
    
    """
        교양 선택 학점 계산
    """

    culture_select_point = 0

    for title, item in subject.items():
        if item[0] == '교선':
            culture_select_point += float(item[2])
    return int(culture_select_point)

def get_line_necessary_point(subject):
    
    """
        계열 필수 학점 계산
    """

    line_necessary_point = 0

    for title, item in subject.items():
        if item[0] == '계필':
            line_necessary_point += float(item[2])
    return int(line_necessary_point)

def get_major_necessary_point(subject):
    """
        학과 필수 학점 계산
    """
    major_necessary_point = 0

    for title, item in subject.items():
        if item[0] == '학필':
            major_necessary_point += float(item[2])
    return int(major_necessary_point)

def get_language_necessary_point(subject):

    """
        언어 영역 학점 계산
    """

    language_necessary_point = 0
    language_average_point = 0
    language_subject_count = 0

    for title, item in subject.items():
        if title in subject_variable.language_subject:
            language_necessary_point += float(item[2])
            language_average_point += calc_average_point(item[3])
            language_subject_count += 1

    return int(language_necessary_point), (language_average_point / language_subject_count) if language_subject_count else 0, language_subject_count

def get_english_necessary_point(subject):
    
    """
        영어 영역 학점 계산
    """

    english_necessary_point = 0
    english_average_point = 0
    english_subject_count = 0

    for title, item in subject.items():
        if title in subject_variable.english_subject:
            english_necessary_point += float(item[2])
            english_average_point += calc_average_point(item[3])
            english_subject_count += 1

    return int(english_necessary_point), (english_average_point / english_subject_count) if english_subject_count else 0, english_subject_count

def get_sw_necessary_point(subject):

    """
        SW 영역 학점 계산
    """

    sw_necessary_point = 0
    sw_average_point = 0
    sw_subject_count = 0

    for title, item in subject.items():
        if title in subject_variable.sw_subject:
            sw_necessary_point += float(item[2])
            sw_average_point += calc_average_point(item[3])
            sw_subject_count += 1

    return int(sw_necessary_point), (sw_average_point / sw_subject_count) if sw_subject_count else 0, sw_subject_count

def get_culture_choice_point(subject):
    
    """
        인문 소양 학점 계산
    """
    culture_choice_point = 0
    culture_average_point = 0
    culture_subject_count = 0

    for title, item in subject.items():
        if title in subject_variable.culture_choice_subject:
            culture_choice_point += float(item[2])
            culture_average_point += calc_average_point(item[3])
            culture_subject_count += 1

    return int(culture_choice_point), (culture_average_point / culture_subject_count) if culture_subject_count else 0, culture_subject_count

def get_founded_subject_necessary_point(subject):

    """
        창업 영역 학점 계산
    """

    founded_subject_necessary_point = 0
    founded_average_point = 0
    founded_subject_count = 0

    for title, item in subject.items():
        if title in subject_variable.creative_subject:
            founded_subject_necessary_point += float(item[2])
            founded_average_point += calc_average_point(item[3])
            founded_subject_count += 1

    return int(founded_subject_necessary_point), (founded_average_point / founded_subject_count) if founded_subject_count else 0, founded_subject_count

def get_creative_necessary_point(subject):
    
    """
        창의 영역 학점 계산
    """
    creative_necessary_point = 0
    creative_average_point = 0
    creative_subject_count = 0

    for title, item in subject.items():
        if "창의적 발상기법" in title or "창의적사고와융합" in title:
            creative_necessary_point += float(item[2])
            creative_average_point += calc_average_point(item[3])
            creative_subject_count += 1

    return int(creative_necessary_point), (creative_average_point / creative_subject_count) if creative_subject_count else 0, creative_subject_count

def get_free_choice_subject_point(subject):
    
    """
        창업 영역 학점 계산
    """
    free_choice_subject_point = 0
    free_choice_average_point = 0
    free_choice_subject_count = 0

    free_choice_subject = []

    for title, item in subject.items():
        if title in subject_variable.free_choice_subject:
            free_choice_subject_point += float(item[2])
            free_choice_average_point += calc_average_point(item[3])
            free_choice_subject_count += 1

    return int(free_choice_subject_point), (free_choice_average_point / free_choice_subject_count) if free_choice_subject_count else 0, free_choice_subject_count

def count_consult(subject):

    """
        자기계발심층상담 과목 카운팅 함수
    """

    count = 0

    for title, item in subject.items():
        if "자기계발심층상담" in title:
            count = count + 1
    return count



def count_uni_subject(subject):
    """
        자기계발심층상담 과목 카운팅 함수
    """

    count = 0

    for title, item in subject.items():
        if "자기계발심층상담" in title:
            count = count + 1

        elif "대학생활과자기혁신" == title and item[3] == "P":
            count = count + 1
    return count
