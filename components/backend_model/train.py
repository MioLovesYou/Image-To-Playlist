from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy

def train(model, train_gen, val_gen, epochs=10):
    model.compile(optimizer=Adam(), loss=BinaryCrossentropy(from_logits=True), metrics=['accuracy'])
    for epoch in range(epochs):
        for batch in range(len(train_gen)):
            x, y = train_gen[batch]
            if x is not None:
                model.train_on_batch(x, y)
        # Validate after each epoch
        for batch in range(len(val_gen)):
            x, y = val_gen[batch]
            if x is not None:
                model.test_on_batch(x, y)
    model.fit(train_gen, validation_data=val_gen, epochs=epochs)
