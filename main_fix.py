import cv2
import mediapipe as mp
import math
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# Initialize audio using scalar method (0.0 to 1.0 scale)
print("Initializing audio control...")
try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    print("✓ Audio control initialized!")
    WINDOWS = True
except Exception as e:
    print(f"✗ Audio failed: {e}")
    volume = None
    WINDOWS = False

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

def get_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

print("\n" + "="*50)
print("Hand Gesture Volume Control")
print("="*50)
print("Instructions:")
print("- Pinch = Lower volume | Spread = Raise volume")
print("- Press 'q' to quit")
print("="*50 + "\n")

while True:
    success, img = cap.read()
    if not success:
        break
    
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            h, w, c = img.shape
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
            
            cv2.circle(img, (thumb_x, thumb_y), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (index_x, index_y), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 255), 3)
            
            distance = get_distance((thumb_x, thumb_y), (index_x, index_y))
            
            # Map to 0.0-1.0 scale (scalar method - more reliable)
            vol_scalar = np.interp(distance, [30, 250], [0.0, 1.0])
            vol_percent = int(vol_scalar * 100)
            
            # Use SetMasterVolumeLevelScalar instead
            if WINDOWS and volume:
                try:
                    volume.SetMasterVolumeLevelScalar(vol_scalar, None)
                except Exception as e:
                    print(f"Error: {e}")
                    WINDOWS = False
            
            # Draw volume bar
            vol_bar = int(np.interp(vol_percent, [0, 100], [400, 150]))
            cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(img, (50, vol_bar), (85, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{vol_percent}%', (40, 450), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            
            mid_x, mid_y = (thumb_x + index_x) // 2, (thumb_y + index_y) // 2
            color = (0, 0, 255) if distance < 50 else (255, 0, 255)
            cv2.circle(img, (mid_x, mid_y), 10, color, cv2.FILLED)
    
    cv2.putText(img, 'Hand Gesture Volume Control', (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    status_color = (0, 255, 0) if WINDOWS else (0, 0, 255)
    status_text = "Audio: ACTIVE" if WINDOWS else "Audio: INACTIVE"
    cv2.putText(img, status_text, (10, 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
    
    cv2.imshow("Hand Gesture Volume Control", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
print("\nGoodbye!")