from SkillWheelScheme import SkillWheelScheme
import cv2
import numpy as np
import math

class SkillWheelPainter:
    def __init__(self, scheme, image_size:int):
        self.scheme = scheme
        if image_size < 256:
            raise ValueError('Too small image size')
        self.image = np.full((image_size, image_size, 3), fill_value=255, dtype="uint8")
        self.image_center = ((image_size-1)//2, (image_size-1)//2)
        self.radius = int(round(image_size * 0.9 * 0.5))
        self.inner_radius = self.radius//2
        self.level12_radius = self.inner_radius + (self.radius - self.inner_radius) * 2 // 3
        self.level23_radius = self.inner_radius + (self.radius - self.inner_radius) // 3
        self.level1_radius = (self.radius + self.level12_radius) // 2
        self.level2_radius = (self.level12_radius + self.level23_radius) // 2
        self.level3_radius = (self.level23_radius + self.inner_radius) // 2
        self.line_thickness = int(min(1., math.ceil(image_size/1000.)))
        self.background_color = (255, 255, 255)
        self.line_color = (0, 0, 0)

    def paint(self):
        angle_ranges = self.scheme.get_categories_angle_ranges()

        index = 0
        for key, angle_range in angle_ranges.items():
            color_level = int(127 + round(index * 128. / len(angle_ranges)-1))
            begin_angle = angle_range[0]
            end_angle   = angle_range[1]
            begin_angle_deg = begin_angle * 180. / math.pi
            end_angle_deg   = end_angle   * 180. / math.pi
            index += 1
            cv2.ellipse(
                img=self.image,
                center=self.image_center,
                axes=(self.radius,self.radius),
                angle=0,
                startAngle=begin_angle_deg,
                endAngle=end_angle_deg,
                color=(color_level, color_level, color_level),
                thickness=-1,
                lineType=cv2.LINE_AA
            )
            # draw line
            x = int(math.floor(self.radius * math.cos(begin_angle)) + self.image_center[0])
            y = int(math.floor(self.radius * math.sin(begin_angle)) + self.image_center[1]) # -sin ?
            cv2.line(self.image, self.image_center, (x,y), self.line_color,
                     thickness=self.line_thickness, lineType=cv2.LINE_AA)

        # inner white field
        cv2.circle(self.image, self.image_center, self.inner_radius, (255, 255, 255), thickness=-1,
                   lineType=cv2.LINE_AA)

        # inner boundary
        cv2.circle(self.image, self.image_center, self.inner_radius, (0,0,0),
                   thickness=self.line_thickness, lineType=cv2.LINE_AA)

        # level 1-2 boundary
        cv2.circle(self.image, self.image_center, self.level12_radius, (0,0,0),
                   thickness=self.line_thickness, lineType=cv2.LINE_AA)

        # level 1-2 boundary
        cv2.circle(self.image, self.image_center, self.level23_radius, (0,0,0),
                   thickness=self.line_thickness, lineType=cv2.LINE_AA)

        # outer boundary
        cv2.circle(self.image,self.image_center,self.radius, (0,0,0), thickness=self.line_thickness, lineType=cv2.LINE_AA)
        return

    def get_image(self):
        return self.image