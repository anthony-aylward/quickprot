import pytest
import shutil
from hashlib import md5
from subprocess import run

@pytest.fixture(scope="module")
def temp_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("temp")


@pytest.fixture()
def quickprot_cmd(
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
        "--debug_info"
    ) + ("-miniprot_PATH", shutil.which("miniprot")) * bool(shutil.which("miniprot"))


def test_quickprot_transdecoder_saccharomyces(
    quickprot_cmd,
    output_file_suffixes,
    output_reference_dir_transdecoder,
    temp_dir
):
    print(quickprot_cmd)
    run(quickprot_cmd, check=True)
    for suffix in output_file_suffixes:
        test_file = f'{temp_dir / "quickprot"}.{suffix}'
        reference_file = f'{output_reference_dir_transdecoder / "quickprot"}.{suffix}'
        print(test_file, reference_file)
        with open(test_file, "rb") as tf, open(reference_file, "rb") as rf:
            if suffix.endswith("gff3"):
                tf.readline()
                rf.readline()
            tf_hash, rf_hash = md5(tf.read()).hexdigest(), md5(rf.read()).hexdigest()
            print(tf_hash, rf_hash, "equal" if tf_hash == rf_hash else "unequal")
            assert tf_hash == rf_hash

