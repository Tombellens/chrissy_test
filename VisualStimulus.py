class VisualStimulus:

    def __init__(self,isThreatening, spatialFrequency, contrastNormalization, name, img ):
        self.isThreatening = isThreatening
        self.spatialFrequency = spatialFrequency
        self.contrastNormalization = contrastNormalization
        self.name = name
        self.img = img
        self.isThreateningBool = self.getIsThreateningBoolFromString()

    def getIsThreateningBoolFromString(self):
        if self.isThreatening == "threatening":
            return True
        if self.isThreatening == "non-threatening":
            return False