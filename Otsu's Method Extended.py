# 𝐼 = 𝑅ound(0.299𝑅 + 0.587𝐺 + 0.114𝐵)
from PIL import Image as im

def main():
    with im.open("input1.bmp") as input_image:
        output_image = (input_image.convert("L"))
        output_image.save("output1.bmp")


if __name__ == "__main__":
    main()
