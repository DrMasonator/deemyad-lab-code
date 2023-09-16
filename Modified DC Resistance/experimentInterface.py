import time

from pymeasure.instruments.keithley import Keithley6221, Keithley7001, Keithley2182
from pymeasure.instruments.cryocon import Cryocon32B
import fourProbeMethods as fp


def resistance(v1, v2, current):
    return (v2 - v1) / current


def average(x, y):
    return (x + y) / 2


class DCMeasurements:
    """ Represents a control system to manage and operate a four-probe measurement using the
    Keithley2182, Keithley6221, Keithley7001, and the cryo-con32B.

    Order of Operation:

    1. Setup volt and switch systems
        a. all optimised volt settings
        b. open all switches in switch

    2. Setup ammeter - AMM: select current and volt limit methods
    3. Turn on current - AMM: current on method
    4. SWITCH MEASURE PROCESS:

        a. Close two switches - SWITCHER: close method
            i. {NAME OF THOSE}
        b. Measure with voltmeter - VOLTMETER: measurement method
        c. Open all switches - SWITCHER: open method
        d. Measure temp and time - CRYO: measure method

        d. Close two switches
            i. {NAME OF THOSE}
        e. Measure with voltmeter
        f. Open all switches
        d. Measure temp and time


    5. Turn off current - AMM: current off method
    6. Turn off ammeter, voltmeter, switcher, and cryo


    Do:

    setup()
    currentSet()
    while Running:
        totalMeasure
    shutdown()

    """


    def __init__(self, voltName, ammName, switchName, cryoName):
        """"
        :param voltName: GPIB interface for voltmeter
        :param ammName: GPIB interface for ammeter
        :param switchName: GPIB interface for switcher
        :param cryoName: GPIB interface for cryocon
        """
        self.current = 0

        self.volt = Keithley2182(voltName)
        self.amm = Keithley6221(ammName)
        self.switch = Keithley7001(switchName)
        self.cryo = Cryocon32B(cryoName)

    def setup(self):
        """ Initializes the voltmeter and cryocon. """
        self.volt.setup()
        self.switch.setup()
        # self.cryo.setup()

    def currentSet(self, current: float, voltLimit: float = 5):
        """ Initializes the current and volt limit. """
        self.current = current

        self.amm.reset()
        self.amm.source_auto_range = 1
        self.amm.source_current = current
        self.amm.source_compliance = voltLimit

    def switchMeasure(self, channel1: str, channel2: str):
        """ Measures the voltage across the sample, returning the time and temps with it. """
        self.switch.channel_closeTwo = (channel1, channel2)

        volt = self.volt.voltage
        tempA = self.cryo.temperature("A")
        tempB = self.cryo.temperature("B")

        currentTime = time.time()

        self.switch.openAll()

        return volt, tempA, tempB, currentTime

    def totalMeasure(self):
        volt1, tempA1, tempB1, currentTime1 = self.switchMeasure("2!1", "2!2")
        volt2, tempA2, tempB2, currentTime2 = self.switchMeasure("2!11", "2!12")

        r = resistance(volt1, volt2, self.current)
        tempA = average(tempA1, tempA2)
        tempB = average(tempB1, tempB2)
        avgTime = average(currentTime1, currentTime2)

        return r, volt1, volt2, tempA, tempB, avgTime

    def shutdown(self):
        """ Successful shutdown procedures for each instrument. """
        self.amm.source_current = 0

        self.volt.shutdown()
        self.amm.shutdown()
        self.switch.shutdown()
        self.cryo.shutdown()

    #############
    # NEW STUFF #
    #############

    def R(self, a, b, c, d):
        """ Opens all channels, the sets the circuit and returns the resistance. """
        self.switch.openAll()
        self.V(c, d)
        self.I(a, b)
        return self.volt.voltage / self.current

    def I(self, minus, plus):
        match minus:
            case "a":
                self.switch.channel_closeOne("2!1")

            case "b":
                self.switch.channel_closeOne("2!2")

            case "c":
                self.switch.channel_closeOne("2!3")

            case "d":
                self.switch.channel_closeOne("2!4")

        match plus:
            case "a":
                self.switch.channel_closeOne("2!5")

            case "b":
                self.switch.channel_closeOne("2!6")

            case "c":
                self.switch.channel_closeOne("2!7")

            case "d":
                self.switch.channel_closeOne("2!8")

    def V(self, minus, plus):
        match minus:
            case "a":
                self.switch.channel_closeOne("2!9")

            case "b":
                self.switch.channel_closeOne("2!10")

            case "c":
                self.switch.channel_closeOne("2!11")

            case "d":
                self.switch.channel_closeOne("2!12")

        match plus:
            case "a":
                self.switch.channel_closeOne("2!13")

            case "b":
                self.switch.channel_closeOne("2!14")

            case "c":
                self.switch.channel_closeOne("2!15")

            case "d":
                self.switch.channel_closeOne("2!16")

    def Rv(self, a, b, c, d):
        return (self.R(a, b, c, d) + self.R(c, d, a, b) + self.R(b, a, d, c) + self.R(d, c, b, a)) / 4

    def Rh(self, a, b, c, d):
        return (self.R(b, c, d, a) + self.R(d, a, b, c) + self.R(c, b, a, d) + self.R(a, d, c, b)) / 4

    def sheetResistance(self):
        a = "a"
        b = "b"
        c = "c"
        d = "d"
        return fp.RsG(self.Rv(a, b, c, d), self.Rh(a, b, c, d))


if __name__ == "__main__":
    # Ω/□
    print("\u03A9/\u25A1")
