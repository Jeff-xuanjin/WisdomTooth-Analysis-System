from PIL import Image

# 打开JPG图片
img = Image.open('input.jpg')

# 保存为PNG
img.save('output.png')