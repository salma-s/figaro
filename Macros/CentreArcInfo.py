class CentreArcInfo():
  def __init__(self, baseShapeType, x, y, dimension):
    if baseShapeType == 'QuarterShape':
      self.line1 = [-10, y, dimension + 10, y]
      self.line2 = [x, -10, x, dimension + 10]
