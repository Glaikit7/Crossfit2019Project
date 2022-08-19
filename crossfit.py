# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import re

# Read in the data
df = pd.read_csv(r'C:\Users\crae1\Documents\GWG\CrossFitGamesData\archive\2019_games_athletes.csv')


# Search for missing data
def missing_data_search():
    for col in df.columns:
        percentage_missing = np.mean(df[col].isnull())
        print('{} - {}%'.format(col, percentage_missing))
missing_data_search()

# Drop rows with incomplete data
df = df[df['overallscore'].notna()]

# Locate missing country of origin value
nf = df[df['countryoforigincode'].isna()]
print(nf)

# Replace code NA with NM for Namibia
df.at[234, 'countryoforigincode'] = 'NM'

# Research for missing data
missing_data_search()

# Change data type of overall score to int64
df['overallscore'] = df['overallscore'].astype('int64')

# Look for inaccurate data for height and weight
hf = df[df['height'] < 1]
print(hf)

wf = df[df['weight'] < 30]
print(wf)


# Drop rows with inaccurate height data
df = df[df['height'] > 1]

# The overall rank column must be converted to the int64 datatype
# The 'T' at the end of the tied rankings has to be dropped

# Converts the overall rank column to the string datatype
df['overallrank'] = df['overallrank'].astype('string')

# Replaces the 'T' with an empty ''
df['overallrank'] = df['overallrank'].str.replace('T', '')

# Converts the overall rank column to the int64 datatype
df['overallrank'] = df['overallrank'].astype('int64')


# Seperate data to look only at the Men's and Women's divisions
men_df = df[df['division'] == 'Men']

women_df = df[df['division'] == 'Women']

# This creates grouped summaries correlating height/weight with overall rank
menheight_df = men_df.groupby('height')['overallrank'].mean()

womenheight_df = women_df.groupby('height')['overallrank'].mean()

menweight_df = men_df.groupby('weight')['overallrank'].mean()

womenweight_df = women_df.groupby('weight')['overallrank'].mean()

# Plot of men's height vs overall ranking
menheight_df.plot(kind='bar', title='Male Athlete Height vs. Average Placing', ylabel='Mean Ranking', xlabel='Height(m))', figsize=(10,6), color='b')

# Plot of men's weight vs overall ranking
menweight_df.plot(kind='bar', title='Male Athlete Weight vs. Average Placing', ylabel='Mean Ranking', xlabel='Weight(kg)', figsize=(10,6), color='r')

# Plot of women's height vs overall ranking
womenheight_df.plot(kind='bar', title='Female Athlete Height vs. Average Placing', ylabel='Mean Ranking', xlabel='Height(m)', figsize=(10,6), color='b')

# Plot of women's weight vs overall ranking
womenweight_df.plot(kind='bar', title='Female Athlete Weight vs. Average Placing', ylabel='Mean Ranking', xlabel='Weight(kg)', figsize=(10,6), color='r')