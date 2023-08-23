from app.services.service import s3
import pandas as pd
import numpy as np
import io
from app.services.loader import dfLoader

class DataAnalyzer():

    @staticmethod
    def load_from_s3(bucket:str, key: str):
        analyzer = DataAnalyzer()
        analyzer._df = dfLoader.load(bucket,key)
        return analyzer
    
    def get_dataframe(self):
        return self._df


    def get_metadata(self):
        metadata = {}
        metadata['data_overview'] = self.generateOverview()
        metadata['data_rownum'] = self._df.shape[0]
        metadata['data_colnum'] = self._df.shape[1]
        metadata['data_sample'] = str(self._df.head())
        return metadata
    
    
    def generateOverview(self):
        """
        To generate the column names, column types and the unique values(for string columns) in `df`

        Parameters:
        df (dataframe): The dataframe to be checked

        Returns:
        description (string): The description of the dataframe (column names, column types and the unique values(for string columns) in `df`
        """

        INCLUDE_COL_DESCRIPTION_VALS = True # Choose whether to include sample values in the column descriptions (within the prompt)
        MAX_UNIQUES_FOR_DESC = 10 # Number of unique values to show in column descriptions (within the prompt)

        description = ""
        for column in self._df:
            col_name = self._df[column].name
            col_type = self._df[column].dtype
            col_description = f"Column Name: {col_name}\nColumn Type: {col_type}"
            if col_type == "object":

                # Get unique values for column descriptions.
                column_values = self._df[col_name].values
                uniques = list(set(column_values))

                # Get most frequent unique value.
                freq_uq_val = self._df[col_name].value_counts().idxmax()

                # Get most frequent unique value count.
                freq_uq_val_count = self._df[col_name].value_counts().max()

                if INCLUDE_COL_DESCRIPTION_VALS:
                    if len(uniques) > MAX_UNIQUES_FOR_DESC:
                        col_description += f"\nSample Values: {str(uniques[0:MAX_UNIQUES_FOR_DESC])}"
                    else:
                        col_description += f"\nSample Values: {str(uniques)}"
                        
                # Add most frequent unique value and count to column description.
                col_description += f"\nMost Frequent Unique Value: {freq_uq_val} ({freq_uq_val_count} times)"
            description += col_description + "\n\n"
        return description.strip()
        

    def find_missing_data(self):
        """
        Return a dictionary of missing data in the dataframe

        Parameters: df (dataframe): The dataframe to be checked

        Returns:
        missing_data (dictionary): The dictionary of missing data in the dataframe
        """
        missing_data = self._df.isnull().sum()
        missing_data = missing_data[missing_data > 0]
        return missing_data.to_dict()


    def find_diff_dtype(self):
        """
        Output a dictionary of columns with mixed data types in the dataframe

        Parameters: df (dataframe): The dataframe to be checked
        Returns: diff_dtype_dict (dictionary): The dictionary of columns with mixed data types in the dataframe
        """
        diff_dtype_dict = dict()
        # Iterate over each column and track data types
        for column in self._df.columns:
            data_type_counts = self._df[column].apply(type).value_counts()
            majority_data_type = data_type_counts.idxmax()
            minority_data_types = data_type_counts[data_type_counts.index != majority_data_type]
            minority_data_type_count = minority_data_types.sum()
            minority_data_types = minority_data_types.index.to_list()
            if minority_data_type_count > 0:
                diff_dtype_dict[column] = majority_data_type, minority_data_types, minority_data_type_count

        return diff_dtype_dict


    def find_duplicate_rows(self):
        """
        Find duplicate rows in the dataframe

        Parameters: df (dataframe): The dataframe to be checked
        Returns: duplicate_pairs (list): The list of duplicate rows in the dataframe
        """

        dups = self._df[self._df.duplicated(keep=False)]
        dups_count = dups.shape[0]
        if dups_count > 0:
            duplicate_pairs = dups.groupby(list(dups.columns)).apply(lambda x: list(x.index))
        else:
            duplicate_pairs = []
        return duplicate_pairs, dups_count

    def detect_outliers_iqr(self,df, column):
        """
        detect outliers using IQR method

        Parameters: df (dataframe): The dataframe to be checked
                    column (string): The column to be checked
        Returns: lower_bound (float): The lower bound of the outliers
                    upper_bound (float): The upper bound of the outliers
                    num_outliers (int): The number of outliers
                    example_outliers_idx (list): The list of index of example outliers
                    example_outliers_val (list): The list of value of example outliers
        """
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR


        example_outliers = None
        example_outliers_idx = []
        example_outliers_val = []
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)][column]
        num_outliers = outliers.shape[0]
        if num_outliers > 3:
            example_outliers = outliers.sample(3)
            example_outliers_idx = list(example_outliers.index)
            example_outliers_val = list(example_outliers.values)

        return lower_bound, upper_bound, num_outliers, example_outliers_idx, example_outliers_val


    def extract_outlier_info(self):
        """
        extract outlier information from the dataframe

        Parameters: df (dataframe): The dataframe to be checked
        Returns: outlier_info (dictionary): The dictionary of outlier information
        """
        outlier_info = dict()
        df = self._df.select_dtypes(include=np.number)
        for column in df.columns:
            lower_bound, upper_bound, num_outliers, example_outliers_idx, example_outliers_val = self.detect_outliers_iqr(df, column)
            if num_outliers > 0:
                outlier_info[column] = lower_bound, upper_bound, num_outliers, example_outliers_idx, example_outliers_val
        return outlier_info
