from pathlib import Path
from PIL import Image
import streamlit as st

from src.db import init_db
from src.styles import inject_css
from src.tasks import add_task, get_tasks, toggle_task
from src.habits import add_habit, get_habits, set_habit_done, is_habit_done_today
from src.weather import get_weather

st.set_page_config(page_title="Cute Habit Tracker", page_icon="👑", layout="wide")
init_db()

st.markdown(inject_css(), unsafe_allow_html=True)

if "weather_city" not in st.session_state:
    st.session_state.weather_city = "San Antonio"
if "weather_api_key" not in st.session_state:
    st.session_state.weather_api_key = ""

left, right = st.columns([1.1, 1])

with left:
    st.markdown('<div class="main-title">Meelo Habit Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Tracking my day :)</div>', unsafe_allow_html=True)

    image_path = Path("assets/meelo_main.png")
    if image_path.exists():
        image = Image.open(image_path)
        st.image(image, use_container_width=True)

with right:
    st.markdown('<div class="cute-card"><b>Today’s Goal</b><br>Be better than yesterday 🌸</div>', unsafe_allow_html=True)

    city = st.text_input("City", value=st.session_state.weather_city)
    api_key = st.text_input("OpenWeather API key", value=st.session_state.weather_api_key, type="password")

    st.session_state.weather_city = city
    st.session_state.weather_api_key = api_key

    if city and api_key:
        try:
            weather = get_weather(city, api_key)
            if weather:
                st.markdown(
                    f'''
                    <div class="weather-card">
                        <b>Weather in {weather["city"]}</b><br>
                        {weather["temp"]:.0f}°F · {weather["description"]} ☁️
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.warning(f"Weather could not be loaded: {e}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tasks")
    with st.form("task_form", clear_on_submit=True):
        title = st.text_input("Task name")
        category = st.text_input("Category")
        due_date = st.date_input("Due date")
        submitted = st.form_submit_button("Add task")
        if submitted and title.strip():
            add_task(title.strip(), category.strip(), str(due_date))

    tasks = get_tasks()
    completed_count = 0

    for task_id, title, category, due_date, completed in tasks:
        checked = st.checkbox(
            f"{title} {'• ' + category if category else ''} {'• due ' + due_date if due_date else ''}",
            value=bool(completed),
            key=f"task_{task_id}"
        )
        if checked != bool(completed):
            toggle_task(task_id, checked)
        if checked:
            completed_count += 1

with col2:
    st.subheader("Habits 🌸")
    with st.form("habit_form", clear_on_submit=True):
        habit_name = st.text_input("Habit name")
        habit_icon = st.text_input("Habit icon", value="🌸")
        habit_submitted = st.form_submit_button("Add habit")
        if habit_submitted and habit_name.strip():
            add_habit(habit_name.strip(), habit_icon.strip() or "🌸")

    habits = get_habits()
    habit_done_count = 0

    for habit_id, name, icon in habits:
        done_today = is_habit_done_today(habit_id)
        checked = st.checkbox(f"{icon} {name}", value=done_today, key=f"habit_{habit_id}")
        if checked != done_today:
            set_habit_done(habit_id, completed=checked)
        if checked:
            habit_done_count += 1

total_items = len(tasks) + len(habits)
done_items = completed_count + habit_done_count
progress = done_items / total_items if total_items else 0

st.divider()
st.subheader("Daily Progress ⭐")
st.progress(progress)
st.markdown(
    f'<div class="reward-card"><b>{done_items}/{total_items}</b> completed today. Keep at it 💗</div>',
    unsafe_allow_html=True
)