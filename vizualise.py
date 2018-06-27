import cv2
from threading import Thread
from utils import visualization_utils as vis_util
import numpy as np

class Vizualise(Thread):

    def __init__(self, name=None, shared_variables = None):
        Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables


    def run(self):

        font = cv2.FONT_HERSHEY_SIMPLEX
        tresh = 0.8
        while True:
            if( len(self.shared_variables.OutputFrame_list) > 0):
                frame = self.shared_variables.OutputFrame_list[0].frame

                if(frame is not None):



                    # No boxes
                    if self.shared_variables.OutputFrame_list[0].boxes == ():
                        pass
                    else:
                        scores =np.squeeze(self.shared_variables.OutputFrame_list[0].boxes[1])
                        classes = np.squeeze(self.shared_variables.OutputFrame_list[0].boxes[2]).astype(np.int32)
                        vis_util.visualize_boxes_and_labels_on_image_array(
                        frame,
                        np.squeeze(self.shared_variables.OutputFrame_list[0].boxes[0]),
                        classes,
                        scores,
                        self.shared_variables.category_index,
                        use_normalized_coordinates=True,
                        min_score_thresh=tresh,
                        line_thickness=8)

                        #Calculate persons
                        i = 0
                        number_of_persons = 0
                        while i < len(scores) :
                            if scores is None or scores[i] > tresh:
                                if classes[i] in self.shared_variables.category_index.keys():
                                    class_name = self.shared_variables.category_index[classes[i]]['name']
                                    if(class_name == 'person'):
                                        number_of_persons += 1
                            #            print(class_name)
                            i += 1

                        self.shared_variables.number_of_persons = number_of_persons


                    cv2.putText(frame, str(self.shared_variables.number_of_persons), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
                    cv2.imshow('Frame', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        cv2.destroyAllWindows()
