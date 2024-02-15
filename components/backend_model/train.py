from model import build_model
from preprocess import preprocess_data
train_dir = '../../datasets/tiny-imagenet-200/train'
val_dir = '../../datasets/tiny-imagenet-200/val'
test_dir = '../../datasets/tiny-imagenet-200/test'

# Load and preprocess the data
train_generator, val_generator, _ = preprocess_data(train_dir, val_dir, test_dir)

# Build the model
model = build_model(input_shape=(64, 64, 3))  # Update the shape accordingly

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Fit the model
history = model.fit(train_generator, validation_data=val_generator, epochs=10)
model.save('models/model.h5')
