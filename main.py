import csv
import math
import datetime
import os
import time
import tkinter as tk
import webbrowser
from random import shuffle

from VisualStimulus import VisualStimulus
from psychopy import visual, event, clock
from win32api import GetSystemMetrics
from PIL import Image, ImageTk

# define constants / project settings
REFRESH_RATE = 60
FRAME_DURATION_IN_MILLIES = 1000 / REFRESH_RATE
IMG_DIMENSIONS = [800, 600]

FIXATION_DURATION_IN_MILLIES = 500
IMG_STIMULUS_DURATION_IN_MILLIES = 53
MASK_DURATION_IN_MILLIES = 500

TOP_LEVEL_DIRECTORIES = [["threatening", ["snake","wasp"]], ["non-threatening",["salamander", "fly"]]]
#TOP_LEVEL_DIRECTORIES = [["threatening", ["snake"]], ["non-threatening",[]]]
THIRD_AND_FOURTH_SUB_LEVEL_DIRECTORIES = [["NoFilter", "contrast-normalized"], ["LSF", "contrast-normalized"],
                                          ["LSF", "no-normalization"], ["HSF", "contrast-normalized"],
                                          ["HSF", "no-normalization"], ["NoFilter", "contrast-normalized"]]
MASK_DIRECTORY = "img/masks"

OUTPUT_FILE_NAME = "threat_detection_exp"
PC_NAME = "PC_1"
FULL_OUTPUT_FILE_NAME = OUTPUT_FILE_NAME + "_" + PC_NAME
FIELD_NAMES_TRIAL_INFO = ["PARTICIPANT_ID", "EXPERIMENT_STARTED", "PC_NAME", "TRIALS", "EMS_NUMBER", "AGE", "VISION", "DEBRIEFING", "RANK", "IS_THREATENING", "SPATIAL_FREQUENCY","CONTRAST-NORMALIZATION", "IMG_NAME","MASK_NAME", "KEY_PRESSED",
                          "CORRECT_ANSWER", "REACTION_TIME_IN_MILLIES", "EST_DISPLAY_TIME"]
PARTICIPANT_INFO_FILE_NAME = "threat_detection_exp_participants"
FIELD_NAMES_PARTICIPANT_INFO_FILE = ["PARTICIPANT_ID", "EMS_NUMBER", "AGE", "VISION", "DEBRIEFING"]

EVEN_KEY_DISTRIBUTION = ['s', 'l']
ODD_KEY_DISTRIBUTION = ['l', 's']

TEXT_FONT_SIZE = 12
TEXT_FONT = "Arial"

PARTICIPANT_ID = 0
EMS_ID = 0
AGE = 18
GENDER = "M"
VISION = "Ja"
DEBRIEFING = "Ja"

QUALTRICS_LINK = "https://kuleuven.eu.qualtrics.com/jfe/form/SV_0Al2O4TyMhY6uxw"

# define utility methods
def get_frames_by_millieseconds(duration_in_millies):
    return math.ceil(duration_in_millies / FRAME_DURATION_IN_MILLIES)


def create_filter_conditions_list(total_elements):
    n = 0
    i = 0
    filter_conditions_list = []
    while n < total_elements:
        filter_conditions_list.append(THIRD_AND_FOURTH_SUB_LEVEL_DIRECTORIES[i])
        if i == len(THIRD_AND_FOURTH_SUB_LEVEL_DIRECTORIES)-1:
            i = 0
        n = n+1
        i = i+1
    return filter_conditions_list

def get_key_distribution_by_id(participant_id):
    key_distribution = []
    if (participant_id % 2) == 0:
        key_distribution = EVEN_KEY_DISTRIBUTION
    else:
        key_distribution = ODD_KEY_DISTRIBUTION
    return key_distribution

