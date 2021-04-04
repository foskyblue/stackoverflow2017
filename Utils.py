import pandas as pd
import numpy as np
from collections import defaultdict
from matplotlib import pyplot as plt


def get_unique(column):
    
    '''
    INPUT
        column - the column name of the data frame that you want to file all it's unique values
    
    OUTPUT
        a set of all unique values in column
    '''
    
    temp = []
    for idx, col in enumerate(column):
        if ';' in str(col):
            for r in col.split(';'):
                temp.append(str(r).strip())
        else:
            temp.append(str(col).strip())
    return set(temp)


def total_count(df, col1, col2, look_for):
    '''
    INPUT:
        df - the pandas dataframe you want to search
        col1 - the column name you want to look through
        col2 - the column you want to count values from
        look_for - a list of strings you want to search for in each row of df[col]
        
    OUTPUT:
        new_df - a dataframe of each look_for with the count of how often it shows up
    '''
    new_df = defaultdict(int)
    #loop through list of ed types
    for val in look_for:
        #loop through rows
        for idx in range(df.shape[0]):
            #if the ed type is in the row add 1
            if val in df[col1][idx]:
                new_df[val] += int(df[col2][idx])
    new_df = pd.DataFrame(pd.Series(new_df)).reset_index()
    new_df.columns = [col1, col2]
    new_df.sort_values('count', ascending=False, inplace=True)
    return new_df


def clean_and_plot(df, possible_vals, column, col, title='Method of Educating Suggested', plot=True):
    '''
    INPUT 
        df - a dataframe holding the CousinEducation column
        title - string the title of your plot
        axis - axis object
        plot - bool providing whether or not you want a plot back
        
    OUTPUT
        study_df - a dataframe with the count of how many individuals
        Displays a plot of pretty things related to the CousinEducation column.
    '''
    
    study = df[column].value_counts().reset_index()
    study.rename(columns={'index': 'method', column: 'count'}, inplace=True)
    study_df = total_count(study, 'method', 'count', possible_vals)

    study_df.set_index('method', inplace=True)
    study_df.rename(columns={'method': col})
    
    
    if plot:
        (study_df/study_df.sum()).plot(kind='bar', legend=None);
        plt.title(title);
        plt.xlabel(col)
        plt.show()
    props_study_df = study_df/study_df.sum()
    return props_study_df


def mean_amt(df, col_name, col_mean, look_for):
    '''
    INPUT:
        df - the pandas dataframe you want to search
        col_name - the column name you want to look through
        col_count - the column you want to count values from
        col_mean - the column you want the mean amount for
        look_for - a list of strings you want to search for in each row of df[col]
    
    OUTPUT:
        df_all - holds sum, square, total, mean, variance, and standard deviation for the col_mean
    '''
    new_df = defaultdict(int)
    squares_df = defaultdict(int)
    denoms = dict()
    for val in look_for:
        denoms[val] = 0
        for idx in range(df.shape[0]):
            if df[col_name].isnull()[idx] == False:
                if val in df[col_name][idx] and df[col_mean][idx] > 0:
                    new_df[val] += df[col_mean][idx]
                    squares_df[val] += df[col_mean][idx]**2 #Needed to understand the spread
                    denoms[val] += 1 
    
    # Turn into dataframes
    new_df = pd.DataFrame(pd.Series(new_df)).reset_index()
    squares_df = pd.DataFrame(pd.Series(squares_df)).reset_index()
    denoms = pd.DataFrame(pd.Series(denoms)).reset_index()
    
    # Change the column names
    new_df.columns = [col_name, 'col_sum']
    squares_df.columns = [col_name, 'col_squares']
    denoms.columns = [col_name, 'col_total']
    
    # Merge dataframes
    df_means = pd.merge(new_df, denoms)
    df_all = pd.merge(df_means, squares_df)
    
    # Additional columns needed for analysis
    df_all['mean_col'] = df_means['col_sum']/df_means['col_total']
    df_all['var_col'] = df_all['col_squares']/df_all['col_total'] - df_all['mean_col']**2
    df_all['std_col'] = np.sqrt(df_all['var_col'])
    df_all['lower_95'] = df_all['mean_col'] - 1.96*df_all['std_col']/np.sqrt(df_all['col_total'])
    df_all['upper_95'] = df_all['mean_col'] + 1.96*df_all['std_col']/np.sqrt(df_all['col_total'])
    return df_all