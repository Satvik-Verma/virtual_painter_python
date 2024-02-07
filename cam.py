import cv2

def open_camera():
    # Open the camera
    cap = cv2.VideoCapture(1)  # 0 for the default camera, you can try changing the value if you have multiple cameras
    
    while True:
        # Read the current frame from the camera
        ret, frame = cap.read()
        
        if not ret:
            # If frame is not valid, continue to the next iteration of the loop
            continue
        
        # Display the frame in a window called "Camera Feed"
        cv2.imshow("Camera Feed", frame)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

# Call the function to open the camera
open_camera()
