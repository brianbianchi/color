import base64
from io import BytesIO
from flask import Flask, render_template, request
from PIL import Image
from analyze import analyze_image

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400
        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400
        if file:
            img = Image.open(file.stream)
            median_rgb, dominant_rgb, actual_color, closest_color = analyze_image(img)
            # Store image in memory
            with BytesIO() as buf:
                img = img.convert('RGB') # RGBA -> RGB
                img.save(buf, 'jpeg')
                image_bytes = buf.getvalue()
            encoded_string = base64.b64encode(image_bytes).decode()    
            return render_template('info.html', 
                                   median_rgb=median_rgb,
                                   dominant_rgb=dominant_rgb,
                                   actual_color=actual_color,
                                   closest_color=closest_color,
                                   img_data=encoded_string)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)