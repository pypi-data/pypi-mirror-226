#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"

from typing import List
from colorama import Fore, Style


def error(msg: str):
    log(":( " + msg, Fore.RED)


def success(msg: str):
    log(":) " + msg, Fore.GREEN)


def warning(msg: str):
    log("!! " + msg, Fore.YELLOW)


def info(msg: str):
    log(":: " + msg, Fore.BLUE)


def log(msg: str, style: str = ""):
    print(style + msg)
    flush()


def ask(
    question: str, options: List[str] = [], answers: List[str] = [], default: str = ""
) -> str:
    flush(Fore.LIGHTCYAN_EX)
    if not options:
        if answers:
            question += f"{answers}"
        if default:
            question += f"[Default:{default}]"
    else:
        answers = [str(x) for x in range(len(options))]
    print(question)
    flush()

    if options:
        for n, op in enumerate(options):
            log(f"    [{n}] {op}", Fore.BLUE)

    prefix = "> "
    if default:
        prefix = f"[Default:{default}]> "
    while True:
        res = input(prefix).strip()
        if not res and default:
            return default
        if answers and res not in answers:
            error(f"Please input one of {answers}")
            continue
        return res


def flush(style: str = Style.RESET_ALL):
    print(style, flush=True)


if __name__ == "__main__":
    log("     静夜思   ", Style.BRIGHT)
    info("床前明月光,")
    warning("疑是地上霜。")
    success("举头望明月,")
    error("低头思故乡。")
    author = ask("以上古诗作者为何人?", ["李白", "杜甫", "王之涣", "孟浩然"])
    if int(author) != 0:
        error("回答错误!")
        warning("正确答案为:李白")
    else:
        success("回答正确!")
    dynasty = ask("请问诗人是哪个朝代的人呢?", answers=["唐", "宋"])
    if dynasty != "唐":
        error("回答错误!")
        warning("正确答案为:唐")
    else:
        success("回答正确!")
