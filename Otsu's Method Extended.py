from PIL import Image as im

INPUT_IMAGE_PATH = "Input_Images/"
OUTPUT_IMAGE_PATH = "Output_Images/"


def main():
    """
    Collects an input image filename from the user.
    Converts the source image to grayscale.
    Calculates the number of regions in the source image.
    Segments them accordingly.
    Outputs the segmented image.
    """

    # Collect input filename from user
    input_filename = get_input_filename()

    # Generate the output filename
    output_file = OUTPUT_IMAGE_PATH + input_filename[:-4] + "-out.bmp"

    # Create a normalized histogram of gray values from input image
    histogram = get_gray_hist(INPUT_IMAGE_PATH + input_filename)

    # Segment the region into two images using Otsu's method for automatic thresholding for two regions
    otsu2_result = otsu_2(histogram)

    # Segment the region into two images using Otsu's method for automatic thresholding for two regions
    otsu3_result = otsu_3(histogram)

    # Segment the region into two images using Otsu's method for automatic thresholding for four regions
    otsu4_result = otsu_4(histogram)

    # Create and save an output image of marked regions using Otsu's method for automatic thresholding for two regions
    convert_image(
        INPUT_IMAGE_PATH + input_filename,
        output_file,
        region_selector(otsu2_result, otsu3_result, otsu4_result),
    )


def region_selector(*args):
    """
    Return histogram information with the lowest variance.
    : param args: The histograms produced by the different versions of Otsu's extended algorithm.
    """

    lowest_variance = float("inf")
    res = {}
    for segmentation_scan in args:
        lowest_variance = min(lowest_variance, segmentation_scan["var"])
        if segmentation_scan["var"] == lowest_variance:
            res = segmentation_scan

    return res


def get_input_filename():
    """
    Collects an input image filename from the user.
    """

    filename = ""
    while not filename:
        try:
            filename = input("Enter the name of the input image file: ")
        except:
            print("Filename entered incorrectly.")
    return filename


def get_gray_hist(filename):
    """
    Returns a dictionary containing a histogram of the normalized gray level values of an input image.
    :param filname: The name of the image input file
    """

    # We create a histogram of gray level values as a dictionary to improve the performance of Otsu's algorithm implementation
    hist = dict()

    # Open input image
    with im.open(filename) as input_image:
        # Unpack input image size tuple
        width, height = input_image.size
        # Iterate through every pixel and convert it to grayscale
        for i in range(0, width):
            for j in range(height):
                # Unpack the pixel value using the x and y coordinates of the pixel. Returns a tuple containing the red, green, and blue values of the pixel
                r, g, b = input_image.getpixel((i, j))
                # Calculate the grayscale value of the pixel using the formula given by the professor
                grayscale_value = 0.299 * r + 0.587 * g + 0.114 * b
                # Add the grayscale value to our histogram
                grayscale_value = int(grayscale_value)
                hist[grayscale_value] = hist.get(grayscale_value, 0) + 1

        # Count the total number of pizels in our image
        total_pix = 0
        for value in list(hist.values()):
            total_pix += value

        # Noirmalize the histogram to improve convenience
        for gray_val in hist:
            hist[gray_val] = hist[gray_val] / total_pix

        return hist


def otsu_2(hist):
    """
    Returns the total minimum variance, threshold determined using Otsu's algorithm for 2 regions, and number of regions (2).
    :param hist: A normalized histogram of gray level values derived from an input image.
    """

    # Initialize the return dictionary with an inital variance, threshold, and region count of 2 (region count does not change)
    min_var = {"var": -1, "t1": -1, "regions": 2}
    # Test all possible gray level values (0 - 255) as threshholds
    for t in range(0, 256):
        # Initialize background and foreground weights and pixel counts
        weight_bg = weight_fg = 0
        bg_total_gray = fg_total_gray = 0
        # Calculate the number of pixels and the weight of the respective foreground and background regions
        for gray_val in hist:
            # Background calculations
            if gray_val <= t:
                weight_bg += hist[gray_val]
                bg_total_gray += gray_val * hist[gray_val]
            # Forground calculations
            else:
                weight_fg += hist[gray_val]
                fg_total_gray += gray_val * hist[gray_val]

        # Catch ZeroDivsionErrors resulting from 0 weights
        try:
            ave_gray_bg = bg_total_gray / weight_bg
            ave_gray_fg = fg_total_gray / weight_fg
        except ZeroDivisionError:
            continue

        # Initialize the region and total variances to 0.0
        var_fg = 0.0
        var_bg = 0.0
        var_total = 0.0

        # Calculate the regional variances
        for gray_val in hist:
            # Sum the background variance by taking the square of the difference between the average gray value of the region and each gray value in the histogram
            # multiplied by the number of pixels of that grayvalue
            if gray_val <= t:
                var_bg += ((gray_val - ave_gray_bg) ** 2) * hist[gray_val]
            # Repeate the above for foreground
            else:
                var_fg += ((gray_val - ave_gray_fg) ** 2) * hist[gray_val]
        # Multiply the regional variances by their respective weights and then sum them to get the total variance
        var_total = (var_fg * weight_fg) + (var_bg * weight_bg)
        # Identify the minimum total variance generated from across all thresholds and collect that variances corresponding variance value and threshold
        if var_total < min_var["var"] or min_var["var"] == -1:
            min_var["var"] = var_total
            min_var["t1"] = t

    return min_var


