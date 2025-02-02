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
        self.levelX_radius = int(round(0.75*self.inner_radius))
        self.line_thickness = int(min(1, round(image_size/1000.)))

        self.background_color = (255, 255, 255)
        self.line_color = (0, 0, 0)

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.skill_radius = (self.level1_radius - self.level2_radius) // 3

    def paint(self):
        angle_ranges = self.scheme.get_categories_angle_ranges()

        index = 0
        for category,  angle_range in angle_ranges.items():
            color_level = int(127 + round(index * 128. / len(angle_ranges)-1))
            begin_angle = angle_range[0]
            end_angle   = angle_range[1]
            begin_angle_deg = round(begin_angle * 180. / math.pi)
            end_angle_deg   = round(end_angle   * 180. / math.pi)
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
        for category, angle_range in angle_ranges.items():
            # unfortunately cv2.ellipse seems to take only integer angle values :<
            begin_angle =  round(angle_range[0]* 180. / math.pi) * math.pi/180.
            # draw line
            x = int(round(self.radius * math.cos(begin_angle)) + self.image_center[0])
            y = int(round(self.radius * math.sin(begin_angle)) + self.image_center[1]) # -sin ?
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
        cv2.circle(self.image,self.image_center,self.radius, (0,0,0),
                   thickness=self.line_thickness, lineType=cv2.LINE_AA)

        # now try to draw skill from levels 1 - 3
        # keep track of every skill's position
        skill_positions = dict()
        for category, angle_range in angle_ranges.items():
            begin_angle = angle_range[0]
            end_angle = angle_range[1]

            skill_levels = [self.scheme.level1, self.scheme.level2, self.scheme.level3]
            skill_level_radii = [self.level1_radius, self.level2_radius, self.level3_radius]

            for i in range(3):
                skills = skill_levels[i][category]
                level_radius = skill_level_radii[i]

                # skills = self.scheme.level1[category]
                n_skills = len(skills)
                if n_skills == 0:
                    continue

                angle_step = (end_angle-begin_angle)/n_skills
                half_step = angle_step*0.5

                for index, skill in enumerate(skills):
                    angle = begin_angle + half_step + angle_step*index
                    x = int(math.floor(level_radius * math.cos(angle)) + self.image_center[0])
                    y = int(math.floor(level_radius * math.sin(angle)) + self.image_center[1])  # -sin ?
                    pos = (x, y)

                    # update dict
                    skill_positions[skill] = pos
                    continue

        # try to draw level X in the middle (no idea how to do it better without hierarchy analysis)
        n_x_skills = len(self.scheme.levelX)
        if n_x_skills > 0:
            x_angle_step = 2*math.pi / n_x_skills
            for index, skill in enumerate(self.scheme.levelX):
                angle = x_angle_step*index
                x = int(math.floor(self.levelX_radius * math.cos(angle)) + self.image_center[0])
                y = int(math.floor(self.levelX_radius * math.sin(angle)) + self.image_center[1])  # -sin ?
                pos = (x, y)

                # update dict
                skill_positions[skill] = pos
                continue

        # draw hierarchy ! just simple arrows
        for skill, dependencies in self.scheme.hierarchy.items():
            skill_pos = skill_positions[skill]
            for dep in dependencies:
                dep_pos = skill_positions[dep]
                # this is a bit more complicated
                # because writing the arrow will be overwritten
                # by skill interior in case of drawing the line from A to B
                # so we need to calculate the end point on the skill's boundary

                direction_vec = (skill_pos[0] - dep_pos[0],skill_pos[1] - dep_pos[1])
                norm = math.sqrt(direction_vec[0]*direction_vec[0] + direction_vec[1]*direction_vec[1])
                direction_vec = (direction_vec[0] / norm, direction_vec[1] / norm)
                # after performing very ugly ops we finally have an unit vector
                # now translate the end position by proper radius value in calculated direction
                end_point = (int(round(skill_pos[0] - direction_vec[0] * self.skill_radius)),
                             int(round(skill_pos[1] - direction_vec[1] * self.skill_radius)))
                # calculate tip length in relation to line length
                tip_length = 10. * self.line_thickness
                tip_length_ratio = tip_length / (norm - self.skill_radius)

                cv2.arrowedLine(self.image, dep_pos, end_point, self.line_color,
                                thickness=self.line_thickness*2, line_type=cv2.LINE_AA,
                                tipLength=tip_length_ratio)

        # now draw the skills
        for skill, pos in skill_positions.items():
            # interior
            cv2.circle(self.image, pos, self.skill_radius, self.background_color, thickness=-1,
                       lineType=cv2.LINE_AA)
            # boundary
            cv2.circle(self.image, pos, self.skill_radius, self.line_color,
                       thickness=self.line_thickness, lineType=cv2.LINE_AA)

            x = pos[0]
            y = pos[1]
            # finally figured out how to center the text within the circle - DONE
            text_size, base_line = cv2.getTextSize(skill,self.font, self.font_scale, self.line_thickness)

            # text_pos = (x - self.skill_radius // 2, y + self.skill_radius // 4)
            text_pos = (x - text_size[0] // 2, y + text_size[1] // 2)
            cv2.putText(self.image, skill, text_pos, self.font, self.font_scale, self.line_color,
                        thickness=self.line_thickness, lineType=cv2.LINE_AA)



        return

    def get_image(self):
        return self.image