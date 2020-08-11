from svgutils.compose import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import os.path
import os
from PyPDF2 import PdfFileMerger, PdfFileReader
import svgutils.transform as st
from pathlib import Path

PROJECT_LOCATION = '/Users/salmas/source/repos/part-iv-project/'
IMAGE_DIRECTORY = '/Users/salmas/source/repos/part-iv-project/Macros/Output/'
EXPORT_PATH_INDIVIDUAL_MCQ_PDF = PROJECT_LOCATION + 'Macros/Output/FormattedMCQs/IndividualMCQs-pdf/'
EXPORT_PATH_INDIVIDUAL_MCQ_SVG = PROJECT_LOCATION + 'Macros/Output/FormattedMCQs/IndividualMCQs-svg/'
EXPORT_PATH_MERGED_MCQ_PDF = PROJECT_LOCATION + 'Macros/Output/FormattedMCQs/mergedMCQs-IsoToOrtho.pdf'
EXPORT_PATH_ISOMETRIC_WITH_FRONT_LABEL = PROJECT_LOCATION + 'Macros/Output/IsometricWithFrontLabel/'
QUESTION_IDS = [1, 2, 3, 4, 5]

# Create required directories
Path(EXPORT_PATH_INDIVIDUAL_MCQ_PDF).mkdir(parents=True, exist_ok=True)
Path(EXPORT_PATH_INDIVIDUAL_MCQ_SVG).mkdir(parents=True, exist_ok=True)
Path(EXPORT_PATH_ISOMETRIC_WITH_FRONT_LABEL).mkdir(parents=True, exist_ok=True)

# Add front arrow overlay to isometric question
labelArrow = PROJECT_LOCATION+'Macros/src/Resources/arrow.svg'
labelText = PROJECT_LOCATION+'Macros/src/Resources/front-text.svg'
labelTextTranslated = PROJECT_LOCATION+'Macros/src/Resources/translated-label-text.svg'
labelArrowTranslated = PROJECT_LOCATION+'Macros/src/Resources/translated-label-arrow.svg'

# MCQ format settings
scaleOrthoAnswer = 0.05
scaleOrthoQuestion = 0.05
scaleIsoAnswer = 0.07
scaleIsoQuestion = 0.07
textWeight = 'bold'
textSize = 10

# # Initialise the output pdf of merged mcqs
merger = PdfFileMerger()
j = 1
for i in QUESTION_IDS:
    # Translate the front label components
    Figure( "180cm", "180cm",
            SVG(labelArrow).scale(0.4)
            .move(790, 3600)
    ).save(labelArrowTranslated)
    Figure( "180cm", "200cm",
            SVG(labelText).scale(3)
            .move(320, 3900)
    ).save(labelTextTranslated)

    svgPathPrefix = IMAGE_DIRECTORY + 'Q' + str(i)

    # Append front label to the isometric drawing
    drawingSvg = st.fromfile(svgPathPrefix + '-1-Isometric.svg')
    labelArrowSvg = st.fromfile(labelArrowTranslated)
    labelTextSvg = st.fromfile(labelTextTranslated)
    drawingSvg.append(labelArrowSvg)
    drawingSvg.append(labelTextSvg)
    isometricWithLabelPath = EXPORT_PATH_ISOMETRIC_WITH_FRONT_LABEL + 'Q' + str(i) + '-1-Isometric-with-front-label.svg'
    drawingSvg.save(isometricWithLabelPath)

    questionPath = isometricWithLabelPath
    optionAPath = svgPathPrefix + '-1-Orthographic.svg'
    optionBPath = svgPathPrefix + '-2-Orthographic.svg'
    optionCPath = svgPathPrefix + '-3-Orthographic.svg'
    optionDPath = svgPathPrefix + '-4-Orthographic.svg'

    svgPagePath = EXPORT_PATH_INDIVIDUAL_MCQ_SVG + 'mcq-' + str(i) + '.svg'
    questionText = 'Question ' + str(j)
    Figure("29.7cm", "21.0cm", 
        Panel(
            SVG(questionPath).scale(scaleIsoQuestion),
            Text(questionText, 25, 20, size=textSize, weight=textWeight)
            ),
        Panel(
            SVG(optionAPath).scale(scaleOrthoAnswer),
            Text("A", 5, 20, size=textSize, weight=textWeight)
            ).move(280, 0),
        Panel(
            SVG(optionBPath).scale(scaleOrthoAnswer),
            Text("B", 5, 20, size=textSize, weight=textWeight)
            ).move(550, 0),
        Panel(
            SVG(optionCPath).scale(scaleOrthoAnswer),
            Text("C", 5, 20, size=textSize, weight=textWeight)
            ).move(280, 270),
        Panel(
            SVG(optionDPath).scale(scaleOrthoAnswer),
            Text("D", 5, 20, size=textSize, weight=textWeight)
            ).move(550, 270)
        ).save(svgPagePath)

    # Convert the page to PDF and add it to the collated pages 
    pdfPagePath = EXPORT_PATH_INDIVIDUAL_MCQ_PDF + 'mcq-' + str(i) + '.pdf'
    renderPDF.drawToFile(svg2rlg(svgPagePath), pdfPagePath)
    page = open(pdfPagePath, "rb")
    merger.append(page)

    j = j + 1

# save PDF of all pages
output = open(EXPORT_PATH_MERGED_MCQ_PDF, "wb")
merger.write(output)

