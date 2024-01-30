import cv2

def find_camera_index():
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"camera index {i} is available.")
            cap.release()
        else:
            print(f"camera index {i} isnt there ")

if __name__ == "__main__":
    find_camera_index()
