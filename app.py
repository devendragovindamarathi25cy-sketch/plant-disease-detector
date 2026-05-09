from flask import Flask, request
from PIL import Image
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load AI model
model = tf.keras.models.load_model("plant_disease_model.h5")

# Disease classes
classes = [
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Potato Early Blight",
    "Rice Brown Spot",
    "Healthy Leaf"
]

# Medicine database
medicine_data = {
    "Tomato Early Blight": {
        "medicine": "Chlorothalonil",
        "suggestion": "Remove infected leaves and avoid overwatering.",
        "severity": "Medium"
    },

    "Tomato Late Blight": {
        "medicine": "Mancozeb",
        "suggestion": "Spray fungicide immediately.",
        "severity": "High"
    },

    "Potato Early Blight": {
        "medicine": "Copper Oxychloride",
        "suggestion": "Use disease-free seeds.",
        "severity": "Medium"
    },

    "Rice Brown Spot": {
        "medicine": "Carbendazim",
        "suggestion": "Improve drainage and use healthy seeds.",
        "severity": "Low"
    },

    "Healthy Leaf": {
        "medicine": "No medicine needed",
        "suggestion": "Your plant is healthy.",
        "severity": "None"
    }
}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>

    <html>

    <head>

        <title>AI Plant Disease Detector</title>

        <style>

            body{
                font-family: Arial;
                background: linear-gradient(to right,#d4fc79,#96e6a1);
                text-align:center;
                padding-top:70px;
            }

            .container{
                background:white;
                width:85%;
                max-width:500px;
                margin:auto;
                padding:35px;
                border-radius:20px;
                box-shadow:0 0 20px rgba(0,0,0,0.2);
            }

            h1{
                color:green;
            }

            input{
                margin-top:20px;
            }

            button{
                margin-top:20px;
                background:green;
                color:white;
                border:none;
                padding:12px 25px;
                border-radius:10px;
                font-size:16px;
                cursor:pointer;
            }

            button:hover{
                background:darkgreen;
            }

        </style>

    </head>

    <body>

        <div class="container">

            <h1>🌿 Real AI Plant Disease Detector</h1>

            <p>Upload crop leaf image to detect disease</p>

            <form action="/predict" method="POST" enctype="multipart/form-data">

                <input type="file" name="leaf" required>

                <br>

                <button type="submit">Detect Disease</button>

            </form>

        </div>

    </body>

    </html>
    '''

@app.route('/predict', methods=['POST'])
def predict():

    file = request.files['leaf']

    image = Image.open(file).convert('RGB')

    image = image.resize((224,224))

    img_array = np.array(image)

    img_array = img_array / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)

    predicted_index = np.argmax(prediction)

    disease_name = classes[predicted_index]

    confidence = round(100 * np.max(prediction),2)

    disease = medicine_data[disease_name]

    return f'''

    <!DOCTYPE html>

    <html>

    <head>

        <title>Prediction Result</title>

        <style>

            body{{
                font-family:Arial;
                background: linear-gradient(to right,#d4fc79,#96e6a1);
                text-align:center;
                padding-top:50px;
            }}

            .card{{
                background:white;
                width:85%;
                max-width:550px;
                margin:auto;
                padding:30px;
                border-radius:20px;
                box-shadow:0 0 20px rgba(0,0,0,0.2);
            }}

            h1{{
                color:red;
            }}

            h2{{
                color:green;
            }}

            img{{
                width:220px;
                border-radius:15px;
                margin-top:15px;
            }}

            .btn{{
                display:inline-block;
                margin-top:20px;
                background:green;
                color:white;
                padding:12px 20px;
                border-radius:10px;
                text-decoration:none;
            }}

        </style>

    </head>

    <body>

        <div class="card">

            <h1>🌿 Disease Detected</h1>

            <h2>{disease_name}</h2>

            <h3>Confidence: {confidence}%</h3>

            <h3>Severity: {disease['severity']}</h3>

            <p>
                <b>Suggestion:</b><br>
                {disease['suggestion']}
            </p>

            <h3>Recommended Medicine:</h3>

            <p>{disease['medicine']}</p>

            <a href="/" class="btn">Check Another Leaf</a>

        </div>

    </body>

    </html>

    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
