import logging
from os import path
import time
import json
import random

# from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot import LiveScatterPlot
from pyqtgraph import mkPen

import ruby as r
import numpy as np
from experimentInterface import DCMeasurements
from PyQt6 import QtWidgets
from selectFilenameUI import Popup
from fourProbeMainUI import Window
from pymeasure.experiment.procedure import Procedure
# from pymeasure.experiment.experiment import Worker, Results
from pymeasure.experiment import ModifiedWorker
from pglive.sources.data_connector import DataConnector
from datetime import datetime

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

fileName: str = ""


def numToID(x: int) -> str:
    """ Converts an int to a hex string. """
    return "0x" + str(hex(x)[2:]).zfill(4)


def validate_input_float(input: QtWidgets.QLineEdit, lower: float, upper: float) -> None:
    """
    Validates a QLineEdit and contains entered values to be a float between lower and upper.

    :param input: The QLineEdit object to validate
    :param lower: lower bound
    :param upper: upper bound
    """
    input_text = input.text()
    try:
        value = float(input_text)
        if lower <= value <= upper:
            pass  # Input is valid
        else:
            input.clear()
    except ValueError:
        input.clear()


def validate_input_float_infinite(input: QtWidgets.QLineEdit) -> None:
    """
    Validates a QLineEdit and contains entered values to be a float.

    :param input: The QLineEdit object to validate
    """
    input_text = input.text()
    try:
        float(input_text)
    except ValueError:
        input.clear()


def validate_int(input: QtWidgets.QLineEdit) -> None:
    """
    Validates a QLineEdit and contains entered values to be an int.

    :param input: The QLineEdit object to validate
    """
    input_text = input.text()
    try:
        int(input_text)
    except ValueError:
        input.clear()


