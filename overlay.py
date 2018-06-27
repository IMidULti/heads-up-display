from wand.image import Image
from wand.display import display
import ffmpeg



with Image(filename='images/circle.png') as circle_img:
    with circle_img.clone() as bg_img:
        with Image(filename='images/needle.png') as needle_img:
            rotated_needle = None
            with needle_img.clone() as fg_img:
                fg_img.rotate(90)
                #rotated_image = needle_img.make_blob()
                bg_img.composite(fg_img, left=0, top=0)
            #fg_img.close()
        bg_img.save(filename='images/circle_with_needle.png')
#circle_img.close()
    