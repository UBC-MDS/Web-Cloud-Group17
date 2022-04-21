from flask import Flask, request, jsonify
from boto3.session import Session
import joblib
import numpy as np
## Import any other packages that are needed

app = Flask(__name__)
app.debug = True

# 1. Load your model here
session = Session(
    aws_access_key_id="ASIAQ3IZ36HL2AQ7SFA6",
    aws_secret_access_key="MZ77hywv4TmfhoII77S4qhQat6J2f42b54Hi/yQD",
    aws_session_token="FwoGZXIvYXdzEJD//////////wEaDOeJdSgwFso86voVziLCAbavNQ40YxRN3VLRxB2i6EeGPaScy1IyvRmdz7JP02y1a2sj3AFdG7seDx2vJ6J/j4wdRpkttiaMQZY21GrcHrpIaVgO5RUeeoXTjYPAV2KZAuZANPMJJ4r+nUzTsDWZj9u0hADoo0t5DYmsCfPfyUIN3jiGLGdKWVk7C2/mWXvBOBPLceSvJhdQW1fiZkfMPSmhwGuYl6Ju3NOAKW8FV4R1m7G2vD05y0dapjysMpQJsEVDeQKB66QRvOZ7kWxHX4U3KPOvh5MGMi2vMGNJgvn4bC41BAxmKQwXUROvnGngwjiAXF4KCLA2wEWuDiqX+MIEZz+6Ujg="
)
s3 = session.resource("s3")
bucket = s3.Bucket("mds-s3-17")
bucket.download_file("output/model.joblib", './data/model.joblib')

model = joblib.load("./data/model.joblib")

# 2. Define a prediction function
def return_prediction(content):

    # format input_data here so that you can pass it to model.predict()
    data = content["data"]
    features = np.array(data)
    return model.predict(features)

# 3. Set up home page using basic html
@app.route("/")
def index():
    # feel free to customize this if you like
    return """
    <h1>Welcome to our rain prediction service</h1>
    To use this service, make a JSON post request to the /predict url with 25 climate model outputs.
    """

# 4. define a new route which will accept POST requests and return model predictions
@app.route('/predict', methods=['POST'])
def rainfall_prediction():
    content = request.json  # this extracts the JSON content we sent
    prediction = return_prediction(content)
    results = {
        "input": str(content["data"]),
        "predictions": str(prediction),
    }  # return whatever data you wish, it can be just the prediction
                     # or it can be the prediction plus the input data, it's up to you
    return jsonify(results)