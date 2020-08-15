from svgutils.compose import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfFileMerger, PdfFileReader
from pathlib import Path
import svgutils.transform as st
from config import PROJECT_LOCATION, IMAGE_DIRECTORY, QUESTION_IDS, MCQ_OPTIONS_PER_QUESTION
import random

EXPORT_PATH_INDIVIDUAL_MCQ_PDF = PROJECT_LOCATION + 'Macros/Output/FormattedMCQs/IndividualMCQs-pdf/'
EXPORT_PATH_INDIVIDUAL_MCQ_SVG = PROJECT_LOCATION + 'Macros/Output/FormattedMCQs/IndividualMCQs-svg/'
EXPORT_PATH_MERGED_MCQ_PDF = PROJECT_LOCATION + 'Macros/Output/FormattedMCQs/MergedMCQs-OrthoToIso.pdf'
EXPORT_PATH_ISOMETRIC_WITH_FRONT_LABEL = PROJECT_LOCATION + 'Macros/Output/IsometricWithFrontLabel/'

# Add front arrow overlay to isometric question
labelArrow = PROJECT_LOCATION+'Macros/src/Resources/arrow.svg'
labelText = PROJECT_LOCATION+'Macros/src/Resources/front-text.svg'
labelTextTranslated = PROJECT_LOCATION+'Macros/src/Resources/translated-label-text.svg'
labelArrowTranslated = PROJECT_LOCATION+'Macros/src/Resources/translated-label-arrow.svg'

# Create required directories
Path(EXPORT_PATH_INDIVIDUAL_MCQ_PDF).mkdir(parents=True, exist_ok=True)
Path(EXPORT_PATH_INDIVIDUAL_MCQ_SVG).mkdir(parents=True, exist_ok=True)

# MCQ format settings
scaleOrthoAnswer = 0.05
scaleOrthoQuestion = 0.05
scaleIsoAnswer = 0.07
scaleIsoQuestion = 0.07
textWeight = 'bold'
textSize = 10

# Initialise the output pdf of merged mcqs
merger = PdfFileMerger()
j = 1
for i in QUESTION_IDS:
  # Translate the front label components
    Figure( "180cm", "180cm",
            SVG(labelArrow).scale(0.4)
            .move(790, 3550)
    ).save(labelArrowTranslated)
    Figure( "180cm", "200cm",
            SVG(labelText).scale(2.8)
            .move(320, 3700)
    ).save(labelTextTranslated)

    optionSuffixes = ['-1-Isometric.svg', '-2-Isometric.svg', '-3-Isometric.svg', '-4-Isometric.svg'];
    random.shuffle(optionSuffixes);

    svgPathPrefix = IMAGE_DIRECTORY + 'Q' + str(i)
    questionPath = svgPathPrefix + '-1-Orthographic.svg'
    optionAPath = svgPathPrefix + optionSuffixes[0];
    optionBPath = svgPathPrefix + optionSuffixes[1];
    optionCPath = svgPathPrefix + optionSuffixes[2];
    optionDPath = svgPathPrefix + optionSuffixes[3];

    for k in range(1, MCQ_OPTIONS_PER_QUESTION + 1):
        # Append front label to the isometric drawing
        drawingSvg = st.fromfile(svgPathPrefix + '-' + str(k) + '-Isometric.svg')
        labelArrowSvg = st.fromfile(labelArrowTranslated)
        labelTextSvg = st.fromfile(labelTextTranslated)
        drawingSvg.append(labelArrowSvg)
        drawingSvg.append(labelTextSvg)
        isometricWithLabelPath = EXPORT_PATH_ISOMETRIC_WITH_FRONT_LABEL + 'Q' + str(i) + '-' + str(k) + '-Isometric.svg'
        drawingSvg.save(isometricWithLabelPath)

    svgPagePath = EXPORT_PATH_INDIVIDUAL_MCQ_SVG + 'mcq-' + str(i) + '.svg'
    questionText = 'Question ' + str(j)
    Figure("29.7cm", "21.0cm", 
        Panel(
            SVG(questionPath).scale(scaleOrthoQuestion),
            Text(questionText, 25, 20, size=textSize, weight=textWeight)
            ),
        Panel(
            SVG(optionAPath).scale(scaleIsoAnswer),
            Text("A", 5, 20, size=textSize, weight=textWeight)
            ).move(280, 0),
        Panel(
            SVG(optionBPath).scale(scaleIsoAnswer),
            Text("B", 5, 20, size=textSize, weight=textWeight)
            ).move(280, 270),
        Panel(
            SVG(optionCPath).scale(scaleIsoAnswer),
            Text("C", 5, 20, size=textSize, weight=textWeight)
            ).move(550, 0),
        Panel(
            SVG(optionDPath).scale(scaleIsoAnswer),
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

