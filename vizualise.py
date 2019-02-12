import cv2
from threading import Thread
from utils import visualization_utils as vis_util
import numpy as np
import statistics


class Vizualise(Thread):

    def __init__(self, name=None, id = 0, shared_variables = None):
        Thread.__init__(self)
        self.name = name
        self.id = id
        self.shared_variables = shared_variables
        self.filter = True

        self.shared_variables.image_of_detections.append(list())

    def get_image_difference(self, image_1, image_2):
        first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

        img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
        img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
        img_template_diff = 1 - img_template_probability_match

        # taking only 10% of histogram diff, since it's less accurate than template method
        commutative_image_diff = (img_hist_diff / 10) + img_template_diff
        return commutative_image_diff

    def imcrop(self, img, bbox):
        x1,y1,x2,y2 = bbox
        if x1 < 0 or y1 < 0 or x2 > img.shape[1] or y2 > img.shape[0]:
             img, x1, x2, y1, y2 = pad_img_to_fit_bbox(img, x1, x2, y1, y2)
        return img[y1:y2, x1:x2, :]

    def pad_img_to_fit_bbox(self, img, x1, x2, y1, y2):
        img = np.pad(img, ((np.abs(np.minimum(0, y1)), np.maximum(y2 - img.shape[0], 0)),
                   (np.abs(np.minimum(0, x1)), np.maximum(x2 - img.shape[1], 0)), (0,0)), mode="constant")
        y1 += np.abs(np.minimum(0, y1))
        y2 += np.abs(np.minimum(0, y1))
        x1 += np.abs(np.minimum(0, x1))
        x2 += np.abs(np.minimum(0, x1))
        return img, x1, x2, y1, y2

    def run(self):

        font = cv2.FONT_HERSHEY_SIMPLEX
        tresh = 0.8 # decide tresh for detection precision
        f_counter = 0
        filter_list = list()
        while True:
            if self.shared_variables.OutputFrame_list[self.id] is not None:
                frame = self.shared_variables.OutputFrame_list[self.id].frame

                if frame is not None:

                    # No boxes
                    if self.shared_variables.OutputFrame_list[self.id].boxes == ():
                        pass
                    else:
                        scores =np.squeeze(self.shared_variables.OutputFrame_list[self.id].boxes[1])
                        classes = np.squeeze(self.shared_variables.OutputFrame_list[self.id].boxes[2]).astype(np.int32)
                        vis_util.visualize_boxes_and_labels_on_image_array(
                        frame,
                        np.squeeze(self.shared_variables.OutputFrame_list[self.id].boxes[0]),
                        classes,
                        scores,
                        self.shared_variables.category_index,
                        use_normalized_coordinates=True,
                        min_score_thresh=tresh,
                        line_thickness=8)

                        #Calculate persons
                        i = 0
                        crop_images = list()

                        while i < len(scores) :
                            if scores is None or scores[i] > tresh:
                                if classes[i] in self.shared_variables.category_index.keys():
                                    class_name = self.shared_variables.category_index[classes[i]]['name']
                                    if(class_name == 'person'):
                                        crop_img = None
                                        # crop detection box
                                        height, width, channels = frame.shape

                                        x = (self.shared_variables.OutputFrame_list[self.id].boxes[0][0][i][0]*width).astype(int) -1
                                        y =( self.shared_variables.OutputFrame_list[self.id].boxes[0][0][i][1]*height).astype(int) -1
                                        xx =( self.shared_variables.OutputFrame_list[self.id].boxes[0][0][i][2]*width).astype(int) -1
                                        yy =( self.shared_variables.OutputFrame_list[self.id].boxes[0][0][i][3]*height).astype(int)-1

                                        crop_img = self.imcrop(frame, (x,y,xx,yy)) #frame[y:yy,x:xx ]

                                        # Create a named colour
                                        red = [0,150,0]
                                        frame[y,x] = red
                                        frame[yy,xx] = red

                                        # check if persons exist on other images
                                        #if len(self.shared_variables.image_of_detections) > 0:
                                        already_detected = False
                                        k = 0

                                        for lis in self.shared_variables.image_of_detections:
                                            if k == self.id:
                                                continue
                                            else:

                                                for img in lis:
                                                    t = self.get_image_difference(img, crop_img)
                                                    if t < 0.6: #90 % alike
                                                        already_detected = True

                                            k += 1

                                        if not already_detected:
                                            # Save image
                                            crop_images.append(crop_img)


                            i += 1

                        # Save images
                        self.shared_variables.image_of_detections[self.id] = crop_images

                        # check many numbers
                        # Calculate amount of detections
                        amount = 0
                        for i in self.shared_variables.image_of_detections:
                            for k in i:
                                amount += 1

                        # easy filter
                        # collect 10 values and use median
                        if self.filter:
                            f_counter += 1
                            filter_list.append(amount)

                            if f_counter >= 10:
                                filter_list.sort()
                                self.shared_variables.number_of_persons = statistics.median(filter_list)
                                filter_list = list()
                                f_counter = 0

                        else:
                            # Save amount
                            self.shared_variables.number_of_persons = amount

                    cv2.putText(frame, str(self.shared_variables.number_of_persons), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
                    cv2.imshow(str(self.id), frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        cv2.destroyAllWindows()
