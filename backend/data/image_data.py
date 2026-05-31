import math
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy
from PIL import Image, ExifTags, ImageOps
import config


class ImageData():
    #if order is changed or adding more or removing, check places to adjust image_data, image_sorting
    PARTS_VECTORS = [
        (11, 12),                        # shoulders  0
        (23, 24),                       # hips        1
        (11, 23), (12, 24),             # torso       2, 3
        (11, 13), (13, 15),             # left arm    4, 5
        (12, 14), (14, 16),             # right arm   6, 7
        (23, 25), (25, 27),             # left leg    8, 9
        (24, 26), (26, 28)              # right leg   10, 11
        # (0, 1), (1, 2), (2, 3), (3, 7),  # face
    ]

    CONNECTION_POINTS = [  
        (14, 12, 11),            # shoulder and right forearm     0
        (12, 11, 13),            # shoulder and left forearm      1
        (26, 24, 23),            # hips and right leg             2
        (24, 23, 25),            # hips and left leg              3

        (24, 12, 11),            # sholder and right torso part   4
        (12, 11, 23),            # sholder and left torso part    5

        (16, 14, 12),            # right hand and right forearm   6
        (11, 13, 15),            # left hand and left forearm     7
        (24, 26, 28),            # right thigh and right calve    8
        (23, 25, 27),            # left thigh and left calve      9

    ]
    

    def __init__(self, path = None, landmarks = None, parts_angles = None, connection_angles = None, model_asset_path=config.model_asset_path):
        self.path = path
        self.landmarks = landmarks
        self.parts_angles = parts_angles
        self.connection_angles = connection_angles
        self.model_asset_path = model_asset_path

        #TODO needed only for newly loaded/added images, not sketch. If information was stored before -> this method not needed to be called
        if self.path != None and self.path != "":
            self.__adjust_image_with_exif_orientation(self.path)

            if self.landmarks is None:
                self.__calculate_landmarks()

        if self.parts_angles is None:
            self.set_angles_for_parts()
        
        if self.connection_angles is None:
            self.set_angles_for_connections_between_parts()



    def __calculate_landmarks(self):
        print(f"Calculating landmarks with mediapipe for {self.path}")
        
        base_options = python.BaseOptions(self.model_asset_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=True)
        detector = vision.PoseLandmarker.create_from_options(options)

        try:
            image = mp.Image.create_from_file(self.path)
        except:
            print(f"Strange path {self.path}")
            print(f"Not able to calculate landmarks")
            return 

        detection_result = detector.detect(image)

        if len(detection_result.pose_landmarks) > 0:
            pose_landmarks_normalized = detection_result.pose_landmarks[0]
            self.landmarks = numpy.array([[landmark.x, landmark.y] for landmark in pose_landmarks_normalized])
            print(self.landmarks)
        else:
            print(f"Not able to calculate landmarks for {self.path}")

    def __adjust_image_with_exif_orientation(self, path):
        """
        if image has exif orientation != 1, it will shown rotated;
        in order to receive coords correctly; exif orientation should be removed or == 1, and image rotated accordently:  .exif_transpose does both;
        then save to original destination """
        #TODO maybe there is a way to not rewrite previous image: landmarks calculation needs path and exif_transpose returns image; also was not able to .exif_transpose mp.Image in .calculate landmarks
        img = Image.open(path)

        for property, value in img.getexif().items():
            # print(f'{k}, {v}')
            if ExifTags.TAGS.get(property) == "Orientation":
                print("Orientation:", value)
                if value != 1:
                    adjusted_image = ImageOps.exif_transpose(img)
                    adjusted_image.save(path)
                return 

    def get_landmarks(self, json):
        pass

    def __calculate_angle_for_vector(self, part_coords):
        """ consider normal xy-coords, angle = 0 starts at (0,1) and then goes till pi: count clockwise; then angle will be negative(around -pi) and goes till 0;
        imagine start for both positive and negatives at 0 and then going till around +-pi, but positives clockwise and negatives counterclockwise;
        so it will be 0(also 0 grad), then 1,57(90 grad), then 3,14(180 grad), then -1,57(-90 grad) and then 0 """

        # if point/s is/are missing => return 0 angle
        if numpy.array_equal(part_coords[0], config.no_point_value) or numpy.array_equal(part_coords[1], config.no_point_value):
            return 0
        
        x1, y1 = part_coords[0]
        x2, y2 = part_coords[1]
        angle = math.atan2(x2 - x1, y2 - y1)

        return angle
    

    def __move_vector_to_root(sefl, vector):
        # vector - [[x1,y1], [x2,y2]]
        # x2 - x1, y2 - y1
        return [vector[1][0] - vector[0][0], vector[1][1] - vector[0][1]]
    
    def __create_vectors_from_three_points(self, left, middle, right):
        # if point/s is/are missing => return None
        if numpy.array_equal(left, config.no_point_value) or numpy.array_equal(middle, config.no_point_value) or numpy.array_equal(right, config.no_point_value):
            return None

        vector1 = [left[0] - middle[0], left[1] - middle[1]]
        vector2 = [right[0] - middle[0], right[1] - middle[1]]
        return [vector1, vector2]



    def __calculate_angle_between_two_vectors(self, vector1, vector2):
        if not vector1 or not vector2:
            return None
        if numpy.array_equal(vector1, config.no_point_value) or numpy.array_equal(vector2, config.no_point_value):
            return 0

        dot_product = vector1[0]*vector2[0] + vector1[1]*vector2[1]
        # print(f'dot: {dot_product}')
        len_vector1_power_two = vector1[0]**2 + vector1[1]**2
        len_vector2_power_two = vector2[0]**2 + vector2[1]**2

        if len_vector1_power_two == 0 or len_vector2_power_two == 0:
            print('Vector length is 0')
            return None

        cos = dot_product / math.sqrt(len_vector1_power_two * len_vector2_power_two)

        # if during calculations cos becomes more that 1 or less than -1
        cos = max(-1, min(1, cos))
        rad = math.acos(cos)

        return rad


    
    def set_angles_for_parts(self):

        angles = []
        for start, end in self.PARTS_VECTORS:
           # if point/s is/are missing => add 0 angle
            if numpy.array_equal(self.landmarks[start], config.no_point_value) or numpy.array_equal(self.landmarks[end], config.no_point_value):
                angles.append(0)
                continue

            angles.append(self.__calculate_angle_for_vector([self.landmarks[start], self.landmarks[end]]))

        self.parts_angles = numpy.array(angles)


    def set_angles_for_connections_between_parts(self):

        angles = []
        for left, middle, right in self.CONNECTION_POINTS:
            if numpy.array_equal(self.landmarks[left], config.no_point_value) or numpy.array_equal(self.landmarks[middle], config.no_point_value) or numpy.array_equal(self.landmarks[right], config.no_point_value):
                angles.append(0)
                continue

            vectors = self.__create_vectors_from_three_points(self.landmarks[left], self.landmarks[middle], self.landmarks[right])
            angles.append(self.__calculate_angle_between_two_vectors(vectors[0], vectors[1]))

        self.connection_angles = numpy.array(angles)


