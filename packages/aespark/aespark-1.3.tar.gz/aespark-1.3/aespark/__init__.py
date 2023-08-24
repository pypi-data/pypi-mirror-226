from .__analysis import (
    Palette,
    piv_transview,
)
from .__broken import (
    Broken,
    parse_phoneber,
)
from .__dataclean import (
    dc_dochide,
    dc_write,
    dc_exceladdtt,
    dc_csvdeltt,
    dc_invischardel,
    dc_amount,
    dc_inandout,
    dc_time,
)
from .__document import MyDocument
from .__union import (
    union_sheet,
    union_sheets,
    build_folder,
)
from .__chart import (
    chart_calendar,
    chart_wordcloud,
    chart_sumcount,
)
from .lcode.evolvement import(
    alter_table,
)

import getpass
import pkg_resources

print(f"# ae{getpass.getuser()}: Welcome to the new world. -aespark v{pkg_resources.get_distribution('aespark').version}")

__all__ =[
    'MyDocument',
    'Palette',
    'piv_transview',
    'Broken',
    'parse_phoneber',
    'dc_dochide',
    'dc_write',
    'dc_exceladdtt',
    'dc_csvdeltt',
    'dc_invischardel',
    'dc_amount',
    'dc_inandout',
    'dc_time',
    'union_sheet',
    'union_sheets',
    'build_folder',
    'chart_calendar',
    'chart_wordcloud',
    'chart_sumcount',
    'alter_table',
]