#define utility classes
class CsvFileWriter:
    def __init__(self, csvFileName, fieldsArray):
        try:
            self.file = open("data/" + csvFileName + ".csv", "r")
        except FileNotFoundError:
            self.file = open("data/" + csvFileName + ".csv", "a+")
            self.file.write(self.column_array_into_csv_string(fieldsArray))
            return
        self.file = open("data/" + csvFileName + ".csv", "a+")


    def column_array_into_csv_string(self, column_array):
        csv_string = ""
        for column in range(len(column_array)):
            if column == 0:
                csv_string = str(column_array[column])
                continue
            if column == (len(column_array)-1):
                csv_string = csv_string + "," + str(column_array[column]) + "\n"
                continue
            csv_string = csv_string + "," + str(column_array[column])

        return csv_string

    def add_row(self, column_array):
        self.file.write(self.column_array_into_csv_string(column_array))

class CsvFileReader:
    def __init__(self, file_name):
        self.file_name = file_name
    def read_last_line(self):
        with open('data/' + self.file_name + ".csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            last_row = []
            for row in csv_reader:
                last_row = row
            return last_row

#define initial frames
class WelcomeFrame:
    def __init__(self, root):
        self.root = root
        self.rootFrame = tk.Frame(self.root, width=GetSystemMetrics(0), height=GetSystemMetrics(1))
        self.textFrame = tk.Frame(self.rootFrame, width=GetSystemMetrics(0) / 3, height=GetSystemMetrics(1) / 5)
        self.pictureFrame = tk.Frame(self.rootFrame, width=GetSystemMetrics(0) / 3, height=GetSystemMetrics(1) / 5)
        self.buttonFrame = tk.Frame(self.rootFrame, width=GetSystemMetrics(0) / 3, height=GetSystemMetrics(1) / 5)

    def next_window(self):
        participant_frame = ParticipantInfoFrame(self.rootFrame)
        self.textFrame.destroy()
        self.pictureFrame.destroy()
        self.buttonFrame.destroy()
        participant_frame.draw()

    def draw(self):
        self.root.geometry(str(GetSystemMetrics(0)) + "x" + str(GetSystemMetrics(1)))
        self.root.title("Welcome")
        welcome_text = tk.Label(self.textFrame,
                                text="Dear participant, \nThank you for participating in this experiment.\nThe "
                                     "goal of this experiment is to study the importance of spatial frequency "
                                     "information in rapid threat detection.\nThroughout evolution, rapid threat "
                                     "detection has always been an advantage for survival. \nResearchers believe "
                                     "that humans and non-human primates adapted to danger in their environments "
                                     "and became faster at detecting threatening stimuli vs "
                                     "non-threatening stimuli.\nThese findings were confirmed in experiments with "
                                     "babies, children, and adults. However, which visual features allow for this "
                                     "rapid threat detection?\nIn this experiment, we will study the role of high "
                                     "and low spatial frequency information in rapid threat detection.",
                                justify=tk.LEFT)
        welcome_text.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        welcome_text.pack(side=tk.TOP)

        self.pictureFrame.columnconfigure([0, 1], minsize=200)
        self.pictureFrame.rowconfigure([0, 1], minsize=50)
        label_LSF_example = tk.Label(self.pictureFrame, text="This is an example of a Low Spatial Frequency")
        label_LSF_example.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        label_LSF_example.grid(row=0, column=0, padx=100)
        label_HSF_example = tk.Label(self.pictureFrame, text="This is an example of a High Spatial Frequency")
        label_HSF_example.grid(row=0, column=1, padx=100)
        label_HSF_example.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        lsf_example_canvas = tk.Canvas(self.pictureFrame, width=400, height=250)
        hsf_example_canvas = tk.Canvas(self.pictureFrame, width=400, height=250)
        lsf_img_example = ImageTk.PhotoImage(Image.open("img/examples/lsf_example.png").resize((400, 250)))
        hsf_img_example = ImageTk.PhotoImage(Image.open("img/examples/hsf_example.png").resize((400, 250)))
        lsf_example_canvas.grid(row=1, column=0)
        hsf_example_canvas.grid(row=1, column=1)
        lsf_example_canvas.create_image(0, 0, anchor=tk.NW, image=lsf_img_example)
        hsf_example_canvas.create_image(0, 0, anchor=tk.NW, image=hsf_img_example)

        next_button = tk.Button(self.buttonFrame, text="Next", command=self.next_window)
        next_button.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        next_button.pack()

        self.rootFrame.pack(fill="both", expand=True, padx=20, pady=20)
        self.textFrame.place(in_=self.rootFrame, anchor="c", relx=.5, rely=.15)
        self.pictureFrame.place(in_=self.rootFrame, anchor="c", relx=.5, rely=.5)
        self.buttonFrame.place(in_=self.rootFrame, anchor="c", relx=.5, rely=.75)

        self.root.mainloop()

class ParticipantInfoFrame:
    def __init__(self, root):
        self.rootFrame= root
        self.questionFrame = tk.Frame(self.rootFrame, width=GetSystemMetrics(0) / 3, height=GetSystemMetrics(1) / 5)
        self.buttonFrame = tk.Frame(self.rootFrame, width=GetSystemMetrics(0) / 3, height=GetSystemMetrics(1) / 5)
        self.participant_id_field = tk.Entry(self.questionFrame)
        self.ems_id_field = tk.Entry(self.questionFrame)
        self.age_field = tk.Entry(self.questionFrame)
        self.gender_field = tk.Entry(self.questionFrame)
        self.vision_field = tk.Entry(self.questionFrame)
        self.debriefing_field = tk.Entry(self.questionFrame)

    def check_for_completeness(self):
        if self.participant_id_field.get() is not "" and self.ems_id_field.get() is not "" and self.age_field.get() is not "" and self.gender_field.get() is not "" and self.vision_field.get() is not "" and self.debriefing_field.get() is not "":
            fileWriter = CsvFileWriter(PARTICIPANT_INFO_FILE_NAME, FIELD_NAMES_PARTICIPANT_INFO_FILE)
            columnData = [self.participant_id_field.get(), self.ems_id_field.get(), self.age_field.get(), self.gender_field.get(), self.vision_field.get(), self.debriefing_field.get()]
            fileWriter.add_row(columnData)

            self.questionFrame.destroy()
            self.buttonFrame.destroy()

            informed_consent = InformedConsent(self.rootFrame)
            informed_consent.draw()


    def draw(self):
        self.questionFrame.columnconfigure([0, 1], minsize=100)
        self.questionFrame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=100)
        participant_id_label = tk.Label(self.questionFrame, text="Participant Number: ")
        participant_id_label.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        participant_id_label.grid(row=0, column=0, padx=100)
        self.participant_id_field.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        self.participant_id_field.grid(row=0, column=1, padx=20)

        ems_id_label = tk.Label(self.questionFrame, text="EMS Number: ")
        ems_id_label.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        ems_id_label.grid(row=1, column=0, padx=100)
        self.ems_id_field.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        self.ems_id_field.grid(row=1, column=1, padx=20)

        age_label = tk.Label(self.questionFrame, text="Age: ")
        age_label.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        age_label.grid(row=2, column=0, padx=100)
        self.age_field.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        self.age_field.grid(row=2, column=1, padx=20)

        gender_label = tk.Label(self.questionFrame, text="Gender (M/F/X/ I do not want to answer): ")
        gender_label.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        gender_label.grid(row=3, column=0, padx=100)
        self.gender_field.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        self.gender_field.grid(row=3, column=1, padx=20)

        vision_label = tk.Label(self.questionFrame, text="I have normal OR corrected to normal vision (Yes/ No): ")
        vision_label.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        vision_label.grid(row=4, column=0, padx=100)
        self.vision_field.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        self.vision_field.grid(row=4, column=1, padx=20)
        
        debriefing_label = tk.Label(self.questionFrame, text="Notify me about the results once the study is completed (Yes/ No): ")
        debriefing_label.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        debriefing_label.grid(row=5, column=0, padx=100)
        self.debriefing_field.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        self.debriefing_field.grid(row=5, column=1, padx=20)

        self.rootFrame.pack(fill="both", expand=True, padx=20, pady=20)
        self.questionFrame.place(in_=self.rootFrame, anchor="c", relx=.5, rely=.15)
        self.questionFrame.pack()

        next_button = tk.Button(self.buttonFrame, text="Next", command=self.check_for_completeness)
        next_button.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        next_button.pack()
        self.buttonFrame.place(in_=self.rootFrame, anchor="c", relx=.5, rely=.75)
        self.buttonFrame.pack()