def otsu_3(hist):
    """
    Returns the total minimum variance, threshold determined using Otsu's algorithm adapted for 3 regions, and number of regions (3).
    :param hist: A normalized histogram of gray level values derived from an input image.
    """

    # Initialize the return dictionary with an inital variance, 2 thresholds, and a region count of 3 (region count does not change)
    min_var = {"var": -1, "t1": -1, "t2": -1, "regions": 3}
    # Test all possible gray level values (0 - 255)^2 as threshholds
    for t1 in range(0, 256):
        print(f"Otsu 3 Round: {t1}")
        for t2 in range(t1 + 1, 256):
            # Initialize background and foreground weights and pixel counts
            weight_a = weight_b = weight_c = 0
            a_total_gray = b_total_gray = c_total_gray = 0
            # Calculate the number of pixels and the weight of the respective foreground and background regions
            for gray_val in hist:
                # A region calculations, note implicit ranges from order of if statements
                if gray_val <= t1:
                    weight_a += hist[gray_val]
                    a_total_gray += gray_val * hist[gray_val]
                # B region calculations, implicit gray_val >= t1
                elif gray_val <= t2:
                    weight_b += hist[gray_val]
                    b_total_gray += gray_val * hist[gray_val]
                #
                else:
                    weight_c += hist[gray_val]
                    c_total_gray += gray_val * hist[gray_val]

            # Catch ZeroDivsionErrors resulting from 0 weights
            try:
                ave_gray_a = a_total_gray / weight_a
                ave_gray_b = b_total_gray / weight_b
                ave_gray_c = c_total_gray / weight_c
            except ZeroDivisionError:
                continue

            # Initialize the region and total variances to 0.0
            var_a = var_b = var_c = 0.0
            var_total = 0.0

            # Calculate the regional variances
            for gray_val in hist:
                # Sum the background variance by taking the square of the difference between the average gray value of the region and each gray value in the histogram
                # multiplied by the number of pixels of that grayvalue
                if gray_val <= t1:
                    var_a += ((gray_val - ave_gray_a) ** 2) * hist[gray_val]
                # Repeate the above for b and c
                elif gray_val <= t2:
                    var_b += ((gray_val - ave_gray_b) ** 2) * hist[gray_val]
                else:
                    var_c += ((gray_val - ave_gray_c) ** 2) * hist[gray_val]
            # Multiply the regional variances by their respective weights and then sum them to get the total variance
            var_total = (var_a * weight_a) + (var_b * weight_b) + (var_c * weight_c)
            # Identify the minimum total variance generated from across all thresholds and collect that variances corresponding variance value and threshold
            if var_total < min_var["var"] or min_var["var"] == -1:
                min_var["var"] = var_total
                min_var["t1"] = t1
                min_var["t2"] = t2

    return min_var


