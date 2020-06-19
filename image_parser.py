



def wrapp_the_image():
    """
    IN PROGRESS
    -> wrapp mrxs image into PIL image object
    """

    ## importation
    from openslide import OpenSlide
    from PIL import Image
    from skimage import filters
    from PIL import ImageFilter
    import numpy
    from matplotlib import pyplot as plt

    ## parameters
    filename = "BGSA1.mrxs"

    ## Extract a PIL object
    mrx_image = OpenSlide(filename)
    truc = mrx_image.get_thumbnail((500,500))


    # Find the edges by applying the filter ImageFilter.FIND_EDGES
    imageWithEdges = truc.filter(ImageFilter.FIND_EDGES)
    # display the new image with edge detection done
    imageWithEdges.show()

    print imageWithEdges

    """
    pil_image = truc.convert('RGB')
    open_cv_image = numpy.array(pil_image)


    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    import cv2
    #Load the image in black and white (0 - b/w, 1 - color).
    img = open_cv_image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);

    #Get the height and width of the image.
    h, w = img.shape[:2]

    #Invert the image to be white on black for compatibility with findContours function.
    imgray = 255 - img
    #Binarize the image and call it thresh.
    ret, thresh = cv2.threshold(imgray, 52, 255, cv2.THRESH_BINARY)
    thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)

    #Find all the contours in thresh. In your case the 3 and the additional strike
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #Calculate bounding rectangles for each contour.
    rects = [cv2.boundingRect(cnt) for cnt in contours]

    print rects
    #Calculate the combined bounding rectangle points.
    top_x = min([x for (x, y, w, h) in rects])
    top_y = min([y for (x, y, w, h) in rects])
    bottom_x = max([x+w for (x, y, w, h) in rects])
    bottom_y = max([y+h for (x, y, w, h) in rects])

    #Draw the rectangle on the image
    out = cv2.rectangle(img, (top_x, top_y), (bottom_x, bottom_y), (0, 255, 0), 2)
    #Save it as out.jpg
    cv2.imwrite('out.jpg', img)
    """


    """

    ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    titles = ['Original Image', 'Global Thresholding (v = 127)','Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [img, th1, th2, th3]
    for i in xrange(4):
        plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()
    """

    """
    from skimage import measure
    import numpy as np

    # Construct some test data
    x, y = np.ogrid[-np.pi:np.pi:100j, -np.pi:np.pi:100j]
    r = np.sin(np.exp((np.sin(x)**3 + np.cos(y)**2)))

    r = numpy.array(truc)
    # Find contours at a constant value of 0.8
    contours = measure.find_contours(r, 0.8)

    # Display the image and plot all contours found
    fig, ax = plt.subplots()
    ax.imshow(r, interpolation='nearest', cmap=plt.cm.gray)

    for n, contour in enumerate(contours):
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
        ax.axis('image')
        ax.set_xticks([])
        ax.set_yticks([])
    plt.show()
    """


    import cv2
    from numpy import array
    pil_image = truc.convert('RGB')
    img = numpy.array(pil_image)
    img2 = array( 200  * (img[:,:,2] > img[:,:, 1]), dtype='uint8')


    edges = cv2.Canny(img2, 70, 50)
    cv2.imwrite('edges.png', edges)

wrapp_the_image()
