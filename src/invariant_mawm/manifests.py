"""Immutable, checksummed dataset manifests."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import hashlib, json
from pathlib import Path
from typing import Mapping

@dataclass(frozen=True)
class DatasetManifest:
    dataset_id: str
    git_commit: str
    generation_command: str
    environment_versions: Mapping[str,str]
    seed: int
    policy_id: str
    episode_count: int
    transition_count: int
    feature_schema: Mapping
    action_schema: Mapping
    split_assignment: str
    anonymization_mapping_hash: str
    payload_checksums: Mapping[str,str]

    def validate(self) -> None:
        if self.split_assignment not in {"Dprop","Dfit","Dtest","Dshift"}: raise ValueError("invalid split")
        if self.episode_count < 0 or self.transition_count < 0: raise ValueError("counts must be nonnegative")
        if not self.git_commit or not self.generation_command: raise ValueError("missing reproduction provenance")

    @property
    def manifest_id(self) -> str:
        self.validate()
        return hashlib.sha256(json.dumps(asdict(self),sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

    def write(self,path:str|Path)->None:
        payload=asdict(self) | {"manifest_id":self.manifest_id}
        Path(path).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")

    def verify_payloads(self, paths: Mapping[str,str|Path]) -> None:
        if set(paths) != set(self.payload_checksums):
            raise ValueError("payload names do not match the manifest")
        mismatches=[name for name,path in paths.items()
                    if sha256_file(path) != self.payload_checksums[name]]
        if mismatches: raise ValueError(f"payload checksum mismatch: {sorted(mismatches)}")

def sha256_file(path:str|Path, chunk_size:int=1024*1024)->str:
    digest=hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda:stream.read(chunk_size),b""): digest.update(chunk)
    return digest.hexdigest()
