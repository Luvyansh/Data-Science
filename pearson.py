import zipfile
import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from scipy.stats import pearsonr

# Define the paths
zip_file_path = './roe.zip'
extraction_dir = '/content/roe_extracted'

# Create the extraction directory if it doesn't exist
os.makedirs(extraction_dir, exist_ok=True)

# Extract the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extraction_dir)

# List the files in the extracted directory
extracted_files = os.listdir(extraction_dir)
html_files = [file for file in extracted_files if file.endswith('.html')]

# Initialize lists to hold the scores
math_scores = []
read_scores = []

# Function to extract scores from HTML
def extract_scores_from_html(file_path):
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        for school in soup.find_all('div', class_='school'):
            try:
                math_score = int(school.find(text='Average Score: Math:').find_next('span').text)
                read_score = int(school.find(text='Average Score: Read:').find_next('span').text)
                math_scores.append(math_score)
                read_scores.append(read_score)
            except AttributeError:
                continue

# Process each HTML file
for html_file in html_files:
    extract_scores_from_html(os.path.join('./roe', html_file))

# Debug prints to check the extracted scores
print("Extracted Math Scores:", math_scores)
print("Extracted Read Scores:", read_scores)

# Create a DataFrame
data = {'Math': math_scores, 'Read': read_scores}
df = pd.DataFrame(data)

# Drop rows with any null values
df = df.dropna()

# Ensure we have at least two rows of data
if len(df) < 2:
    print("Not enough data to calculate Pearson correlation coefficient.")
else:
    # Calculate the Pearson correlation coefficient
    correlation, _ = pearsonr(df['Math'], df['Read'])
    print(f'Pearson correlation coefficient: {correlation}')