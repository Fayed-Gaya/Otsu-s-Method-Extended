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

    # Create and save an output image of marked regions using Otsu's method for automatic thresholding for two regions
    convert_image(INPUT_IMAGE_PATH + input_filename, output_file, otsu2_result)


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

    # Open input image
    with im.open(filename) as input_image:
        # Unpack input image size tuple
        width, height = input_image.size
        # Create the output image in black and white mode using the size collected from the input image
        gray_image = im.new("L", (width, height))
        # Why do we call load()? Is it because it returns an image access object which is the only way to to write to an image object?
        gray_map = gray_image.load()

        # Iterate through every pixel and convert it to grayscale
        for i in range(0, width):
            for j in range(height):
                # Unpack the pixel value using the x and y coordinates of the pixel. Returns a tuple containing the red, green, and blue values of the pixel
                r, g, b = input_image.getpixel((i, j))
                # Calculate the grayscale value of the pixel using the formula given by the professor
                grayscale = 0.299 * r + 0.587 * g + 0.114 * b
                # Write the grayscale value to output image through the image access object
                gray_map[i, j] = int(grayscale)
                # gray_image.save("grayscale.bmp")

        # We create a histogram of gray level values as a dictionary to improve the performance of Otsu's algorithm implementation
        hist = dict()
        # Iteratre through every pixel in our grayscale image and insert it in our dictionary
        for i in range(0, width):
            for j in range(height):
                gray_val = gray_map[i, j]
                hist[gray_val] = hist.get(gray_val, 0) + 1

        # We then normalize the historgram to ?
        total_pix = 0
        for gray_val in hist:
            total_pix += hist[gray_val]

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

        # Avoid the division be zero error (could replace this with a try and except clause?)
        if weight_bg == 0 or weight_fg == 0:
            continue
        ave_gray_bg = bg_total_gray / weight_bg
        ave_gray_fg = fg_total_gray / weight_fg

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
        gray_image = im.new("L", (width, height))
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
                gray_map[i, j] = int(grayscale)

        # Identify the number of regions in the image
        num_regions = var_dict["regions"]
        # Segment a two region image
        if num_regions == 2:
            # Assign the pixel a binary value respective to its region determined using the threshold from the dictionary paramter
            for i in range(0, width):
                for j in range(0, height):
                    # Turn background pixels black
                    if gray_map[i, j] <= var_dict["t1"]:
                        gray_map[i, j] = 0
                    # Turn foreground pixels white
                    else:
                        gray_map[i, j] = 255
        # Segment a three region image
        elif num_regions == 3:
            return var_dict  # placeholder
        # Segment a four region image
        elif num_regions == 4:
            return var_dict  # placeholder
        # Convert the structure into a try and except clause?
        else:
            print("region error")

        # Save the output image
        gray_image.save(out_name)


if __name__ == "__main__":
    main()
