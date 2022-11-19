import cv2
from vse.model.yolov3.configs import YOLO_INPUT_SIZE, YOLO_COCO_CLASSES
from vse.model.yolov3.yolov3 import read_class_names
from vse.model.yolov3.utils import image_preprocess, postprocess_boxes, nms, Load_Yolo_model
import tensorflow as tf
import numpy as np

def detect_image(Yolo, image_path, input_size=YOLO_INPUT_SIZE, score_threshold=0.3, iou_threshold=0.45):
    original_image      = cv2.imread(image_path)
    original_image      = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    original_image      = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    image_data = image_preprocess(np.copy(original_image), [input_size, input_size])
    image_data = image_data[np.newaxis, ...].astype(np.float32)

    pred_bbox = Yolo.predict(image_data)

    pred_bbox = [tf.reshape(x, (-1, tf.shape(x)[-1])) for x in pred_bbox]
    pred_bbox = tf.concat(pred_bbox, axis=0)

    bboxes = postprocess_boxes(pred_bbox, original_image, input_size, score_threshold)
    bboxes = nms(bboxes, iou_threshold, method='nms')

    all_classes = read_class_names(YOLO_COCO_CLASSES)
    labels = []
    for i, bbox in enumerate(bboxes):
        class_ind = int(bbox[5])
        label = all_classes[class_ind]
        labels.append(label)

    labels = list(set(labels))
    return labels


# image_path   = "istockphoto-1018141890-612x612.jpg"
# video_path   = "test.mp4"
#
# yolo = Load_Yolo_model()
# detect_image(yolo, image_path, input_size=YOLO_INPUT_SIZE)
