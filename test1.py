import cv2
import mediapipe as mp
import numpy as np

# Initialize hand tracking module
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize canvas and color
canvas = np.zeros((480, 640, 3), dtype=np.uint8)
color = (0, 0, 0)  # Initial color is black

# Set up webcam
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# Initialize previous hand landmark position
prev_x, prev_y = 0, 0

with mp_hands.Hands(static_image_mode=False,
                    max_num_hands=1,
                    min_detection_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Failed to read video")
            break

        # Flip the image horizontally for a mirror effect
        image = cv2.flip(image, 1)

        # Convert image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process hand tracking
        results = hands.process(image_rgb)

        # Clear canvas if hand is not detected
        if results.multi_hand_landmarks is None:
            canvas = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Draw landmarks and lines on image
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get hand landmarks
                for i, landmark in enumerate(hand_landmarks.landmark):
                    x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])

                    # Draw circles at each landmark
                    cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

                    # Connect landmarks with lines using selected color
                    if i > 0:
                        cv2.line(canvas, (prev_x, prev_y), (x, y), tuple(reversed(color)), 5)
                    
                    # Update previous landmark position
                    prev_x, prev_y = x, y

        # Display canvas and video feed
        cv2.imshow("Canvas", canvas)
        cv2.imshow("Virtual Painter", image)

        # Handle key press events
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('r'):
            color = (0, 0, 255)  # Set color to red
        elif key == ord('g'):
            color = (0, 255, 0)  # Set color to green
        elif key == ord('b'):
            color = (255, 0, 0)  # Set color to blue

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
