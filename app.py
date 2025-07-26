import os
from flask import Flask, render_template, request
from PIL import Image, ImageOps, ImageDraw, ImageFont
from rembg import remove
import io
import random
from Matcher import find_best_match

app = Flask(__name__)

BASE_DIR = 'dataset'  
OUTPUT_DIR = 'static/output'
UPLOAD_DIR = 'static/uploads'
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_opposite_category(cat):
    return 'bottom' if cat == 'upper' else 'upper'

def remove_bg(image_path):
    with open(image_path, 'rb') as f:
        img_bytes = f.read()
    result = remove(img_bytes)
    return Image.open(io.BytesIO(result))

def create_styled_moodboard(upload_img_path, matched_img_path, output_path):
    def draw_decorations(draw, width, height):
        pastel_colors = [(255, 204, 204), (204, 255, 229), (204, 229, 255), (255, 255, 204)]
        for _ in range(10):
            radius = random.randint(15, 30)
            x = random.randint(0, width - radius)
            y = random.randint(0, height - radius)
            color = random.choice(pastel_colors)
            draw.ellipse((x, y, x + radius, y + radius), fill=color)

        symbols = ['★', '♡', '✿', '❀']
        try:
            deco_font = ImageFont.truetype("arial.ttf", 18)
        except IOError:
            deco_font = ImageFont.load_default()

        for _ in range(6):
            x = random.randint(0, width - 20)
            y = random.randint(0, height - 20)
            draw.text((x, y), random.choice(symbols), fill="gray", font=deco_font)

    top_img = remove_bg(upload_img_path)
    bottom_img = remove_bg(matched_img_path)

    base_width = 300
    top_img = ImageOps.contain(top_img, (base_width, int(base_width * top_img.height / top_img.width)))
    bottom_img = ImageOps.contain(bottom_img, (base_width, int(base_width * bottom_img.height / bottom_img.width)))

    padding = 20
    spacing = 15
    canvas_width = base_width + 2 * padding
    canvas_height = top_img.height + bottom_img.height + 3 * padding + spacing

    moodboard = Image.new("RGBA", (canvas_width, canvas_height), (255, 250, 240, 255))
    draw = ImageDraw.Draw(moodboard)
    draw_decorations(draw, canvas_width, canvas_height)

    moodboard.paste(top_img, (padding, padding), top_img)
    moodboard.paste(bottom_img, (padding, padding + top_img.height + spacing), bottom_img)

    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    quote = "✨ Fashion is the armor to survive everyday life ✨"
    bbox = draw.textbbox((0, 0), quote, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (canvas_width - text_width) // 2
    text_y = canvas_height - padding
    draw.text((text_x, text_y), quote, fill="black", font=font)

    moodboard.convert("RGB").save(output_path, "JPEG")

@app.route('/', methods=['GET', 'POST'])
def index():
    moodboard_filename = None

    if request.method == 'POST':
        gender = request.form.get('gender')
        category = request.form.get('category')
        uploaded_file = request.files.get('image')

        if gender and category and uploaded_file:
            upload_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
            uploaded_file.save(upload_path)

            opposite_cat = get_opposite_category(category)
            matched_img_path = find_best_match(BASE_DIR, gender, opposite_cat, upload_path)
            if not matched_img_path:
                return "No match found in dataset!", 400

            output_filename = f"moodboard_{uploaded_file.filename.rsplit('.', 1)[0]}.jpg"
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            # Ensure correct placement: top, bottom
            if category == "upper":
                create_styled_moodboard(upload_path, matched_img_path, output_path)
            else:
                create_styled_moodboard(matched_img_path, upload_path, output_path)

            moodboard_filename = output_filename

    return render_template('index.html', moodboard=moodboard_filename)

if __name__ == '__main__':
    app.run(debug=True)
