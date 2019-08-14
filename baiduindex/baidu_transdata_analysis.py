# 其实这个部分最简单，也就是图像处理了，调用一个函数就可以了；
import pytesseract

index = []
index_image = Image.open(str(path) + "zoom.jpg")
num = pytesseract.image_to_string(index_image)
if num:
  index.append(num)