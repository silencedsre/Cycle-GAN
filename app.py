from flask import Flask, request
from flask_cors import CORS
import json
from PIL import Image
from src.cyclegan import *
from flask import send_file, url_for

app = Flask(__name__)

# Allow
CORS(app)

def convert_image(file):
    img = Image.open(file)
    img = np.array(img)
    img = tf.convert_to_tensor(
        img, dtype=None, dtype_hint=None, name=None
    )

    img = tf.reshape(tf.cast(tf.image.resize(img, (int(img_rows), int(img_cols))), tf.float32) / 127.5 - 1,
               (1, img_rows, img_cols, channels))

    # img = tf.image.convert_image_dtype(img, tf.float32)
    # img = tf.image.resize(img, [img_cols, img_rows])
    # img = tf.expand_dims(img, axis=0)
    return img


def load_model():
    generator_g = generator()
    generator_f = generator()

    generator_g.load_weights('./src/temp/models/generator_g.h5')
    generator_f.load_weights('./src/temp/models/generator_f.h5')

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
        img = convert_image(file=file)
        img = img.numpy()
        print(f"Shape of image {img.shape}")
        generator_g, generator_f = load_model()
        y_hat = generator_g.predict(img.reshape((1, img_rows, img_cols, channels)))

        y_hat = (y_hat)*255
        y_hat = y_hat[0].astype(np.uint8)
        im = Image.fromarray(y_hat)
        filename = time.time()
        im.save(f"./static/{filename}.jpg")
        filename = f"{filename}.jpg"
        return url_for('static', filename=filename)

@app.route('/photo_to_monet', methods=['GET', 'POST'])
def photo_to_monet():
    if request.method == 'POST':
        print("request files", request.files)
        file = request.files['file']
        img = convert_image(file=file)
        img = img.numpy()
        print(f"Shape of image {img.shape}")
        generator_g, generator_f = load_model()
        x_hat = generator_f.predict(img.reshape((1, img_rows, img_cols, channels)))

        x_hat = (x_hat)*255
        x_hat = x_hat[0].astype(np.uint8)
        im = Image.fromarray(x_hat)
        filename = time.time()
        im.save(f"./static/{filename}.jpg")
        filename = f"{filename}.jpg"
        return url_for('static', filename=filename)

if __name__ == "__main__":
    app.run(debug=True)