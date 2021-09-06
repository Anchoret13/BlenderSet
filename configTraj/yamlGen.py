import yaml
import os

import argparse

def get_yaml_data(yaml_file):
    file = open(yaml_file, 'r')
    file_data = file.read()
    file.close

    data = yaml.load(file_data)
    return data

def generate_yaml_doc(data, yaml_file):
    file = open(yaml_file, 'w')
    yaml.dump(data, file)
    file.close()





parser = argparse.ArgumentParser(description='number of camera pose')
parser.add_argument('size', type=int, help='dataset size')
parser.add_argument('iteration', type=int, help='iteration')
args = parser.parse_args()



current_path = os.path.abspath("./configTraj")
yaml_path_1 = os.path.join(current_path, 'origin_config.yaml')
new_data = get_yaml_data(yaml_path_1)

new_data['modules'][3]['config']['cam_poses'][0]['location']['start_angle']+=(180/args.size)*args.iteration

name = '%d'%(args.iteration)+'.yaml'
yaml_path_2 = os.path.join(current_path, name)
generate_yaml_doc(new_data, yaml_path_2)