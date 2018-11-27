import pandas as pd
import csv, json
import datetime
import re

class JSONConverter:
	def __init__(self, raw_data:str,idx_cols_to_keep):
		self.df = pd.read_csv(raw_data, usecols=idx_cols_to_keep, encoding='utf-8')

	def convert(self,new_col_n,json_file_name):
		self.change_column_names(new_col_n)
		self.clean_content()
		self.add_constant_values()
		self.export_to_json(json_file_name)

	def change_column_names(self,new_col_n):
		self.df.columns = new_col_n
		# print(self.df)

	def clean_content(self):
		self.df.iloc[:,0] = self.df.iloc[:,0].str.split("\\.\\s{1,}")		
		self.df.iloc[:,2] = pd.to_datetime(self.df.iloc[:,2],infer_datetime_format=True, unit='ns')

	def add_constant_values(self):
		self.df['type'] = 'blog-post'
		self.df['employeeID'] = ''
		self.df['sensitivity'] = 'public'
		self.df['generatedDate'] = datetime.datetime.utcnow().isoformat()
		self.df['tags'] = ''

	def export_to_json(self, json_file_name):
		out = self.df.to_json(orient='records')[1:-1].replace('},{', '} {')
		with open(json_file_name, 'w') as f:
			f.write(out)

if __name__ == "__main__":
	#name of the input
	raw_data = "blogs_en_sample.csv"
	
	#name of the output
	json_file_name = "blogs.json"

	#list of indexes of the columns to import from the database
	idx_cols_to_keep = [3,5,7]

	#new column names
	new_col_n = ['content', 'source', 'sourceDate']

	convert_en = JSONConverter(raw_data, idx_cols_to_keep).convert(new_col_n,json_file_name)