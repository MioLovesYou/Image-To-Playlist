import pandas as pd
import os
import numpy as np
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import Sequence

class SentimentDataGenerator(Sequence):
    def __init__(self, csv_file, image_dir, batch_size=32, shuffle=True):
        self.df = pd.read_csv(csv_file)
        # gettin rid of the rows without image filenames coz they're useless here
        self.df.dropna(subset=['filename'], inplace=True)
        self.image_dir = image_dir
        self.batch_size = batch_size
        self.shuffle = shuffle  # shuffle to avoid order bias 
        self.indices = self.df.index.tolist()  # keep track of our data rows

    def __len__(self):
        return len(self.indices) // self.batch_size

    def on_epoch_end(self):
        # end of each round, shuffle fi 
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __getitem__(self, index):
        # grab a batch's worth of data
        # Figure out which ones to grab
        batch_indices = self.indices[index * self.batch_size:(index + 1) * self.batch_size]
        
        batch_images = []
        batch_labels = []
        
        for i in batch_indices:
            filename = self.df.iloc[i, 0]
            
            # skip if we got an empty or messed up filename
            if pd.isna(filename) or filename.strip() == '':
                print(f"Oops, found a bad filename at index {i}") #
                continue
            
            img_path = os.path.join(self.image_dir, filename)
            
            # Try to open and prep the image
            try:
                img = image.load_img(img_path, target_size=(224, 224))
                img = image.img_to_array(img)
                img = np.expand_dims(img, axis=0)  # Make it batch-ready
                img = preprocess_input(img)        # Make it model-ready
                
                # grab the label from the row
                label = self.df.iloc[i, 1:].values.astype('float32')
                
                # keep the image and label
                batch_images.append(img)
                batch_labels.append(label)
            except Exception as e:
                # if something goes wrong, just say so and move on
                print(f"Couldn't process file {img_path}: {e}")
                continue
        
        # If we didn't get any good images, just return nothing
        if not batch_images:
            return None, None
        
        # Stick all the images together and make a proper labels array
        return np.vstack(batch_images), np.array(batch_labels)
