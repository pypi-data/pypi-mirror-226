import cv2
import logging
from datetime import datetime
from pathlib import Path
from ultralytics import YOLO
import os
import torch
import time
import uuid

class VideoProcessor:

    def __init__(self, detection_model_path, classification_model_path, video_path, 
                 save_video=False, detection_save_crops = False, classification_save_crops = False, detection_conf = 0.3,
                 classification_conf = 0.3, detection_image_size = 1280, classification_image_size = 128, detection_classes = None, 
                 classification_classes = None):
        
        self.detection_model = YOLO(detection_model_path)
        self.print_detection_model = torch.load(detection_model_path)
        self.video_path = video_path
        self.log_path = "logs"
        self.save_video = save_video
        self.detection_save_crops = detection_save_crops
        self.classification_save_crops = classification_save_crops
        self.detection_conf = detection_conf
        self.classification_image_size = classification_image_size 
        self.classification_conf = classification_conf
        self.detection_image_size = detection_image_size
        self.detection_classes = detection_classes
        self.classification_classes = classification_classes
        self.current_time = time.time()
        self.setup_logging()

        if classification_model_path and os.path.isfile(classification_model_path):
            self.classification_model = YOLO(classification_model_path)
            self.print_classification_model = torch.load(classification_model_path)
        else:
            self.classification_model = None
            self.print_classification_model = None

    def setup_logging(self):
        log_folder = Path(self.log_path)
        log_folder.mkdir(exist_ok=True)
        log_file = log_folder / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(levelname)s: %(message)s",
            handlers=[
                logging.FileHandler(log_file)
            ]
        )

    def crop_with_padding(self, frame, xmin, ymin, xmax, ymax, desired_aspect_ratio=1.0, min_width=100, min_height=100):
        frame_height, frame_width = frame.shape[:2]
        bbox_width = xmax - xmin
        bbox_height = ymax - ymin
        if bbox_width >= bbox_height:
            target_width = min_width
            target_height = int(min_width / desired_aspect_ratio)
        else:
            target_height = min_height
            target_width = int(min_height * desired_aspect_ratio)
        horizontal_padding = max((target_width - bbox_width) // 2, 0)
        vertical_padding = max((target_height - bbox_height) // 2, 0)

        padded_xmin = max(xmin - horizontal_padding, 0)
        padded_ymin = max(ymin - vertical_padding, 0)
        padded_xmax = min(xmax + horizontal_padding, frame_width)
        padded_ymax = min(ymax + vertical_padding, frame_height)
        padded_image = frame[padded_ymin:padded_ymax, padded_xmin:padded_xmax]

        return padded_image
    
    def draw_text_with_rectangle(self, text, x, y, font=cv2.FONT_HERSHEY_SIMPLEX, scale=0.6, thickness=2):
        text_width, _ = cv2.getTextSize(text, font, scale, thickness)
        rect_width = text_width[0] + 10
        rect_height = 30
        rect_x2 = x - 10
        rect_y2 = y - 10
        rect_x1 = rect_x2 - rect_width
        rect_y1 = rect_y2 - rect_height

        return rect_x1, rect_y1, rect_x2, rect_y2

    def process_video(self):
        if os.path.isfile(self.video_path):
            video_paths = [self.video_path]
        elif os.path.isdir(self.video_path):
            video_paths = [
                os.path.join(self.video_path, filename)
                for filename in os.listdir(self.video_path)
                if filename.endswith((".mp4", ".avi", ".MP4", ".MOV"))
            ]
        elif self.video_path.startswith("rtsp://"):
            video_paths = [self.video_path]
        else:
            logging.error(f"Invalid video path: {self.video_path}")
            return
        logging.info(f"Detection Model: {self.print_detection_model['model']}")
        
        if self.classification_model:
            logging.info(f"Classification Model: {self.print_classification_model['model']}")

        for video_path in video_paths:
            cap = cv2.VideoCapture(video_path)
            frame_count = 0

            if self.save_video:
                video_output_folder = "saved_video"
                os.makedirs(video_output_folder, exist_ok=True)
                video_name = os.path.splitext(os.path.basename(video_path))[0]
                video_output_path = os.path.join(video_output_folder, f"{video_name}_{self.current_time}.avi")
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                out = cv2.VideoWriter(video_output_path, fourcc, 20.0, (frame_width, frame_height))

            while True:
                start_time = cv2.getTickCount()
                ret, frame = cap.read()
                try:
                    frame2 = frame.copy()
                except:
                    break
                if not ret:
                    break
                try:
                    detection_results = self.detection_model.predict(frame, conf=self.detection_conf, verbose=False,
                                                                    imgsz=self.detection_image_size,
                                                                    classes=self.detection_classes)
                    boxes = detection_results[0].boxes.xyxy.cpu().tolist()
                    classes = detection_results[0].boxes.cls.cpu().tolist()
                    scores = detection_results[0].boxes.conf.cpu().tolist()

                    detection_names = self.detection_model.names
                    for i in range(len(boxes)):
                        box = boxes[i]
                        cls = classes[i]
                        score = scores[i]

                        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])

                        detection_roi = self.crop_with_padding(frame2, x1, y1, x2, y2, desired_aspect_ratio=1.0, min_width=100,
                                                            min_height=100)

                        if self.detection_save_crops:
                            detection_class = detection_names[cls]
                            detection_crops_folder = "detection_crops"
                            os.makedirs(detection_crops_folder, exist_ok=True)
                            detection_crop_folder = os.path.join(detection_crops_folder, detection_class)
                            os.makedirs(detection_crop_folder, exist_ok=True)

                            unique_id = str(uuid.uuid4().hex)
                            detection_crop_path = os.path.join(detection_crop_folder, f"detection_crop_{frame_count}_{self.current_time}_{unique_id}.jpg")
                            cv2.imwrite(detection_crop_path, detection_roi)

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                        if self.classification_model:
                            classification_roi = self.crop_with_padding(frame2, x1, y1, x2, y2, desired_aspect_ratio=1.0,
                                                                    min_width=100, min_height=100)

                            try:
                                classification_results = self.classification_model.predict(classification_roi,
                                                                                        conf=self.classification_conf,
                                                                                        verbose=False,
                                                                                        imgsz=self.classification_image_size,
                                                                                        classes=self.classification_classes)

                                classification_classes = list(classification_results[0].names.values())
                                probabilities = classification_results[0].probs.top1
                                max_prob_class = classification_classes[probabilities]

                                if self.classification_save_crops:
                                    classification_crops_folder = "classification_crops"
                                    os.makedirs(classification_crops_folder, exist_ok=True)
                                    classification_class_folder = os.path.join(classification_crops_folder, max_prob_class)
                                    os.makedirs(classification_class_folder, exist_ok=True)
                                    classification_crop_path = os.path.join(classification_class_folder, f"classification_crop_{frame_count}_{self.current_time}_{unique_id}.jpg")
                                    cv2.imwrite(classification_crop_path, classification_roi)

                                rect_x1_cls, rect_y1_cls, rect_x2_cls, rect_y2_cls = self.draw_text_with_rectangle(
                                    max_prob_class, x2, y1)
                                cv2.rectangle(frame, (rect_x1_cls, rect_y1_cls), (rect_x2_cls, rect_y2_cls), (255, 0, 255), -1)
                                cv2.putText(frame, f'{max_prob_class} {score:.2f}', (rect_x1_cls + 5, rect_y2_cls - 5),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

                            except KeyError as e:
                                logging.error(f"Error processing classification for frame {frame_count} in video {video_path}: {str(e)}")
                        else:
                            class_name = detection_names[cls]
                            rect_x1_det, rect_y1_det, rect_x2_det, rect_y2_det = self.draw_text_with_rectangle(class_name, x2, y1)
                            cv2.rectangle(frame, (rect_x1_det, rect_y1_det), (rect_x2_det, rect_y2_det), (255, 0, 255), -1)
                            cv2.putText(frame, f'{class_name} {score:.2f}', (rect_x1_det + 5, rect_y2_det - 5),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

                    end_time = cv2.getTickCount()
                    fps = cv2.getTickFrequency() / (end_time - start_time)
                    cv2.putText(frame, "FPS "f'{fps:.2f}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2, cv2.LINE_AA)
                    if self.save_video:
                        out.write(frame)
                    frame_count += 1
                    frame = cv2.resize(frame,(1280,720))
                    cv2.imshow('frame', frame)
                except Exception as e:
                    logging.error(f"Error processing frame {frame_count} in video {video_path}: {str(e)}")
                if cv2.waitKey(1) == ord('q'):
                    break
            cap.release()
            if self.save_video:
                out.release()
        cv2.destroyAllWindows()

