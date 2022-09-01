import pathlib
import configparser
import shutil
import enum
from sre_constants import CATEGORY

output = pathlib.Path("./.out")
shutil.rmtree(output, ignore_errors=True)
output.mkdir(exist_ok=True)


@enum.unique
class Category(enum.Enum):
    CD = "CDs"
    HVHS = "Home-VHS"
    RVHS = "Retail-VHS"


counters = {
    Category.CD: 0,
    Category.HVHS: 0,
    Category.RVHS: 0,
}

cfg = configparser.ConfigParser()
cfg.read(".input.ini", encoding="utf-8")

with open(f".out/media.lua", encoding="utf-8", mode="w") as definition:
    with open(f".out/media.txt", encoding="utf-8", mode="w") as text:
        names = cfg.sections()

        definition.write("RecMedia = RecMedia or {}\n\n")

        for name in names:
            media = cfg[name]
            category = Category(media["category"])
            counters[category] += 1
            id = str(counters[category]).zfill(3)

            definition_lines = ""
            text_lines = ""
            line_num = 0
            # Collect definition and text lines.
            for line in media["lines"].split("\n"):
                if not line:
                    continue
                line_num += 1

                definition_lines += f'    {{ text = "RM_UAMEDIA_{category.name}{id}_{line_num}", r = 0.0, g = 0.6, b = 0.4, codes = "BOR-1" }},\n'

                text_line_decor = "[img=music]" if category == Category.CD else ""
                text_lines += f'RM_UAMEDIA_{category.name}{id}_{line_num} = "{text_line_decor}{line}{text_line_decor}"\n'

            # Write definition.
            definition.write(
                f"""
RecMedia["RM_UAMEDIA_{category.name}{id}"] = {{
itemDisplayName = "RM_UAMEDIA_{category.name}{id}_name",
title = "RM_UAMEDIA_{category.name}{id}_title",
subtitle = nil,
author = "RM_UAMEDIA_{category.name}{id}_author",
extra = "RM_UAMEDIA_{category.name}{id}_extra",
spawning = 0,
category = "{category.value}",
lines = {{
{definition_lines}  }},
}};
    """.strip()
                + "\n\n"
            )

            # Write text.
            text.write(
                f"""
RM_UAMEDIA_{category.name}{id}_name = "{media["name"]}"
RM_UAMEDIA_{category.name}{id}_title = "{media["title"]}"
RM_UAMEDIA_{category.name}{id}_author = "{media["author"]}"
RM_UAMEDIA_{category.name}{id}_extra = "{media["extra"]}"
{text_lines}
    """.strip()
                + "\n\n"
            )
