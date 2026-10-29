import re
from pathlib import Path

from sudachipy import tokenizer, dictionary
from wanakana import to_katakana, is_kana
import pysubs2


# Load Sudachi (small dict = fast & decent; use core/full for better accuracy)
dict_obj = dictionary.Dictionary(dict_type="small").create()
mode = tokenizer.Tokenizer.SplitMode.C   # C = longest matching → best for compounds
tok = tokenizer.Tokenizer(dict_obj, mode)


def get_furigana(text: str) -> str:
    """Return text with inline furigana like 漢字[かんじ]"""
    if not any(0x4E00 <= ord(c) <= 0x9FFF for c in text):
        return text  # no kanji → return as-is

    result = []
    for m in tok.tokenize(text):
        surface = m.surface()
        reading = m.reading_form()   # already hiragana

        if is_kana(surface):
            result.append(surface)
        elif reading and reading != surface:
            # Convert reading to hiragana if needed (Sudachi usually gives hiragana)
            reading = reading.lower()
            result.append(f"{surface}[{reading}]")
        else:
            result.append(surface)

    return "".join(result)


def srt_to_furigana_ass(input_srt: str | Path, output_ass: str | Path = None):
    if output_ass is None:
        output_ass = Path(input_srt).with_suffix(".furigana.ass")

    subs = pysubs2.load(str(input_srt), encoding="utf-8")

    for line in subs:
        if not line.text.strip():
            continue

        # Clean up any weird HTML/tags that might be in your subs
        clean = re.sub(r'<.*?>', '', line.text).strip()

        # Add furigana
        with_ruby = get_furigana(clean)

        # Option A: simple bracket style (many players show it nicely)
        line.text = with_ruby

        # Option B: real ASS ruby (better rendering in VLC / mpv)
        # line.text = ruby_ass_style(clean, with_ruby)

    # Optional: set a style that looks good with furigana
    if "Default" in subs.styles:
        style = subs.styles["Default"]
        style.fontsize = 36
        style.outline = 1.5
        style.shadow = 0.8
        style.marginv = 30

    subs.save(str(output_ass))
    print(f"Saved → {output_ass}")


# Optional: more beautiful ruby using ASS tags (positioned above)
# (uncomment & adjust if you want true ruby instead of [reading] style)
"""
def ruby_ass_style(base: str, reading: str) -> str:
    return f" {base} {{\\fscx50\\fscy50\\bord0\\1c&HFFFFFF&\\3c&H000000&}}{reading}{{\\r}}"
    # more advanced versions exist with \\pos tweaking
"""


if __name__ == "__main__":
    # Change this to your file
    srt_file = "Welcome to the N.H.K. - S01E01.subgen.large-v3-turbo.jpn.srt"
    srt_to_furigana_ass(srt_file)