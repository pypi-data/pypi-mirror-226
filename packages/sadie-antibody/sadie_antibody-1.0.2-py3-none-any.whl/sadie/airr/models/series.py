from typing import Any, Dict, Optional

import pandas as pd
from pydantic import BaseModel, root_validator


# TODO: https://docs.airr-community.org/en/stable/news.html
# confirm match 1.4.1 schema
class AirrSeriesModel(BaseModel):
    sequence_id: Optional[str]
    cdr1: Optional[str]
    cdr1_aa: Optional[str]
    cdr1_end: Optional[int]
    cdr1_start: Optional[int]
    cdr2: Optional[str]
    cdr2_aa: Optional[str]
    cdr2_end: Optional[int]
    cdr2_start: Optional[int]
    cdr3: Optional[str]
    cdr3_aa: Optional[str]
    # cdr3_aa_length: Optional[int]
    cdr3_end: Optional[int]
    cdr3_start: Optional[int]
    complete_vdj: Optional[bool]
    d_alignment_end: Optional[int]
    d_alignment_start: Optional[int]
    d_call: Optional[str]
    d_cigar: Optional[str]
    d_family: Optional[str]
    d_germline_alignment: Optional[str]
    d_germline_alignment_aa: Optional[str]
    d_germline_end: Optional[int]
    d_germline_start: Optional[int]
    d_identity: Optional[float]
    d_score: Optional[float]
    d_sequence_alignment: Optional[str]
    d_sequence_alignment_aa: Optional[str]
    d_sequence_end: Optional[int]
    d_sequence_start: Optional[int]
    d_support: Optional[str]
    fwr1: Optional[str]
    fwr1_aa: Optional[str]
    fwr1_end: Optional[int]
    fwr1_start: Optional[int]
    fwr2: Optional[str]
    fwr2_aa: Optional[str]
    fwr2_end: Optional[int]
    fwr2_start: Optional[int]
    fwr3: Optional[str]
    fwr3_aa: Optional[str]
    fwr3_end: Optional[int]
    fwr3_start: Optional[int]
    fwr4: Optional[str]
    fwr4_aa: Optional[str]
    fwr4_end: Optional[int]
    fwr4_start: Optional[int]
    germline_alignment: Optional[str]
    germline_alignment_aa: Optional[str]
    j_alignment_end: Optional[int]
    j_alignment_start: Optional[int]
    j_call: Optional[str]
    j_cigar: Optional[str]
    j_family: Optional[str]
    j_germline_alignment: Optional[str]
    j_germline_alignment_aa: Optional[str]
    j_germline_end: Optional[int]
    j_germline_start: Optional[int]
    j_identity: Optional[float]
    j_score: Optional[float]
    j_sequence_alignment: Optional[str]
    j_sequence_alignment_aa: Optional[str]
    j_sequence_end: Optional[int]
    j_sequence_start: Optional[int]
    j_support: Optional[str]
    junction: Optional[str]
    junction_aa: Optional[str]
    junction_aa_length: Optional[int]
    junction_length: Optional[int]
    locus: Optional[str]
    np1: Optional[str]
    np1_length: Optional[int]
    np2: Optional[str]
    np2_length: Optional[int]
    productive: Optional[bool]
    rev_comp: Optional[bool]
    sequence: Optional[str]
    sequence_alignment: Optional[str]
    sequence_alignment_aa: Optional[str]
    stop_codon: Optional[bool]
    v_alignment_end: Optional[int]
    v_alignment_start: Optional[int]
    v_call: Optional[str]
    v_cigar: Optional[str]
    # v_family: Optional[str]
    v_germline_alignment: Optional[str]
    v_germline_alignment_aa: Optional[str]
    v_germline_end: Optional[int]
    v_germline_start: Optional[int]
    v_identity: Optional[float]
    v_score: Optional[float]
    v_sequence_alignment: Optional[str]
    v_sequence_alignment_aa: Optional[str]
    v_sequence_end: Optional[int]
    v_sequence_start: Optional[int]
    v_support: Optional[str]
    vj_in_frame: Optional[bool]
    # chain: Optional[str]
    species: Optional[str]

    @root_validator(pre=True)
    def fix_dependent_attrs(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Fixes dependent attributes that are not the proper type"""
        cleaned_values = {}
        # Remove all null values
        for k, v in values.items():
            # any null values as string by mistake
            if isinstance(v, str):
                if v.lower() in ["<na>", "na", "nan", "", "none"]:
                    v = None
            # nan to None: we have hybrid types in the data so nan types cannot be leveraged & will break some logic
            # elif isinstance(v, pd._libs.missing.NAType):
            #     v = None
            cleaned_values[k] = v
        return cleaned_values