class InformedConsent:
    def __init__(self, root_frame):
        self.root_frame = root_frame
        self.button_frame = tk.Frame(self.root_frame, width=GetSystemMetrics(0) / 3, height=GetSystemMetrics(1) / 5)
        self.consent_canvas = tk.Canvas(self.root_frame, width=700, height=900)

    def next_screen(self):
        self.button_frame.destroy()
        self.consent_canvas.destroy()
        experiment_information = ExperimentInformation(self.root_frame)
        experiment_information.draw()

    def draw(self):
        global consent_image
        next_button = tk.Button(self.button_frame, text="I Agree", command=self.next_screen)
        next_button.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        next_button.pack()
        self.button_frame.place(in_=self.root_frame, anchor="c", relx=.5, rely=.9)

        consent_image = ImageTk.PhotoImage(Image.open("img/examples/informedconsent.png").resize((700, 900)))
        self.consent_canvas.create_image(20, 20, anchor=tk.NW, image=consent_image)
        self.consent_canvas.place(in_=self.root_frame, anchor="c", relx=.5, rely=0.40)

class ExperimentInformation:
    def __init__(self, root_frame):
        self.root_frame = root_frame
        self.text_frame = tk.Frame(self.root_frame, width=GetSystemMetrics(0) / 3, height=GetSystemMetrics(1) / 5)
        self.button_frame = tk.Frame(self.root_frame, width=GetSystemMetrics(0) / 3, height=GetSystemMetrics(1) / 5)

    def next_screen(self):
        self.root_frame.master.destroy()
    def draw(self):
        fileReader = CsvFileReader(PARTICIPANT_INFO_FILE_NAME)
        participant_id = int(fileReader.read_last_line()[0])
        key_distribution = get_key_distribution_by_id(participant_id)

        next_button = tk.Button(self.button_frame, text="Next", command=self.next_screen)
        next_button.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        next_button.pack()
        self.button_frame.place(in_=self.root_frame, anchor="c", relx=.5, rely=0.75)

        welcome_text = tk.Label(self.text_frame,
                                text="Information about the experiment:\n\nDuring the experiment, different pictures "
                                     "of snakes, salamanders, wasps, and flies will be \nshown in a visual computer "
                                     "task. First, you will see a fixation cross at the center of the screen.\nPlease "
                                     "look at the cross when it is shown. Then the cross will be followed by a "
                                     "picture. The\npicture will flash on the screen very quickly and then be "
                                     "immediately covered, so make sure\nyou are paying attention. Finally, "
                                     "you will have to respond whether the picture you saw was a\nthreatening or "
                                     "non-threatening animal.\n\nTo register your answer, please press " + key_distribution[0].capitalize() + " on the keyboard for a threatening stimulus and " + key_distribution[1].capitalize() + " for\na non-threatening stimulus. The key labels will always be repeated on the screen when you\nneed to answer. Try your best to respond as quickly and as accurately as possible. Sometimes\nthe pictures will be blurry or hard to see, but please try to respond as best as you can. You will\nnot receive feedback when you give your answer. You will receive short breaks throughout\nthe experiment. The experiment will end with a short survey.\n\n\nBe aware, if you press next the actual experiment will start. If you have any questions before\nthe start of the experiment, please contact the researcher.",
                                justify=tk.LEFT)
        welcome_text.config(font=(TEXT_FONT, TEXT_FONT_SIZE))
        welcome_text.pack(side=tk.TOP)
        self.text_frame.place(in_=self.root_frame,anchor="c", relx=.5, rely=.25)

