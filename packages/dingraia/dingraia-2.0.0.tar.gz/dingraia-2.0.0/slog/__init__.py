import ast
import inspect
import datetime
import linecache

from .element import *


color_map = {
        "red"    : "\033[0;31m",
        "green"  : "\033[0;32m",
        "yellow" : "\033[0;33m",
        "blue"   : "\033[0;34m",
        "magenta": "\033[0;35m",
        "cyan"   : "\033[0;36m",
        "grey"   : "\033[0;37m",
        "white"  : "\033[0;38m",
        "RED"    : "\033[0;41m",
        "GREEN"  : "\033[0;42m",
        "YELLOW" : "\033[0;43m",
        "BLUE"   : "\033[0;44m",
        "MAGENTA": "\033[0;45m",
        "CYAN"   : "\033[0;46m",
        "GREY"   : "\033[0;47m",
        "WHITE"  : "\033[0;48m",
        "reset"  : "\033[0m",
    }


def colorer(message: str, level_color: str = '', f_sign: str = "<", e_sign: str = ">", ignore_sign: str = "\\"):
    if level_color and level_color not in color_map:
        raise ValueError("Using level color with invalid color!")
    message = message.replace(f"{ignore_sign}{f_sign}", "<Ignore>")
    for color in color_map:
        message = message.replace(f"{f_sign}/{color}{e_sign}", color_map["reset"] + (color_map[level_color] if level_color else ""))
        message = message.replace(f"{f_sign}{color}{e_sign}", (color_map["reset"] if level_color else "") + color_map[color])
    message = message.replace(f"{f_sign}/{e_sign}", color_map["reset"] + (color_map[level_color] if level_color else ""))
    message = message.replace("<Ignore>", f"{f_sign}")
    if not message.endswith(color_map['reset']):
        message += color_map['reset']
    return message


