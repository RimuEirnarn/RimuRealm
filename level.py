from cmd import Cmd
from shlex import split
from re import compile as re_compile, escape as re_escape
from string import punctuation, whitespace
from typing import Any

import matplotlib.pyplot as plt
import matplotlib as mpl

PLOT_ARGS = {
    'layout': 'constrained'
}

inf = float('inf')
nan = float('nan')
Base_EXP = 42
Base_Rank_EXP = 190

Linear_Scaling_Factor = 542
Exponential_Scaling_Factor = 1.59
INT_Scaling_Factor = 70

re_check_name = re_compile(f"[{re_escape(punctuation.replace('_', '')+whitespace)}]+")

class Percentage:
    def __init__(self, p: int | float):
        self._p = max(min(100, p), 0)

    def __radd__(self, o: 'int | float | Percentage'):
        if isinstance(o, Percentage):
            return Percentage((o.value + (self.value/100) * o.value))
        return o + (self.value/100) * o

    def __add__(self, o: 'int | float | Percentage'):
        if isinstance(o, Percentage):
            return Percentage((self.value + (o.value/100) * self.value))
        return o + (self.value/100) * o

    def __rsub__(self, o: 'int | float | Percentage'):
        if isinstance(o, Percentage):
            return Percentage((o.value - (self.value/100) * o.value))
        return o - (self.value/100) * o

    def __sub__(self, o: 'int | float | Percentage'):
        if isinstance(o, Percentage):
            return Percentage((self.value - (o.value/100) * self.value))
        return o - (self.value/100) * o

    def __round__(self):
        return Percentage(round(self._p))

    @property
    def value(self):
        return self._p

    def __repr__(self) -> str:
        return f"{self._p}%"


def INT_scaling(int_value):
    if int_value > 100:
        int_value = 100
    if int_value < 0:
        int_value = 0
    return Percentage(int_value * INT_Scaling_Factor / 100)

def calculate_level(level, int_value):
    if level >= 10000:
        return inf
    if level >= 1:
        #print(f"{Base_EXP} + ({level} - 1) * {Linear_Scaling_Factor} - {INT_scaling(int_value)}")
        return round(Base_EXP + (level - 1) * Linear_Scaling_Factor - INT_scaling(int_value))
    if level < 0:
        return nan
    #print(f"{Base_EXP} - {INT_scaling(int_value)}")
    return round(Base_EXP - INT_scaling(int_value))

def calculate_rank_level(level, int_value):
    if level >= 5.0:
        return inf
    if level > 0.1:
        #print(f"{Base_Rank_EXP} * {Exponential_Scaling_Factor} ^ (({level} - 0.1) * 10) - {INT_scaling(int_value)}")
        return round(Base_Rank_EXP * Exponential_Scaling_Factor ** ((level - 0.1) * 10) - INT_scaling(int_value))
    if level < 0:
        return nan
    #print(f"{Base_Rank_EXP} - {INT_scaling(int_value)}")
    return round(Base_Rank_EXP - INT_scaling(int_value))

def plot_all(int_value):
    print(f"Calculating level by INT {int_value}")
    rlv = range(1, 10000)
    rrv = [a/10 for a in range(1, 50)]
    lv = [calculate_level(i, int_value) for i in rlv]
    rv = [calculate_rank_level(i, int_value) for i in rrv]
    _, (ax_level, ax_rank) = plt.subplots(1, 2, **PLOT_ARGS) # type: ignore
    ax_level.plot(tuple(rlv), lv, label="Level")
    ax_level.set_xlabel("Level")
    ax_level.set_ylabel("Max EXP")
    ax_level.set_title("Level (0-10000)")
    ax_level.legend()

    ax_rank.plot(tuple(rrv), rv, label="Rank Level")
    ax_rank.set_xlabel("Rank Level")
    ax_rank.set_ylabel("Max Rank EXP")
    ax_rank.set_title("Rank Level (0-10000)")
    ax_rank.legend()

    plt.show()


def plot_level(int_value):
    print(f"Calculating level by INT {int_value}")
    rlv = range(1, 10000)
    lv = [calculate_level(i, int_value) for i in rlv]
    _, ax_level = plt.subplots()
    ax_level.plot(tuple(rlv), lv, label="Level")
    ax_level.set_xlabel("Level")
    ax_level.set_ylabel("Max EXP")
    ax_level.set_title("Level (0-10000)")
    ax_level.legend()

    plt.show()

def plot_rank_level(int_value):
    print(f"Calculating rank level by INT {int_value}")
    rrv = [a/10 for a in range(1, 50)]
    rv = [calculate_rank_level(i, int_value) for i in rrv]
    _, ax_rank = plt.subplots(**PLOT_ARGS) # type: ignore
    
    ax_rank.plot(tuple(rrv), rv, label="Rank Level")
    ax_rank.set_xlabel("Rank Level")
    ax_rank.set_ylabel("Max Rank EXP")
    ax_rank.set_title("Rank Level (0-10000)")
    ax_rank.legend()

    plt.show()


class CLI(Cmd):
    intro = "Level benchmark"
    prompt = "> "
    vars_: dict[str, Any] = {
        'int': 62
    }
    
    def do_set(self, arg):
        """Set a variable"""
        if arg == '':
            for k,v in self.vars_.items():
                print(f"set {k}={v!r}")
            return
        if not '=' in arg:
            print(f"ERR: {arg} is not a valid syntax")
            return
        var, value_ = arg.split("=", 1)
        if re_check_name.search(var):
            print(f"ERR: {arg} is not a valid syntax")
            return
        value = split(value_)[0]
        try:
            self.vars_[var] = int(value)
            return
        except ValueError:
            pass

        try:
            self.vars_[var] = float(value)
            return
        except ValueError:
            pass

        self.vars_[var] = value

    def do_calc(self, arg):
        """Do calculation"""
        int_value = int(self.vars_.get('int', 62))
        print(f"Max EXP is reduced by {INT_scaling(int_value)}")
        if arg == '':
            plot_all(int_value)
        elif arg == 'lv':
            plot_level(int_value)
        elif arg == 'rv':
            plot_rank_level(int_value)
        else:
            print(f"ERR: Unknown option {arg!r}")

    def do_exit(self, _):
        """Exit"""
        print()
        return True

    do_EOF = do_exit

if __name__ == "__main__":
    CLI().cmdloop()
