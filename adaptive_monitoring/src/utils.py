from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np


def upscale_df(sampled_df, original_df):
    """Upscale the sampled DataFrame to match the original DataFrame."""
    return sampled_df.resample('1s').interpolate(method='linear').reindex(original_df.index).ffill()


def truncate_df(df, date, N):
    """Truncate the DataFrame to a smaller size of N rows starting from the given date."""
    return df[df.index >= date].head(N)
    

def mean_absolute_error(df, sampled_df, scale_factor=1):
    """Calculate the absolute error between two DataFrames."""
    # upscale the sampled dataframe to match the original dataframe
    sampled_df = upscale_df(sampled_df, df)

    if df.shape != sampled_df.shape:
        raise ValueError("DataFrames must have the same shape.")
    
    values = df["value"].to_numpy() / scale_factor
    sampled_values = sampled_df["value"].to_numpy() / scale_factor
    
    return np.abs(values - sampled_values).mean()

def mean_absolute_percentage_error(df, sampled_df, scale_factor=1, epsilon=1e-8):
    """Calculate the absolute percentage error between two DataFrames."""
    # upscale the sampled dataframe to match the original dataframe
    sampled_df = upscale_df(sampled_df, df)

    if df.shape != sampled_df.shape:
        raise ValueError("DataFrames must have the same shape.")
    
    values = df["value"].to_numpy() / scale_factor
    sampled_values = sampled_df["value"].to_numpy() / scale_factor

    absolute_percentage_errrors = np.abs((values - sampled_values) / (values + epsilon)) * 100
    mape = absolute_percentage_errrors.mean()
    return mape


def pointwise_absolute_error(df, sampled_df, scale_factor=1):
    """Calculate pointwise error two DataFrames."""
   
    # upscale the sampled dataframe to match the original dataframe
    sampled_df = upscale_df(sampled_df, df)  

    if df.shape != sampled_df.shape:
        raise ValueError("DataFrames must have the same shape.")
    
    values = df["value"].to_numpy() / scale_factor
    sampled_values = sampled_df["value"].to_numpy() / scale_factor

    return np.abs(values - sampled_values)


def compression_ratio(original_df, sampled_df):
    """Calculate the reduction in data points."""
    original_rows = original_df.shape[0]
    sampled_rows = sampled_df.shape[0]
    if original_rows == 0:
        return 0
    compression_ratio = 1 - (sampled_rows / original_rows)
    return compression_ratio

def preprocess_data(file_path, normalize=False):
    """Preprocess the dataset for analysis."""
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('date', inplace=True)
    df.drop(["timestamp"], inplace=True, axis=1)
    df = df[~df.index.duplicated(keep='first')]
    if normalize:
        df = normalize(df)
    return df

def normalize(df):
    """Normalize the dataset using min-max scaling."""
    return (df - df.min()) / (df.max() - df.min())