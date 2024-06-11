import streamlit as st
import streamlit.components.v1 as stc
import re
from datetime import datetime
from datetime import timedelta
import time


def get_japanese_day(input_date):
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    return weekdays[input_date.weekday()]


def check_character(input_string):
    
    regex_pattern = r"[^a-z0-9]"  
    if re.search(regex_pattern, input_string):
        return False
    else:
        if len(input_string) == 7:
            return True
        else:
            return False


def check_time(input_string):
    
    regex_pattern = r"[^0-9:]"  
    if re.search(regex_pattern, input_string):
        return False
    else:
        if len(input_string) == 5 and input_string[2] == ":":
            return True
        else:
            return False


if __name__ == "__main__":

    st.set_page_config(
        page_title="議事録補助",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={},
    )

    st.sidebar.title("🔰サイドバー🔰")
    cnt_str = "テキストを入力"

    st.sidebar.header("文字数カウント")
    cnt_str = st.sidebar.text_area(label=f"Ctrl+Enterでカウント", value=cnt_str)
    st.sidebar.write(f"{len(cnt_str)}文字")
    st.sidebar.header("その他")
    st.sidebar.text(
        "ここに出席管理システムとか\nGROWIの議事録ページとかの\nリンクを貼るのもアリかも。"
    )


    st.write(
        """
    <style>
    .right-link {
        float: right;
        display: inline-block;
        padding: 8px 16px;
        background-color: #FFC800;
        color: #ffffff;
        text-decoration: none;
        border-radius: 4px;
        cursor: pointer;
    }.right-link:hover {
        background-color: #FF6400;
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("議事録補助")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("📝入力欄")
    with col2:
        if st.button("風船を飛ばす！🎈", use_container_width=True, key="balloon2"):
            st.balloons()

    (col1, col2) = st.columns([3, 1])
    with col1:
        st.subheader("ページ下部のテンプレに反映されます。")
    with col2:
        st.write(
            '<a href="#template" class="right-link">ジャンプ！</a>',
            unsafe_allow_html=True,
        )
    # 移動用アンカー
    st.write('<a id="input"></a>', unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        num_author = "s23t3xx"
        num_author = st.text_input(label="議事録担当者の学籍番号", value=num_author)
        if not check_character(num_author):
            st.error("学籍番号は半角小文字で先頭にsがついている必要があります。")
    with col2:
        last_name_author = "香川"
        last_name_author = st.text_input(
            label="議事録担当者の姓", value=last_name_author
        )
        if any(char.isspace() for char in last_name_author):
            st.error("入力に空白を含まないでください。")
    with col3:
        first_name_author = "太郎"
        first_name_author = st.text_input(
            label="議事録担当者の名", value=first_name_author
        )
        if any(char.isspace() for char in first_name_author):
            st.error("入力に空白を含まないでください。")

    attendees = "○ B3 〇〇、ＸＸ\n○ B2 □□\n○ B1 △△"
    attendees = st.text_area(
        "出席者(出席管理システムからコピペしてください。)", value=attendees
    )

    last_name_next_author = "苗字"
    last_name_next_author = st.text_input(
        label="次回議事録担当者の姓", value=last_name_next_author
    )
    if any(char.isspace() for char in last_name_next_author):
        st.error("入力に空白を含まないでください。")

    st.divider()

    # 入力ボックスの数を保持する変数
    cnt_activity = st.session_state.get("cnt_activity", 1)

    col1, col2 = st.columns(2)

    with col1:
        plus_button = st.button("進行を追加", type="primary", use_container_width=True)
    if plus_button:
        cnt_activity += 1

    with col2:
        minus_Button = st.button("進行を削除", type="primary", use_container_width=True)
    if minus_Button and (st.session_state["cnt_activity"] > 1):
        cnt_activity -= 1

    # cnt_activityの値を更新
    st.session_state["cnt_activity"] = cnt_activity

    # 入力ボックスとテキストの表示
    timetable = []  # 入力されたテキストを保持するリスト
    for i in range(cnt_activity):
        col1, col2, col3 = st.columns(3)
        with col1:
            text_input = st.text_input(
                f"開始時刻 {i+1}", value="18:30", key=f"beginning{i}"
            )
            if not check_time(text_input):
                st.error("不適切な時間です。")
            timetable.append(text_input)  # 入力されたテキストをリストに追加

        with col2:
            text_input = st.text_input(f"終了時刻 {i+1}", value="20:30", key=f"end{i}")
            if not check_time(text_input):
                st.error("不適切な時間です。")
            timetable.append(text_input)  # 入力されたテキストをリストに追加

        with col3:
            text_input = st.text_input(
                f"活動内容 {i+1}", value="定例活動", key=f"activity{i}"
            )
            timetable.append(text_input)  # 入力されたテキストをリストに追加
    activity_all = ""
    for i in range(0, len(timetable), 3):
        activity_all += (
            "○ " + timetable[i] + "-" + timetable[i + 1] + f" {timetable[i+2]}\n"
        )
    st.divider()
    activity_details = "● 自己紹介LT\n\n活動内容を具体的に記述。\n\n● チーム開発\n\n○ チーム〇〇\n\n活動内容を具体的に記述。 \n\n○ チームＸＸ\n\n活動内容を具体的に記述。"
    activity_details = st.text_area("活動", value=activity_details, height=500)
    st.divider()
    # 入力ボックスの数を保持する変数
    cnt_announcement = st.session_state.get("cnt_announcement", 1)

    col1, col2 = st.columns(2)
    # 「追加」ボタンが押されたときの処理
    with col1:
        if st.button("連絡を追加", type="primary", use_container_width=True):
            cnt_announcement += 1

    # 「削除」ボタンが押されたときの処理
    with col2:
        if (
            st.button("連絡を削除", type="primary", use_container_width=True)
            and cnt_announcement > 1
        ):
            cnt_announcement -= 1

    # cnt_activityの値を更新
    st.session_state["cnt_announcement"] = cnt_announcement

    # 入力ボックスとテキストの表示
    entered_announcement = []  # 入力されたテキストを保持するリスト
    for i in range(cnt_announcement):

        text_input2 = st.text_input(
            f"連絡事項 {i+1}", value="△Ｘ〇について", key=f"announcement{i}"
        )
        entered_announcement.append(text_input2)  # 入力されたテキストをリストに追加

        text_input2 = st.text_area(
            f"連絡事項の詳細 {i+1}",
            value="連絡事項を具体的に記述。",
            key=f"announcement_details{i}",
        )
        entered_announcement.append(text_input2)  # 入力されたテキストをリストに追加

    announcement_all = ""
    for i in range(0, len(entered_announcement), 2):
        announcement_all += (
            "● "
            + entered_announcement[i]
            + "\n\n"
            + entered_announcement[i + 1]
            + "\n\n"
        )

    st.divider()

    comment_author = "備考"
    comment_author = st.text_area("備考", value=comment_author)
    # 移動用アンカー
    st.write('<a id="template"></a>', unsafe_allow_html=True)
    st.divider()

    beginning_timetable = "18:30"
    end_timetable = "20:30"
    activity = "hoge活動"
    # 今日の日付を取得
    today = datetime.today()
    weekday_japanese = get_japanese_day(today)
    weekday_number = -1
    current_date = ""
    for i in range(7):
        current_date = today + timedelta(days=i + 1)
        weekday_number = current_date.weekday()  # 曜日を数字で取得
        if weekday_number == 2:
            break
        if weekday_number == 4:
            break
    date1 = current_date
    current_date = ""
    for i in range(7):
        current_date = date1 + timedelta(days=i + 1)
        weekday_number = current_date.weekday()  # 曜日を数字で取得
        if weekday_number == 2:
            break
        if weekday_number == 4:
            break
    date2 = current_date
    current_date = ""
    for i in range(7):
        current_date = date2 + timedelta(days=i + 1)
        weekday_number = current_date.weekday()  # 曜日を数字で取得
        if weekday_number == 2:
            break
        if weekday_number == 4:
            break
    date3 = current_date

    (col1, col2) = st.columns([3, 1])
    with col1:
        st.header("📋テンプレ欄（コピー専用）")
    with col2:
        st.write(
            '<a href="#input" class="right-link">入力に戻る！</a>',
            unsafe_allow_html=True,
        )

    st.code(
        "□ SLP 定例活動 "
        + datetime.now().strftime(f"%Y.%m.%d({weekday_japanese}) ")
        + f"{num_author} {last_name_author}{first_name_author}\n\n"
        + "★ 次第\n\n"
        + f"● 出席\n\n{attendees}\n\n"
        + f"議事 {last_name_author}\n\n"
        + f"次回議事 {last_name_next_author}\n\n"
        + "● 進行\n\n"
        + f"{activity_all}\n"
        + "★ 活動\n\n"
        + f"{activity_details}\n\n"
        + "★ 連絡\n\n"
        + f"{announcement_all}"
        + "■ 予定\n\n"
        + date1.strftime(f"%Y.%m.%d({get_japanese_day(date1)}) ")
        + f"{beginning_timetable}-{end_timetable} 定例活動\n"
        + date2.strftime(f"%Y.%m.%d({get_japanese_day(date2)}) ")
        + f"{beginning_timetable}-{end_timetable} 定例活動\n"
        + date3.strftime(f"%Y.%m.%d({get_japanese_day(date3)}) ")
        + f"{beginning_timetable}-{end_timetable} 定例活動\n\n"
        + "■ 備考\n\n"
        + f"{comment_author}\n\n"
    )
    if st.button("風船を飛ばす！🎈", use_container_width=True, key="balloon1"):
        st.balloons()
