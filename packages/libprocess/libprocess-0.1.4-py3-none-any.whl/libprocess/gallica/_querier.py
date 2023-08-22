"""
The entrance to querier class.
"""

import json
import os
from typing import List, Union

from jsonschema import validate
from libquery import Gallica as _Gallica
from libquery.utils.jsonl import load_jl

from ._process_metadata import process_batch
from ._schema import schema_metadata


class Gallica(_Gallica):
    """
    The querier for the `Gallica` data source.
    """

    def validate_metadata(self) -> None:
        metadata = load_jl(self.metadata_path)
        validate(instance=metadata, schema=schema_metadata)

    def process_metadata(
        self,
        save_path: str,
        use_img: bool = False,
        uuids: Union[List[str], None] = None,
    ) -> None:
        """
        Args
        ----
        save_path : str
            The path to save the processing metadata file.
        use_img : bool
            Whether to use image to compute metadata.
        uuids : Union[List[str], None]
            The uuids of entries whose metadata are to be processed.
            If uuids = None, all the entries will be processed.
        """

        output_dir = os.path.dirname(save_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        img_dir = self.img_dir if use_img else None
        processed_metadata = process_batch(self.metadata_path, img_dir, uuids)

        with open(save_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(processed_metadata, indent=4, ensure_ascii=False))
