from tensorflow.keras.preprocessing.image import ImageDataGenerator

def preprocess_data(train_dir, val_dir, test_dir, target_size=(64, 64), batch_size=32):
    # Assuming the ImageDataGenerator is properly configured for preprocessing
    train_datagen = ImageDataGenerator(rescale=1./255)
    val_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical')  # or 'binary' if you have binary classes

    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical')  # or 'binary'

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical')  # or 'binary'

    return train_generator, val_generator, test_generator