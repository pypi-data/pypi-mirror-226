#     Copyright (c) 2023, Kevan White (Thyripian)
#     All rights reserved.

#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions are met:
#       Compliance with MIT License clauses.

#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#     AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#     IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#     DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#     FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#     DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#     SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#     OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#     OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pandas as pd
from sklearn.preprocessing import LabelEncoder

def reshape_data(df, new_shape):
    """
    Reshapes the DataFrame to the specified shape.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        new_shape (tuple): The target shape (rows, columns).

    Returns:
        pd.DataFrame: The reshaped DataFrame.
    """
    return df.values.reshape(new_shape)

def encode_cats(df, columns):
    """
    Encodes categorical variables in the specified columns using label encoding.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (list): The list of columns to encode.

    Returns:
        pd.DataFrame: The DataFrame with encoded categorical variables.
    """
    df_encoded = df.copy()
    for col in columns:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df[col])
    return df_encoded

def create_bins(df, column, bins, labels=None):
    """
    Bins the values of a specific column into discrete intervals.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column (str): The name of the column to bin.
        bins (list or int): The bin edges or the number of bins.
        labels (list, optional): The labels for the resulting bins.

    Returns:
        pd.DataFrame: The DataFrame with binned values.
    """
    df_binned = df.copy()
    df_binned[column] = pd.cut(df[column], bins=bins, labels=labels)
    return df_binned