# MAIN SCRIPT
# read visual stimuli from files into experiment
visual_stimuli = []
for directoryN in range(len(TOP_LEVEL_DIRECTORIES)):
    for first_subdirectoryN in range(len(TOP_LEVEL_DIRECTORIES[directoryN][1])):
        second_sub_level_directories = os.listdir(
            "img/" + TOP_LEVEL_DIRECTORIES[directoryN][0] + "/" + TOP_LEVEL_DIRECTORIES[directoryN][1][first_subdirectoryN])
        filter_conditions = create_filter_conditions_list(len(second_sub_level_directories))
        shuffle(filter_conditions)
        for second_subdirectoryN in range(len(second_sub_level_directories)):
            isThreatening = TOP_LEVEL_DIRECTORIES[directoryN][0]
            animal = TOP_LEVEL_DIRECTORIES[directoryN][1][first_subdirectoryN]
            id = second_sub_level_directories[second_subdirectoryN]
            spatialFrequency = filter_conditions[second_subdirectoryN][0]
            contrastNormalization = filter_conditions[second_subdirectoryN][1]
            name = os.listdir("img/" + isThreatening + "/" + animal + "/" +second_sub_level_directories[second_subdirectoryN] + "/" + spatialFrequency + "/" + contrastNormalization)[0].split('.pn')[0]
            visual_stimuli.append(
                VisualStimulus(isThreatening, spatialFrequency, contrastNormalization, name,
                               Image.open("img/" + isThreatening + "/" +
                                          animal + "/" +
                                          second_sub_level_directories[second_subdirectoryN] + "/" +
                                          spatialFrequency + "/" + contrastNormalization + "/" + name + ".png" )))
