# AI-Outfit-Accessor
This project is a simple web app that generates a fashion mood board by matching uploaded clothing items (tops or bottoms) with the best complementary item from a dataset using color and shape similarity.

## Features
- Upload a clothing item (top or bottom)
- Automatically finds the best matching item from the dataset (e.g., upload a shirt, get matching pants)
- Generates a mood board image with both items
- Simple, easy-to-use web interface

## How it works
- Uses color histogram and aspect ratio to match items
- Always displays the uploaded item in its correct position (top or bottom)
- Matching logic is simple and fast (no deep learning required)

## Setup
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd AI-Outfit-Acc
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   (You may need to create a `requirements.txt` with: `flask pillow scikit-learn rembg numpy`)
3. **Run the app:**
   ```bash
   python app.py
   ```
4. **Open your browser:**
   Go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Project Structure
- `app.py` - Main Flask app
- `Matcher.py` - Matching logic
- `dataset/` - Clothing images (organized by gender/category)
- `static/` - Output moodboards, uploads, and styles
- `templates/` - HTML templates
