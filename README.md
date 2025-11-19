# Hand Gesture Volume Control

Control your system volume using hand gestures detected through your webcam.

## Features
- Real-time hand tracking using MediaPipe
- Control volume by pinching/spreading thumb and index finger
- Visual feedback with volume bar and percentage

## Requirements
- Python 3.7+
- Webcam
- Windows OS (for volume control)

## Installation

1. Clone or download this repository
2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
.\venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the program:
```bash
python main_fixed.py
```

**Controls:**
- **Pinch** thumb and index finger together → Lower volume
- **Spread** thumb and index finger apart → Raise volume
- Press **'q'** to quit

## Troubleshooting

If audio control doesn't work:
1. Ensure `pycaw` version is `20230407`: `pip install pycaw==20230407`
2. Check that your audio drivers are working
3. Try running as Administrator

## Demo
The program displays:
- Live webcam feed with hand tracking
- Green volume bar on the left
- Volume percentage
- Audio status indicator

---

**Note:** This project currently supports Windows only. For macOS/Linux, modify the audio control section accordingly.