# noinspection PyUnresolvedReferences
class ExperimentRun:
    """
    Experiment UI and procedure handler.

    Controls main UI, Experiment, and file writes.
    """

    global fileName

    """ Setup Operations """

    def __init__(self):
        self.Dialog = None
        self.pop = None
        self.procedure = None
        self.worker = None

        with open('config.json', 'r') as file:
            # read
            self.jsonData = json.load(file)

        self.current = 0
        self.paused = False
        self.running = False
        self.message = QtWidgets.QMessageBox()

        self.customFile = ""
        self.rubyFreq = ""
        self.rubyTemp = ""
        self.refFreq = ""
        self.refTemp = ""
        self.pressure = ""
        self.userID = ""

        self.num = self.jsonData["runID"]

        self.MainWindow = QtWidgets.QMainWindow()
        runWindow = Window()
        runWindow.setupUi(self.MainWindow)
        self.window = runWindow

        self.defaults()
        self.limiters()
        self.connections()

    def show(self) -> None:
        """ Displays the MainWindow. """
        self.MainWindow.show()

    def limiters(self) -> None:
        """ Functions defined to limit input parameters in some manner. """
        self.window.currentLine.editingFinished.connect(lambda: validate_input_float(self.window.currentLine, 0, .1))

    def defaults(self) -> None:
        """ Sets the initial values for the window UI. """
        # Parameters Box
        self.window.currentLine.setText(self.jsonData["current"])
        self.window.voltLimLine.setText(self.jsonData["voltLimit"])
        self.window.measureTypeBox.setCurrentIndex(int(self.jsonData["measurementType"]))
        self.window.directorySelect.setText(self.jsonData["directory"])

        # OTD Box
        self.window.OTDSpinBox.setProperty("value", int(self.jsonData["OTDSet"]))

        # Graph Tab
        self.window.xaxisCombo.setCurrentIndex(1)
        self.window.yaxisCombo.setCurrentIndex(0)

    def connections(self) -> None:

        def pauseButton() -> None:
            """ Controls pause flag. When paused, graph is stopped. """
            if self.paused is False:
                self.window.pauseButton.setText("Unpause")
                self.paused = True

            else:
                self.window.pauseButton.setText("Pause")
                self.paused = False

        def start_abortButton() -> None:
            """
            This function represents the actions that occur when the start / abort button is pressed.
            """
            # Runs Start Procedure
            if not self.running:
                self.startProcedure()

            # Runs Shutdown Procedure
            else:
                self.abortProcedure()

        def xComboChange() -> None:
            self.procedure.xComboChanged = True

        def yComboChange() -> None:
            self.procedure.yComboChanged = True

        self.window.start_abort.clicked.connect(lambda: start_abortButton())
        self.window.pauseButton.clicked.connect(lambda: pauseButton())

        plot_curve = LiveScatterPlot(pen=mkPen('y'), symbol="o", size=4)

        self.window.plotWidget.addItem(plot_curve)
        self.window.connector = DataConnector(plot_curve, update_rate=100)

        self.window.xaxisCombo.currentIndexChanged.connect(lambda: xComboChange())
        self.window.yaxisCombo.currentIndexChanged.connect(lambda: yComboChange())

        self.window.heatingButton.setEnabled(False)
        self.window.heatingMethodBox.setEnabled(False)
        self.window.heaterAButton.setEnabled(False)
        self.window.heaterBButton.setEnabled(False)
        self.window.OTDButton.setEnabled(False)

    """ Procedures """

    def startProcedure(self) -> None:
        """ When this is runs, the filename popup appears - prompting the potential start of the experiment """
        if self.window.directorySelect.get_starting_directory() != '/' and self.window.currentLine.text() != "":

            def clickedOK() -> None:
                global fileName

                successfulStart = False
                temperature = ""

                user = self.pop.userIDLine.text()
                fileLine = self.pop.customFileLine.text()
                sample = self.pop.customSampleLine.text()
                fileRuby = self.pop.rubyFrequencyLine.text()
                fileRubyTemp = self.pop.temperatureLine.text()
                fileRefRuby = self.pop.referenceFrequencyLine.text()
                fileRefTemp = self.pop.referenceTempLine.text()
                type = self.pop.warming_coolingCombo.currentText()
                A = self.pop.checkA.isChecked()
                B = self.pop.checkB.isChecked()
                C = self.pop.checkC.isChecked()
                D = self.pop.checkD.isChecked()

                checkList = [A, B, C, D]
                directory = self.window.directorySelect.get_starting_directory()

                # Sets the orientation list
                trueCount = 0
                index = 0
                leads1 = ""
                leads2 = ""
                reference = ["a", "b", "c", "d"]
                for e in checkList:
                    if e:
                        leads1.join(reference[index])
                        leads1 = leads1 + reference[index]
                        trueCount += 1
                    else:
                        leads2 = leads2 + reference[index]
                    index += 1

                # Sets the orientation text
                orientation = ""

                # NO USER SELECTED; ERROR
                if user == "":
                    self.message.setText("Enter a user ID")
                    self.message.exec()

                # This runs if Custom file has been selected
                elif fileLine != "":
                    fileName = f"{fileLine}_{numToID(self.num)}.csv"
                    successfulStart = True

                elif trueCount != 2 and trueCount != 0:
                    self.message.setText("Select either two or no lead orientations.")
                    self.message.exec()

                # This runs if you have selected rubyFreq and refRubyFreq
                elif sample != "" or fileLine != "":

                    # Sets the Pressure text
                    self.pressure = ""
                    if fileRuby != "" and fileRefRuby != "":
                        self.rubyFreq = float(fileRuby)
                        self.refFreq = float(fileRefRuby)

                        self.pressure = r.Pressure(self.rubyFreq, self.refFreq)

                        # Sets the Temperature text with temp correction pressures
                        if fileRubyTemp != "" and fileRefTemp != "":
                            self.rubyTemp = float(fileRubyTemp)
                            self.refTemp = float(fileRefTemp)

                            self.pressure = r.PressureRef(self.refFreq, self.refTemp, self.rubyFreq, self.rubyTemp)
                            temperature = "@" + fileRubyTemp + "K_"

                        self.pressure = str(self.pressure) + "GPa_"

                    # Sets the warming/cooling type, with an N/A action
                    if type == "N/A":
                        typeString = ""

                    else:
                        typeString = f"{type}_"

                    # Sets orientation
                    if trueCount == 2:
                        orientation = f"V{leads1}_I{leads2}_"

                    # Build filename
                    fileName = f'{sample}_{typeString}{self.pressure}{temperature}{orientation}{numToID(self.num)}.csv'
                    successfulStart = True

                # Failed to start
                else:
                    self.message.setText("Enter custom filename or sample name.")
                    self.message.exec()

                """ Everything works, start running the experiment! """
                if successfulStart:
                    self.current = self.window.currentLine.text()
                    self.Dialog.close()

                    self.window.start_abort.setText("Abort")

                    self.jsonData["current"] = self.current
                    self.jsonData["voltLimit"] = self.window.voltLimLine.text()
                    self.jsonData["measurementType"] = self.window.measureTypeBox.currentIndex()
                    self.jsonData["directory"] = self.window.directorySelect.get_starting_directory()

                    self.jsonData["OTDSet"] = self.window.OTDSpinBox.value()

                    self.jsonData["userID"] = self.pop.userIDLine.text()
                    self.jsonData["sampleName"] = self.pop.customSampleLine.text()
                    self.jsonData["type"] = self.pop.warming_coolingCombo.currentIndex()

                    self.jsonData["runID"] = self.num

                    newData = json.dumps(self.jsonData, indent=4)
                    with open('config.json', 'w') as f:
                        # write
                        f.write(newData)

                    self.running = True

                    self.window.tabWidget.setCurrentIndex(1)

                    filePath = path.join(directory, fileName)
                    self.procedure = DC4P4LExperiment(self, filePath)

                    self.window.IDLine.setText(numToID(self.num))

                    # results = Results(self.procedure, filePath)
                    # self.worker = Worker(self.procedure)

                    self.worker = ModifiedWorker(self.procedure)
                    self.worker.start()

                    self.window.currentOutLine.setText(self.window.currentLine.text())

            def clickedCancel() -> None:
                self.Dialog.close()

            self.Dialog = QtWidgets.QDialog()

            """ Setup """
            # Initializes the popup
            self.pop = Popup()
            self.pop.setupUi(self.Dialog)

            """ Connections """
            # The OK Button is clicked
            self.pop.buttonBox.accepted.connect(lambda: clickedOK())

            # The Cancel button is clicked
            self.pop.buttonBox.rejected.connect(lambda: clickedCancel())

            """ Limiters """
            # Limits the ruby frequency to be any float
            self.pop.rubyFrequencyLine.editingFinished.connect(
                lambda: validate_input_float_infinite(self.pop.rubyFrequencyLine))

            # Limits the ruby temp to be possible temperature floats
            self.pop.temperatureLine.editingFinished.connect(
                lambda: validate_input_float(self.pop.temperatureLine, 0, 10000))

            # Limits the reference ruby frequency to be any float
            self.pop.referenceFrequencyLine.editingFinished.connect(
                lambda: validate_input_float_infinite(self.pop.referenceFrequencyLine))

            # Limits the reference temp to be possible temperature floats
            self.pop.referenceTempLine.editingFinished.connect(
                lambda: validate_input_float(self.pop.referenceTempLine, 0, 10000))

            # Limits the userID to be an int
            self.pop.userIDLine.editingFinished.connect(lambda: validate_int(self.pop.userIDLine))

            """ Defaults """
            # Sets the userID, sample, and run type to their last ran value
            self.pop.userIDLine.setText(self.jsonData["userID"])
            self.pop.customSampleLine.setText(self.jsonData["sampleName"])
            self.pop.warming_coolingCombo.setCurrentIndex(self.jsonData["type"])

            # Sets the reference frequency and temp to usual entries
            self.pop.referenceFrequencyLine.setText("694.22")
            self.pop.referenceTempLine.setText("298")

            """ Execution """
            self.Dialog.exec()

            # This should only happen if a filename is chosen and all params are selected

        else:
            self.message.setText("Select a Directory and Current before starting!")
            self.message.exec()

    def abortProcedure(self) -> None:
        self.window.start_abort.setText("Start")
        self.procedure.stopFlag = True
        self.worker.join(1)


        self.window.heatingButton.setEnabled(False)
        self.window.heatingButton.setText("OFF")
        self.window.heatingLED.setValue(False)

        self.window.heatingMethodBox.setEnabled(False)

        self.window.heaterAButton.setEnabled(False)
        self.window.heaterAButton.setText("OFF")
        self.window.heaterALED.setValue(False)

        self.window.heaterBButton.setEnabled(False)
        self.window.heaterBButton.setText('OFF')
        self.window.heaterBLED.setValue(False)

        self.window.OTDButton.setEnabled(False)
        self.window.OTDButton.setText('ON')
        self.window.OTDLED.setValue(False)


        self.running = False


