import face_recognition
import cv2
import numpy as np
import os
import time
from PIL import Image, UnidentifiedImageError  # Import Pillow and its specific error

# --- Configuration ---
# Directory for images of known faces
KNOWN_FACES_DIR = 'bekannte_gesichter'
# Directory for videos to be analyzed
VIDEOS_DIR = 'videos'
# Tolerance: How close face encodings must be to be considered a match.
# Smaller value = stricter (fewer false positives, but possibly fewer true positives).
# Larger value = more tolerant (more true positives, but possibly more false positives).
TOLERANCE = 0.6
# Frame Skip: Skip X frames to speed up processing.
# At 25 FPS, FRAME_SKIP=25 means approximately 1 frame per second is analyzed.
FRAME_SKIP = 25
# Output file name for the detection log
OUTPUT_LOG_FILE = 'face_detection_log.txt'

# --- Learn Known Faces ---
print("Learning known faces...")
known_face_encodings = []
known_face_names = []

# Iterate through all subdirectories in the known faces directory
# Each subdirectory represents a person
for name in os.listdir(KNOWN_FACES_DIR):
    person_dir = os.path.join(KNOWN_FACES_DIR, name)

    # Skip if it's not a directory (e.g., .DS_Store on macOS)
    if not os.path.isdir(person_dir):
        continue

    # Load all images in this person's folder
    for filename in os.listdir(person_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Case-insensitive file extension check
            image_path = os.path.join(person_dir, filename)
            loaded_image_rgb = None  # This will hold the image in the final RGB format

            try:
                # Attempt to load image using OpenCV, including alpha channel if present
                # IMREAD_UNCHANGED ensures all channels (e.g., 4 for RGBA) are loaded
                cv_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

                if cv_image is None:
                    print(
                        f"Error: OpenCV could not load image file {image_path}. It might be corrupted or an unsupported format.")
                    continue  # Skip to next file if loading fails

                # Ensure image data type is 8-bit unsigned integer (np.uint8)
                if cv_image.dtype != np.uint8:
                    cv_image = cv_image.astype(np.uint8)
                    print(f"Converted image {image_path} data type to np.uint8.")

                # Handle different channel counts and convert to RGB (3 channels)
                if len(cv_image.shape) == 3:  # Color image (could be BGR, RGB, BGRA, RGBA)
                    if cv_image.shape[2] == 4:  # BGRA or RGBA (4 channels, e.g., with alpha)
                        # Convert BGRA to BGR, dropping the alpha channel
                        loaded_image_bgr = cv2.cvtColor(cv_image, cv2.COLOR_BGRA2BGR)
                        print(f"Converted 4-channel image {image_path} to 3-channel BGR (dropping alpha).")
                    elif cv_image.shape[2] == 3:  # BGR (standard OpenCV color image)
                        loaded_image_bgr = cv_image
                        # print(f"Image {image_path} is already 3-channel BGR.")
                    else:
                        print(
                            f"Warning: Image {image_path} has an unsupported number of channels ({cv_image.shape[2]}). Skipping.")
                        continue  # Skip to next file
                elif len(cv_image.shape) == 2:  # Grayscale image (1 channel)
                    # Convert grayscale to 3-channel BGR by duplicating the channel
                    loaded_image_bgr = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2BGR)
                    print(f"Converted grayscale image {image_path} to 3-channel BGR.")
                else:
                    print(f"Warning: Image {image_path} has an unexpected shape {cv_image.shape}. Skipping.")
                    continue  # Skip to next file

                # Finally, convert from BGR (OpenCV default) to RGB (face_recognition expectation)
                loaded_image_rgb = cv2.cvtColor(loaded_image_bgr, cv2.COLOR_BGR2RGB)
                print(f"Successfully loaded and converted image {image_path} to RGB.")

                # --- Critical Step: Ensure array is contiguous and correct dtype for dlib ---
                # dlib often expects contiguous arrays with specific data types.
                # This ensures the array is C-contiguous and has the correct dtype.
                final_image_for_dlib = np.ascontiguousarray(loaded_image_rgb, dtype=np.uint8)
                print(
                    f"Image {image_path} array shape for dlib: {final_image_for_dlib.shape}, dtype: {final_image_for_dlib.dtype}")

                # Generate face encodings for the image
                encoding = face_recognition.face_encodings(final_image_for_dlib)
                if encoding:
                    known_face_encodings.append(encoding[0])
                    known_face_names.append(name)  # The folder name is the person's name
                else:
                    print(
                        f"Warning: No face found in image: {image_path}. Please check the image (e.g., face is clear, frontal).")

            except Exception as e:
                print(f"Error loading/processing image {image_path}: {e}")

