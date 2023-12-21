from flask import Flask, jsonify, request, send_from_directory
import cv2
import numpy as np
from collections import deque
import base64
import io

app = Flask(__name__)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

colors = {
    'red': {
        'lower': np.array([0, 100, 100]),
        'upper': np.array([10, 255, 255])
    },
    'green': {
        'lower': np.array([36, 100, 100]),
        'upper': np.array([86, 255, 255])
    },
    'blue': {
        'lower': np.array([110, 100, 100]),
        'upper': np.array([130, 255, 255])
    
    },
    'yellow': {
        'lower': np.array([20, 100, 100]),
        'upper': np.array([30, 255, 255]),
        'color': (0, 255, 255)
    },
    'black': {
        'lower': np.array([0, 0, 0]),
        'upper': np.array([180, 255, 30]),
        'color': (0, 0, 0)
    },
    'white': {
        'lower': np.array([0, 0, 200]),
        'upper': np.array([180, 255, 255]),
        'color': (255, 255, 255)
    }
}

@app.route('/detect-color', methods=['POST'])
def detect_color():
    # Get image data from the request
    image_data = request.json['image']
    image_data = base64.b64decode(image_data.split(',')[1])

    # Convert the image data to a numpy array
    nparr = np.fromstring(image_data, np.uint8)

    # Read the image
    imgOriginal = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert the image to HSV
    hsv = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    # Loop over the colors dictionary
    for color_name, color_info in colors.items():
        # Create a mask for the current color
        mask = cv2.inRange(hsv, color_info['lower'], color_info['upper'])

        # If the mask contains any white pixels, the color is present in the image
        if cv2.countNonZero(mask) > 0:
            return jsonify({'color': color_name})

    # If no color was detected, return an error
    return jsonify({'error': 'No color detected'}), 400
if __name__ == '__main__':
    app.run(debug=True)