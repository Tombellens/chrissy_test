import math
import datetime
import os
from random import shuffle

from CsvFileWriter import CsvFileWriter
from VisualStimulus import VisualStimulus
from psychopy import visual, event, clock
from win32api import GetSystemMetrics
from PIL import Image

# define constants / project settings
REFRESH_RATE = 60
FRAME_DURATION_IN_MILLIES = 1000 / REFRESH_RATE
IMG_DIMENSIONS=[800,600]


FIXATION_DURATION_IN_MILLIES = 500
IMG_STIMULUS_DURATION_IN_MILLIES = 53
MASK_DURATION_IN_MILLIES = 500
TOP_LEVEL_DIRECTORIES = ["threatening", "non-threatening"]
FIRST_SUB_LEVEL_DIRECTORIES = ["full", "low", "high"]
OUTPUT_FILE_NAME = "threat_detection_exp"
PC_NAME = "PC_1"
FULL_OUTPUT_FILE_NAME = OUTPUT_FILE_NAME + "_" + PC_NAME
FIELD_NAMES_GENERAL_INFO = ["PARTICIPANT_ID", "EXPERIMENT_STARTED", "PC_NAME", "TRIALS"]
FIELD_NAMES_TRIAL_INFO = ["PARTICIPANT_ID", "RANK", "IS_THREATENING", "SPATIAL_FREQUENCY", "IMG_NAME", "KEY_PRESSED",
                          "CORRECT_ANSWER", "REACTION_TIME_IN_MILLIES"]
#to be deleted once funcitonality for the participant to fill in his own id is implemented
PARTICIPANT_ID = 1

# define utility methods
def get_frames_by_millieseconds(duration_in_millies):
    return math.ceil(duration_in_millies / FRAME_DURATION_IN_MILLIES)

#MAIN SCRIPT
# read visual stimuli from files into experiment
visual_stimuli = []
for directoryN in range(len(TOP_LEVEL_DIRECTORIES)):
    for first_subdirectoryN in range(len(FIRST_SUB_LEVEL_DIRECTORIES)):
        second_sub_level_directories = os.listdir(
            "img/" + TOP_LEVEL_DIRECTORIES[directoryN] + "/" + FIRST_SUB_LEVEL_DIRECTORIES[first_subdirectoryN])
        for second_subdirectoryN in range(len(second_sub_level_directories)):
            visual_stimuli.append(
                VisualStimulus(TOP_LEVEL_DIRECTORIES[directoryN], FIRST_SUB_LEVEL_DIRECTORIES[first_subdirectoryN],
                               second_sub_level_directories[second_subdirectoryN],
                               Image.open("img/" + TOP_LEVEL_DIRECTORIES[directoryN] + "/" +
                                          FIRST_SUB_LEVEL_DIRECTORIES[first_subdirectoryN] + "/" +
                                          second_sub_level_directories[second_subdirectoryN])))
fileWriter = CsvFileWriter(FULL_OUTPUT_FILE_NAME, FIELD_NAMES_TRIAL_INFO)

# set-up the window
window = visual.Window([GetSystemMetrics(0), GetSystemMetrics(1)], monitor="testMonitor", units="deg")
fixation_cross = visual.ShapeStim(window,
                                  vertices=((0, -0.5), (0, 0.5), (0, 0), (-0.5, 0), (0.5, 0)),
                                  lineWidth=5,
                                  closeShape=False,
                                  lineColor="white"
                                  )
grating_stimulus = visual.GratingStim(window, tex='sin', mask='gauss', sf=5, size=10,
                                      name='gabor', autoLog=False)
fixation_duration_in_frames = get_frames_by_millieseconds(FIXATION_DURATION_IN_MILLIES)
stimulus_duration_in_frames = get_frames_by_millieseconds(IMG_STIMULUS_DURATION_IN_MILLIES)
mask_duration_in_frames = get_frames_by_millieseconds(MASK_DURATION_IN_MILLIES)
total_duration_in_frames = fixation_duration_in_frames + stimulus_duration_in_frames + mask_duration_in_frames

#randomize stimuli order
shuffle(visual_stimuli)

#main loop
for visualImageStimN in range(len(visual_stimuli)):
    visual_stimulus = visual_stimuli[visualImageStimN]
    column_data = [str(PARTICIPANT_ID), str(visualImageStimN), visual_stimulus.isThreatening, visual_stimulus.spatialFrequency,
                   visual_stimulus.name]
    image_stimulus = visual.ImageStim(image=visual_stimuli[visualImageStimN].img.resize((IMG_DIMENSIONS[0], IMG_DIMENSIONS[1])), win=window)

    #display the fixation, the image stimulus and the mask/ grating
    for frameN in range(total_duration_in_frames):
        if 0 <= frameN < fixation_duration_in_frames:
            fixation_cross.draw()
        if fixation_duration_in_frames <= frameN < fixation_duration_in_frames + stimulus_duration_in_frames:
            image_stimulus.draw()
        if fixation_duration_in_frames + stimulus_duration_in_frames <= frameN:
            grating_stimulus.draw()
        window.flip()

    #display the message-screen
    message1 = visual.TextStim(win=window, pos=[0, +2], text='S = Threatening')
    message2 = visual.TextStim(win=window, pos=[0, -2], text='L = Non-threatening')
    message1.draw()
    message2.draw()
    window.flip()

    #register the answer
    rightKeyReleased = False
    key = ""
    initialTime = datetime.datetime.now()
    accurate_answer = False
    selected_key = ""
    while not rightKeyReleased:
        allKeys = event.waitKeys()
        keyDownTime = datetime.datetime.now()
        for key in allKeys:
            if key == "s":
                rightKeyReleased = True
                selected_key = "s"
                if visual_stimulus.isThreateningBool: accurate_answer = True
            if key == "l":
                rightKeyReleased = True
                selected_key = "l"
                if visual_stimulus.isThreateningBool is not True: accurate_answer = True

    time_elapsed_in_millies = (keyDownTime - initialTime).microseconds / 1000

    #write the answer to the csv table
    column_data.append(selected_key)
    column_data.append(str(accurate_answer))
    column_data.append(str(time_elapsed_in_millies))
    fileWriter.add_row(column_data)
