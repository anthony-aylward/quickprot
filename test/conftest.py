import pytest
from pathlib import Path

def pytest_addoption(parser):
    parser.addoption(
        "--TD2", action="store_true", default=False, help="Include TD2 in the test run"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "td2: mark test as using TD2")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--TD2"):
        # --TD2 given in cli: do not skip TD2 tests
        return
    skip_td2 = pytest.mark.skip(reason="need --TD2 option to run")
    for item in items:
        if "td2" in item.keywords:
            item.add_marker(skip_td2)


@pytest.fixture
def quickprot():
    return Path(__file__).parent.parent / "quickprot.py"


@pytest.fixture
def saccharomyces_proteins():
    return Path(__file__).parent / "data" / "uniprotkb_reviewed_true_AND_taxonomy_id_4930_Saccharomyces.fasta.gz"


@pytest.fixture
def saccharomyces_cerevisiae_chr1():
    return Path(__file__).parent / "data" / "Saccharomyces_cerevisiae.R64-1-1.dna_sm.chromosome.I.fa.gz"


@pytest.fixture
def output_file_suffixes():
    return (
        "cds.fasta",
        "gff3",
        "longest.cds.fasta",
        "longest.gff3",
        "longest.pep.fasta",
        "pep.fasta",
        "transcript.gtf",
        "uniprotkb_reviewed_true_AND_taxonomy_id_4930_Saccharomyces.fasta.miniprot_output.outs_0.95.gff3"
    )


@pytest.fixture
def output_reference_dir_transdecoder():
    return Path(__file__).parent / "data" / "output_transdecoder"


@pytest.fixture
def output_reference_dir_td2():
    return Path(__file__).parent / "data" / "output_td2"
