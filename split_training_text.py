import os
import random
import pathlib
import subprocess
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

training_text_file = 'langdata/vie.training_text'

lines = []

with open(training_text_file, 'r') as input_file:
    for line in input_file.readlines():
        lines.append(line.strip())

output_directory = 'tesstrain/data/vietnamese-ocr-model-ground-truth'

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

random.shuffle(lines)

count = 1000

lines = lines[:count]

line_count = 0
for line in lines:
    training_text_file_name = pathlib.Path(training_text_file).stem
    line_training_text = os.path.join(output_directory, f'{training_text_file_name}_{line_count}.gt.txt')
    with open(line_training_text, 'w') as output_file:
        output_file.writelines([line])

    file_base_name = f'vie_{line_count}'

    subprocess.run([
        'text2image',
        f'--fonts_dir={os.getenv('FONTS_DIR')}', # path to the font directory
        '--font=ARIAL',
        f'--text={line_training_text}',
        f'--outputbase={output_directory}/{file_base_name}',
        '--max_pages=1',
        '--strip_unrenderable_words',
        '--leading=32',
        '--xsize=3600',
        '--ysize=480',
        '--char_spacing=1.0',
        '--exposure=0',
        '--unicharset_file=langdata/vie.unicharset'
    ])

    line_count += 1
