from tensorflow.keras.preprocessing.image import ImageDataGenerator

def preprocess_data(
    train_dir, val_dir, test_dir, 
    target_size=(64, 64),
    batch_size=32
    ):

    train_datagen = ImageDataGenerator(rescale=1./255)
    val_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)

    #training  preprocessing
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical' #categorical cause there's ,ore than 2 classes
    )  

    #validation  preprocessing
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical'
    ) 

    #testing preprocessing
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical'
    ) 

    return train_generator, val_generator, test_generator
    