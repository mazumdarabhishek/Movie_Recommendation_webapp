#from App_Logger.AppLogging import App_logger
from Model_Building.stemData import stemIT
from  Model_Building.WordsToVectors import WordsToVecotrs
from Model_Building.JSONExtractor import Json_Extractor
from Model_Building.Data_PreProcessing import DataPreProcessing
import pandas as pd
import pickle
import os

class Build_save_Data:

    def __init__(self):
        #self.logger = App_logger()
        self.movies_path = "data/tmdb_5000_movies.csv/tmdb_5000_movies.csv"
        self.credits_path = "data/tmdb_5000_credits.csv/tmdb_5000_credits.csv"
        self.movies = pd.read_csv(self.movies_path)
        self.credits = pd.read_csv(self.credits_path)
        self.Preprocessor = DataPreProcessing(self.movies,self.credits)
        self.df = None

    def preProcess(self):

        #Merging data
        self.Preprocessor.mergeData()
        #removing unwanted columns
        columns_for_removal = ['id','title','overview','genres','keywords','cast','crew']
        self.Preprocessor.removeUnwantedColumns(columns_for_removal)
        # Drop records with missing values
        self.Preprocessor.dropMissingRecords()
        #get the data frame
        self.df = self.Preprocessor.getDataFrame()

        #Data Engineering steps, for more details view ipython notebook
        ext = Json_Extractor('name', None)
        self.df['genres'] = self.df['genres'].apply(ext.Extractor)
        self.df['keywords'] = self.df['keywords'].apply(ext.Extractor)
        ext_2 = Json_Extractor('name', count=3)  # we need only the first 3 lead actor's names
        self.df['cast'] = self.df['cast'].apply(ext_2.Extractor)
        ext_3 = Json_Extractor('name', val='Director')
        self.df['crew'] = self.df['crew'].apply(ext_3.ExtraxtSingle)

        #remove space between names and keywords
        self.df['genres'] = self.df['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
        self.df['keywords'] = self.df['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
        self.df['cast'] = self.df['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
        self.df['crew'] = self.df['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

        # converting string over view to list
        self.df['overview'] = self.df['overview'].apply(lambda x: x.split())

        # Concatenating modified columns into tags column.  for this reason, the overview column as type casted to list
        self.df['tags'] = self.df['overview'] + self.df['genres'] + self.df['keywords'] + self.df['cast'] + \
                           self.df['crew']

        #Recreating the data frame with only the relevant columns
        self.df = self.df[['id', 'title', 'tags']]
        #re casting tags list to string
        self.df['tags'] = self.df['tags'].apply(lambda x: " ".join(x))
        # converting tags information to lower case

        self.df['tags'] = self.df.tags.apply(lambda x: x.lower())


    def stemingTags(self):
        stem = stemIT(columns='tags', data=self.df)
        self.df['tags'] = stem.stem_apply()

    def executeBuild(self):

        self.preProcess()
        self.stemingTags()

        vec = WordsToVecotrs(5000)

        vectors = vec.getVectors(self.df, 'tags')

        similarity = vec.getSimilarity()

        #save similarity data into Modeled_Data Directory
        path = "Modeled_Data"
        similarity_file_path = os.path.join(path,"similarity.pkl")

        pickle.dump(similarity,open(similarity_file_path,'wb'))







