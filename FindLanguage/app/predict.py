import fasttext

# Load the model once at the start
model = fasttext.load_model('./models/lid.176.ftz')

def predict_language(content):
    predictions = model.predict(content, k=1)
    language_code = predictions[0][0].replace("__label__", "")
    return language_code
