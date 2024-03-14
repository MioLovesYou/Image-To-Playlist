def evaluate(model, test_gen):
    results = model.evaluate(test_gen)
    print(f"Test Loss, Test Accuracy: {results}")
