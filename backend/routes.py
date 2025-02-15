# from flask import Flask, Response, jsonify, send_file # type: ignore
# import cv2 # type: ignore
# import time
# from inference_sdk import InferenceHTTPClient # type: ignore
# from flask_cors import CORS # type: ignore

# app = Flask(__name__)
# CORS(app)

# # Open webcam
# cap = cv2.VideoCapture(0)

# # Initialize Roboflow Client
# CLIENT = InferenceHTTPClient(
#     api_url="https://outline.roboflow.com",
#     api_key="bTMMcL56FvfEg04EEMji"
# )

# MODEL_ID = "taco-trash-annotations-in-context/16"
# IMAGE_FOLDER = "./saved_detections"
# image_list = []

# # Stability tracking
# stable_frames = {}
# required_stable_frames = 5
# previous_boxes = {}
# image_count = {}
# detected_timestamps = {}

# # Minimum size for detection
# MIN_WIDTH = 300
# MIN_HEIGHT = 300

# def generate_frames():
#     """ Capture frames, detect objects, and stream video with bounding boxes. """
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         result = CLIENT.infer(frame, model_id=MODEL_ID)

#         for obj in result.get("predictions", []):
#             x, y, w, h = int(obj["x"]), int(obj["y"]), int(obj["width"]), int(obj["height"])
#             class_name = obj["class"]

#             # Ignore small detections
#             if w < MIN_WIDTH or h < MIN_HEIGHT:
#                 continue

#             # Bounding box tracking
#             bbox = (x, y, w, h)
#             if class_name in previous_boxes:
#                 prev_x, prev_y, prev_w, prev_h = previous_boxes[class_name]
#                 box_shift = abs(x - prev_x) + abs(y - prev_y) + abs(w - prev_w) + abs(h - prev_h)
#                 if box_shift > 50:
#                     stable_frames[class_name] = 0

#             previous_boxes[class_name] = bbox
#             stable_frames[class_name] = stable_frames.get(class_name, 0) + 1

#             cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (0, 255, 0), 2)
#             cv2.putText(frame, f"{class_name} ({stable_frames[class_name]}/{required_stable_frames})",
#                         (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#             if stable_frames[class_name] >= required_stable_frames:
#                 timestamp = str(int(time.time()))
#                 crop_path = f"{IMAGE_FOLDER}/{timestamp}.jpg"
#                 cropped_img = frame[y - h // 2: y + h // 2, x - w // 2: x + w // 2]
#                 cv2.imwrite(crop_path, cropped_img)
#                 image_list.append(timestamp + ".jpg")

#                 print(f"✅ Object '{class_name}' detected and cropped! Saved as {timestamp}.jpg")

#                 detected_timestamps[class_name] = time.time()
#                 stable_frames[class_name] = 0  # Reset stability count

#         # Show "Object Detected!" message for 2 seconds
#         current_time = time.time()
#         for detected_class, timestamp in detected_timestamps.items():
#             if current_time - timestamp < 2:
#                 cv2.putText(frame, "✅ Object Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

#         # Encode frame as JPEG
#         _, buffer = cv2.imencode('.jpg', frame)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/detections', methods=['GET'])
# def list_detections():
#     return jsonify({"images": image_list})

# @app.route('/detections/<filename>')
# def get_detection(filename):
#     try:
#         return send_file(f"{IMAGE_FOLDER}/{filename}", mimetype='image/jpeg')
#     except:
#         return jsonify({"error": "Image not found"}), 404

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)

from flask import Flask, Response, request, jsonify, send_from_directory
import cv2
import time
import os
from flask_cors import CORS  # Enable CORS for React

app = Flask(__name__)
CORS(app)

# Initialize camera
cap = None  # Camera is initially off
camera_active = False

# Initialize Roboflow Client
from inference_sdk import InferenceHTTPClient
CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="bTMMcL56FvfEg04EEMji"
)

MODEL_ID = "taco-trash-annotations-in-context/16"

# Ensure images directory exists
IMAGE_FOLDER = "saved_detections"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

image_list = []  # Track saved images
stable_frames = {}
required_stable_frames = 5
previous_boxes = {}
detected_timestamps = {}

MIN_WIDTH = 300
MIN_HEIGHT = 300

def generate_frames():
    """ Capture frames, detect objects, and stream video with bounding boxes. """
    global cap, camera_active

    while camera_active:
        success, frame = cap.read()
        if not success:
            break

        result = CLIENT.infer(frame, model_id=MODEL_ID)

        for obj in result.get("predictions", []):
            x, y, w, h = int(obj["x"]), int(obj["y"]), int(obj["width"]), int(obj["height"])
            class_name = obj["class"]

            if w < MIN_WIDTH or h < MIN_HEIGHT:
                continue

            bbox = (x, y, w, h)
            if class_name in previous_boxes:
                prev_x, prev_y, prev_w, prev_h = previous_boxes[class_name]
                box_shift = abs(x - prev_x) + abs(y - prev_y) + abs(w - prev_w) + abs(h - prev_h)
                if box_shift > 50:
                    stable_frames[class_name] = 0

            previous_boxes[class_name] = bbox
            stable_frames[class_name] = stable_frames.get(class_name, 0) + 1

            cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name} ({stable_frames[class_name]}/{required_stable_frames})",
                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if stable_frames[class_name] >= required_stable_frames:
                timestamp = str(int(time.time())) + ".jpg"
                crop_path = os.path.join(IMAGE_FOLDER, timestamp)
                cropped_img = frame[y - h // 2: y + h // 2, x - w // 2: x + w // 2]
                cv2.imwrite(crop_path, cropped_img)

                if timestamp not in image_list:
                    image_list.append(timestamp)

                print(f"✅ Object '{class_name}' detected! Saved as {crop_path}")

                cv2.putText(frame, "✅ Object Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                detected_timestamps[class_name] = time.time()
                stable_frames[class_name] = 0  

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/start_camera')
def start_camera():
    """ Start the camera. """
    global cap, camera_active
    if not camera_active:
        cap = cv2.VideoCapture(0)  # Open the webcam
        camera_active = True
        print("✅ Camera started!")
        return jsonify({"status": "Camera started"}), 200
    return jsonify({"status": "Camera already running"}), 400

@app.route('/stop_camera')
def stop_camera():
    """ Stop the camera. """
    global cap, camera_active
    if camera_active:
        camera_active = False
        cap.release()
        print("🛑 Camera stopped!")
        return jsonify({"status": "Camera stopped"}), 200
    return jsonify({"status": "Camera is not running"}), 400

@app.route('/video_feed')
def video_feed():
    """ Streams live webcam feed with object detection. """
    if camera_active:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return jsonify({"status": "Camera is off"}), 400

@app.route('/detections', methods=['GET'])
def list_detections():
    """ Returns a list of saved images. """
    return jsonify({"images": image_list})

@app.route('/detections/<filename>')
def get_detection(filename):
    """ Serves a saved image from saved_detections directory. """
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)