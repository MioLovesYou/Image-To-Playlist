import pandas as pd
import os

# for processed pics iomages
image_directory = 'C:/Users/Mio/Desktop/AI-driven Image to Music Playlist Generator/Image-To-Playlist/Image-To-Playlist/datasets/sentiment-dataset/processed'

# test csv
csv_file_path = 'C:/Users/Mio/Desktop/AI-driven Image to Music Playlist Generator/Image-To-Playlist/Image-To-Playlist/datasets/sentiment-dataset/processed/test_preprocessed_annotations.csv'
data = pd.read_csv(csv_file_path)

# quick check for missing file names
nan_filenames = data.iloc[:, 0].isna().sum()
print(f"Number of NaN filenames in the CSV: {nan_filenames}")

# # loopin through to make sure all our files are there
for index, row in data.iterrows():
    filename = row.iloc[0]
    if pd.isna(filename):
        print(f"Missing filename found at row {index}")
        continue
    file_path = os.path.join(image_directory, filename)
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
    else:
        print(f"File found: {file_path}")#
