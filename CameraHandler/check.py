import cv2

def capture_image():
    # Attempt to open the camera (change the index to 0 or 1 based on your camera setup)
    camera_index = 0  # Try with 0 if 1 doesn't work
    cap = cv2.VideoCapture(camera_index)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open camera with index {camera_index}")
        return

    # Read a frame from the camera
    ret, frame = cap.read()
    if ret:
        # Save the frame as an image file
        image_filename = "captured_image.jpg"
        cv2.imwrite(image_filename, frame)
        print(f"Image captured and saved as {image_filename}")
    else:
        print("Error: Failed to capture image.")

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_image()
