from ultralytics import YOLO
import cv2
import numpy as np
import util
import sys
sys.path.append('C:/Users/DELL/Desktop/ANPR/automatic-number-plate-recognition-python-yolov8-main/sort')
from sort import Sort

#from sort.tracker import SortTracker
from util import get_car, read_license_plate, write_csv


results = {}

mot_tracker = Sort()

# load models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('C:/Users/DELL/Desktop/ANPR/automatic-number-plate-recognition-python-yolov8-main/best.pt')

# load video
cap = cv2.VideoCapture('C:/Users/DELL/Desktop/ANPR/automatic-number-plate-recognition-python-yolov8-main/pexels_videos_2103099 (2160p) (1).mp4')

vehicles = [2, 3, 5, 7]

# read frames
frame_nmr = -1
ret = True
while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    if ret and frame_nmr <20:
        results[frame_nmr] = {}
        # detect vehicles
        detections = coco_model(frame)[0]
        #print(detections)
        detections_ = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicles:
                detections_.append([x1, y1, x2, y2, score])

        # track vehicles
        track_ids = mot_tracker.update(np.asarray(detections_))


        # detect license plates"""
        license_plates = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            print(license_plate)
            x1, y1, x2, y2, score, class_id = license_plate

            # assign license plate to car
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

            if car_id != -1:

                # crop license plate
                license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                # process license plate
                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                # read license plate number
                license_plate_text= read_license_plate(license_plate_crop_thresh)

                if license_plate_text is not None:
                    results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                  'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                    'text': license_plate_text,
                                                                    'bbox_score': score,}}
                                                                    #'text_score': license_plate_text_score}}

# write results
write_csv(results, 'C:/Users/DELL/Desktop/ANPR/test2.csv')