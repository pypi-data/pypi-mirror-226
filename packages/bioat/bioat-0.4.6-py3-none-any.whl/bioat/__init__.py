"""Doc of bioat.

"""
from __future__ import annotations, absolute_import
from bioat.logger import get_logger  # must be the first
from bioat.about import about
from bioat.bamtools import BamTools
from bioat.bedtools import BedTools
from bioat.exceptions import BioatFileFormatError, BioatFileNameError, BioatParameterFormatError
from bioat.fastxtools import FastxTools
from bioat.hictools import HiCTools
from bioat.mgitools import MgiTools
from bioat.searchtools import SearchTools
from bioat.systemtools import SystemTools
from bioat.tabletools import TableTools
from bioat.target_seq import TargetSeq
from bioat.version import (__version__, __author__, __doc_format__)

__name__ = "bioat"
