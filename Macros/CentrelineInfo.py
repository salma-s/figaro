class CentrelineInfo():
  
  def __init__(self, x, y, z, start, end, centreArcLen):
    self.x = x # None for Right view
    self.y = y # None for Front view
    self.z = z # None for Top view
    self.start = start
    self.end = end
    self.centreArcLen = centreArcLen
