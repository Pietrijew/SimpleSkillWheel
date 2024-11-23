import os.path
import cv2
import CsvInputLoader
from SkillWheelPainter import SkillWheelPainter

def generate_skill_wheel():
    input_dir = 'Input'
    print("Loading scheme from {} ...", input_dir)
    scheme = CsvInputLoader.load_scheme(input_dir)
    print('Scheme loaded!')

    angle_ranges = scheme.get_categories_angle_ranges()
    print(angle_ranges)

    output_dir = 'Output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    painter = SkillWheelPainter(scheme=scheme, image_size=2048)
    painter.paint()
    image = painter.get_image()
    output_file = os.path.join(output_dir, 'image.png')
    cv2.imwrite(output_file, image)


if __name__ == "__main__":
    generate_skill_wheel()
