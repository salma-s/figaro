# -----------------   Config    -----------------
# Set all config here before running Main.FCMacro
# -----------------------------------------------

EXPORT_FOLDER_PATH = '/Users/gargi/Fourth Year Projects/P4P/Output/Temp'
TEMPLATE_PATH_ISO = '/Users/gargi/Fourth Year Projects/P4P/Templates/blank-iso.svg'
TEMPLATE_PATH_ORTHO= '/Users/gargi/Fourth Year Projects/P4P/Templates/blank-ortho.svg'

# Size of the matrix
MATRIX_X = 2
MATRIX_Y = 2
MATRIX_Z = 2

# Size (length, width, height) of a unit in the matrix
UNIT = 100

# Complexity of features in a shape
SHAPE_COMPLEXITY = 'SIMPLE' # "SIMPLE", "NORMAL", "COMPLEX"

# Type of mutation to apply to create distractors in MCQs
DISTRACTOR_TYPE = 'DISSIMILAR' # "DISSIMILAR", "SIMILAR", "DIFF_ROTATION"

# MCQ Options per Question. Count is inclusive of correct answer.
# Not more than 4 is recommended for a DIFF_ROTATION distractor type.
MCQ_OPTIONS_PER_QUESTION = 1

NUMBER_OF_MCQS = 1 # The number of MCQs to generate

MCQ_START_NUM = 1 # The question number of the first MCQ outputted

# Directory of project
# Required for MCQMergerIsoToOrtho and MCQMergerOrthoToIso
PROJECT_LOCATION = '/Users/salmas/source/repos/part-iv-project/'

# Directory contaning individual iso and ortho SVGs to be converted into formatted MCQs
# Required for MCQMergerIsoToOrtho and MCQMergerOrthoToIso
IMAGE_DIRECTORY = '/Users/salmas/source/repos/part-iv-project/Macros/Output/'

