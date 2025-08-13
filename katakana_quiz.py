import streamlit as st
import random
from katakana_data import katakana_data, katakana_dakuten_data, katakana_yo_on_data, katakana_soku_on_data

st.set_page_config(page_title="가타카나 학습 퀴즈", page_icon="🇯🇵", layout="centered")

# 세션 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'current_katakana' not in st.session_state:
    st.session_state.current_katakana = None
if 'multiple_choices' not in st.session_state:
    st.session_state.multiple_choices = []
if 'correct_answer_index' not in st.session_state:
    st.session_state.correct_answer_index = 0
if 'is_answered' not in st.session_state:
    st.session_state.is_answered = False

# 학습 세트 선택
learning_set_mode = st.selectbox(
    "학습 세트 선택",
    ["기본모드", "탁음/반탁음모드", "요음모드", "혼합모드"],
    key="learning_set_mode_select"
)

if learning_set_mode == "기본모드":
    current_dataset = katakana_data
elif learning_set_mode == "탁음/반탁음모드":
    current_dataset = katakana_dakuten_data
elif learning_set_mode == "요음모드":
    current_dataset = katakana_yo_on_data
else:
    # 혼합모드
    current_dataset = {**katakana_data, **katakana_dakuten_data, **katakana_yo_on_data, **katakana_soku_on_data}

# 퀴즈 타입 선택
quiz_type = st.selectbox(
    "퀴즈 모드 선택",
    ["가타카나 -> 영어 입력", "가타카나 -> 한국어 입력", "영-한 발음 -> 가타카나 5개 중 선택"],
    key="quiz_type_select"
)

# 문제 생성
def generate_multiple_choices(correct_katakana):
    all_katakana = list(current_dataset.keys())
    choices = [correct_katakana] + random.sample([k for k in all_katakana if k != correct_katakana], 4)
    random.shuffle(choices)
    return choices, choices.index(correct_katakana)

def new_question():
    st.session_state.current_katakana = random.choice(list(current_dataset.keys()))
    st.session_state.feedback = ""
    st.session_state.multiple_choices = []
    st.session_state.correct_answer_index = 0
    st.session_state.is_answered = False

# 초기 문제 설정
if st.session_state.current_katakana is None:
    new_question()

# 퀴즈 표시
st.title("가타카나 퀴즈")

st.write(f"점수: {st.session_state.score} / {st.session_state.total_questions}")

if quiz_type == "가타카나 -> 영어 입력":
    st.markdown(f"## {st.session_state.current_katakana}")
    user_answer = st.text_input("영어로 입력하세요:", key="english_input")
    if st.button("제출", key="submit_button_english"):
        st.session_state.total_questions += 1
        correct_english = current_dataset[st.session_state.current_katakana]['english']
        if user_answer.lower() == correct_english.lower():
            st.session_state.score += 1
            st.session_state.feedback = "정답입니다!"
        else:
            st.session_state.feedback = f"오답입니다. 정답은 {correct_english} 입니다."
        st.session_state.is_answered = True

elif quiz_type == "가타카나 -> 한국어 입력":
    st.markdown(f"## {st.session_state.current_katakana}")
    user_answer = st.text_input("한국어로 입력하세요:", key="korean_input")
    if st.button("제출", key="submit_button_korean"):
        st.session_state.total_questions += 1
        correct_korean = current_dataset[st.session_state.current_katakana]['korean']
        if user_answer == correct_korean:
            st.session_state.score += 1
            st.session_state.feedback = "정답입니다!"
        else:
            st.session_state.feedback = f"오답입니다. 정답은 {correct_korean} 입니다."
        st.session_state.is_answered = True

elif quiz_type == "영-한 발음 -> 가타카나 5개 중 선택":
    if not st.session_state.multiple_choices:
        choices, correct_index = generate_multiple_choices(st.session_state.current_katakana)
        st.session_state.multiple_choices = choices
        st.session_state.correct_answer_index = correct_index

    correct_english = current_dataset[st.session_state.current_katakana]['english']
    correct_korean = current_dataset[st.session_state.current_katakana]['korean']
    st.markdown(f"## 발음: {correct_english} ({correct_korean})")

    for i, choice in enumerate(st.session_state.multiple_choices):
        if st.button(choice, key=f"choice_{i}"):
            st.session_state.total_questions += 1
            if i == st.session_state.correct_answer_index:
                st.session_state.score += 1
                st.session_state.feedback = "정답입니다!"
            else:
                st.session_state.feedback = f"오답입니다. 정답은 {st.session_state.multiple_choices[st.session_state.correct_answer_index]} 입니다."
            st.session_state.is_answered = True

st.write(st.session_state.feedback)

if st.session_state.is_answered:
    if st.button("다음 문제", key="next_question_button"):
        new_question()
        st.rerun()
else:
    st.button("다음 문제", key="next_question_button", disabled=True)


