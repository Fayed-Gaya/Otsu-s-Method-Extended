Computer Vision

In the original Otsu’s method for automatic thresholding, we seek to find a threshold t that minimizes the weighted sum of within-group variances background and foreground pixels that result from thesholding the grayscale image at value t
with 𝐻𝐻(𝑗) the grayscale histogram, N the total number of pixels in the image, and 𝐺 the number of
gray level values. We will extend the Otsu’s method to automatically segment an image that contains
anywhere from two to four regions, with the background being one of the four regions. The number
of regions in the input image will not be known ahead of time. For each test image, our program will
output the number of regions in the image, the threshold values as determined by the extended
Otsu’s method, and the segmented image results.
