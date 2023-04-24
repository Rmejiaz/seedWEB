import tensorflow as tf
import cv2
import numpy as np

class Counter:
    def __init__(self, model_path):
        
        if model_path[-2:] == "h5":
        
            self.model = tf.keras.models.load_model(model_path)
            self.type = "tf"
        elif model_path[-6:]=="tflite":
            self.interpreter = tf.lite.Interpreter(model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.type = "tflite"
        
    def letterbox(self, im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better val mAP)
            r = min(r, 1.0)

        # Compute padding
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return im, r, (dw, dh)

    
    def predict(self, img):

        if self.type == "tflite":
            # Preprocess the input image
            input_shape = self.input_details[0]['shape'][1:3]
            # resized_image = cv2.resize(img, input_shape)

            image, ratio, dwdh = self.letterbox(img, auto=False)
            print("ratio: ", ratio)
            print("dwdh: ", dwdh)
            # image = image.transpose((2, 0, 1))
            image = np.expand_dims(image, 0)
            image = np.ascontiguousarray(image)

            input_data = image.astype(np.float32)
            input_data /= 255



            # input_data = np.expand_dims(resized_image, axis=0)
            # input_data = input_data.astype('float32') / 255.
            print("Input data shape: ",input_data.shape)
            print("Input data max: ",input_data.max())
            print("Input data min:",input_data.min())
            
            # Run the detection
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            self.output_data = self.interpreter.get_tensor(self.output_details[0]['index'])

            # # Process the output
            class_indexes = self.output_data[:, 5,:].argmax()
            class_ids = self.output_data[:]
            print("Class ids: ", class_ids)
            confidences = self.output_data[..., 4]
            print(self.output_data)
            print(self.output_data[...,0:4])
            boxes = (self.output_data[..., 0:4] * img.shape[0])/100
            print("boxes:", boxes)

            # Filter out weak detections
            mask = confidences > 50
            class_ids = class_ids[mask]
            print("Class ids: ", class_ids)
            confidences = confidences[mask]
            boxes = boxes[mask]
            print(boxes)
            print(confidences)


            # Get the bounding boxes and class labels.
            boxes = self.output_data[:, :, 0:4]
            classes = self.output_data[:, :, 5:]
            object_count = {'germinated':0, 'no_germinated':0}
            # Display the predictions.
            for i in range(len(boxes)):
                for box, cls in zip(boxes[i], classes[i]):
                    if cls[np.argmax(cls)] > 0.5:
                        x1, y1, x2, y2 = box
                        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        cv2.putText(img, str(np.argmax(cls)), (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        
                        # if cls_id == 0:
                        #     object_count['Germinated'] += 1
                        # elif cls_id == 1:
                        #     object_count['No_germinated'] += 1


            # Return the result image and object count

            ori_images = [img.copy()]
            names = ["No germinada", "Germinada"]
            colors = {name:[np.random.randint(0, 255) for _ in range(3)] for i,name in enumerate(names)}


            result = img.copy()
            
            return result, object_count













