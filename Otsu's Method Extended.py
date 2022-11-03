# 𝐼 = 𝑅ound(0.299𝑅 + 0.587𝐺 + 0.114𝐵)
from PIL import Image as im


def main():
    with im.open("input1.bmp") as input_image:
        width, height = input_image.size
        gray_image = im.new('L', (width, height))
        pixel_map = gray_image.load()

        # convert to grayscale
        for i in range(0, width):
            for j in range(height):
                r, g, b = input_image.getpixel((i, j))
                grayscale = (0.299 * r + 0.587 * g + 0.114 * b)
                pixel_map[i, j] = (int(grayscale))
                # gray_image.save("grayscale.bmp")

        total_pix = width * height
        for t in range(0, 1):
            # calculate weights and average gray values
            fg_total_pix = fg_total_gray = 0
            bg_total_pix = bg_total_gray = 0
            for i in range(0, width):
                for j in range(0, height):
                    gray_val = pixel_map[i, j]
                    if (gray_val > t):
                        fg_total_pix += 1
                        fg_total_gray += gray_val
                    else:
                        bg_total_pix += 1
                        bg_total_gray += gray_val

            weight_fg = (fg_total_pix/total_pix)
            ave_gray_fg = (fg_total_gray/total_pix)
            weight_bg = (bg_total_pix/total_pix)
            ave_gray_bg = (bg_total_gray/total_pix)

            # calculate regional variances
            var_fg = 0.0
            var_bg = 0.0
            var_total = 0.0
            for i in range(0, width):
                for j in range(0, height):
                    gray_val = pixel_map[i, j]
                    if (gray_val > t):
                        var_fg += ((gray_val - ave_gray_fg)**2)/total_pix
                    else:
                        var_bg += ((gray_val - ave_gray_bg)**2)/total_pix

            var_total = (var_fg * weight_fg) + (var_bg * weight_bg)


if __name__ == "__main__":
    main()
