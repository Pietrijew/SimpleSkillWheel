import math


class SkillWheelScheme:
  def __init__(self, categories, level1, level2, level3, levelX, hierarchy):
    self.categories = categories
    self.level1 = level1
    self.level2 = level2
    self.level3 = level3
    self.levelX = levelX
    self.hierarchy = hierarchy

  def __getitem__(self, key):
    # print("Inside `__getitem__` method!")
    return getattr(self, key)

  def get_categories_angle_ranges(self):
    angle_ranges = dict()
    n_categories = len(self.categories)
    if n_categories == 0:
      raise ValueError('There must be at least one category, you dumb fuck!')
    angle_per_category = 2*math.pi / n_categories
    for i in range(n_categories):
      # use tuples
      angle_ranges[self.categories[i]] = (i*angle_per_category, (i+1)*angle_per_category)
    return angle_ranges