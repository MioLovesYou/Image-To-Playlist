def save_model(model, filepath):
    model.save(filepath)

def load_model(filepath):
    return tf.keras.models.load_model(filepath)
