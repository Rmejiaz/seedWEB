import tflite_runtime.interpreter as tflite
import cv2
import numpy as np

class Counter:
    def __init__(self, model_path):

        if model_path[-2:] == "h5":

            self.model = tf.keras.models.load_model(model_path)
            self.type = "tf"
        elif model_path[-6:]=="tflite":
            self.interpreter = tflite.Interpreter(model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.type = "tflite"
    def non_max_suppression_fast(self, boxes, classes, overlapThresh = 0.8):
        # Return an empty list, if no boxes given
        if len(boxes) == 0:
            return [], []


        new_boxes = boxes.copy()

        new_boxes[:, 0] = boxes[:, 0] - boxes[:, 2]/2
        new_boxes[:, 1] = boxes[:, 1] - boxes[:, 3]/2
        new_boxes[:, 2] = boxes[:, 0] + boxes[:, 2]/2
        new_boxes[:, 3] = boxes[:, 1] + boxes[:, 3]/2



        x1 = new_boxes[:, 0]  # x coordinate of the top-left corner
        y1 = new_boxes[:, 1]  # y coordinate of the top-left corner
        x2 = new_boxes[:, 2]  # x coordinate of the bottom-right corner
        y2 = new_boxes[:, 3]  # y coordinate of the bottom-right corner

        # Compute the area of the bounding new_boxes and sort the bounding
        # new_Boxes by the bottom-right y-coordinate of the bounding box
        areas = (x2 - x1 + 1) * (y2 - y1 + 1) # We add 1, because the pixel at the start as well as at the end counts
        # The indices of all new_boxes at start. We will redundant indices one by one.
        indices = np.arange(len(x1))
        for i,box in enumerate(new_boxes):
            # Create temporary indices  
            temp_indices = indices[indices!=i]
            # Find out the coordinates of the intersection box
            xx1 = np.maximum(box[0], new_boxes[temp_indices,0])
            yy1 = np.maximum(box[1], new_boxes[temp_indices,1])
            xx2 = np.minimum(box[2], new_boxes[temp_indices,2])
            yy2 = np.minimum(box[3], new_boxes[temp_indices,3])
            # Find out the width and the height of the intersection box
            w = np.maximum(0, xx2 - xx1  + 1)
            h = np.maximum(0, yy2 - yy1 + 1)
            # compute the ratio of overlap
            overlap = (w * h) / (areas[temp_indices] + areas[i] - (w*h))
            # if the actual boungding box has an overlap bigger than treshold with any other box, remove it's index 
             
            if np.any(overlap > overlapThresh):
                indices = indices[indices != i]
                
        #return only the boxes at the remaining indices
        return boxes[indices].astype(int), classes[indices]

    def predict(self, image):

        img = image.copy()

        if self.type == "tflite":

            # Load and preprocess the image

            image_resized = cv2.resize(img, (self.input_details[0]['shape'][2], self.input_details[0]['shape'][1]))
            image_normalized = image_resized / 255.0
            image_input = np.expand_dims(image_normalized, axis=0).astype(self.input_details[0]['dtype'])

            # Run the inference
            self.interpreter.set_tensor(self.input_details[0]['index'], image_input)
            self.interpreter.invoke()
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])

            output_data = output_data[0].T

            # Extract bounding box coordinates
            boxes = output_data[:, 0:4]
            scores = output_data[:, 4:]
            valid_indices = np.where(scores > 0.5)[0]

            valid_boxes = boxes[valid_indices]
            classes = scores.argmax(axis=1)[valid_indices]


            valid_boxes_2, valid_classes_2 = self.non_max_suppression_fast(valid_boxes, classes)
            
    
            # Draw bounding boxes on the image
            for box, class_ in zip(valid_boxes_2, valid_classes_2):
                x, y, w, h = box
                x = int(x * img.shape[1]/self.input_details[0]['shape'][2])
                y = int(y * img.shape[0]/self.input_details[0]['shape'][1])
                w = int(w * img.shape[1]/self.input_details[0]['shape'][2])
                h = int(h * img.shape[0]/self.input_details[0]['shape'][1])
                if class_ == 0:
                  cv2.rectangle(img, (int(x - w/2), int(y - h/2)), (int(x + w/2), int(y + h/2)), (0, 255, 0), 2)
                else:
                  cv2.rectangle(img, (int(x - w/2), int(y - h/2)), (int(x + w/2), int(y + h/2)), (255, 0, 0), 2)


            object_count = {"germinated": np.count_nonzero(valid_classes_2==0), "no_germinated": np.count_nonzero(valid_classes_2==1)}

            # Return the result image and object count

            return img, object_count













