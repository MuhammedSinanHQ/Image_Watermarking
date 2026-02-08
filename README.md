# Image Watermarking Web Application

A production-ready Flask web application for adding watermarks to images. This app allows users to add text or logo watermarks to their images with customizable opacity, position, and scale settings.

## Features

- 🖼️ **Multiple Image Input Methods**
  - Upload image files directly
  - Provide image URL
  
- 💧 **Flexible Watermark Options**
  - Add text watermarks
  - Add logo/image watermarks
  - Combine both text and logo
  
- ⚙️ **Customizable Settings**
  - Opacity control (0.0 - 1.0)
  - Position selection (top-left, top-right, bottom-left, bottom-right, center)
  - Scale adjustment (0.1x - 3.0x)
  
- 📥 **Easy Output**
  - Preview watermarked image instantly
  - Download button for saving results

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Image Processing**: OpenCV, PIL (Pillow)
- **Deployment**: Gunicorn, Render
- **Frontend**: HTML5, CSS3, JavaScript

## Local Development

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/MuhammedSinanHQ/Image_Watermarking.git
cd Image_Watermarking
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

### Using the Application

1. **Upload or provide an image**:
   - Click "Upload Image File" to select a local image, OR
   - Paste an image URL in the "Enter Image URL" field

2. **Add watermark** (optional):
   - Upload a logo file, OR
   - Enter text in the "Text Watermark" field, OR
   - Use both for combined watermarks

3. **Adjust settings**:
   - Choose watermark position
   - Adjust opacity slider
   - Adjust scale slider

4. **Process**:
   - Click "✨ Apply Watermark"
   - View the result
   - Click "⬇️ Download Image" to save

## Deployment on Render

### Free Deployment Steps

1. **Create a Render account**:
   - Go to [render.com](https://render.com)
   - Sign up for a free account

2. **Connect your repository**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select this repository

3. **Configure the service**:
   - **Name**: image-watermarking (or your preferred name)
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. **Deploy**:
   - Click "Create Web Service"
   - Wait for the deployment to complete
   - Access your app at the provided URL

### Alternative: Using render.yaml

This repository includes a `render.yaml` file for automated deployment:

1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically detect and use the `render.yaml` configuration
5. Click "Apply" to deploy

### Environment Variables (Optional)

For production, you may want to set:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secret-key`

## Project Structure

```
Image_Watermarking/
├── app.py                      # Main Flask application
├── templates/
│   └── index.html             # Web UI template
├── static/
│   └── output/                # Generated watermarked images
├── requirements.txt           # Python dependencies
├── render.yaml               # Render deployment config
├── Procfile                  # Process file for deployment
├── README.md                 # This file
└── Image_Watermarking.ipynb  # Original notebook demo
```

## Supported Image Formats

- PNG
- JPG/JPEG
- BMP
- WEBP

## Technical Details

- **Max file size**: 16 MB
- **Framework**: Flask 3.0.0
- **Server**: Gunicorn (for production)
- **Image processing**: OpenCV (headless version for server deployment)

## Security Considerations

- File upload size limited to 16 MB
- Only allowed image formats accepted
- URL timeout set to 10 seconds
- Secure filename handling

## License

This project is open source and available for educational and commercial use.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

## Acknowledgments

- Built with Flask and OpenCV
- Inspired by the need for simple, free image watermarking tools
- Designed for easy deployment on Render's free tier
