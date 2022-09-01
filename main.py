import pathlib
import configparser
import shutil
import enum
from sre_constants import CATEGORY

output = pathlib.Path("./.out")
shutil.rmtree(output)
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

names = cfg.sections()
for name in names:
    media = cfg[name]
    category = Category(media["category"])
    counters[category] += 1
    id = str(counters[category]).zfill(3)

    definition_lines = ""
    text_lines = ""
    line_num = 0
    for line in media["lines"].split("\n"):
        if not line:
            continue
        line_num += 1

        definition_lines += f'    {{ text = "RM_UAMEDIA_{category.name}{id}_{line_num}", r = 0.0, g = 0.6, b = 0.4, codes = "BOR-1" }},\n'

        text_line_decor = "[img=music]" if category == Category.CD else ""
        text_lines += f'RM_UAMEDIA_{category.name}{id}_{line_num} = "{text_line_decor}{line}{text_line_decor}"\n'

    with open(f".out/{name}_definition.txt", encoding="utf-8", mode="w") as f:
        f.write(
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
        )

    with open(f".out/{name}_text.txt", encoding="cp1251", mode="w") as f:
        f.write(
            f"""
RM_UAMEDIA_{category.name}{id}_name = "{media["name"]}"
RM_UAMEDIA_{category.name}{id}_title = "{media["title"]}"
RM_UAMEDIA_{category.name}{id}_author = "{media["author"]}"
RM_UAMEDIA_{category.name}{id}_extra = "{media["extra"]}"

{text_lines}
  """.strip()
        )
