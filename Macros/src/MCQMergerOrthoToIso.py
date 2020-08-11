from svgutils.compose import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import os.path
import os
from PyPDF2 import PdfFileMerger, PdfFileReader

IMAGE_DIRECTORY = '/Users/salmas/source/repos/part-iv-project/Macros/Output/'
EXPORT_PATH_INDIVIDUAL_MCQ_PDF = '/Users/salmas/source/repos/part-iv-project/Macros/Output/FormattedMCQs/IndividualMCQs-pdf/'
EXPORT_PATH_INDIVIDUAL_MCQ_SVG = '/Users/salmas/source/repos/part-iv-project/Macros/Output/FormattedMCQs/IndividualMCQs-svg/'
EXPORT_PATH_MERGED_MCQ_PDF = '/Users/salmas/source/repos/part-iv-project/Macros/Output/FormattedMCQs/mergedMCQs.pdf'
QUESTION_IDS = [1, 2, 3, 4, 5]

# Add front arrow overlay to isometric question

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
    questionPath = IMAGE_DIRECTORY + 'Q' + str(i) + '-1-Orthographic.svg'
    optionAPath = IMAGE_DIRECTORY + 'Q' + str(i) + '-1-Isometric.svg'
    optionBPath = IMAGE_DIRECTORY + 'Q' + str(i) + '-2-Isometric.svg'
    optionCPath = IMAGE_DIRECTORY + 'Q' + str(i) + '-3-Isometric.svg'
    optionDPath = IMAGE_DIRECTORY + 'Q' + str(i) + '-4-Isometric.svg'

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
            ).move(550, 0),
        Panel(
            SVG(optionCPath).scale(scaleIsoAnswer),
            Text("C", 5, 20, size=textSize, weight=textWeight)
            ).move(280, 270),
        Panel(
            SVG(optionDPath).scale(scaleIsoAnswer),
            Text("D", 5, 20, size=textSize, weight=textWeight)
            ).move(550, 270)
        ).save(svgPagePath)

    # Convert the page to PDF and add it to the collated pages 
    pdfPagePath = EXPORT_PATH_INDIVIDUAL_MCQ_PDF + 'mcq-' + str(i) + '.pdf'
    print(svgPagePath)
    renderPDF.drawToFile(svg2rlg(svgPagePath), pdfPagePath)
    page = open(pdfPagePath, "rb")
    merger.append(page)

    j = j + 1

# save PDF of all pages
output = open(EXPORT_PATH_MERGED_MCQ_PDF, "wb")
merger.write(output)