fileWriter = CsvFileWriter(FULL_OUTPUT_FILE_NAME, FIELD_NAMES_TRIAL_INFO)

#read masks into experiment
mask_img = []
for mask_file_directory in os.listdir(MASK_DIRECTORY):
    mask_img.append(Image.open(MASK_DIRECTORY + '/' + mask_file_directory))


#Initial frames

root_window = tk.Tk()

welcome_frame = WelcomeFrame(root_window)
welcome_frame.draw()

fileReader = CsvFileReader(PARTICIPANT_INFO_FILE_NAME)
participant_info = fileReader.read_last_line()
PARTICIPANT_ID = int(participant_info[0])
EMS_ID = participant_info[1]
AGE = participant_info[2]
VISION = participant_info[3]
DEBRIEFING = participant_info[4]
TIME_STARTED = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
TRIALS = len(visual_stimuli)

# set-up the window for the experiment
window = visual.Window([GetSystemMetrics(0), GetSystemMetrics(1)], monitor="testMonitor", units="deg")
fixation_cross = visual.ShapeStim(window,
                                  vertices=((0, -0.5), (0, 0.5), (0, 0), (-0.5, 0), (0.5, 0)),
                                  lineWidth=5,
                                  closeShape=False,
                                  lineColor="white"
                                  )
fixation_duration_in_frames = get_frames_by_millieseconds(FIXATION_DURATION_IN_MILLIES)
stimulus_duration_in_frames = get_frames_by_millieseconds(IMG_STIMULUS_DURATION_IN_MILLIES)
mask_duration_in_frames = get_frames_by_millieseconds(MASK_DURATION_IN_MILLIES)
total_duration_in_frames = fixation_duration_in_frames + stimulus_duration_in_frames + mask_duration_in_frames

