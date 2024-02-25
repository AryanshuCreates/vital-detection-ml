To change video to your desired change the youtube url in code to the desired one.

Breakdown of the main functionalities:

Downloading YouTube Video: The function download_youtube_video(youtube_link) downloads the YouTube video using the pytube library.

Detecting Text Regions: The function detect_text_regions(frame) takes a frame as input, identifies text regions using contour detection, and returns the bounding boxes of these regions.

Enhancing Readability: The function enhance_readability(frame) improves the readability of the frame by converting it to grayscale and inverting it.

Processing Frame: The function process_frame(frame) applies the readability enhancement and text region detection to a frame, drawing rectangles around the detected text regions.

Acquiring Video Frames: The function acquire_video_frames(youtube_link) downloads the YouTube video, extracts frames from it, processes each frame, and saves the processed frames to disk.

Extracting Text from Frame: The function extract_text_from_frame(frame_filename) reads a frame from disk, converts it to grayscale, performs OCR using pytesseract, and returns the extracted text.
