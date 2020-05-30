from flask import Flask, request
from flask_cors import CORS
import json
from src.cyclegan import *
from flask import send_file

app = Flask(__name__)

# Allow
CORS(app)


def load_model():
    generator_g = generator()
    generator_f = generator()

    generator_g.load_weights('./temp/models/generator_g.h5')
    generator_f.load_weights('./temp/models/generator_f.h5')

    return generator_g, generator_f

def preprocess(img):
    return tf.reshape(tf.cast(tf.image.resize(img, (int(img_rows), int(img_cols))), tf.float32) / 127.5 - 1, (1, img_rows, img_cols, channels))


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/monet_to_photo', methods=['GET', 'POST'])
def monet_to_photo():
    if request.method == 'POST':
        print("request files", request.files)
        file = request.files['file']
        img = preprocess(img=file)
        img = img.numpy()
        print(f"Shape of image {img.shape}")
        generator_g, generator_f = load_model()
        y_hat = generator_g.predict(img.reshape((1, img_rows, img_cols, channels)))

        #todo save y_hat as png or sth
        if request.args.get('type') == '1':
            filename = 'ok.gif'
        else:
            filename = 'error.gif'
        return send_file(filename, mimetype='image/gif')



@app.route('/photo_to_monet', methods=['GET', 'POST'])
def photo_to_monet():
    if request.method == 'POST':
        print("request files", request.files)
        file = request.files['file']
        img = preprocess(img=file)
        img = img.numpy()
        print(f"Shape of image {img.shape}")
        generator_g, generator_f = load_model()
        x_hat = generator_f.predict(img.reshape((1, img_rows, img_cols, channels)))

        #todo save x_hat as png or sth
        if request.args.get('type') == '1':
            filename = 'ok.gif'
        else:
            filename = 'error.gif'
        return send_file(filename, mimetype='image/gif')

if __name__ == "__main__":
    app.run(debug=True)