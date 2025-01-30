# ----------------------------------------------------------
# کد نویسی شده توسط: محمدحسام پوراکبر
# تاریخ ایجاد: 2025/01/29
# توضیحات: این برنامه برای مدیریت و نمایش لیست دروس طراحی شده است.
# ----------------------------------------------------------

import streamlit as st
import pandas as pd
import re

# -----------------------------
# عنوان صفحه
st.title(":probing_cane:ساخت برنامه درسی هوشمند")
st.markdown('<span style="font-size: 12px;">[نحوه دریافت فایل لیست ورودی استاد](https://t.me/HesamsLabe) | [فایل تست](https://uupload.ir/view/book1_ukv6.xlsx/)</span>', unsafe_allow_html=True)

# باکس آپلود فایل
uploaded_file = st.file_uploader('فایل خود را انتخاب کنید', type=['xlsx'])

# تابع استخراج زمان
def extract_time(text):
    # اطمینان از اینکه ورودی یک رشته معتبر است
    if isinstance(text, str):
        # استفاده از الگوی ریجکس برای استخراج زمان (مثل 15:30 تا 17:29)
        match = re.search(r'\d{2}:\d{2} تا \d{2}:\d{2}', text)
        if match:
            return match.group(0)
    return None

# تابع تغییر روز
def check_day(text):
    if pd.isna(text):  #*
        return "روزی اعلام نشده"
    
    words = text.split()

    if len(words) < 8:
        day = words[0]
        match day:
            case "شنبه": return "0شنبه"
            case "يكشنبه": return "1يكشنبه"
            case "دوشنبه": return "2دوشنبه"
            case "سه": return "3سه شنبه"
            case "چهارشنبه": return "4چهارشنبه"
            case "پنج": return "5پنجشنبه"
            case "جمعه": return "6جمعه"
            case _: return day
            
    elif len(words) > 8:
        day = words[0]
        if day == "هفته":
            week_data = words[2]
            match week_data:
                case "شنبه": return '0' + words[0]+" " + words[1] + " " + "شنبه"
                case "يكشنبه": return '1' + words[0]+" " + words[1] + " " + "1يكشنبه"
                case "دوشنبه": return '2' + words[0] + " " + words[1] + " " + "دوشنبه"
                case "سه": return '3' + words[0] + " " + words[1] + " " + "سه شنبه"
                case "چهارشنبه": return '4' + words[0] + " " + words[1] + " " + "چهارشنبه"
                case "پنج": return '5' + words[0] + " " + words[1] + " " + "پنجشنبه"
                case "جمعه": return '6' + words[0] + " " + words[1] + " " + "جمعه"
                case _: return "روز غیرقابل شناسایی"
        else:
            match day:
                case "شنبه": return "0شنبه"
                case "يكشنبه": return "1يكشنبه"
                case "دوشنبه": return "2دوشنبه"
                case "سه": return "3سه شنبه"
                case "چهارشنبه": return "4چهارشنبه"
                case "پنج": return "5پنجشنبه"
                case "جمعه": return "6جمعه"
                case _: return day
    else:
        day = words[0]
        if day == "هفته":
            week_data = words[2]
            match week_data:
                case "شنبه": return '0' + words[0]+" " + words[1] + " " + "شنبه"
                case "يكشنبه": return '1' + words[0]+" " + words[1] + " " + "1يكشنبه"
                case "دوشنبه": return '2' + words[0] + " " + words[1] + " " + "دوشنبه"
                case "سه": return '3' + words[0] + " " + words[1] + " " + "سه شنبه"
                case "چهارشنبه": return '4' + words[0] + " " + words[1] + " " + "چهارشنبه"
                case "پنج": return '5' + words[0] + " " + words[1] + " " + "پنجشنبه"
                case "جمعه": return '6' + words[0] + " " + words[1] + " " + "جمعه"
                case _: return "روز غیرقابل شناسایی"
    
    
