import argparse  
import json

from os import listdir
from os.path import join, basename, dirname

def make_KITTI_format(bbox, object_class):
    '''
    ---------------------------------[15 labels]--------------------------------
    1 type Describes the type of object: 'Car', 'Van', 'Truck',
    'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram',
    'Misc' or 'DontCare'
    1 truncated Float from 0 (non-truncated) to 1 (truncated), where
    truncated refers to the object leaving image boundaries
    1 occluded Integer (0,1,2,3) indicating occlusion state:
    0 = fully visible, 1 = partly occluded
    2 = largely occluded, 3 = unknown
    1 alpha Observation angle of object, ranging [-pi..pi]
    4 bbox 2D bounding box of object in the image (0-based index):
    contains left, top, right, bottom pixel coordinates
    3 dimensions 3D object dimensions: height, width, length (in meters)
    3 location 3D object location x,y,z in camera coordinates (in meters)
    1 rotation_y Rotation ry around Y-axis in camera coordinates [-pi..pi]
    ----------------------------------------------------------------------------
    1 score Only for results: Float, indicating confidence in
    detection, needed for p/r curves, higher is better.
    =>
    Car 0.00 0 -1.58 587.01 173.33 614.12 200.12 1.65 1.67 3.64 -0.65 1.71 46.70 -1.59
    Cyclist 0.00 0 -2.46 665.45 160.00 717.93 217.99 1.72 0.47 1.65 2.45 1.35 22.10 -2.35
    '''
    # uselesee values
    truncated = 0
    occlusion = 3
    alpha = -1
    dimension_3d = [-1, -1, -1]
    location_3d = [-1, -1, -1]
    rotation_y = -1

    # make KITTI format
    bbox_format = f"{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}"
    dimension_3d_format = f"{dimension_3d[0]} {dimension_3d[1]} {dimension_3d[2]}"
    location_3d_format = f"{location_3d[0]} {location_3d[1]} {location_3d[2]}"

    kitti_label = f"{object_class} {truncated} {occlusion} {alpha} {bbox_format} {dimension_3d_format} {location_3d_format} {rotation_y}\n"

    return kitti_label


def load_json(path):
    f = open(path, 'r')
    datas = json.load(f)
    f.close()
    return datas

def main():
    parser = argparse.ArgumentParser(description='convert setting')
    
    # input, output dirrectory setting
    parser.add_argument('-i', '--input_dir', help='input ".json" file directory.', required=True)
    parser.add_argument('-o', '--output_dir', help='output ".txt" file directory.', required=True)
    
    parser.add_argument('-r', '--road_info', help='insert road info at the front of file name. ex) AU, AL ...', default=None)
    parser.add_argument('-f', '--filtering', help='filtering(remove) label whose center y is lower than f_value.', default=None, type=float)
    
    args = parser.parse_args()


    json_dir = args.input_dir
    output_dir = args.output_dir


    json_list = [x for x in listdir(json_dir) if x.endswith('.json')]


    for json_file in json_list:
    
        datas = load_json(join(json_dir, json_file))
   
        label_file_name = datas['asset']['name'].replace('.jpg', '.txt')

        # add road info for road
        if args.road_info is not None:
            label_file_name = f"{args.road_info}_{label_file_name}"

        print(label_file_name)
    
        line = ''

        for data in datas['regions']:

            object_class = data['tags'][0]

            # data['points'][0:4] : left top, right top, right bottom, leftbottom
            bbox = [int(data['points'][0]['x']), int(data['points'][0]['y']), int(data['points'][2]['x']), int(data['points'][2]['y'])]

            if (args.filtering is not None) and ((bbox[1] + bbox[3]) / 2) < args.filtering:
                continue

            line += make_KITTI_format(bbox, object_class)

        f = open(join(output_dir, label_file_name), 'w')
        f.write(line)
        f.close()

def group_json():
    parser = argparse.ArgumentParser(description='convert setting')
    
    # input, output dirrectory setting
    parser.add_argument('-i', '--input_dir', help='input ".json" file directory.', required=True)
    parser.add_argument('-o', '--output_dir', help='output ".txt" file directory.', required=True)
    
    parser.add_argument('-r', '--road_info', help='insert road info at the front of file name. ex) AU, AL ...', default=None)
    parser.add_argument('-f', '--filtering', help='filtering(remove) label whose center y is lower than f_value.', default=None, type=float)
    
    args = parser.parse_args()


    
    folder_list = listdir(args.input_dir)

    output_dir = args.output_dir

    for fd_list in folder_list:

        json_list = [x for x in listdir(join(args.input_dir, fd_list, 'json')) if x.endswith('.json')]

        for json_file in json_list:
        
            datas = load_json(join(args.input_dir, fd_list, 'json', json_file))
    
            label_file_name = datas['asset']['name'].replace('.jpg', '.txt')

            # add road info for road
            if args.road_info is not None:
                label_file_name = f"{args.road_info}_{label_file_name}"

            print(label_file_name)
        
            line = ''

            for data in datas['regions']:

                object_class = data['tags'][0]

                # data['points'][0:4] : left top, right top, right bottom, leftbottom
                bbox = [int(data['points'][0]['x']), int(data['points'][0]['y']), int(data['points'][2]['x']), int(data['points'][2]['y'])]

                if (args.filtering is not None) and ((bbox[1] + bbox[3]) / 2) < args.filtering:
                    continue

                line += make_KITTI_format(bbox, object_class)

            f = open(join(output_dir, label_file_name), 'w')
            f.write(line)
            f.close()


if __name__ == "__main__":
    main()
    # group_json()