def otsu_4(hist):
    """
    Returns the total minimum variance, threshold determined using Otsu's algorithm adapted for 4 regions, and number of regions (4).
    :param hist: A normalized histogram of gray level values derived from an input image.
    """

    # Initialize the return dictionary with an inital variance, 3 thresholds, and region count of 4 (region count does not change)
    min_var = {"var": -1, "t1": -1, "t2": -1, "t3": -1, "regions": 4}
    # Test all possible gray level values (0 - 255)^3 as threshholds
    for t1 in range(0, 256):
        print(f"Otsu 4 Round: {t1}")
        for t2 in range(t1 + 1, 256):
            for t3 in range(t2 + 1, 256):
                # Initialize background and foreground weights and pixel counts
                weight_a = weight_b = weight_c = weight_d = 0
                a_total_gray = b_total_gray = c_total_gray = d_total_gray = 0
                # Calculate the number of pixels and the weight of the respective foreground and background regions
                for gray_val in hist:
                    # A region calculations, note implicit ranges from order of if statements
                    if gray_val <= t1:
                        weight_a += hist[gray_val]
                        a_total_gray += gray_val * hist[gray_val]
                    # B region calculations, implicit gray_val > t1
                    elif gray_val <= t2:
                        weight_b += hist[gray_val]
                        b_total_gray += gray_val * hist[gray_val]
                    # C region calculations, implicit gray_val > t2
                    elif gray_val <= t3:
                        gray_val <= t1
                        weight_c += hist[gray_val]
                        c_total_gray += gray_val * hist[gray_val]
                    else:
                        weight_d += hist[gray_val]
                        d_total_gray += gray_val * hist[gray_val]

                # Catch ZeroDivsionErrors resulting from 0 weights
                try:
                    ave_gray_a = a_total_gray / weight_a
                    ave_gray_b = b_total_gray / weight_b
                    ave_gray_c = c_total_gray / weight_c
                    ave_gray_d = d_total_gray / weight_d
                except ZeroDivisionError:
                    continue

                # Initialize the region and total variances to 0.0
                var_a = var_b = var_c = var_d = 0.0
                var_total = 0.0

                # Calculate the regional variances
                for gray_val in hist:
                    # Sum the background variance by taking the square of the difference between the average gray value of the region and each gray value in the histogram
                    # multiplied by the number of pixels of that grayvalue
                    if gray_val <= t1:
                        var_a += ((gray_val - ave_gray_a) ** 2) * hist[gray_val]
                    # Repeate the above for b, c, and d
                    elif gray_val <= t2:
                        var_b += ((gray_val - ave_gray_b) ** 2) * hist[gray_val]
                    elif gray_val <= t3:
                        var_c += ((gray_val - ave_gray_c) ** 2) * hist[gray_val]
                    else:
                        var_d += ((gray_val - ave_gray_d) ** 2) * hist[gray_val]
                # Multiply the regional variances by their respective weights and then sum them to get the total variance
                var_total = (
                    (var_a * weight_a)
                    + (var_b * weight_b)
                    + (var_c * weight_c)
                    + (var_d * weight_d)
                )
                # Identify the minimum total variance generated from across all thresholds and collect that variances corresponding variance value and threshold
                if var_total < min_var["var"] or min_var["var"] == -1:
                    min_var["var"] = var_total
                    min_var["t1"] = t1
                    min_var["t2"] = t2
                    min_var["t3"] = t3

    return min_var


def convert_image(in_name, out_name, var_dict):
    """
    Converts the input image into grayscale based on the threshold calculated by Otsu's method of automatic thresholding.
    :param in_name: The filename of the input image
    :param out_name: The filename of the output image
    :param var_dict: A dictionary containing the calculate minimum variance, the threshold value, and the number of regions
    """

    # Open the input image
    with im.open(in_name) as input_image:
        # Get input image size (mode, size, color)
        width, height = input_image.size
        # Create the output image object in black and white mode using the collected input image dimensions
        gray_image = im.new("RGB", (width, height))
        # Create an image access object to be able write to the output image object
        gray_map = gray_image.load()

        # Iterate through every pixel and convert it to grayscale
        for i in range(0, width):
            for j in range(height):
                # Unpack the pixel value using the x and y coordinates of the pixel. Returns a tuple containing the red, green, and blue values of the pixel
                r, g, b = input_image.getpixel((i, j))
                # Calculate the grayscale value of the pixel using the formula given by the professor
                grayscale = 0.299 * r + 0.587 * g + 0.114 * b
                # Write the grayscale value to output image through the image access object
                gray_map[i, j] = (int(grayscale), int(grayscale), int(grayscale))

        # Identify the number of regions in the image
        num_regions = var_dict["regions"]
        # Segment a two region image
        if num_regions == 2:
            # Assign the pixel a binary value respective to its region determined using the threshold from the dictionary paramter
            for i in range(0, width):
                for j in range(0, height):
                    # Turn background pixels black
                    if gray_map[i, j][0] <= var_dict["t1"]:
                        gray_map[i, j] = (0, 0, 0)
                    # Turn foreground pixels white
                    else:
                        gray_map[i, j] = (255, 255, 255)
        # Segment a three region image
        elif num_regions == 3:
            ...
        # Segment a four region image
        elif num_regions == 4:
            for i in range(0, width):
                for j in range(0, height):
                    if gray_map[i, j][0] <= var_dict["t1"]:
                        gray_map[i, j] = (0, 0, 0)
                    elif gray_map[i, j][0] <= var_dict["t2"]:
                        gray_map[i, j] = (255, 0, 0)
                    elif gray_map[i, j][0] <= var_dict["t3"]:
                        gray_map[i, j] = (0, 255, 0)
                    # Turn foreground pixels white
                    else:
                        gray_map[i, j] = (0, 0, 255)
        # Convert the structure into a try and except clause?
        else:
            print("region error")

        # Save the output image
        gray_image.save(out_name)


if __name__ == "__main__":
    main()
