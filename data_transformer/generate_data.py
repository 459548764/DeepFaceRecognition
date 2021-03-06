

from scipy import ndimage, misc
from skimage import io, img_as_uint
import logging
import config
import os

from data_transformer.detect_extract_faces import detect_extract_faces



logging.basicConfig(level=logging.DEBUG, filename="logfile.log", filemode="w",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")

    
    
    
def resize_data(image_in_path, image_out_path):
    # print(imagePath)
    image = ndimage.imread(image_in_path, mode='RGB')
    
    imageResized = misc.imresize(image, (96, 96))
    io.imsave(image_out_path, imageResized)

def extract_resize_faces_for_training(transform_type):
    person_path = [os.path.join(config.path_dict['face_snapshot_path'], file)
                     for file in os.listdir(config.path_dict['face_snapshot_path'])
                     if file != '.DS_Store']
    print (person_path)
    
    for person_path in person_path:
        person_name = os.path.basename(person_path)
        logging.info('Running Detection for %s ..........', str(person_name))
        person_image_paths = [os.path.join(person_path, file)
                              for file in os.listdir(person_path)
                              if file != '.DS_Store']
        print (person_image_paths)
        
        
        if not os.path.exists(
                os.path.join(config.path_dict['face_detection_path'], person_name)):
            os.makedirs(os.path.join(config.path_dict['face_detection_path'], person_name))
            
        if not os.path.exists(
                os.path.join(config.path_dict['face_extracted_path'], person_name)):
            os.makedirs(os.path.join(config.path_dict['face_extracted_path'], person_name))
            
        if not os.path.exists(
                os.path.join(config.path_dict['face_snapshot_resized_path'], person_name)):
            os.makedirs(os.path.join(config.path_dict['face_snapshot_resized_path'], person_name))


        for num, person_image_path in enumerate(person_image_paths):
            if transform_type == 'extract_resize':
                ext_path = os.path.join(config.path_dict['face_extracted_path'],
                                        person_name, '%s.jpg'%str(num))
                det_path = os.path.join(config.path_dict['face_detection_path'],
                                        person_name, '%s.jpg' % str(num))
                # print (ext_path)
                _ = detect_extract_faces(image_path=person_image_path,
                                         face_extracted_path=ext_path,
                                         face_detection_path=det_path,
                                         store=True)
            else:
                rsize_path = os.path.join(config.path_dict['face_snapshot_resized_path'],
                                        person_name, '%s.jpg' % str(num))
                resize_data(image_in_path=person_image_path, image_out_path=rsize_path)


