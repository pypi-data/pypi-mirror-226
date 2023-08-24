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

def data(df, rules):
    """
    Validates the DataFrame based on specified rules.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        rules (dict): A dictionary containing validation rules.

    Returns:
        bool: True if the data is valid, False otherwise.
        list: A list of error messages if the data is invalid.
    """
    errors = []

    for column, constraints in rules.items():
        if 'type' in constraints:
            if not df[column].apply(type).eq(constraints['type']).all():
                errors.append(f"Type mismatch in column '{column}'.")
        
        if 'min_value' in constraints:
            if df[column].min() < constraints['min_value']:
                errors.append(f"Values below {constraints['min_value']} found in column '{column}'.")
        
        if 'max_value' in constraints:
            if df[column].max() > constraints['max_value']:
                errors.append(f"Values above {constraints['max_value']} found in column '{column}'.")
        
        # Additional constraints can be added here

    return len(errors) == 0, errors
