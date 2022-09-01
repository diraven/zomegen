import pathlib
import configparser
import shutil

output = pathlib.Path("./.out")
shutil.rmtree(output)
output.mkdir(exist_ok=True)

cfg = configparser.ConfigParser()
cfg.read(".input.ini", encoding="utf-8")

names = cfg.sections()
for name in names:
    media = cfg[name]
    definition_lines = ""
    text_lines = ""
    line_num = 0
    for line in media["lines"].split("\n"):
        if not line:
            continue
        line_num += 1
        definition_lines += f'    {{ text = "RM_UAMEDIA_vhs{media["id"]}_{line_num}", r = 0.0, g = 0.6, b = 0.4, codes = "BOR-1" }},\n'
        text_lines += f'RM_UAMEDIA_vhs{media["id"]}_{line_num} = "{line}"\n'

    with open(f".out/{name}_definition.txt", encoding="utf-8", mode="w") as f:
        f.write(
            f"""
  RecMedia["RM_UAMEDIA_vhs{media["id"]}"] = {{
  itemDisplayName = "RM_UAMEDIA_vhs{media["id"]}_name",
  title = "RM_UAMEDIA_vhs{media["id"]}_title",
  subtitle = nil,
  author = "RM_UAMEDIA_vhs{media["id"]}_author",
  extra = "RM_UAMEDIA_vhs{media["id"]}_extra",
  spawning = 0,
  category = "Retail-VHS",
  lines = {{
{definition_lines}  }},
}};
  """.strip()
        )

    with open(f".out/{name}_text.txt", encoding="cp1251", mode="w") as f:
        f.write(
            f"""
RM_UAMEDIA_vhs001_name = "{media["name"]}"
RM_UAMEDIA_vhs001_title = "{media["title"]}"
RM_UAMEDIA_vhs001_author = "{media["author"]}"
RM_UAMEDIA_vhs001_extra = "{media["extra"]}"

{text_lines}
  """.strip()
        )
