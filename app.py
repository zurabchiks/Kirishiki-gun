"""
-------------------------------------------------
   @File Name:     app.py
   @Author:        Siplusplusov (KIRISHIKI TEAM)
   @Date:          2023/11/16
   @Description: Streamlit app file
-------------------------------------------------
"""

from pathlib import Path
from typing import Any

from PIL import Image
import streamlit as st

import config
from ultralytics import YOLO
from utils import load_model, infer_uploaded_image, infer_uploaded_video, infer_uploaded_webcam

# setting page layout
st.set_page_config(
    page_title="Распознвание оружия от KIRISHIKI",
    page_icon="🔫",
    layout="wide",
    initial_sidebar_state="expanded"
    )

# main page heading
st.title("Распознавание оружия от KIRISHIKI")

# sidebar
st.sidebar.header("⚙️Настройка модели")

# model options
task_type = st.sidebar.selectbox(
    "Выберите задание",
    ["Детекция","Сегментация"],
)

model_type = None
if task_type == "Детекция":
    model_type = st.sidebar.selectbox(
        "Модель",
        config.DETECTION_MODEL_LIST
    )
elif task_type == "Сегментация":
    model_type = st.sidebar.selectbox(
        "Модель",
        config.SEGMENT_MODEL_LIST
    )
else:
    st.error("😔К сожалению, только функция ДЕТЕКЦИИ доступна")

confidence = float(st.sidebar.slider(
    "📌Точность", 30, 100, 50)) / 100

model_path = ""
if model_type:

    if task_type == "Детекция":
        model_path = Path(config.DETECTION_MODEL_DIR, str(model_type))
    if task_type == "Сегментация":
        model_path = Path(config.SEGMENT_MODEL_DIR, str(model_type))
else:
    st.error("Выберите модель в меню")

model = load_model(model_path)

# load pretrained DL model
try:
    model = load_model(model_path)
except Exception as e:
    st.error(f"Что-то поломалось, проверьте директорию с моделью: {model_path}")

# image/video options
st.sidebar.header("📥Загрузка данных")
source_selectbox = st.sidebar.selectbox(
    "Источник",
    config.SOURCES_LIST
)

source_img = None
if source_selectbox == config.SOURCES_LIST[0]: # Image
    infer_uploaded_image(confidence, model)
elif source_selectbox == config.SOURCES_LIST[1]: # Video
    infer_uploaded_video(confidence, model)
elif source_selectbox == config.SOURCES_LIST[2]: # Webcam
    infer_uploaded_webcam(confidence, model)
else:
    st.error("Currently only 'Image' and 'Video' source are implemented")