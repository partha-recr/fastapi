from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pickle
import numpy as np

app = FastAPI()

# Load model and vectorizer
with open("seeded_kmeans.pkl", "rb") as model_file:
    loaded_kmeans = pickle.load(model_file)

with open("tfidf_vectorizer.pkl", "rb") as vectorizer_file:
    loaded_vectorizer = pickle.load(vectorizer_file)

print("Model and vectorizer loaded successfully!")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello, World!"})

# Function to predict clusters for new logs
def predict_cluster_from_pickle(new_texts):
    X_new = loaded_vectorizer.transform(new_texts)  # Transform new text into TF-IDF
    predicted_clusters = loaded_kmeans.predict(X_new)  # Predict cluster
    return predicted_clusters

@app.post("/predict")
def predictActions():
    inputValue = request.form['inputError']
    print('Value is:',inputValue)
    arr = np.array([inputValue])
    print('Arr value is:',arr)
    predicted_clusters_values = predict_cluster_from_pickle(arr)
    print('Predicted val:',predicted_clusters_values[0]) 
    return str(predicted_clusters_values[0])

#@app.get("/")
#def home():
#    return render_template('index.html')
#    return {"message": "Welcome to FastAPI"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

@app.post("/add")
def add_numbers(data: dict):
    return {"result": data["num1"] + data["num2"]}
