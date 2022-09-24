
def default_pair_pattern() -> str:
    pattern_title = r'([а-яА-ЯёЁa-zA-Z0-9\s\,\-\(\)\/\:]+?\.)'  # 0
    pattern_lecturer = r'([а-яА-ЯёЁae\s\_]+\s([а-яА-я]\.?){1,2})?'  # 1
    pattern_type = r'((лабораторные занятия|семинар|лекции)?\.)'  # 3
    pattern_subgroup = r'(\([абАБ]\)\.)?'  # 5
    pattern_classroom = r'([^\[\]]+?\.)'  # 6
    pattern_date = r'(\[((\,)|(\s?(\d{2}\.\d{2})\-(\d{2}\.\d{2})\s*?([чкЧК]\.[нН]\.{1,2})|(\s?(\d{2}\.\d{2}))))+\])'  # 7

    return r'\s?'.join(
        [
            pattern_title,
            pattern_lecturer,
            pattern_type,
            pattern_subgroup,
            pattern_classroom,
            pattern_date
        ]
    )


def default_range_date_pattern() -> str:
    return r'\s?(\d{2}\.\d{2})-(\d{2}\.\d{2})\s*?([чк]\.[н]\.)'


def default_single_date_pattern() -> str:
    return r'\s?(\d{2}\.\d{2})'


def default_time_line() -> tuple:
    return (
        ('8:30', '10:10'),
        ('10:20', '12:00'),
        ('12:20', '14:00'),
        ('14:10', '15:50'),
        ('16:00', '17:40'),
        ('18:00', '19:30'),
        ('19:40', '21:10'),
        ('21:20', '22:50'),
    )
