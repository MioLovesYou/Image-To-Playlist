import os
import pandas as pd
from PIL import Image, ImageFile
from sklearn.model_selection import train_test_split

# main vars
IMAGE_DIR = 'datasets/sentiment-dataset/images'
CSV_FILE = 'datasets/sentiment-dataset/annotationsTest.csv'
OUTPUT_DIR = 'datasets/sentiment-dataset/processed'
PROCESSED_CSV = 'preprocessed_annotations.csv'

# corrupted / half dfownlaoaded pics 
ImageFile.LOAD_TRUNCATED_IMAGES = True

os.makedirs(OUTPUT_DIR, exist_ok=True)

def resize_images(image_directory, size=(224, 224)):
    # goin through the images to make em all the same s
    for image_filename in os.listdir(image_directory):
        image_path = os.path.join(image_directory, image_filename)
        try:
            with Image.open(image_path) as img:
                # switch 2 rgb incase
                if img.mode in ['RGBA', 'LA', 'P']:
                    img = img.convert('RGB')
                img = img.resize(size)
                img.save(os.path.join(OUTPUT_DIR, image_filename), 'JPEG')
        except IOError as e:
            print(f"Error processing image {image_filename}: {e}")

def normalize_likert(value):
    # max is 9 so -1 then device by 8 - 8/8 = 1    0 / 8 = 0 
    return (float(value) - 1) / 8

def process_annotations_row(row):
    # takes a row, does math on it to average stuff, 
    parts = row.strip().split(';')
    image_name = parts[1]  # The filename remains the same
    annotations = parts[2:]  # The rest are annotations

     # split up responses, ignoring the 26th one -- - 26 is filler 
    annotator_responses = [annotations[i*26:(i+1)*26-1] for i in range(5)]

    # #33 average out each question across all  annotators
    average_annotations = []
    for question_idx in range(25):  # For each question
        question_responses = [float(annotator_responses[i][question_idx]) for i in range(5)]
        # Normalize the first tw responses
        if question_idx < 2:
            question_responses = [normalize_likert(score) for score in question_responses]
        question_average = sum(question_responses) / len(question_responses)
        average_annotations.append(question_average)

    return [image_name] + average_annotations

def preprocess_annotations(csv_file):
    #applies processing to all rows of the CSV file and returns a new Df
    df = pd.read_csv(csv_file, header=None, names=['annotations'])
    df = df['annotations'].apply(process_annotations_row).apply(pd.Series)
    return df

def split_dataset(df, train_size=0.7, val_size=0.15):
    #splitting into sets
    train, temp = train_test_split(df, train_size=train_size, random_state=42)
    val, test = train_test_split(temp, test_size=val_size / (1 - train_size), random_state=42)
    return train, val, test

def export_to_csv(df, filename):
    df.to_csv(filename, index=False)

def main():
    #  Main function to execute all steps. 
  # resizing all imgs - pass directory
    resize_images(IMAGE_DIR)

    # create new df adfter processing all rows
    processed_df = preprocess_annotations(CSV_FILE)

    # splitting
    train_df, val_df, test_df = split_dataset(processed_df)

    # doen save
    export_to_csv(train_df, os.path.join(OUTPUT_DIR, 'train_' + PROCESSED_CSV))
    export_to_csv(val_df, os.path.join(OUTPUT_DIR, 'val_' + PROCESSED_CSV))
    export_to_csv(test_df, os.path.join(OUTPUT_DIR, 'test_' + PROCESSED_CSV))

    print("Data preprocessing complete!")

if __name__ == "__main__":
    main()
