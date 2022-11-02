# 𝐼 = 𝑅ound(0.299𝑅 + 0.587𝐺 + 0.114𝐵)
from PIL import Image as im


def main():
    with im.open("input1.bmp") as input_image:
        width, height = input_image.size
        output_image = im.new('L', (width, height))
        pixel_map = output_image.load()

        # convert to grayscale
        for i in range(0, width):
            for j in range(height):
                r, g, b = input_image.getpixel((i, j))
                grayscale = (0.299 * r + 0.587 * g + 0.114 * b)
                pixel_map[i, j] = (int(grayscale))
                output_image.save("output1.bmp")


if __name__ == "__main__":
    main()
