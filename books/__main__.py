from ast import parse
import pathlib
import configparser
import shutil
import enum
from sre_constants import CATEGORY

output = pathlib.Path("./.out")
shutil.rmtree(output, ignore_errors=True)
output.mkdir(exist_ok=True)


book_counter = 0

cfg = configparser.ConfigParser()
cfg.read(".input.ini", encoding="utf-8")

with open(f".out/books.lua", encoding="utf-8", mode="w") as definition:
    with open(f".out/books.txt", encoding="utf-8", mode="w") as text:
        definition.write(
            """
--
-- Please, do not delete this comment.
-- This file is generated with ZoMeGen by DiRaven
-- https://github.com/diraven/zomegen
--
        """.strip()
            + "\n\n"
        )

        titles = cfg["books"]["titles"]
        print(titles)

        for title in titles.strip().splitlines():
            book_counter += 1
            definition.write(
                f"""
-- {title}
item book_ukrlit_{book_counter}
{{
  DisplayCategory = Literature,
  DisplayName = book_ukrlit_{book_counter},
  Type = Literature,
  Icon = Book,
  Weight = 0.5,
  UnhappyChange = -40,
  StressChange = -40,
  BoredomChange = -50,
  FatigueChange = +5,
  StaticModel = Book,
  WorldStaticModel = BookClosedGround,
}}
    """.strip()
                + "\n\n"
            )

            # Write text.
            text.write(
                f"""
DisplayName_book_ukrlit_{book_counter} = "{title}",
    """.strip()
                + "\n"
            )
