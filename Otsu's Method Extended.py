from PIL import Image as im


def main():
    hist = gray_hist("input1.bmp")
    otsu2_result = otsu_2(hist)
    print(otsu2_result)


def gray_hist(filename):
    # Open input image
    with im.open(filename) as input_image:
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

        # create histogram
        hist = dict()
        for i in range(0, width):
            for j in range(height):
                gray_val = pixel_map[i, j]
                hist[gray_val] = hist.get(gray_val, 0) + 1

        # normalize histogram
        total_pix = 0
        for gray_val in hist:
            total_pix += hist[gray_val]

        for gray_val in hist:
            hist[gray_val] = hist[gray_val]/total_pix

        return hist


def otsu_2(hist):
    ################### OTSU 2 REGIONS ####################
    # set flag values for min variance
    min_var = {"var": -1, "t1": -1}
    # Test all possible thresholds
    for t in range(0, 256):
        # calculate weights and average gray values
        weight_bg = weight_fg = 0
        bg_total_gray = fg_total_gray = 0
        for gray_val in hist:
            if (gray_val <= t):
                weight_bg += hist[gray_val]
                bg_total_gray += (gray_val * hist[gray_val])
            else:
                weight_fg += hist[gray_val]
                fg_total_gray += (gray_val * hist[gray_val])

        # avoid division by zero
        if (weight_bg == 0 or weight_fg == 0):
            continue
        ave_gray_bg = (bg_total_gray/weight_bg)
        ave_gray_fg = (fg_total_gray/weight_fg)

        # calculate regional variances
        var_fg = 0.0
        var_bg = 0.0
        var_total = 0.0
        for gray_val in hist:
            if (gray_val <= t):
                var_bg += ((gray_val - ave_gray_bg)**2) * \
                    hist[gray_val]  # implicit division by 1
            else:
                var_fg += ((gray_val - ave_gray_fg)**2) * hist[gray_val]
        #print(f"VBG: {var_bg}, VFG: {var_fg}")
        # calculate total variance for current threshold
        var_total = (var_fg * weight_fg) + (var_bg * weight_bg)
        # save min variance and threshold, -1 to set first min
        if (var_total < min_var["var"] or min_var["var"] == -1):
            min_var["var"] = var_total
            min_var["t1"] = t

    return min_var


if __name__ == "__main__":
    main()
