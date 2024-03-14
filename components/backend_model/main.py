from data_loader import SentimentDataGenerator
from model import build_model
from train import train
from evaluate import evaluate
from serialize import save_model


IMAGE_DIR = 'datasets/sentiment-dataset/processed'
TRAIN_CSV = 'datasets/sentiment-dataset/processed/train_preprocessed_annotations.csv'
VAL_CSV = 'datasets/sentiment-dataset/processed/val_preprocessed_annotations.csv'
TEST_CSV = 'datasets/sentiment-dataset/processed/test_preprocessed_annotations.csv'
MODEL_SAVE_PATH = 'models/model.h5' #need 2 change this later

# Hyperparameters - change these - testing ect 
BATCH_SIZE = 32
EPOCHS = 10

# Data loading
train_gen = SentimentDataGenerator(TRAIN_CSV, IMAGE_DIR, batch_size=BATCH_SIZE)
val_gen = SentimentDataGenerator(VAL_CSV, IMAGE_DIR, batch_size=BATCH_SIZE)
test_gen = SentimentDataGenerator(TEST_CSV, IMAGE_DIR, batch_size=BATCH_SIZE)

# Model building
model = build_model(num_classes=25)  # Assuming 25 sentiment labels

# Model training
train(model, train_gen, val_gen, epochs=EPOCHS)

# Model evaluation
evaluate(model, test_gen)

# Model serialization
save_model(model, MODEL_SAVE_PATH)
