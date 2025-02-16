from flask import Flask, Response, request, jsonify, send_from_directory, stream_with_context  # type: ignore
import cv2  # type: ignore
import time
import os
import json
from flask_cors import CORS  # type: ignore  # Enable CORS for React
from inference_sdk import InferenceHTTPClient  # type: ignore
import threading
import queue
from geminiOutput import getImageData  # synchronous API call
from dotenv import load_dotenv
import asyncio

app = Flask(__name__)
CORS(app)

cap = None
camera_active = False
frame_thread = None
frame_queue = queue.Queue(maxsize=3)

load_dotenv()
key = os.getenv("VISION")

# Initialize Roboflow Client
CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key=key
)

MODEL_ID = "taco-trash-annotations-in-context/16"

IMAGE_FOLDER = "saved_detections"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

image_list = []
stable_frames = {}
required_stable_frames = 5
previous_boxes = {}
detected_timestamps = {}

MIN_WIDTH = 200
MIN_HEIGHT = 200

last_detection_time = 0  
DETECTION_DISPLAY_DURATION = 3

api_call_scheduled = False

api_results = []

sse_queue = queue.Queue()

api_loop = asyncio.new_event_loop()

def run_api_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

api_thread = threading.Thread(target=run_api_loop, args=(api_loop,), daemon=True)
api_thread.start()

async def process_get_image_data(crop_path):
    loop = asyncio.get_running_loop()
    print(f"[DEBUG] In process_get_image_data for crop_path: {crop_path}")
    try:
        answer = await loop.run_in_executor(None, getImageData, crop_path)
    except Exception as e:
        print(f"[ERROR] Exception during getImageData: {e}")
        answer = None
    if answer is None:
        print("[DEBUG] getImageData returned None.")
    else:
        print(f"[DEBUG] getImageData returned: {answer}")
    api_results.append(answer)
    sse_queue.put(answer)
    print("API response received and queued:", answer)

async def frame_worker():
    global cap, camera_active, last_detection_time, api_call_scheduled

    crop_path = None
    while camera_active:
        detection_occurred = False
        current_time = time.time()
        success, frame = cap.read()
        if not success:
            continue

        result = CLIENT.infer(frame, model_id=MODEL_ID)

        best_obj = None
        best_area = 0
        for obj in result.get("predictions", []):
            x = int(obj["x"])
            y = int(obj["y"])
            w = int(obj["width"])
            h = int(obj["height"])
            if w < MIN_WIDTH or h < MIN_HEIGHT:
                continue
            area = w * h
            if area > best_area:
                best_area = area
                best_obj = obj

        if best_obj is not None:
            x = int(best_obj["x"])
            y = int(best_obj["y"])
            w = int(best_obj["width"])
            h = int(best_obj["height"])
            class_name = best_obj["class"]

            bbox = (x, y, w, h)
            if class_name in previous_boxes:
                prev_x, prev_y, prev_w, prev_h = previous_boxes[class_name]
                box_shift = abs(x - prev_x) + abs(y - prev_y) + abs(w - prev_w) + abs(h - prev_h)
                if box_shift > 50:
                    stable_frames[class_name] = 0

            previous_boxes[class_name] = bbox
            stable_frames[class_name] = stable_frames.get(class_name, 0) + 1

            half_w, half_h = w // 2, h // 2
            cv2.rectangle(frame, (x - half_w, y - half_h), (x + half_w, y + half_h), (0, 255, 0), 2)
            cv2.putText(frame, f"({stable_frames[class_name]}/{required_stable_frames})",
                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)

            if stable_frames[class_name] >= required_stable_frames:
                timestamp = f"{int(current_time)}.jpg"
                crop_path = os.path.join(IMAGE_FOLDER, timestamp)
                cropped_img = frame[y - half_h: y + half_h, x - half_w: x + half_w]
                cv2.imwrite(crop_path, cropped_img)

                if timestamp not in image_list:
                    image_list.append(timestamp)

                print(f"[DEBUG] Object '{class_name}' detected! Saved as {crop_path}")

                last_detection_time = current_time
                stable_frames[class_name] = 0

                detection_occurred = True

        if current_time - last_detection_time < DETECTION_DISPLAY_DURATION:
            text = "OBJECT DETECTED!"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.5
            thickness = 3
            text_size, baseline = cv2.getTextSize(text, font, font_scale, thickness)
            text_x = int((frame.shape[1] - text_size[0]) / 2)
            text_y = int(text_size[1] + 20)

            cv2.rectangle(frame,
                          (text_x - 10, text_y - text_size[1] - 10),
                          (text_x + text_size[0] + 10, text_y + 10),
                          (0, 0, 0), -1)
            cv2.putText(frame, text, (text_x, text_y),
                        font, font_scale, (0, 0, 255), thickness, cv2.LINE_AA)
            
            if crop_path and not api_call_scheduled:
                try:
                    asyncio.run_coroutine_threadsafe(process_get_image_data(crop_path), api_loop)
                    print("[DEBUG] API call scheduled for crop_path:", crop_path)
                    api_call_scheduled = True
                except Exception as e:
                    print("[ERROR] Could not schedule API call:", e)
        else:
            api_call_scheduled = False

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()

        try:
            frame_queue.put(frame_bytes, block=False)
        except queue.Full:
            try:
                frame_queue.get_nowait()
            except queue.Empty:
                pass
            frame_queue.put(frame_bytes)

        if detection_occurred:
            freeze_until = time.time() + 2
            while time.time() < freeze_until and camera_active:
                try:
                    frame_queue.put(frame_bytes, block=False)
                except queue.Full:
                    try:
                        frame_queue.get_nowait()
                    except queue.Empty:
                        pass
                    frame_queue.put(frame_bytes)
                time.sleep(0.1)

def generate_frames():
    """Flask generator: yields processed frames from the queue for the video feed."""
    while camera_active or not frame_queue.empty():
        try:
            frame_bytes = frame_queue.get(timeout=0.1)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except queue.Empty:
            continue

@app.route('/start_camera')
def start_camera():
    global cap, camera_active, frame_thread
    if not camera_active:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        camera_active = True

        frame_thread = threading.Thread(target=lambda: asyncio.run(frame_worker()), daemon=True)
        frame_thread.start()

        print("✅ Camera started!")
        return jsonify({"status": "Camera started"}), 200
    return jsonify({"status": "Camera already running"}), 400

@app.route('/stop_camera')
def stop_camera():
    global cap, camera_active, frame_thread
    if camera_active:
        camera_active = False
        if frame_thread is not None:
            frame_thread.join(timeout=2)
        cap.release()
        sse_queue.put({"status": "stop"})
        print("🛑 Camera stopped!")
        return jsonify({"status": "Camera stopped"}), 200
    return jsonify({"status": "Camera is not running"}), 400

@app.route('/video_feed')
def video_feed():
    if camera_active:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return jsonify({"status": "Camera is off"}), 400

@app.route('/detections', methods=['GET'])
def list_detections():
    return jsonify({"images": image_list})

@app.route('/detections/<filename>')
def get_detection(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/api_results', methods=['GET'])
def get_api_results():
    return jsonify({"api_results": api_results})

@app.route('/stream_api')
def stream_api():
    def event_stream():
        yield "data: communication response start\n\n"
        while True:
            try:
                message = sse_queue.get(timeout=0.5)
                yield "data: " + json.dumps(message) + "\n\n"
                if isinstance(message, dict) and message.get("status") == "stop":
                    break
            except queue.Empty:
                print("pn")
    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)