import cv2
from pytube import YouTube
import os
import pytesseract

VIDEO_FILENAME = "downloaded_video.mp4"

def download_youtube_video(youtube_link):
    if os.path.exists(VIDEO_FILENAME):
        print("Video already downloaded.")
        return VIDEO_FILENAME

    print("Downloading YouTube video...")
    yt = YouTube(youtube_link)
    video_stream = yt.streams.filter(file_extension='mp4').first()
    video_stream.download(filename=VIDEO_FILENAME)
    print("Video downloaded successfully.")
    return VIDEO_FILENAME


def detect_text_regions(frame):
    contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = 100
    text_regions = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            text_regions.append((x, y, w, h))
    return text_regions


def enhance_readability(frame):
    if len(frame.shape) == 3:  # Check if the frame is already a color image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame  # If already grayscale, no need to convert
    inverted = cv2.bitwise_not(gray)
    return inverted


def process_frame(frame):
    if len(frame.shape) == 3:  # Check if the frame is already a color image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame  # If already grayscale, no need to convert
    processed_frame = enhance_readability(frame)
    text_regions = detect_text_regions(processed_frame)
    for (x, y, w, h) in text_regions:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame, text_regions


def acquire_video_frames(youtube_link):
    video_file = download_youtube_video(youtube_link)
    cap = cv2.VideoCapture(video_file)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frames extraction completed.")
            break

        frame_count += 1
        processed_frame = enhance_readability(frame)
        processed_frame, text_regions = process_frame(processed_frame)
        frame_filename = f"frame_{frame_count}.jpg"
        cv2.imwrite(frame_filename, processed_frame)

        print(f"Frame {frame_count} processed and saved as {frame_filename}")

    cap.release()
    os.remove(video_file)
    print(f"All frames extracted, processed, and saved successfully. Total frames: {frame_count}")


def extract_text_from_frame(frame_filename):
    # Read the frame
    frame = cv2.imread(frame_filename)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform OCR using pytesseract
    extracted_text = pytesseract.image_to_string(gray)

    return extracted_text

if __name__ == "__main__":
    youtube_link = 'https://www.youtube.com/watch?v=StTuvR_l-OY'
    acquire_video_frames(youtube_link)

    for i in range(2300, 7625 + 1):
        frame_filename = f"frame_{i}.jpg"
        extracted_text = extract_text_from_frame(frame_filename)
        print(f"Text extracted from {frame_filename}: {extracted_text}")
