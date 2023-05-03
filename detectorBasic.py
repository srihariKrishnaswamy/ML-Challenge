import argparse
from typing import List, Optional, Union, Dict

import numpy as np
import torch

import norfair
from norfair import Detection, Paths, Tracker, Video
import yolov5

DISTANCE_THRESHOLD_BBOX: float = 0.7
DISTANCE_THRESHOLD_CENTROID: int = 30
MAX_DISTANCE: int = 10000

classifications: List[str] = ['annelida', 'arthropoda', 'cnidaria', 'echinodermata', 'fish',
                              'mollusca', 'other-invertebrates', 'porifera', 'unidentified-biology']

class OrganismDetection:
    def __init__(self, num_id:int, classification:str) -> None:
        self.num_id: int = num_id
        self.classification: str = classification
        self.frames: List[int] = []
    
    def add_detection(self, frame:int):
        "Registers a detection, including the frame of appearance and confidence level."
        self.frames.append(frame)

    def get_first_last_frame(self) -> tuple[int, int]:
        "Returns the first and last frame of appearance as a tuple."
        return (self.frames[0], self.frames[len(self.frames) - 1])    

class YOLO:
    def __init__(self, model_name: str, device: Optional[str] = None):
        if device is not None and "cuda" in device and not torch.cuda.is_available():
            raise Exception(
                "Selected device='cuda', but cuda is not available to Pytorch."
            )
        # automatically set device if its None
        elif device is None:
            device = "cuda:0" if torch.cuda.is_available() else "cpu"

        # load model
        self.model = yolov5.load('iterations/seventh.pt', device=device)

    def __call__(
        self,
        img: Union[str, np.ndarray],
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.45,
        image_size: int = 720,
        classes: Optional[List[int]] = None,
    ) -> torch.tensor:

        self.model.conf = conf_threshold
        self.model.iou = iou_threshold
        if classes is not None:
            self.model.classes = classes
        detections = self.model(img, size=image_size)
        return detections

def euclidean_distance(detection, tracked_object):
    """Returns euclidean distance between two points."""
    return np.linalg.norm(detection.points - tracked_object.estimate)

def center(points):
    return [np.mean(np.array(points), axis=0)]

def yolo_detections_to_norfair_detections(
    yolo_detections: torch.tensor, track_points: str = "bbox"  # bbox or centroid
) -> List[Detection]:
    """convert detections_as_xywh to norfair detections"""
    norfair_detections: List[Detection] = []

    if track_points == "centroid":
        detections_as_xywh = yolo_detections.xywh[0]
        for detection_as_xywh in detections_as_xywh:
            centroid = np.array(
                [detection_as_xywh[0].item(), detection_as_xywh[1].item()]
            )
            scores = np.array([detection_as_xywh[4].item()])
            norfair_detections.append(
                Detection(
                    points=centroid,
                    scores=scores,
                    label=int(detection_as_xywh[-1].item()),
                )
            )
    elif track_points == "bbox":
        detections_as_xyxy = yolo_detections.xyxy[0]
        for detection_as_xyxy in detections_as_xyxy:
            bbox = np.array(
                [
                    [detection_as_xyxy[0].item(), detection_as_xyxy[1].item()],
                    [detection_as_xyxy[2].item(), detection_as_xyxy[3].item()],
                ]
            )
            #HAD LABEL FIELD HERE
            scores = np.array(
                [detection_as_xyxy[4].item(), detection_as_xyxy[4].item()]
            )
            norfair_detections.append(
                Detection(
                    points=bbox, scores=scores, label=int(detection_as_xyxy[-1].item())
                )
            )

    return norfair_detections

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Track objects in a video.")
    parser.add_argument("files", type=str, nargs="+", help="Video files to process")
    parser.add_argument(
        "--model-name", type=str, default="iterations/seventh", help="YOLOv5 model name"
    )
    parser.add_argument(
        "--img-size", type=int, default="640", help="YOLOv5 inference size (pixels)"
    )
    parser.add_argument(
        "--conf-threshold",
        type=float,
        default="0.25",
        help="YOLOv5 object confidence threshold",
    )
    parser.add_argument(
        "--iou-threshold", type=float, default="0.45", help="YOLOv5 IOU threshold for NMS"
    )
    parser.add_argument(
        "--classes",
        nargs="+",
        type=int,
        help="Filter by class: --classes 0, or --classes 0 2 3",
    )
    parser.add_argument(
        "--device", type=str, default=None, help="Inference device: 'cpu' or 'cuda'"
    )
    parser.add_argument(
        "--track-points",
        type=str,
        default="bbox",
        help="Track points: 'centroid' or 'bbox'",
    )
    parser.add_argument("--output_csv", type=str, default="out.csv", 
        help="Output path for the tracking data CSV file.") #WILL BE REPLACED WITH EXCEL

    parser.add_argument("--output_video", type=str, default="out.mp4",
        help="Output video file if only running one file at a time.")
    
    args = parser.parse_args()
    model = YOLO(args.model_name, device=args.device)
    video_path_to_data: Dict[str, Dict[int, OrganismDetection]] = {}

    for input_path in args.files:
        video = Video(input_path=input_path)

        distance_function = "iou" if args.track_points == "bbox" else "euclidean"
        distance_threshold = (
            DISTANCE_THRESHOLD_BBOX
            if args.track_points == "bbox"
            else DISTANCE_THRESHOLD_CENTROID
        )

        tracker = Tracker(
            distance_function=distance_function,
            distance_threshold=distance_threshold,
        )

        # track_id_to_data: Dict[int, OrganismDetection] = {}

        for frame in video:
            yolo_detections = model(
                frame,
                conf_threshold=args.conf_threshold,
                iou_threshold=args.iou_threshold,
                image_size=args.img_size,
                classes=args.classes,
            )
            detections = yolo_detections_to_norfair_detections(
                yolo_detections, track_points=args.track_points
            )
            tracked_objects = tracker.update(detections=detections)
            #drawing bounding boxes
            norfair.draw_boxes(frame, detections)
            norfair.draw_tracked_boxes(frame, tracked_objects)
            video.write(frame)