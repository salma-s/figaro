from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import glob, os
from config import IMAGE_DIRECTORY_FOR_SVG_TO_PNG

os.chdir(IMAGE_DIRECTORY_FOR_SVG_TO_PNG)
for svgFile in glob.glob("*.svg"):
    drawing = svg2rlg(svgFile)
    pngFilename = os.path.splitext(svgFile)[0]+'.png'
    renderPM.drawToFile(drawing, pngFilename, fmt = "PNG")
