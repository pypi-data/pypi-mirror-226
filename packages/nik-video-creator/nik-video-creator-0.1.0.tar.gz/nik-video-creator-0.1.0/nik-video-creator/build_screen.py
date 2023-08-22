import cv2
import numpy as np 
from PIL import Image, ImageDraw, ImageFont

### by nikhil #####

def alpha_blend(foreground, background, alpha, x, y):
    """
    Perform alpha blending.
    
    Parameters:
    - foreground: The top image.
    - background: The image where the top image will be overlaid.
    - alpha: The transparency mask.
    - x, y: The coordinates to overlay the top image.
    
    Returns:
    - Blended image.
    """
    h, w, _ = foreground.shape
    blended = background.copy()
    for c in range(3):
        blended[y:y+h, x:x+w, c] = (foreground[:, :, c] * alpha + blended[y:y+h, x:x+w, c] * (1 - alpha))
    return blended

def build_screen(screen_file, combine_file_name, x_coordinate, sceen_name, text_to_be_added): 

    x_coordinate = x_coordinate - 300
    
    # Load the images
    background = cv2.imread('background.png')
    overlay = cv2.imread(screen_file)
    mobile = cv2.imread('features/mobile_2.png')

    #resise image
    h_o, w_o, _ = overlay.shape
    overlay = cv2.resize(overlay, (int(w_o * 0.72), int(h_o * 0.60)))   
    overlay = overlay[0: 490, 0:400] 


    #mask
    threshold = 10
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.inRange(mobile[:, :, :3], (0, 0, 0), (threshold, threshold, threshold))
    eroded_mask = cv2.erode(mask, kernel, iterations=1)
    dilated_eroded_mask = cv2.dilate(eroded_mask, kernel, iterations=1) 
    cv2.imshow('Mask', mask)
    contours, _ = cv2.findContours(dilated_eroded_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  

    
    largest_contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    refined_mask = np.zeros_like(mask)
    cv2.drawContours(refined_mask, [largest_contour], -1, (255), thickness=cv2.FILLED)
    refined_alpha_channel = refined_mask / 255.0
    

    h_o, w_o, _ = overlay.shape
    m_h_o, m_w_o, _ = mobile.shape[:3] 
    h_b, w_b, _ = background.shape 
    x, y = x_coordinate + 20, 210 
    m_x, m_y = x_coordinate, 135


    #background[m_y:m_y+m_h_o, m_x: m_x+m_w_o] = mobile 
    background = alpha_blend(mobile[:, :, :3], background, refined_alpha_channel, m_x, m_y)
    background[y:y+h_o, x:x+w_o] = overlay 


    # if text_to_be_added == True:
    #     font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    #     font_scale = 2
    #     font_thickness = 3
    #     text = sceen_name
    #     (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

    #     if x_coordinate == 400:
    #         x = x_coordinate + 350
    #     else:
    #         x = x_coordinate - 400  
    #     y = background.shape[0] - 540  

    #     cv2.putText(background, text, (x, y), font, font_scale, (255, 255, 255), font_thickness, lineType=cv2.LINE_AA)  


    ## ----- Apply white color ----- ######## 
    # Define a mask for black color
    # Here we are assuming that any pixel with RGB values (0,0,0) is black.
    # You can change the thresholds if you need to catch near-black colors.
    lower = np.array([0, 0, 0], dtype="uint8")
    upper = np.array([1, 1, 1], dtype="uint8")
    mask = cv2.inRange(background, lower, upper)

    # Change black to white
    background[mask == 255] = [255, 255, 255]


    

    # Save the modified image

    if text_to_be_added:
        # Convert OpenCV image to Pillow format
        pil_image = Image.fromarray(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))

        # Load the custom font
        font_path = 'features/Rubik-Medium.ttf'
        font_size = 47
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(pil_image)

        text = sceen_name
        if x_coordinate == 400:
            x = x_coordinate + 350
        else:
            x = x_coordinate - 400  
        y = background.shape[0] - 540  

        draw.text((x, y), text, font=font, fill=(255, 255, 255))

        # Convert Pillow image back to OpenCV format
        background = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


    cv2.imwrite(combine_file_name, background)

    return combine_file_name

if __name__ == "__main__":
    
    new_image_path = "./features/first.png"


    build_screen(new_image_path, "combined_right_image_mnm.jpg", 1330, "Splash Screen", True)






    