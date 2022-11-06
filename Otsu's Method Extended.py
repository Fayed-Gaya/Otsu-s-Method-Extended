from PIL import Image as im


def main():
    hist = get_gray_hist("blackroll-duoball.bmp")
    otsu2_result = otsu_2(hist)
    convert_image("blackroll-duoball.bmp",
                  "otsu_result_blackroll.bmp", otsu2_result)


# takes image filename as input and returns histogram dict based on grayscale version of original image
def get_gray_hist(filename):
    # Open input image
    with im.open(filename) as input_image:
        # Get input image size (mode, size, color)
        width, height = input_image.size
        # Create an image object of input image dimensions
        gray_image = im.new('L', (width, height))
        # Create an image access object to be able to manipulate the outptu image
        gray_map = gray_image.load()

        # convert to grayscale
        for i in range(0, width):
            for j in range(height):
                # Unpack pixel values for all pixel's in the input image
                r, g, b = input_image.getpixel((i, j))
                # Apply professor given grayscale converion formula
                grayscale = (0.299 * r + 0.587 * g + 0.114 * b)
                # Write to output image using pixeel_map image access object
                gray_map[i, j] = (int(grayscale))
                # gray_image.save("grayscale.bmp")

        # create histogram
        hist = dict()
        for i in range(0, width):
            for j in range(height):
                gray_val = gray_map[i, j]
                hist[gray_val] = hist.get(gray_val, 0) + 1

        # normalize histogram
        total_pix = 0
        for gray_val in hist:
            total_pix += hist[gray_val]

        for gray_val in hist:
            hist[gray_val] = hist[gray_val]/total_pix

        return hist

# converts image into visual, grayscale representation of segmented regions


def convert_image(in_name, out_name, var_dict):
    # Open input image
    with im.open(in_name) as input_image:
        # Get input image size (mode, size, color)
        width, height = input_image.size
        # Create an image object of input image dimensions
        gray_image = im.new('L', (width, height))
        # Create an image access object to be able to manipulate the outptu image
        gray_map = gray_image.load()

        # convert to grayscale
        for i in range(0, width):
            for j in range(height):
                # Unpack pixel values for all pixel's in the input image
                r, g, b = input_image.getpixel((i, j))
                # Apply professor given grayscale converion formula
                grayscale = (0.299 * r + 0.587 * g + 0.114 * b)
                # Write to output image using pixeel_map image access object
                gray_map[i, j] = (int(grayscale))

        # segmentation on grayscale image 2 regions
        if (var_dict["regions"] == 2):
            for i in range(0, width):
                for j in range(0, height):
                    if (gray_map[i, j] <= var_dict["t1"]):
                        gray_map[i, j] = 0
                    else:
                        gray_map[i, j] = 255
        else:
            return var_dict  # placeholder, eventually code out 3 and 4 region versions

        gray_image.save(out_name)


# takes histogram as input and returns dict with total minimum variance (var), threshold (t1), and number of regions (regions)
def otsu_2(hist):
    ################### OTSU 2 REGIONS ####################
    # set flag values for min variance, threshold, and set region number to 2
    min_var = {"var": -1, "t1": -1, "regions": 2}
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
                var_bg += ((gray_val - ave_gray_bg)**2) * hist[gray_val]
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
