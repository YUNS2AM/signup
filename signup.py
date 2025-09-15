from logging import PlaceHolder
import streamlit as st
import pandas as pd
import os
import time

# 유효성 검사 함수
def validate_signup(username, password, email_id, email_domain):
    email = f"{email_id}@{email_domain}"
    if len(username) < 6:
        return False, "아이디는 최소 6자 이상이어야 합니다."
    if len(password) < 8:
        return False, "비밀번호는 최소 8자 이상이어야 합니다."
    if len(email_id) < 3:
        return False, "유효한 이메일 주소를 입력하세요."
    if  not email_domain:
        return False, "이메일을 선택해 주세요."
    return True, ""

# 사용자 저장 함수 (CSV)
def save_user(username, password, email_id, email_domain):
    if os.path.exists("users.csv"):
        df = pd.read_csv("users.csv")
    else:
        df = pd.DataFrame(columns=["username", "password", "email_id",'email_domain'])
    
    if username in df["username"].values:
        return False, "이미 존재하는 아이디입니다."
    
    new_row = pd.DataFrame([{"username": username, "password": password, "email_id": email_id, "email_domain":email_domain}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("users.csv", index=False)

    PlaceHolder = st.empty()
    emojis = ["📫 회원가입 성공!", "📪 회원가입 성공!", "📭 회원가입 성공!", "📬 회원가입 성공!"]  # 바꿀 이모티콘 리스트

    for i in range(20):  # 20번 바꾸기
        emoji = emojis[i % len(emojis)]
        PlaceHolder.markdown(f"<h3 style='text-align:center;'>{emoji}</h1>", unsafe_allow_html=True)
        time.sleep(0.2)  # 0.2초마다 바꾸기
    return True, "🎉 가입을 축하합니다!"

# 스트림릿 UI
st.title("📩 회원가입")

with st.form("signup_form"):
    username = st.text_input("아이디", placeholder="abcde123")
    password = st.text_input("비밀번호", type="password", placeholder="영문, 숫자, 특수문자 조합 8글자 이상")
    col1, col2 = st.columns(2)
    with col1:
        email_id = st.text_input("이메일", placeholder="12345")
    with col2:
        email_domain = st.selectbox("이메일 선택",['naver.com','gmail.com','daum.net','kakao.com','hanmail.net'])
    submitted = st.form_submit_button("회원가입")

    if submitted:
        valid, msg = validate_signup(username, password, email_id, email_domain)
        if not valid:
            st.error(msg)
        else:
            success, msg = save_user(username, password, email_id, email_domain)
            if success:
                st.success(msg)
            else:
                st.error(msg)

