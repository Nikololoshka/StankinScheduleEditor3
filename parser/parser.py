from datetime import datetime

from utils.walk import walk
from .config import ParserConfig
from .result import ParserResult

import fitz

import os
import re


class Parser:

    def __init__(self, config: ParserConfig = ParserConfig()):
        self._config = config

    def parse_schedule(self, schedule_path: str, schedule_name: str = None) -> ParserResult:
        if schedule_name is None:
            schedule_name = os.path.basename(schedule_path)

        doc = fitz.Document(filename=schedule_path)
        page = doc.load_page(0)

        text_blocks = page.get_text('blocks')
        time_blocks = self._detect_time_blocks(text_blocks)

        pairs = []
        for block in text_blocks:
            block_pairs = self._extract_block(block, time_blocks)
            if block_pairs is not None:
                for block_pair in block_pairs:
                    block_pair = self._pair_transform(block_pair)
                    self._pair_lint(schedule_name, block_pair)
                    pairs.append(block_pair)

        return ParserResult(
            path=schedule_path,
            name=schedule_name,
            pairs=pairs
        )

    def parse_schedules(self, folder_path: str):
        for filepath in walk(folder_path):
            name = os.path.basename(filepath)
            yield self.parse_schedule(filepath, name)

    def _extract_block(self, block, time_blocks):
        x0, y0, x1, y1, text, block_type, block_no = block
        text = text.replace('\n', ' ')

        pairs = []
        text_pairs = re.findall(r'.*?]', text)

        if text_pairs:
            # Время для блока
            time_pair = self._detect_block_time(x0, x1, time_blocks)
            for text_pair in text_pairs:
                # Текст для парсинга
                text_pair = self._append_cleaners(text_pair).strip()

                match = re.fullmatch(self._config.pair_pattern, text_pair)
                try:
                    if match is None:
                        print(f'Match is None. {text_pair}.')
                        continue

                    pair = self._extract_pair(match, time_pair)
                    pairs.append(pair)

                except Exception as e:
                    print(e)

        return pairs

    def _extract_pair(self, match, block_time):
        return {
            'title': match.group(1)[0:-1].strip(),
            'lecturer': self._extract_pair_lecturer(match.group(2)),
            'type': self._extract_pair_type(match.group(4)),
            'subgroup': self._extract_pair_subgroup(match.group(6)),
            'classroom': self._extract_pair_classroom(match.group(7)),
            'time': {
                'start': block_time[0],
                'end': block_time[1]
            },
            'dates': self._extract_pair_dates(match.group(8))
        }

    def _extract_pair_dates(self, dates_str):
        dates = []

        text_dates = dates_str.replace('[', '').replace(']', '').strip().lower().split(',')
        for text_date in text_dates:

            match = re.match(self._config.date_range_pattern, text_date)
            if match is not None:
                freq = match.group(3)

                if freq == 'к.н.':
                    freq = 'every'
                elif freq == 'ч.н.':
                    freq = 'throughout'
                else:
                    raise Exception(f'Неизвестная периодичность даты {freq}')

                # new method '/'
                dates.append({
                    'frequency': freq,
                    'date': self._convert_date(match.group(1)) + '-' + self._convert_date(match.group(2)),
                })
                continue

            match = re.match(self._config.date_single_pattern, text_date)
            if match is not None:
                dates.append({
                    'frequency': 'once',
                    'date': self._convert_date(match.group(1))
                })

        return dates

    def _convert_date(self, old_date):
        return datetime.strptime(old_date, '%d.%m').replace(self._config.schedule_year).strftime('%Y.%m.%d')
        # .strftime('%Y-%m-%d') new method

    @staticmethod
    def _extract_pair_lecturer(lecturer_str):
        if lecturer_str is None:
            return ''

        return lecturer_str[0:-1].strip()

    @staticmethod
    def _extract_pair_classroom(classroom_str):
        if classroom_str is None:
            return ''

        return classroom_str[0:-1].strip()

    @staticmethod
    def _extract_pair_type(type_str):
        type_str = type_str[0:-1].strip().lower()

        if 'семинар' in type_str:
            return 'Seminar'
        elif 'лекции' in type_str:
            return 'Lecture'
        elif 'лабораторные занятия' in type_str:
            return 'Laboratory'

        raise Exception(f'Не удалось найти тип пары "{type_str}"')

    @staticmethod
    def _extract_pair_subgroup(subgroup_str):
        if subgroup_str is None:
            return 'Common'
        elif subgroup_str[0:-1].upper() == '(А)':
            return 'A'
        elif subgroup_str[0:-1].upper() == '(Б)':
            return 'B'

        raise Exception(f'Не удалось найти подгруппу пары "{subgroup_str}"')

    def _detect_time_blocks(self, text_blocks) -> list:
        for block in text_blocks:
            x0, y0, x1, y1, text, block_type, block_no = block
            if '8:30' in text:
                x0, x1 = 46, 794
                delta = (x1 - x0) / 8
                times_grid = [(v, x0 + i * delta, x0 + (i + 1) * delta) for i, v in enumerate(self._config.time_line)]
                return times_grid

        raise Exception('Не удалось найти время пары')

    def _append_cleaners(self, text_pair: str) -> str:
        now = text_pair
        for cleaner in self._config.text_cleaners:
            now = cleaner(now)

        return now

    def _pair_lint(self, schedule_name, pair):
        for lint in self._config.pair_lints:
            lint(schedule_name, pair)

    def _pair_transform(self, pair):
        for transform in self._config.pair_transforms:
            pair = transform(pair)

        return pair

    @staticmethod
    def _detect_block_time(start_block: int, end_block: int, time_blocks: list):
        start_delta = 100_000
        start_time = ''

        end_delta = 100_000
        end_time = ''

        for (start_text, end_text), start, end in time_blocks:
            if abs(start_block - start) < start_delta:
                start_delta = abs(start_block - start)
                start_time = start_text

            if abs(end_block - end) < end_delta and end_block - end < 10:
                end_delta = abs(end_block - end)
                end_time = end_text

        return start_time, end_time