if not known_face_encodings:
    print("Error: No known faces found to learn. Please place images in 'bekannte_gesichter/<PersonName>/'.")
    exit()

print(f"Learned faces: {known_face_names}")

# --- Process Videos ---
print("\nStarting video analysis...")
# Dictionary to store results: {Video_Filename: [{person: Name, timestamp: Timestamp}]}
detection_log = {}

for video_file in os.listdir(VIDEOS_DIR):
    # Ensure it's a supported video file
    if not video_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
        continue

    video_path = os.path.join(VIDEOS_DIR, video_file)
    print(f"\nAnalyzing video: {video_file}")

    # Open the video with OpenCV
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video: {video_file}")
        continue

    # Get video metadata
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"  FPS: {fps:.2f}, Total Frames: {total_frames}")

    current_frame_number = 0
    while True:
        # Read the next frame
        ret, frame = cap.read()
        if not ret:
            break  # End of video reached

        # Skip frames to speed up processing
        if current_frame_number % FRAME_SKIP != 0:
            current_frame_number += 1
            continue

        # Convert the frame from BGR (OpenCV) to RGB (face_recognition)
        rgb_frame = frame[:, :, ::-1]

        # Find all faces and their encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            # Compare the found face with the known faces
            # 'compare_faces' returns a list of booleans
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, TOLERANCE)
            name = "Unknown"

            # Find the index of the best matching known face
            # (the one with the smallest "distance" to the currently found face)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            # Check if face_distances is not empty to avoid IndexError
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)

                # If the best match is actually a hit (based on TOLERANCE)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            # If a known face was found, log it
            if name != "Unknown":
                timestamp_seconds = current_frame_number / fps
                minutes = int(timestamp_seconds // 60)
                seconds = int(timestamp_seconds % 60)
                milliseconds = int((timestamp_seconds - int(timestamp_seconds)) * 1000)

                time_str = f"{minutes:02}:{seconds:02}:{milliseconds:03}"

                if video_file not in detection_log:
                    detection_log[video_file] = []

                # Simple logic to avoid logging every single frame,
                # but rather the first occurrence or after a certain time span.
                # Here: only log if this person hasn't been seen in the last 5 seconds.
                found_recently = False
                for entry in detection_log[video_file]:
                    # Check if person appears in the same video and timestamp is close
                    if entry['person'] == name and abs(entry['frame'] - current_frame_number) < fps * 5:
                        found_recently = True
                        break

                if not found_recently:
                    detection_log[video_file].append(
                        {'person': name, 'timestamp': time_str, 'frame': current_frame_number})
                    print(f"  Found: {name} in Frame {current_frame_number} (Time: {time_str})")

        current_frame_number += 1

    cap.release()  # Close the video file
    print(f"  Video {video_file} analysis complete.")

# --- Output Results to Console and File ---
print("\n--- Analysis Results ---")

# Get the full path for the output file
full_output_path = os.path.abspath(OUTPUT_LOG_FILE)
print(f"Attempting to write results to: {full_output_path}")

try:
    # Open the output file in write mode ('w'). It will be created or overwritten.
    with open(OUTPUT_LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("--- Face Detection Analysis Results ---\n")
        f.write(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        if not detection_log:
            print("No known faces found in the videos.\n")  # Added newline for file
            f.write("No known faces found in the videos.\n")
        else:
            for video, entries in detection_log.items():
                print(f"\nVideo: {video}")
                f.write(f"\nVideo: {video}\n")
                if not entries:
                    print("  No known faces found.")
                    f.write("  No known faces found.\n")
                else:
                    # Sort entries by frame number (i.e., chronologically)
                    entries_sorted = sorted(entries, key=lambda x: x['frame'])
                    for entry in entries_sorted:
                        log_line = f"  - Person: {entry['person']}, Time: {entry['timestamp']}\n"
                        print(log_line.strip())  # strip() to remove newline for console
                        f.write(log_line)
    print(f"\nAnalysis complete. Results successfully saved to '{full_output_path}'.")
except IOError as e:
    print(
        f"Error: Could not write to output file '{full_output_path}'. Please check permissions or disk space. Error: {e}")
