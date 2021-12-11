import os
import shutil


def read_input(filename='example.txt'):
    with open(filename) as f:
        inputs = f.read().strip().split('\n')
    return inputs


def create_dirs_and_templates():
    for i in range(8, 25):
        d_f_name = str(i).zfill(2)
        os.makedirs(d_f_name, exist_ok=True)
        py_file = os.path.join(d_f_name, d_f_name + '.py')
        ex_file = os.path.join(d_f_name, 'example.txt')
        for s, d in zip(['template.py', 'example.txt'], [py_file, ex_file]):
            if not os.path.isfile(d):
                shutil.copyfile(s, d)


if __name__ == "__main__":
    create_dirs_and_templates()
