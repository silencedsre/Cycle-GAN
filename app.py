from flask import Flask, request
from flask_cors import CORS
from PIL import Image
from src.cyclegan import *
from flask import url_for

from matplotlib.pyplot import imsave


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
        y_hat = y_hat[0] * 0.5 + 0.5
        filename = time.time()
        imsave(f'./static/{filename}.png', y_hat, format="png")
        filename = f"{filename}.png"
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
        x_hat = x_hat[0] * 0.5 + 0.5
        filename = time.time()
        imsave(f"./static/{filename}.png", x_hat, format="png")
        filename = f"{filename}.png"
        return url_for('static', filename=filename)

if __name__ == "__main__":
    app.run(debug=True)