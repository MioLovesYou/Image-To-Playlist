from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

def build_model(num_classes):
    # grabbin the  InceptionV3 not including the top layer (the classification layer)
    base_model = InceptionV3(weights='imagenet', include_top=False)
    x = base_model.output  # get potput 
    
    # add a global average pooling layer to reduce dimensions and get redady for classification
    x = GlobalAveragePooling2D()(x)
    
    # guessing / prediction =  num_classes  - 25 since thats howm any annotaitn
    predictions = Dense(num_classes, activation='softmax')(x)
    
    # create the final model--  inputs and outputs
    model = Model(inputs=base_model.input, outputs=predictions)

    # freezing the base layers so it dont update when trianing
    for layer in base_model.layers:
        layer.trainable = False

    return model



# current inception 
# modelsa: inception net, vgg, residual networks
# different model accuracies take note
# more epoches
# tensorflow visual loss - visualised between training and validation 
# justify epoches - use visualisation