import csv
from invariant_mawm.supplementary import TRANSPORT_CATALOG, generate_transport_catalog

def test_transport_tables_derive_from_same_catalog(tmp_path):
    csv_path,tex_path=generate_transport_catalog(tmp_path)
    rows=list(csv.DictReader(csv_path.open()))
    assert rows==list(TRANSPORT_CATALOG)
    latex=tex_path.read_text()
    assert all(row["fitting_method"].replace("_","\\_") in latex for row in TRANSPORT_CATALOG)
