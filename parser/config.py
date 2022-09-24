from .defaults import default_single_date_pattern, default_range_date_pattern, \
    default_pair_pattern, default_time_line

from .transforms import duration_fixer
from .lint import duration_lint

from datetime import datetime


class ParserConfig:

    def __init__(
            self,
            schedule_year: int = datetime.now().year,
            time_line: tuple = default_time_line(),
            pair_pattern: str = default_pair_pattern(),
            date_single_pattern: str = default_single_date_pattern(),
            date_range_pattern: str = default_range_date_pattern(),
            date_format: str = '%Y.%m.%d',
            text_cleaners: tuple = (lambda t: t.replace('_Вакансия', ''),),
            pair_lints: tuple = (duration_lint,),
            pair_transforms: tuple = (duration_fixer,),
    ):
        self.date_range_pattern = date_range_pattern
        self.date_single_pattern = date_single_pattern
        self.schedule_year = schedule_year
        self.pair_pattern = pair_pattern
        self.time_line = time_line
        self.date_format = date_format
        self.text_cleaners = text_cleaners
        self.pair_lints = pair_lints
        self.pair_transforms = pair_transforms
