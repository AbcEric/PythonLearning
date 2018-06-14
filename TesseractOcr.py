from PIL import Image

import pytesseract

# , lang='chi_sim'
#text = pytesseract.image_to_string(Image.open('c:/temp/verifycode.png'))
text = pytesseract.image_to_string(Image.open('c:/temp/demo.png'))
print(text)