class logger:
    
    @classmethod
    def info(
            cls,
            *__message,
            module_name: str = "",
            color: str = "",
            colors: bool = False,
            f_sign: str = "<",
            e_sign: str = ">",
            ignore_sign: str = "\\"
    ):
        __message = ''.join([str(x) for x in __message])
        __time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        lies = cls._get_caller(inspect.currentframe())
        if not color:
            if colors:
                __message = colorer(__message, f_sign=f_sign, e_sign=e_sign, ignore_sign=ignore_sign)
            print(f"{__time} I/{f'{lies[1]}:{lies[2]}' if not module_name else module_name}: {__message}")
        else:
            if color in color_map:
                if colors:
                    __message = colorer(__message, level_color=color, f_sign=f_sign, e_sign=e_sign, ignore_sign=ignore_sign)
                print(f"{color_map[color]}{__time} I/{f'{lies[1]}:{lies[2]}' if not module_name else module_name}: {__message}{color_map['reset']}")
                
    @classmethod
    def warning(
            cls,
            *__message,
            module_name: str = "",
            colors: bool = False,
            f_sign: str = "<",
            e_sign: str = ">",
            ignore_sign: str = "\\"
    ):
        __message = ''.join([str(x) for x in __message])
        __time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        lies = cls._get_caller(inspect.currentframe())
        if colors:
            __message = colorer(__message, level_color="yellow", f_sign=f_sign, e_sign=e_sign, ignore_sign=ignore_sign)
        print(Yellow(f"{__time} W/{f'{lies[1]}:{lies[2]}' if not module_name else module_name}: {__message}"))
        
    @classmethod
    def success(
            cls,
            *__message,
            module_name: str = "",
            colors: bool = False,
            f_sign: str = "<",
            e_sign: str = ">",
            ignore_sign: str = "\\"
    ):
        __message = ''.join([str(x) for x in __message])
        __time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        lies = cls._get_caller(inspect.currentframe())
        if colors:
            __message = colorer(__message, level_color="green", f_sign=f_sign, e_sign=e_sign, ignore_sign=ignore_sign)
        print(Green(f"{__time} S/{f'{lies[1]}:{lies[2]}' if not module_name else module_name}: {__message}"))
        
    @classmethod
    def error(
            cls,
            *__message,
            module_name: str = "",
            colors: bool = False,
            f_sign: str = "<",
            e_sign: str = ">",
            ignore_sign: str = "\\"
    ):
        __message = ''.join([str(x) for x in __message])
        __time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        lies = cls._get_caller(inspect.currentframe())
        if colors:
            __message = colorer(__message, level_color="red", f_sign=f_sign, e_sign=e_sign, ignore_sign=ignore_sign)
        print(Red(f"{__time} E/{f'{lies[1]}:{lies[2]}' if not module_name else module_name}: {__message}"))
        
    @classmethod
    def critical(
            cls,
            *__message,
            module_name: str = "",
            colors: bool = False,
            f_sign: str = "<",
            e_sign: str = ">",
            ignore_sign: str = "\\"
    ):
        __message = ''.join([str(x) for x in __message])
        __time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        lies = cls._get_caller(inspect.currentframe())
        if colors:
            __message = colorer(__message, level_color="white RED", f_sign=f_sign, e_sign=e_sign, ignore_sign=ignore_sign)
        print(White(RedBackGround(f"{__time} E/{f'{lies[1]}:{lies[2]}' if not module_name else module_name}: {__message}")))
    
    @classmethod
    def exception(
            cls,
            *__message,
            module_name: str = "",
            colors: bool = False,
            f_sign: str = "<",
            e_sign: str = ">",
            ignore_sign: str = "\\"
    ):
        error_exception = None
        for x in __message:
            if isinstance(x, Exception):
                error_exception = x
                break
        __message = ''.join([str(x) for x in __message if not isinstance(x, Exception)])
        __time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        lies = cls._get_caller(inspect.currentframe())
        if colors:
            __message = colorer(__message, level_color="red", f_sign=f_sign, e_sign=e_sign, ignore_sign=ignore_sign)
        if not __message:
            __message = str(error_exception) if error_exception else ""
        print(Red(f"{__time} E/{f'{lies[1]}:{lies[2]}' if not module_name else module_name}: {__message}"))
        stack = inspect.trace()
        for t in stack:
            filename = t[1]
            line_number = t[2]
            func_name = t[3]
            o_vars = {}
            print(
                f"   \033[31;1mFile \033[0;34m{filename} \033[33mline \033[0;1m{line_number} \033[31min \033[0;1m{func_name}:\033[0m")
            for i in range(max(line_number - 2, 1), min(line_number + 3, len(linecache.getlines(filename)) + 1)):
                line = linecache.getline(filename, i)
                line = line[:-1] if line.endswith('\n') else line
                if line:
                    marker = "--->" if i == line_number else "    "
                    int_len = len(str(min(line_number + 2, len(linecache.getlines(filename)) + 1)))
                    si = str(i)
                    si = ' ' * (int_len - len(si)) + si
                    print(f"   \033[31;1m{marker}\033[32;1m{si}: \033[0m{line}")
                    if i == line_number:
                        frame_locals = t[0].f_locals
                        vars = cls._extract_variables(line.strip())
                        if frame_locals:
                            for var in vars:
                                if str(var) in frame_locals:
                                    o_vars[var] = frame_locals[var]
            if o_vars:
                for v, i in o_vars.items():
                    print(f"   \033[34;1m{v}: {i}\033[0m")
        if error_exception is not None:
            print(f"\033[31;1m{error_exception.__class__.__name__}\033[0;1m: {error_exception}\033[0m")
        else:
            print(f"\033[31;1mNone\033[0;1m: None\033[0m")
            
    @staticmethod
    def _extract_variables(code_str):
        tree = ast.parse(code_str)
        variables = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                variables.add(node.id)
        return variables

    @staticmethod
    def _get_caller(f_back) -> list:
        caller_frame = f_back.f_back
        module_name = caller_frame.f_back.f_globals["__name__"]
        line = caller_frame.f_lineno
        func_name = caller_frame.f_code.co_name
        return [module_name, func_name, line]
    