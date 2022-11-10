import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from xgboost import XGBRegressor


# Data loading
df = pd.read_csv('data/co2_emission.csv')


# Data validation
del df['co2 rating']
del df['smog rating']

df['model year'] = df['model year'].astype(str)
df['cylinders'] = df['cylinders'].astype(str)


# Data preparation
df_train, df_test = train_test_split(df, test_size=0.2, random_state=11)

# Creating target series
y_train = df_train['co2 emissions (g/km)']
y_test = df_test['co2 emissions (g/km)']

# Removing target from train sets
drop_cols = ['co2 emissions (g/km)', 
             'model', 
             'fuel consumption comb (mpg)', 
             'fuel consumption city (l/100 km)',
             'fuel consumption hwy (l/100 km)',
            ]

X_train = df_train.drop(drop_cols, axis=1)
X_test = df_test.drop(drop_cols, axis=1)

# Pipeline
def make_pipeline(model, df):
    """Create a pipeline for a model."""

    cat_transf = OneHotEncoder(sparse=False,
                               handle_unknown="ignore")

    std_scaler = StandardScaler()

    # Determining categorical and numerical columns
    df_cat_cols = list(df.loc[:, df.dtypes == object].columns)
    df_num_cols = list(df.loc[:, df.dtypes != object].columns)

    transformer = ColumnTransformer(transformers=[("cat", cat_transf, df_cat_cols),
                                                  ("num_scaler", std_scaler, df_num_cols)],
                                    remainder='passthrough'
                                   )

    steps = [("transformer", transformer),
             ("model", model)]
    
    return Pipeline(steps)

# Model training
model = XGBRegressor(n_estimators=200,
                     max_depth=7,
                     eta=0.2)

pipe_model = make_pipeline(model, X_train)

pipe_model.fit(X_train, y_train)

# Saving the model
import pickle

with open('co2_model.bin', 'wb') as f_out:
    pickle.dump((pipe_model), f_out)


