import tesserocr
from PIL import Image

image = Image.open('code.jpg')
result = tesserocr.imgage_to_text(image)
print(result)

print(tesserocr.file_to_text('image.png'))


# 对于有干扰的验证码，可以通过“转灰度”、“二值化” 等操作来
#  净化图片，使图片黑白分明，变得容易识别；

# 利用Image对象的convert()方法，传入参数L，可以将图片转化为“灰度图像”
image = image.convert('L')
image.show()

# convert()方法，传入参数“1” 可以对图片二值化处理：
image = image.convert('1')
image.show()

# 可以指定二值化的阀值，
# 先将原图转化成灰度图，然后再指定二值化阀值
image = image.convert('L')
threshold = 127
table = []
for i in range(256):
	if i < threshold:
		table.append(0)
	else:
		table.append(1)
image = image.point(table, '1')
result = tesserocr.image_to_text(image)
print(result)