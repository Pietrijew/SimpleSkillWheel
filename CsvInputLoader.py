import os
import os
import pandas
from SkillWheelScheme import SkillWheelScheme

def clear_nan(list_with_nan):
    cleaned_list = [x for x in list_with_nan if str(x) != 'nan']
    return cleaned_list

def load_scheme(input_directory):
    categories_file = os.path.join(input_directory, 'categories.csv')
    level1_file = os.path.join(input_directory, 'level_1.csv')
    level2_file = os.path.join(input_directory, 'level_2.csv')
    level3_file = os.path.join(input_directory, 'level_3.csv')
    levelX_file = os.path.join(input_directory, 'level_X.csv')
    hierarchy_file = os.path.join(input_directory, 'hierarchy.csv')

    categories_csv = pandas.read_csv(categories_file)
    categories = categories_csv.iloc[:, 0].to_list()

    level1_csv = pandas.read_csv(level1_file)
    level2_csv = pandas.read_csv(level2_file)
    level3_csv = pandas.read_csv(level3_file)
    levelX_csv = pandas.read_csv(levelX_file, header=None)
    hierarchy_csv = pandas.read_csv(hierarchy_file, header=None)

    level_1 = dict()
    level_2 = dict()
    level_3 = dict()
    for category in categories:
        level_1[category] = clear_nan(level1_csv[category].to_list())
        level_2[category] = clear_nan(level2_csv[category].to_list())
        level_3[category] = clear_nan(level3_csv[category].to_list())

    level_X = levelX_csv.iloc[:, 0].to_list()
    hierarchy = dict()
    for index, row in hierarchy_csv.iterrows():
        hierarchy[row.iloc[0]] = clear_nan(row.iloc[1:].to_list())

    print('Level 1:')
    print(level_1)
    print('Level 2:')
    print(level_2)
    print('Level 3:')
    print(level_3)
    print('Level X:')
    print(level_X)
    print('Hierarchy:')
    print(hierarchy)

    return SkillWheelScheme(
        categories=categories,
        level1=level_1,
        level2=level_2,
        level3=level_3,
        levelX=level_X,
        hierarchy=hierarchy
    )
    # print(categories_csv)
    # print('categories shape:', categories_csv.shape)
    # print(categories)




