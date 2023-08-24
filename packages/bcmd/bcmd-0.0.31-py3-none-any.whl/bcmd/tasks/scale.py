from typing import Final

import typer
from beni import bcolor, bfunc, btask
from beni.bfunc import toFloat
from prettytable import PrettyTable

app: Final = btask.app


@app.command()
@bfunc.syncCall
async def scale(
    a: float = typer.Argument(..., help='原始数值'),
    b: float = typer.Argument(..., help='原始数值'),
    c: str = typer.Argument(..., help='数值 或 ?'),
    d: str = typer.Argument(..., help='数值 或 ?'),
):
    '按比例计算数值，例子：beni scale 1 2 3 ?'
    if not ((c == '?') != (d == '?')):
        return bcolor.printRed('参数C和参数D必须有且仅有一个为?')
    print()
    if c == '?':
        dd = toFloat(d)
        cc = a * dd / b
        table = PrettyTable()
        table.field_names = [bcolor.yellow('原始'), bcolor.yellow('计算')]
        table.add_row([a, bcolor.magenta(str(cc))])
        table.add_row([b, dd])
        print(table.get_string())
    if d == '?':
        cc = toFloat(c)
        dd = b * cc / a
        table = PrettyTable()
        table.field_names = [bcolor.yellow('原始'), bcolor.yellow('计算')]
        table.add_row([a, cc])
        table.add_row([b, bcolor.magenta(str(dd))])
        print(table.get_string())
    print()
