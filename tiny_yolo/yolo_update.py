import cv2
import numpy as np

CONF_THRESH, NMS_THRESH = 0.9, 0.99
colors = [[0, 0, 255]]
first_threshold = 100
second_threshold = 200


def init_yolo(config, weights):
    # Load the network
    net = cv2.dnn.readNetFromDarknet(config, weights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    # Get the output layer from YOLO
    layers = net.getLayerNames()
    output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return net, output_layers


def get_bounding_box(frame, net, output_layers):
    if frame is None:
        return None
    height, width, channels = frame.shape

    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    # print(output_layers)
    layer_outputs = net.forward(output_layers)
    class_ids, confidences, b_boxes = [], [], []
    for output in layer_outputs:
        for detection in output:
            scores = detection[4:]
            class_id = 0  # class 0 is person
            confidence = scores[class_id]
            # if confidence > CONF_THRESH:
            # print("confidence", confidence)
            if confidence > CONF_THRESH:
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                b_boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

    try:
        # Perform non maximum suppression for the bounding boxes to filter overlapping and low confident bounding boxes
        indices = cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten()  # .tolist()
    except:
        indices = []
    if len(indices) == 0:
        return None
    x, y, w, h = b_boxes[indices[0]]
    print(w)
    return x, y, w, h


def add_bounding_box(image, bbox):
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(image, p1, p2, (255, 0, 0), 2, 1)
    return image


def add_size(image, size):
    cv2.putText(image, "SIZE: " + str(round(size, 2)), (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0),
                2)
    return image

# if __name__ == '__main__':
#    # can be downloaded from https://pjreddie.com/darknet/yolo/
#    config = 'tiny_yolo/yolov3.cfg'
#    weights = 'tiny_yolo/yolov3.weights'
#    net, background = init_yolo(config, weights)
#
#    i = 0
#    fps = 0
#    cv2.namedWindow('Detection and tracking')
#
#    while video.is_open():
#        i += 1
#        if i >= 1000: # for not playing entire video
#            break
#
#        ret, image, fps = video.last_frame()
#        #image = cv2.resize(image,(608,608), interpolation = cv2.INTER_AREA)
#        cv2.setWindowTitle('Detection and tracking', f'FPS: {fps}')
#        if not ret:
#            print("No frame")
#            continue
#
#        bbox = get_bounding_box(image, net, background)
#
#        if bbox is not None:
#            p1 = (int(bbox[0]), int(bbox[1]))
#            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
#            cv2.rectangle(image, p1, p2, (255, 0, 0), 2, 1)
#        cv2.imshow('Detection and tracking', image)
#        key = cv2.waitKey(1)
#
