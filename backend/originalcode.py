import cv2
import time
from inference_sdk import InferenceHTTPClient

# Initialize the Inference Client with your API key
CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="bTMMcL56FvfEg04EEMji"  # Replace with your actual Roboflow API key
)

# Model details
MODEL_ID = "taco-trash-annotations-in-context/16"

# Open webcam
cap = cv2.VideoCapture(0)

# Stability tracking
stable_frames = {}  # Track the number of frames an object has been detected
required_stable_frames = 5  # Number of stable frames before cropping
previous_boxes = {}  # Track bounding box positions to ensure stability
image_count = {}  # Track number of images saved per object
detected_timestamps = {}  # Store timestamps for when an object is detected

# Minimum size for objects (adjust as needed)
MIN_WIDTH = 300  # Minimum width of detected object
MIN_HEIGHT = 300  # Minimum height of detected object

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Save the current frame to a temporary file
    temp_filename = "temp_frame.jpg"
    cv2.imwrite(temp_filename, frame)

    # Run inference on the frame
    result = CLIENT.infer(temp_filename, model_id=MODEL_ID)

    for obj in result.get("predictions", []):
        x, y, w, h = int(obj["x"]), int(obj["y"]), int(obj["width"]), int(obj["height"])
        class_name = obj["class"]

        # Ignore small objects BEFORE processing (NO BOUNDING BOX DRAWN)
        if w < MIN_WIDTH or h < MIN_HEIGHT:
            continue  # Skip small detections entirely (no box drawn, no stability tracking)

        # Get the bounding box
        bbox = (x, y, w, h)

        # Check if the object is already being tracked
        if class_name in previous_boxes:
            prev_x, prev_y, prev_w, prev_h = previous_boxes[class_name]
            box_shift = abs(x - prev_x) + abs(y - prev_y) + abs(w - prev_w) + abs(h - prev_h)

            # If the bounding box shifts too much, reset the stability count
            if box_shift > 50:  # Threshold for movement
                stable_frames[class_name] = 0

        # Update bounding box history
        previous_boxes[class_name] = bbox

        # Increment stability counter
        if class_name not in stable_frames:
            stable_frames[class_name] = 1
        else:
            stable_frames[class_name] += 1

        # Draw bounding box only if the object meets the size requirement
        if w >= MIN_WIDTH and h >= MIN_HEIGHT:  # Double-check before drawing
            cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name} ({stable_frames[class_name]}/{required_stable_frames} -- W:{w} H:{h})",
                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)        

        # If object is stable for required frames, crop and save
        if stable_frames[class_name] >= required_stable_frames:
            # Track count per class to prevent overwriting
            if class_name not in image_count:
                image_count[class_name] = 1
            else:
                image_count[class_name] += 1

            # Generate unique filename
            timestamp = int(time.time())  # Get current timestamp
            crop_filename = f"cropped_{class_name}_{image_count[class_name]}_{timestamp}.jpg"

            cropped_img = frame[y - h // 2: y + h // 2, x - w // 2: x + w // 2]
            cv2.imwrite(crop_filename, cropped_img)

            print(f"✅ Object '{class_name}' detected and cropped! Saved as {crop_filename}")

            # Store the detection timestamp
            detected_timestamps[class_name] = time.time()

            # Reset stability count to allow capturing again
            stable_frames[class_name] = 0

    # Show "Object Detected!" message for 2 seconds after detection
    current_time = time.time()
    for detected_class, timestamp in detected_timestamps.items():
        if current_time - timestamp < 2:
            cv2.putText(frame, f"✅ Object Detected!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # Show the frame with detections
    cv2.imshow("Live Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()