if uploaded_file is not None:
    # خواندن داده‌ها از فایل اکسل
    data = pd.read_excel(uploaded_file)
    
    # استخراج ستون‌های مربوط به درس و استاد
    lesson_unit = data['نام درس']  # فایل درسی
    teachers_data = data["استاد"]
    
    # متغیر برای ذخیره داده‌های انتخاب‌شده
    if "selected_data" not in st.session_state:
        st.session_state.selected_data = pd.DataFrame(columns=data.columns)

    # متغیر برای نگهداری انتخاب‌های قبلی
    if "previous_selections" not in st.session_state:
        st.session_state.previous_selections = []

    # انتخاب درس‌ها
    selections_students = st.multiselect(
        "درس‌هایی که این ترم بهش نیاز دارید رو انتخاب کنید",
        lesson_unit.drop_duplicates().sort_values()
    )
    # حذف داده‌های مربوط به درس‌های حذف‌شده از انتخاب‌های قبلی
    removed_lessons = set(st.session_state.previous_selections) - set(selections_students)
    for removed_lesson in removed_lessons:
        st.session_state.selected_data = st.session_state.selected_data[st.session_state.selected_data['نام درس'] != removed_lesson]

    # به‌روزرسانی لیست انتخاب‌های قبلی
    st.session_state.previous_selections = selections_students
    
    if selections_students:
        # پردازش هر درس انتخابی
        for option in selections_students:
            # فیلتر کردن درس انتخاب با داده درس اصلی
            filtered_teachers = data[lesson_unit == option]
             
            # انتخاب استاد برای درس
            Selected_course = st.segmented_control(
                f"استاد مورد نظر درس «:book: :blue[{option}]:book:» را انتخاب کنید:",
                filtered_teachers['استاد'].drop_duplicates().tolist(),
                key=option  # استفاده از کلید یکتا برای هر درس
            )

            # حذف داده‌های قبلی مربوط به این درس قبل از اضافه کردن داده جدید
            st.session_state.selected_data = st.session_state.selected_data[~(st.session_state.selected_data['نام درس'] == option)]

            # پیدا کردن سطر مربوط به استاد و درس انتخاب‌شده
            selected_row = data[
                (data["نام درس"] == option) & (data["استاد"] == Selected_course)
            ]
            
            # اضافه کردن داده‌های جدید به متغیر `selected_data`
            st.session_state.selected_data = pd.concat(
                [st.session_state.selected_data, selected_row],
                ignore_index=True
            )
        
        if not st.session_state.selected_data.empty:
            # استخراج روز
            st.session_state.selected_data["روز"] = st.session_state.selected_data["زمانبندي تشکيل کلاس"].apply(check_day)
            
            # استخراج زمان
            st.session_state.selected_data["زمان"] = st.session_state.selected_data["زمانبندي تشکيل کلاس"].apply(extract_time)
            
            # حذف ستون‌های اضافی
            st.session_state.selected_data = st.session_state.selected_data.drop(columns=["كليدهاي فرمان", "Unnamed: 1", "نام كلاس درس"])
            st.session_state.selected_data["كد درس"] = (st.session_state.selected_data["كد درس"]).astype(str)
            st.session_state.selected_data = st.session_state.selected_data[[
                "روز", "زمان", "نام درس", "استاد", "كد درس","تعداد واحد نظري",
                "تعداد واحد عملي", "نوع درس", "گروه آموزشی",
                "دانشکده", "نوع ارائه", "سطح ارائه", "واحد" ,"استان"
                ]]
            #st.table(st.session_state.selected_data)
            # نمایش داده‌ها
            st.header("برنامه شما ساخته شد")
            st.write(st.session_state.selected_data)
            
on = st.toggle("تنظیمات پیشرفته")
st.markdown("«نوشته شده توسط «محمدحسام پوراکبر")

if on:
    st.markdown("[نظرات و پیشنهاداتتون رو میتونید در اینجا بنویسید](https://t.me/MohmmadHesamPourakbar)" )
    st.markdown("[ارتباط](https://www.linkedin.com/in/he3amtesla/)" )      
   # csv_data = st.session_state.selected_data.to_csv(index=False).encode('utf-8-sig')
    #st.download_button(
     #   label="دانلود برنامه",
      #  data=csv_data,
     #   file_name="program.csv",
     #   mime="text/csv"
  #  )
            
#sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
#selected = st.feedback("thumbs")
#if selected is not None:
   # st.markdown(f"You selected: {sentiment_mapping[selected]}")
