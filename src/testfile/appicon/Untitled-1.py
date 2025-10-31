from PIL import Image

png_file = "C:\GitHub\daily-report\\app\\appIcon\diary-left-svgrepo-com.png"
ico_file ="C:\GitHub\daily-report\\app\\appIcon\diary-left-svgrepo-com.ico"

img = Image.open(png_file)  
img.save(ico_file)  

#Icon　形式への変換