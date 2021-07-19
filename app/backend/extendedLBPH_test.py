from common import *


def recognise_face(img):
    training_data_hist1 = readList(fileName='train1.txt')
    training_data_hist2 = readList(fileName='train2.txt')
    labels1 = readLabeslFromFile(fileName='labels1.txt')
    labels2 = readLabeslFromFile(fileName='labels2.txt')
    image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    dim = (198, 198)
    if  image.shape[0] <=160 or image.shape[1] <= 160:
        dim = (100,100)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    image = cv2.equalizeHist(image)
    image = extended_lbp(image, 1,8)
    image_grids = img_to_grid(image, x=7, y = 7)
    testHist = calculate_weighted_hist(image_grids)
    result = "unknown"
    if image.shape[0] <=160 or image.shape[1] <= 160:
        result = get_perfect_match(training_data_hist2 , testHist,labels2)
    else:
        result = get_perfect_match(training_data_hist1 , testHist,labels1)
    return result

