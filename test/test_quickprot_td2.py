import pytest
import shutil
from Bio import SeqIO
from hashlib import md5
from subprocess import run

@pytest.fixture(scope="module")
def temp_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("temp")


@pytest.fixture()
def quickprot_cmd_td2(
    quickprot,
    saccharomyces_proteins,
    saccharomyces_cerevisiae_chr1,
    temp_dir
):
    return (
        quickprot,
        "--query", saccharomyces_proteins,
        "--genome", saccharomyces_cerevisiae_chr1,
        "--prefix", temp_dir / "quickprot",
        "--debug_info",
        "-ORFSoftware", "TD2"
    ) + ("-miniprot_PATH", shutil.which("miniprot")) * bool(shutil.which("miniprot"))



@pytest.mark.td2
def test_quickprot_td2_saccharomyces(
    quickprot_cmd_td2,
    output_file_suffixes_transcript,
    output_file_suffixes_protein,
    output_reference_dir_td2,
    temp_dir
):
    print(quickprot_cmd_td2)
    run(quickprot_cmd_td2, check=True)
    for suffix in output_file_suffixes_transcript:
        test_file = temp_dir / f'{"quickprot"}.{suffix}'
        reference_file = output_reference_dir_td2 / f'{"quickprot"}.{suffix}'
        print(test_file, reference_file)
        with open(test_file, "rb") as tf, open(reference_file, "rb") as rf:
            tf_hash, rf_hash = md5(tf.read()).hexdigest(), md5(rf.read()).hexdigest()
            print(tf_hash, rf_hash, "equal" if tf_hash == rf_hash else "unequal")
            assert tf_hash == rf_hash
    for suffix in output_file_suffixes_protein:
        output_file = temp_dir / f'{"quickprot"}.{suffix}'
        print(output_file)
        assert output_file.is_file() and output_file.stat().st_size > 0
        if "fasta" in suffix:
            try:
                *_,  last_record = SeqIO.parse(output_file, "fasta")
                print(last_record)
            except ValueError:
                assert False
        elif "gff3" in suffix:
            with open(output_file, "rt") as handle:
                for line in handle:
                    if line.strip() and not line.startswith("#"):
                        _, _, feature, start, end, _, strand, phase, _ = line.split("\t")
                        assert all(
                            (
                                feature in ("gene", "mRNA", "exon", "CDS"),
                                int(start) >= 0,
                                int(end) >= 0,
                                strand in ("+", "-", ".", "?"),
                                phase in ("0", "1", "2", ".")
                            )
                        )
