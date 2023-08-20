from typing import cast, Optional
from sqlite3 import Connection
from pathlib import Path
from .better_json_tools import load_jsonc
from .utils import parse_format_version
from ._views import dbtableview
import json

@dbtableview(
    properties={
        "path": (Path, "NOT NULL")
    },
    connects_to=["ResourcePack"]
)
class BpBlockFile: ...

@dbtableview(
    properties={
        "identifier": (str, "NOT NULL"),
        "icon": (str, "")
    },
    connects_to=["BpBlockFile"]
)
class BpBlock: ...

@dbtableview(
    properties={
        "identifier": (str, "NOT NULL"),
        "jsonPath": (str, "NOT NULL"),
    },
    connects_to=["BpBlock"],
    weak_connects_to=[
        ("identifier", "LootTable", "identifier")
    ]
)
class BpBlockLootField: ...

@dbtableview(
    properties={
        "identifier": (str, "NOT NULL"),
        "jsonPath": (str, "NOT NULL"),
    },
    connects_to=["BpBlock"],
    weak_connects_to=[
        ("identifier", "Geometry", "identifier")
    ]
)
class BpBlockGeometryField: ...

@dbtableview(
    properties={
        "jsonPath": (str, "NOT NULL"),
    },
    connects_to=["BpBlock"]
)
class BpBlockMaterialInstancesField: ...

@dbtableview(
    properties={
        "identifier": (str, "NOT NULL"),
        "jsonPath": (str, "NOT NULL"),
        "texture": (str, "NOT NULL"),
        "renderMethod": (str, "NOT NULL"),
    },
    connects_to=["BpBlockMaterialInstancesField"],
    # TODO - weak connect texture to the short name of the terrain_texture field
)
class BpBlockMaterialInstancesFieldInstance: ...

BP_BLOCK_BUILD_SCRIPT = (
    BpBlockFile.build_script +
    BpBlock.build_script
)


def load_bp_blocks(db: Connection, bp_id: int):
    bp_path: Path = db.execute(
        "SELECT path FROM BehaviorPack WHERE BehaviorPack_pk = ?",
        (bp_id,)
    ).fetchone()[0]

    for bp_block_path in (bp_path / "blocks").rglob("*.json"):
        load_bp_block(db, bp_block_path, bp_id)

def load_bp_block(db: Connection, bp_block_path: Path, bp_id: int):
    cursor = db.cursor()
    # BP BLOCK FILE
    cursor.execute(
        "INSERT INTO BpBlockFile (path, BehaviorPack_fk) VALUES (?, ?)",
        (bp_block_path.as_posix(), bp_id)
    )
    # TODO
    raise NotImplementedError("TODO")