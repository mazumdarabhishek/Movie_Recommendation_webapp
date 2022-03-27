# helper function for extracting data from list of dictionaries
import ast  # for converting String type of list to literal list.


class Json_Extractor:
    def __init__(self, whatToExtract='name', count=None, val=None):
        self.whatToExtract = whatToExtract
        self.count = count
        self.val = val

    def Extractor(self, obj):
        """
            Decription: This function extracts relevant information mentioned in whatToExtract. It also has count function which can be set to
                        specific count till which the function will output relevant information
            Return: Returns  a list of extracted information.
            Created by: Abhishek Mazumdar
        """
        if self.count == None:
            try:
                temp_info = []
                for i in ast.literal_eval(obj):
                    temp_info.append(i[
                                         self.whatToExtract])  # as a dictionary data, key is provided to extract the name. and reject all other info like Id etc.
                return temp_info
            except Exception as e:
                return "Error occured while running Extractor() :: %s" % e
        else:
            try:
                counter = 0
                temp_info = []
                for i in ast.literal_eval(obj):
                    if counter != self.count:
                        temp_info.append(i[self.whatToExtract])
                        counter += 1
                    else:
                        break
                return temp_info
            except Exception as e:
                return "Error occured while running Extractor() :: %s" % e

    def ExtraxtSingle(self, obj):
        try:
            temp_info = []
            for i in ast.literal_eval(obj):
                if list(i.values()).count(self.val) == 1:
                    temp_info.append(i[
                                         self.whatToExtract])  # as a dictionary data, key is provided to extract the name. and reject all other info like Id etc.
                    break
            return temp_info
        except Exception as e:
            return "Error occured while running Extractor() :: %s" % e