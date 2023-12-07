"""
-------------------------------------------------
   @File Name:     utils.py
   @Author:        Siplusplusov (KIRISHIKI TEAM)
   @Date:          2023/11/16
   @Description: Settings file type, using for
                 yolo and detection
-------------------------------------------------
"""

from ultralytics import YOLO
import streamlit as st
import cv2
from PIL import Image
import tempfile
import PIL
import config

def _display_detected_frames(conf, model, st_frame, image):
    """
    Display the detected objects on a video frame using the YOLOv8 model.
    :param conf (float): Confidence threshold for object detection.
    :param model (YOLOv8): An instance of the `YOLOv8` class containing the YOLOv8 model.
    :param st_frame (Streamlit object): A Streamlit object to display the detected video.
    :param image (numpy array): A numpy array representing the video frame.
    :return: None
    """
    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720 * (9 / 16))))

    # Predict the objects in the image using YOLOv8 model
    res = model.predict(image, conf=conf)

    # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='С разметкой',
                   channels="BGR",
                   use_column_width=True
                   )


@st.cache_resource
def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model


def infer_uploaded_image(conf, model):
    """
    Execute inference for uploaded image
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """



    source_img = st.sidebar.file_uploader(
        label="Выберите изображение...",
        type=("jpg", "jpeg", "png", 'bmp', 'webp')
    )

    col1, col2 = st.columns(2)

    with col1:
        if source_img is None:
            default_image_path = str(config.DEFAULT_IMAGE,)
            default_image = PIL.Image.open(default_image_path)
            st.image(default_image_path, caption="Без разметки",
                     use_column_width=True)

        else:
            if source_img:
                uploaded_image = Image.open(source_img)
                # adding the uploaded image to the page with caption
                st.image(
                    image=source_img,
                    caption="Без разметки",
                    use_column_width=True
                )
        if source_img:
            btn = st.button("Определить✅")

    with col2:
        if source_img is None:
            default_detected_image_path = str(config.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(default_detected_image_path)
            st.image(default_detected_image_path, caption='С разметкой',use_column_width=True)
        else:
            if source_img:
                if btn:
                    with st.spinner("Начинаем..."):
                        res = model.predict(uploaded_image,
                                        conf=conf)
                    boxes = res[0].boxes
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(res_plotted,
                     caption="С разметкой",
                     use_column_width=True)

                    try:
                        with st.expander("Результаты"):
                            for box in boxes:
                                st.write(box.xywh)
                    except Exception as ex:
                        st.write("Картинка не выгружена!")
                        st.write(ex)


def infer_uploaded_video(conf, model):
    """
    Execute inference for uploaded video
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """
    source_video = st.sidebar.file_uploader(
        label="Выберите файл с видео..."
    )

    if source_video:
        st.video(source_video)

    if source_video:
        if st.button("Определить✅"):
            with st.spinner("Начинаем..."):
                try:
                    tfile = tempfile.NamedTemporaryFile()
                    tfile.write(source_video.read())
                    vid_cap = cv2.VideoCapture(
                        tfile.name)
                    st_frame = st.empty()
                    while (vid_cap.isOpened()):
                        success, image = vid_cap.read()
                        if success:
                            _display_detected_frames(conf,
                                                     model,
                                                     st_frame,
                                                     image
                                                     )
                        else:
                            vid_cap.release()
                            break
                except Exception as e:
                    st.error(f"Ошибка в загрузке видео: {e}")


def infer_uploaded_webcam(conf, model):
    """
    Execute inference for webcam.
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """
    try:
        flag = st.button(
            label="Остановить/начать"
        )
        vid_cap = cv2.VideoCapture(0)  # local camera
        st_frame = st.empty()
        while not flag:
            success, image = vid_cap.read()
            if success:
                _display_detected_frames(
                    conf,
                    model,
                    st_frame,
                    image
                )
            else:
                vid_cap.release()
                break
    except Exception as e:
        st.error(f"Ошибка в загрузке видео: {str(e)}")
