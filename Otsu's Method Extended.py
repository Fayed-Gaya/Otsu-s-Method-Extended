from PIL import Image as im


def main():
    # Open input image
    with im.open("input1.bmp") as input_image:
        # Get input image size (mode, size, color)
        width, height = input_image.size
        # Create an image object of input image dimensions
        gray_image = im.new('L', (width, height))
        # Create an image access object to be able to manipulate the outptu image
        pixel_map = gray_image.load()

        # convert to grayscale
        for i in range(0, width):
            for j in range(height):
                # Unpack pixel values for all pixel's in the input image
                r, g, b = input_image.getpixel((i, j))
                # Apply professor given grayscale converion formula
                grayscale = (0.299 * r + 0.587 * g + 0.114 * b)
                # Write to output image using pixeel_map image access object
                pixel_map[i, j] = (int(grayscale))
                # gray_image.save("grayscale.bmp")

        total_pix = width * height
        # What is this outer for loop used for? Region counting?
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
