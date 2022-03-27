#from App_Logger.AppLogging import App_logger
import pandas as pd

class DataPreProcessing:
    def __init__(self,movies,credits):
        self.movies = movies
        self.credits = credits
        #self.logger = App_logger()


    def mergeData(self):
        self.data = self.movies.merge(self.credits,on='title')


    def removeUnwantedColumns(self,columns:list):

        self.df = self.data[columns]



    def dropMissingRecords(self):

        self.df.dropna(inplace=True)

    def getDataFrame(self):

        return self.df





