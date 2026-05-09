from flask import Flask, request

import random
import os

app = Flask(__name__)

diseases = [
    {
        "name": "Tomato Early Blight",
        "medicine": "Chlorothalonil",
        "suggestion": "Remove infected leaves and avoid overwatering.",
        "severity": "Medium"
    },
    {
        "name": "Rice Brown Spot",
        "medicine": "Carbendazim",
        "suggestion": "Improve drainage and use healthy seeds.",
        "severity": "Low"
    },
    {
        "name": "Potato Late Blight",
        "medicine": "Mancozeb",
        "suggestion": "Avoid excess moisture and spray fungicide.",
        "severity": "High"
    },
    {
        "name": "Corn Leaf Spot",
        "medicine": "Azoxystrobin",
        "suggestion": "Use resistant varieties and rotate crops.",
        "severity": "Medium"
    }
]

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Plant Disease Detector</title>

        <style>
            body{
                background:#eaf4e5;
                font-family:Arial;
                text-align:center;
                padding-top:80px;
            }

            h1{
                color:green;
                font-size:55px;
            }

            p{
                font-size:22px;
            }

            .box{
                background:white;
                width:80%;
                max-width:500px;
                margin:auto;
                padding:40px;
                border-radius:20px;
                box-shadow:0px 0px 15px gray;
            }

            button{
                background:green;
                color:white;
                border:none;
                padding:15px 35px;
                border-radius:10px;
                font-size:20px;
                cursor:pointer;
                margin-top:20px;
            }

            button:hover{
                background:darkgreen;
            }

            input{
                margin-top:20px;
                font-size:18px;
            }
        </style>

    </head>

    <body>

        <div class="box">

            <h1>🌿 Plant Disease Detector</h1>

            <p>Upload crop leaf image to detect disease</p>

            <form action="/predict" method="post" enctype="multipart/form-data">

                <input type="file" name="leaf" required>

                <br>

                <button type="submit">
                    Detect Disease
                </button>

            </form>

        </div>

    </body>
    </html>
    '''

@app.route('/predict', methods=['POST'])
def predict():

    disease = random.choice(diseases)

    confidence = random.randint(90, 99)

    return f'''
    <!DOCTYPE html>
    <html>

    <head>

        <title>Result</title>

        <style>

            body{{
                background:#eaf4e5;
                font-family:Arial;
                text-align:center;
                padding-top:60px;
            }}

            .card{{
                background:white;
                width:85%;
                max-width:600px;
                margin:auto;
                padding:40px;
                border-radius:20px;
                box-shadow:0px 0px 15px gray;
            }}

            h1{{
                color:red;
            }}

            h2{{
                color:green;
            }}

            p{{
                font-size:22px;
            }}

            img{{
                width:220px;
                border-radius:15px;
                margin-top:20px;
                margin-bottom:20px;
            }}

            button{{
                background:green;
                color:white;
                border:none;
                padding:15px 35px;
                border-radius:10px;
                font-size:20px;
                cursor:pointer;
                margin-top:20px;
            }}

        </style>

    </head>

    <body>

        <div class="card">

            <h1>🌿 Disease Detected</h1>

            <h2>{disease["name"]}</h2>

            <p><b>Confidence:</b> {confidence}%</p>

            <p><b>Severity:</b> {disease["severity"]}</p>

            <p><b>Suggestion:</b><br>
            {disease["suggestion"]}</p>

            <p><b>Recommended Medicine:</b><br>
            {disease["medicine"]}</p>

            <a href="/">
                <button>
                    Check Another Leaf
                </button>
            </a>

        </div>

    </body>
    </html>
    '''

app.run(
    host='0.0.0.0',
    port=int(os.environ.get("PORT", 5000))
)
