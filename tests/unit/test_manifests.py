import hashlib, json
import pytest
from invariant_mawm.manifests import DatasetManifest, sha256_file

def manifest(**updates):
    values=dict(dataset_id="d",git_commit="abc",generation_command="collect --seed 0",
      environment_versions={"env":"1"},seed=0,policy_id="random",episode_count=2,
      transition_count=3,feature_schema={"x":"float"},action_schema={"n":2},
      split_assignment="Dprop",anonymization_mapping_hash="hash",payload_checksums={"data":"sum"})
    values.update(updates); return DatasetManifest(**values)

def test_manifest_id_write_and_checksum(tmp_path):
    payload=tmp_path/"data"; payload.write_text("transitions")
    checksum=sha256_file(payload)
    first=manifest(payload_checksums={"data":checksum}); second=manifest(payload_checksums={"data":checksum})
    assert first.manifest_id==second.manifest_id
    target=tmp_path/"manifest.json"; first.write(target)
    assert json.loads(target.read_text())["manifest_id"]==first.manifest_id
    assert sha256_file(target)==hashlib.sha256(target.read_bytes()).hexdigest()
    first.verify_payloads({"data":payload})
    payload.write_text("tampered")
    with pytest.raises(ValueError): first.verify_payloads({"data":payload})

def test_manifest_validation():
    with pytest.raises(ValueError): manifest(split_assignment="train").manifest_id
    with pytest.raises(ValueError): manifest(transition_count=-1).manifest_id
