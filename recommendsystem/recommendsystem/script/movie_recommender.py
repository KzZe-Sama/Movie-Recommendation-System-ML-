import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
###### helper functions. Use them when needed #######
class MovieRecommender:
	##Step 1: Read CSV File
	# method read_csv reads csv data
	dataFrame = pd.read_csv("movie_dataset.csv")
	def get_title_from_index(self,index):
		return self.dataFrame[self.dataFrame.index == index]["title"].values[0]

	def get_director_from_title(self,title):
		return self.dataFrame[self.dataFrame.title == title]["director"].values[0]
	
	def get_index_from_title(self,title):
		return self.dataFrame[self.dataFrame.title == title]["index"].values[0]
	def get_overview_from_title(self,title):
		return self.dataFrame[self.dataFrame.title == title]["overview"].values[0]
	def get_homepage_from_title(self,title):
		return self.dataFrame[self.dataFrame.title == title]["homepage"].values[0]
	##################################################
	##Step 2: Select Features
	features = ["keywords","cast","genres","director"]
	def combine_features(self,row):
		return row['keywords'] + " " + row['cast']+" " + row['genres']+" " + row['director']
	def print_similar_movie(self,index):
		return self.get_title_from_index(index)
	def main(self,movie_name):
		
			##Step 3: Create a column in DF which combines all selected features
			for feature in self.features:
				self.dataFrame[feature] = self.dataFrame[feature].fillna('')
			self.dataFrame["combined_features"] = self.dataFrame.apply(self.combine_features,axis=1)
		
		
				
			# print(dataFrame["combined_features"].head())
			##Step 4: Create count matrix from this new combined column
			cv = CountVectorizer()
			count_matrix = cv.fit_transform(self.dataFrame["combined_features"])

			##Step 5: Compute the Cosine Similarity based on the count_matrix
			cosine_sim = cosine_similarity(count_matrix)
			# print(cosine_sim)
			movie_user_likes = movie_name

			## Step 6: Get index of this movie from its title
			movie_index = self.get_index_from_title(movie_user_likes)
			# print(movie_index)
			## Step 7: Get a list of similar movies in descending order of similarity score
			similar_movies = list(enumerate(cosine_sim[movie_index]))
			# print(similar_movies)
			sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)
			# print(sorted_similar_movies)
			## Step 8: Print titles of first 50 movies

			
			
			start = 0
			result = []
			while True:

				if start <=20:
					index = sorted_similar_movies[start][0]
					movie_title = self.print_similar_movie(index)
					movie_homepage = self.get_homepage_from_title(movie_title)
					movie_director = self.get_director_from_title(movie_title)
					movie_overview = self.get_overview_from_title(movie_title)
					if str(movie_homepage) == "nan":
						movie_homepage = "#"
					
					if str(movie_director) == "":
						movie_director = "Unknown"
					data = {
						"movie_title":movie_title,
						"movie_homepage":movie_homepage,
						"movie_director":movie_director,
						"movie_overview":movie_overview
					}
					result.append(data)
					start+=1
				
				else:
					break
			result.pop(0)
			return result
		
		
		

		
	

	