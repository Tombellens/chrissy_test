import os,shutil, pathlib

#utility functions
def get_first_sub_level_names(name):
    first_sub_level_name = 'snake'
    if 'hoornaar' in name or 'wesp' in name:
        first_sub_level_name = 'wasp'
    else:
        if 'vlieg' in name:
            first_sub_level_name = 'fly'
        else:
            if 'salamander' in name:
                first_sub_level_name = 'salamander'
    return first_sub_level_name

#main script
root_path = 'E://_development/programs/PsychoPy/chrissy_test'
source_images_path = root_path + '/source/'
destination_images_path = root_path + '/img'

image_names = os.listdir(source_images_path)

for image_name in image_names:
    parsed_name = image_name.split('_')
    top_level_name = 'non-threatening'
    if 'hoornaar' in parsed_name[0]  or 'wesp' in parsed_name[0] or 'slang' in parsed_name[0] or 'Slang' in parsed_name[0]:
        top_level_name = 'threatening'
    first_sub_level_name = get_first_sub_level_names(parsed_name[0])
    rank_identifier = parsed_name[0].split(' ')[1]
    spatial_frequency = 'NoFilter' if 'FS' in parsed_name[1] else parsed_name[1]
    normalization = 'no-normalization' if 'unnorm' in parsed_name[2] else 'contrast-normalized'
    dst =  'img/' + top_level_name + '/' + first_sub_level_name + '/' + rank_identifier + '/' + spatial_frequency + '/' + normalization
    if not os.path.isdir(dst):
        pathlib.Path(dst).mkdir(parents= True, exist_ok=True)
    shutil.move('source/' + image_name,  dst)



            

