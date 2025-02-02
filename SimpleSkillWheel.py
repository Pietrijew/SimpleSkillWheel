import os.path
import cv2
import CsvInputLoader
from SkillWheelPainter import SkillWheelPainter


def generate_skill_wheel(input_directory='Input-7'):

    print("Loading scheme from {} ...", input_directory)
    scheme = CsvInputLoader.load_scheme(input_directory)
    print('Scheme loaded!')

    angle_ranges = scheme.get_categories_angle_ranges()
    print(angle_ranges)

    output_dir = 'Output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    painter = SkillWheelPainter(scheme=scheme, image_size=2048)
    painter.paint()
    image = painter.get_image()
    output_filename = os.path.basename(input_directory) + '_image.png'
    output_file = os.path.join(output_dir, output_filename)
    cv2.imwrite(output_file, image)


if __name__ == "__main__":
    # generate from example data
    generate_skill_wheel('Input-7')
    generate_skill_wheel('Input-8')
