from histogram_face import FaceRecognition
from GUI import GUI
import py2exe
if __name__ == "__main__":
    face_recognition = FaceRecognition(
        classifier_path="haarcascades\\haarcascade_frontalface_default.xml",
        threshold=80
    )
    gui = GUI()
    gui.add_label("請選擇功能")
    gui.add_button(text="新增人臉", command_func=face_recognition.create_origin_face)
    gui.add_button(text="臉部辨識", command_func=face_recognition.verify_process)
    gui.add_button(text="臉部偵測", command_func=face_recognition.detect_face)
    gui.add_button(text="新增表情", command_func=face_recognition.add_new_emotion)
    gui.add_button(text="困惑情緒辨識", command_func=face_recognition.detect_confused_emotion)
    gui.run()
    # face_recognition.catch_face(path="origin.jpg",output_filename="origin")