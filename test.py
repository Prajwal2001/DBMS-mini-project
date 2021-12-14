import pyqrcode
import png

# String which represents the QR code
s = "This is my qrcode"

# Generate QR code
url = pyqrcode.create(s)

# Create and save the png file naming "myqr.png"
url.png('myqr.png', scale=6)
