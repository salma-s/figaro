class CentreArcInfo():
  def __init__(self, baseShapeType, x, y, dimension):
    if baseShapeType == 'QuarterShape':
      self.line1 = [-10, y, dimension + 10, y]
      self.line2 = [x, -10, x, dimension + 10]
    if baseShapeType == 'SemiCircle':
      self.line1 = [x[0] - 10, dimension, x[1] + 10, dimension]
      self.line2 = [dimension, y[0] - 10, dimension, y[1] + 10]
    if baseShapeType == "SemiHoleInCuboid":
      self.line1 = [x[0] - 10, dimension[1], x[1] + 10, dimension[1]]
      self.line2 = [dimension[0], y[0] - 10, dimension[0], y[1] + 10]
