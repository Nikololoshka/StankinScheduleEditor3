import json
import os

from tqdm import tqdm

from parser.config import ParserConfig
from parser.parser import Parser
from parser.lint import duration_lint
from parser.transforms import duration_fixer
from utils.walk import walk

if __name__ == '__main__':
    parser = Parser(
        config=ParserConfig(
            text_cleaners=(
                lambda t: t.replace('_Вакансия ', ''),
                lambda t: t.replace('С/З СТАНКИН 1', 'С/З СТАНКИН'),
                lambda t: t.replace('- ', '-'),
                lambda t: t.replace(' - ', '-'),
                lambda t: t.replace('- ', '-'),
                lambda t: t.replace(
                    'Оборудование цифровых производств. Интегрированные роботизированные системы',
                    'Оборудование цифровых производств, Интегрированные роботизированные системы'
                )
            ),
            pair_lints=(duration_lint,),
            pair_transforms=(duration_fixer,)
        )
    )

    folder_path = './Расписания от 09.09.22 v3'

    progress = tqdm(
        iterable=list(walk(folder_path)),
        desc='------',
        bar_format='Extracting: {desc} | Total: {bar:20} {r_bar}',
        unit=' file(-s)'
    )

    for filepath in progress:
        name = os.path.basename(filepath)
        progress.set_description_str(name)
        schedule = parser.parse_schedule(filepath, name)

        json_path = filepath[:-4] + '.json'
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(schedule.pairs, file, ensure_ascii=False, indent=4)