# noinspection PyUnresolvedReferences,PyBroadException
class DC4P4LExperiment(Procedure):

    def __init__(self, main: ExperimentRun, dataFile) -> None:
        super().__init__()

        self.dataFile = dataFile

        self.main = main
        self.DC = DCMeasurements

        self.resistanceList = []
        self.tempAList = []
        self.tempBList = []
        self.timeList = []
        self.voltPList = []
        self.voltMList = []

        self.xCategory = "Temperature A"
        self.yCategory = "Resistance"

        self.method = "manual"

        self.xComboChanged = False
        self.yComboChanged = False
        self.heating = False
        self.heatingA = False
        self.heatingB = False
        self.OTD = True

        self.x = 0
        self.y = 0
        self.APower = 0
        self.BPower = 0

        self.xList = []
        self.yList = []

        self.stopFlag = False
        self.dataColumns = ['Resistance (Rel. \u03A9)', 'Time (s)', 'Temperature A (K)', 'Temperature B (K)',
                            'Voltage + (V)', 'Voltage - (V)']

        self.connections()

    def xComboChange(self) -> None:
        try:
            selection = self.main.window.xaxisCombo.currentText()
            self.xCategory = selection

            match self.xCategory:
                case "Resistance":
                    self.xList = self.resistanceList.copy()

                case "Temperature A":
                    self.xList = self.tempAList.copy()

                case "Temperature B":
                    self.xList = self.tempBList.copy()

                case "Time":
                    self.xList = self.timeList.copy()

                case "Voltage +":
                    self.xList = self.voltPList.copy()

                case "Voltage -":
                    self.xList = self.voltMList.copy()

            match self.yCategory:
                case "Resistance":
                    self.yList = self.resistanceList.copy()

                case "Temperature A":
                    self.yList = self.tempAList.copy()

                case "Temperature B":
                    self.yList = self.tempBList.copy()

                case "Time":
                    self.yList = self.timeList.copy()

                case "Voltage +":
                    self.yList = self.voltPList.copy()

                case "Voltage -":
                    self.yList = self.voltMList.copy()

        finally:
            self.xComboChanged = False

    def yComboChange(self) -> None:
        """ Once the xCombo is changes """
        try:
            selection = self.main.window.yaxisCombo.currentText()
            self.yCategory = selection

            match self.xCategory:
                case "Resistance":
                    self.xList = self.resistanceList.copy()

                case "Temperature A":
                    self.xList = self.tempAList.copy()

                case "Temperature B":
                    self.xList = self.tempBList.copy()

                case "Time":
                    self.xList = self.timeList.copy()

                case "Voltage +":
                    self.xList = self.voltPList.copy()

                case "Voltage -":
                    self.xList = self.voltMList.copy()

            match self.yCategory:
                case "Resistance":
                    self.yList = self.resistanceList.copy()

                case "Temperature A":
                    self.yList = self.tempAList.copy()

                case "Temperature B":
                    self.yList = self.tempBList.copy()

                case "Time":
                    self.yList = self.timeList.copy()

                case "Voltage +":
                    self.yList = self.voltPList.copy()

                case "Voltage -":
                    self.yList = self.voltMList.copy()

        finally:
            self.yComboChanged = False

    def xSelect(self) -> float:
        """
        Selects the next x value using xCategory.
        :return: the next x value
        """
        match self.xCategory:
            case "Resistance":
                x = self.resistanceList[-1]

            case "Temperature A":
                x = self.tempAList[-1]

            case "Temperature B":
                x = self.tempBList[-1]

            case "Time":
                x = self.timeList[-1]

            case "Voltage +":
                x = self.voltPList[-1]

            case "Voltage -":
                x = self.voltMList[-1]

            case _:
                x = 0

        return x

    def ySelect(self) -> float:
        """
        Selects the next y value using yCategory.
        :return: the next y value
        """
        match self.yCategory:
            case "Resistance":
                y = self.resistanceList[-1]

            case "Temperature A":
                y = self.tempAList[-1]

            case "Temperature B":
                y = self.tempBList[-1]

            case "Time":
                y = self.timeList[-1]

            case "Voltage +":
                y = self.voltPList[-1]

            case "Voltage -":
                y = self.voltMList[-1]

            case _:
                y = 0

        return y

    def heatingMethodSelect(self) -> None:
        # Method is Manual
        if self.main.window.heatingMethodBox.currentIndex() == 0:
            self.method = "manual"

            self.main.window.heatingButton.setEnabled(True)
            self.main.window.heaterAButton.setEnabled(True)
            self.main.window.heaterBButton.setEnabled(True)

        # Method is Automatic
        if self.main.window.heatingMethodBox.currentIndex() == 1:
            self.method = "automatic"

            self.main.window.heatingButton.setEnabled(False)
            self.main.window.heaterAButton.setEnabled(False)
            self.main.window.heaterBButton.setEnabled(False)

    def OTDSourceChange(self) -> None:
        index = self.main.window.OTDInputBox.currentIndex()
        if index == 0:
            source = "A"

        else:
            source = "B"

        self.DC.cryo.OTDSourceSet(source)

    def OTDTempChange(self) -> None:
        value = self.main.window.OTDSpinBox.value()
        self.DC.cryo.OTDValueSet(value)

    """ Connections """

    def connections(self) -> None:

        def LEDCheck():
            # Main heating LED check
            if self.heating and (self.heatingA or self.heatingB) and (self.APower > 0 or self.BPower > 0):
                self.main.window.heatingLED.setValue(True)

            else:
                self.main.window.heatingLED.setValue(False)

            # Heating A LED check
            if self.heating and self.heatingA and self.APower > 0:
                self.main.window.heaterALED.setValue(True)

            else:
                self.main.window.heaterALED.setValue(False)

            # Heating B LED check
            if self.heating and self.heatingB and self.BPower > 0:
                self.main.window.heaterBLED.setValue(True)

            else:
                self.main.window.heaterBLED.setValue(False)


        def heatingButton() -> None:
            if self.heating is False:
                self.main.window.heatingButton.setText("ON")
                self.heating = True

            else:
                self.main.window.heatingButton.setText("OFF")
                self.heating = False
            LEDCheck()

        def heatingAButton():
            if self.heatingA:
                self.heatingA = False
                self.main.window.heaterAButton.setText("OFF")
            else:
                self.heatingA = True
                self.main.window.heaterAButton.setText("ON")
            LEDCheck()

        def heatingBButton():
            if self.heatingB:
                self.heatingB = False
                self.main.window.heaterBButton.setText("OFF")
            else:
                self.heatingB = True
                self.main.window.heaterBButton.setText("ON")
            LEDCheck()

        def heatingAPowerChanged():
            self.APower = self.main.window.aSpinBox.value()
            LEDCheck()

        def heatingBPowerChanged():
            self.BPower = self.main.window.bSpinBox.value()
            self.DC.cryo.write("")
            LEDCheck()


        def OTDButton():
            if self.OTD:
                self.OTD = False
                self.main.window.OTDButton.setText("OFF")
                # UNCOMMENT
                # self.DC.cryo.write("OVERTEMP: ENABLE OFF")
            else:
                self.OTD = True
                self.main.window.OTDButton.setText("ON")
                # UNCOMMENT
                # self.DC.cryo.write("OVERTEMP: ENABLE ON")


        # UNCOMMENT
        # self.main.window.OTDInputBox.currentIndexChanged.connect(lambda: OTDSourceChange())
        # self.main.window.OTDSpinBox.currentIndexChanged.connect(lambda: OTDTempChange())

        self.main.window.heatingButton.clicked.connect(lambda: heatingButton())
        self.main.window.heatingButton.setEnabled(True)

        self.main.window.heatingMethodBox.currentIndexChanged.connect(lambda: self.heatingMethodSelect())
        self.main.window.heatingMethodBox.setEnabled(True)

        self.main.window.heaterAButton.clicked.connect(lambda: heatingAButton())
        self.main.window.heaterAButton.setEnabled(True)

        self.main.window.heaterBButton.clicked.connect(lambda: heatingBButton())
        self.main.window.heaterBButton.setEnabled(True)

        self.main.window.OTDButton.clicked.connect(lambda: OTDButton())
        self.main.window.OTDButton.setEnabled(True)

        self.main.window.aSpinBox.valueChanged.connect(lambda: heatingAPowerChanged())
        self.main.window.bSpinBox.valueChanged.connect(lambda: heatingBPowerChanged())

    """ Defaults """
    def defaults(self):
        pass

    def initializedValues(self):
        self.heatingMethodSelect()

        # UNCOMMENT
        # self.OTDSourceChange()
        # self.OTDTempChange()

        self.APower = self.main.window.aSpinBox.value()
        self.BPower = self.main.window.bSpinBox.value()



    """ Execution """

    def startup(self) -> None:
        """ Executes the commands needed at the start-up of the measurement """
        global fileName

        # Writes info to log tab on main UI
        user = self.main.jsonData["users"][self.main.pop.userIDLine.text()]
        text = f'{user} started experiment {numToID(self.main.num)} under filename {fileName}.'
        log.info(text)

        try:
            # Writes experiment to log file
            with open("log.txt", mode="at") as f:
                dt_string = datetime.now().strftime("%m/%d/%Y %H:%M:%S : ")
                f.write(f"{dt_string}" + text)

            # Writes the useful experimental information as comments above
            # with open(self.dataFile, "w") as f:
            #     line = ""
            #     if self.main.pressure != "":
            #
            #     f.write(f"# Experiment was started by {user} at {dt_string[:-3]}." +
            #             f"\n# Pressure: {self.main.pressure[:-1]}")

            # Writes the data columns to top of csv file using DATA_COLUMNS entries.
            temp = ""
            for i in range(1, len(self.DATA_COLUMNS)):
                temp = temp + "," + str(self.DATA_COLUMNS[i])

            labels = str(self.DATA_COLUMNS[0]) + temp
            with open(self.dataFile, "a") as f:
                f.write(labels)

        except Exception:
            log.exception('Execution failed')

        try:
            # Experiment stuff

            # UNCOMMENT
            # voltName = self.main.jsonData["voltName"]
            # ammName = self.main.jsonData["ammName"]
            # switchName = self.main.jsonData["switchName"]
            # cryoName = self.main.jsonData["cryoName"]
            # self.DC = DCMeasurements(voltName, ammName, switchName, cryoName)
            # self.DC.setup()
            # self.DC.currentSet(self.current)

            self.initializedValues()
            pass

        except Exception:
            log.exception('Execution failed')

    DATA_COLUMNS = ['Resistance (Rel. \u03A9)', 'Time (s)', 'Temperature A (K)', 'Temperature B (K)',
                    'Voltage + (V)', 'Voltage - (V)']

    def execute(self) -> None:
        """
        Preforms the commands needed for the measurement itself. During execution the shutdown method will always
        be run following this method. This includes when Exceptions are raised.
        """

        startTime = time.time()
        i = 0

        while not self.stopFlag:
            while not self.main.paused:
                # Tries to read values from machines
                try:
                    # resistance, voltP, voltM, tempA, tempB, t = self.DC.totalMeasure()
                    # currentTime = t - startTime
                    pass

                except Exception:
                    log.exception('Execution failed')

                resistance = 300 + 10 * np.sin(i / 50) + 5 * np.sin(i / 30 + 1) - .01 * i + 100 * np.sin(i / 701) + \
                             random.gauss(0, 1)
                tempA = 300 - .1 * i + random.gauss(0, .1)
                tempB = 300 - .1 * i + random.gauss(0, .1)
                t = time.time()
                voltP = float(self.main.current) * resistance
                voltM = float(self.main.current) * resistance - random.gauss(0, .0001)
                currentTime = t - startTime

                self.resistanceList.append(resistance)
                self.tempAList.append(tempA)
                self.tempBList.append(tempB)
                self.timeList.append(currentTime)
                self.voltPList.append(voltP)
                self.voltMList.append(voltM)

                data = [
                    "{:e}".format(resistance),
                    "{:e}".format(currentTime),
                    "{:e}".format(tempA),
                    "{:e}".format(tempB),
                    "{:e}".format(voltP),
                    "{:e}".format(voltM)
                ]

                self.main.window.resistanceLine.setText(data[0])
                self.main.window.timeLine.setText(data[1])
                self.main.window.tempALine.setText(data[2])
                self.main.window.tempBLine.setText(data[3])
                self.main.window.voltPlusLine.setText(data[4])
                self.main.window.voltMinusLine.setText(data[5])

                # Appends data to data file
                temp = ""
                for e in range(1, len(data)):
                    temp = temp + "," + str(data[e])

                line = "\n" + str(data[0]) + temp
                try:
                    with open(self.dataFile, "a") as f:
                        f.write(line)

                except Exception:
                    log.exception('Execution failed')

                # Graphs y, x
                # Initialized values
                try:
                    if i == 0:
                        self.main.window.connector.cb_set_data(self.resistanceList.copy(), self.tempAList.copy())

                    # Runs when x-axis should be changed
                    if self.xComboChanged:
                        self.xComboChange()
                        self.main.window.connector.cb_set_data(self.yList, self.xList)

                    # Runs when y-axis should be changed
                    elif self.yComboChanged:
                        self.yComboChange()
                        self.main.window.connector.cb_set_data(self.yList, self.xList)

                    # Writes newest value
                    else:
                        self.main.window.connector.cb_append_data_point(self.ySelect(), self.xSelect())

                except Exception:
                    log.exception("Failed to Graph.")

                self.emit('results', data)

                # Runs if the thread should end
                if self.stopFlag:
                    break

                i += 1
                time.sleep(.05)

            # These are for when the axis are changed while paused
            if self.xComboChanged:
                self.xComboChange()
                self.main.window.connector.cb_set_data(self.yList.copy(), self.xList.copy())

            elif self.yComboChanged:
                self.yComboChange()
                self.main.window.connector.cb_set_data(self.yList.copy(), self.xList.copy())

    def shutdown(self) -> None:
        """ Executes the commands necessary to shut down the instruments and leave them in a safe state.
        This method is always run at the end. """

        text = f"Experiment {numToID(self.main.num)} was stopped."
        log.info(text)

        # Increases and sets the run number by one into the json file.
        self.main.num += 1
        self.main.jsonData["runID"] = self.main.num
        newData = json.dumps(self.main.jsonData, indent=4)

        try:
            with open('config.json', 'w') as f:
                f.write(newData)

            with open("log.txt", mode="at") as f:
                dt_string = datetime.now().strftime("%m/%d/%Y %H:%M:%S : ")
                f.write("\n" + f"{dt_string}" + text + "\n\n")

        except Exception:
            log.exception('Execution failed')


if __name__ == "__main__":
    from sys import exit, argv

    app = QtWidgets.QApplication(argv)
    ui = ExperimentRun()
    ui.show()

    ret = app.exec()

    # After UI is closed procedure:
    try:
        ui.procedure.stopFlag = True
        ui.worker.join(1)

    except AttributeError:
        print("No Worker")

    finally:
        pass

    # Finish
    exit(ret)