# randomize stimuli & mask order
shuffle(visual_stimuli)
shuffle(mask_img)

#break before experiment starts
time.sleep(3)
#pick right key distribution-set
key_distribution = get_key_distribution_by_id(PARTICIPANT_ID)

# main loop for the experiment
for visualImageStimN in range(len(visual_stimuli)):
    visual_stimulus = visual_stimuli[visualImageStimN]
    column_data = [str(PARTICIPANT_ID), TIME_STARTED, PC_NAME, str(TRIALS), str(EMS_ID), str(AGE), VISION, DEBRIEFING, str(visualImageStimN), visual_stimulus.isThreatening,
                   visual_stimulus.spatialFrequency,
                   visual_stimulus.contrastNormalization,
                   visual_stimulus.name,
                   mask_img[visualImageStimN].filename.replace(MASK_DIRECTORY, "")]
    image_stimulus = visual.ImageStim(
        image=visual_stimuli[visualImageStimN].img.resize((IMG_DIMENSIONS[0], IMG_DIMENSIONS[1])), win=window)
    mask_stimulus = visual.ImageStim(
        image = mask_img[visualImageStimN].resize((IMG_DIMENSIONS[0], IMG_DIMENSIONS[1])), win=window)

    # display the fixation, the image stimulus and the mask/ grating

    display_initial_time = 0;
    display_stop_time = 0;
    for frameN in range(total_duration_in_frames):
        if 0 <= frameN <= fixation_duration_in_frames:
            fixation_cross.draw()
            display_initial_time = datetime.datetime.now()
        if fixation_duration_in_frames < frameN < fixation_duration_in_frames + stimulus_duration_in_frames:
            image_stimulus.draw()
            display_stop_time = datetime.datetime.now()
        if fixation_duration_in_frames + stimulus_duration_in_frames <= frameN:
            mask_stimulus.draw()
        window.flip()

    display_time_elapsed_in_millies = (display_stop_time - display_initial_time).microseconds / 1000
    # display the message-screen
    message1 = visual.TextStim(win=window, pos=[0, +2], text=key_distribution[0].capitalize() + ' = Threatening')
    message2 = visual.TextStim(win=window, pos=[0, -2], text=key_distribution[1].capitalize() + ' = Non-threatening')
    message1.draw()
    message2.draw()
    window.flip()

    # register the answer
    rightKeyReleased = False
    key = ""
    initialTime = datetime.datetime.now()
    accurate_answer = False
    selected_key = ""
    while not rightKeyReleased:
        allKeys = event.waitKeys()
        keyDownTime = datetime.datetime.now()
        for key in allKeys:
            if key == key_distribution[0]:
                rightKeyReleased = True
                selected_key = key_distribution[0]
                if visual_stimulus.isThreateningBool: accurate_answer = True
            if key == key_distribution[1]:
                rightKeyReleased = True
                selected_key = key_distribution[1]
                if visual_stimulus.isThreateningBool is not True: accurate_answer = True

    time_elapsed_in_millies = (keyDownTime - initialTime).microseconds / 1000

    # write the answer to the csv table
    column_data.append(selected_key)
    column_data.append(str(accurate_answer))
    column_data.append(str(time_elapsed_in_millies))
    column_data.append(str(display_time_elapsed_in_millies))
    fileWriter.add_row(column_data)


#go to qualtrics
window.flip()
message1 = visual.TextStim(win=window, pos=[0, 0], text="This is the end of the first part of the experiment. Please "
                                                        "press ENTER to continue to the second part.")

selected_key = ""
rightKeyReleased = False
while not rightKeyReleased:
    allKeys = event.waitKeys()
    keyDownTime = datetime.datetime.now()
    for key in allKeys:
        if key == '\n' or key== '\r':
            rightKeyReleased = True
            webbrowser.open(QUALTRICS_LINK)


