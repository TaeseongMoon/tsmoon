import os
import collections
from os.path import join, basename, dirname
from glob import glob


class Balanced_Class:

    def __init__(self):
        self.class_dict = {'car':0, 'bus':0, 'hdv':0, 'truck':0, 'motorcycle':0, 'firetruck':0, 'police':0, 'ambulance':0}
        self.day = {}
        self.weather = {'foggy':0, 'rainy':0, 'snowy':0, 'snow':0}
        self.ch = True

    def class_counter(self, txt_file):
        with open(txt_file) as f:
            lines = f.readlines()
            classes = [x.split(' ')[0] for x in lines]
        if self.ch and not self.car_filter(classes): 
            for class_name in classes:
                if class_name not in self.class_dict.keys():
                    print(class_name)
                    raise KeyError
                self.class_dict[class_name] += 1


    def weather_counter(self, img_file):
        weather_name = basename(img_file).split('_')[-1][:-4]
        if weather_name in self.weather.keys():
            self.weather[weather_name] += 1


    def count_class(self):
        annotation_path = '/data/ptits/dataset/01-20/total_annotation'
        anno_files = glob(join(annotation_path,'*.txt'))
        print(len(anno_files))
        for anno_file in anno_files:
            self.class_counter(anno_file)
        print(self.class_dict)


    def car_filter(self, classes):
        return list(set(classes)) == ['car']
        
    def count_weather(self):
        img_path = '/data/ptits/dataset/01-20/total_img'
        image_files = glob(join(img_path,'*.jpg'))
        print(len(image_files))
        for img_file in image_files:
            self.weather_counter(img_file)
        print(self.weather)

    

if __name__ == "__main__":
    a = Balanced_Class()
    a.count_class()
