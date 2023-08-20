"""
__init__
~~~~~~~~

A Python module for creating names using other names as building blocks.
"""
from mkname.db import (
    get_names,
    get_names_by_kind,
    get_cultures,
    get_kinds
)
from mkname.init import get_config, get_db
from mkname.mkname import (
    build_compound_name,
    build_from_syllables,
    select_name
)
from mkname.mod import (
    add_letters,
    add_punctuation,
    compound_names,
    double_letter,
    double_vowel,
    garble,
    make_scifi,
    mods,
    translate_characters,
    vulcanize,
)
