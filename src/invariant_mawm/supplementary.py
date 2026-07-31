"""Generate supplementary transport tables from one authoritative catalog."""
from __future__ import annotations
import csv
from pathlib import Path

TRANSPORT_CATALOG=(
 {"transport_family":"bounded_affine","formula":"clip(alpha*phi+delta_a,l,u)","parameters":"alpha; action offsets; bounds","fitting_method":"deterministic clipped residual search","supported_feature_types":"numeric","special_cases":"constant; persistence; increment; countdown; reset","worst_case_complexity":"O(N^2*A)","known_failure_modes":"confounding and unidentifiable extrapolated clipping"},
 {"transport_family":"delayed_copy","formula":"psi[t-m]","parameters":"source; m<=4","fitting_method":"exact enumeration","supported_feature_types":"type-compatible","special_cases":"persistence; cross-feature; cross-agent","worst_case_complexity":"O(N*m*F^2)","known_failure_modes":"spurious autocorrelation"},
 {"transport_family":"slot_permutation","formula":"phi_next[sigma(i)]=phi_now[i]","parameters":"permutation","fitting_method":"lexicographic exact assignment","supported_feature_types":"slot-homogeneous","special_cases":"fixed; action-conditioned","worst_case_complexity":"O(n!*n)","known_failure_modes":"duplicate values and factorial scaling"},
)

def generate_transport_catalog(output_dir:str|Path)->tuple[Path,Path]:
    output=Path(output_dir); output.mkdir(parents=True,exist_ok=True)
    fields=tuple(TRANSPORT_CATALOG[0]); csv_path=output/"transport_catalog.csv"
    with csv_path.open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fields,lineterminator="\n"); writer.writeheader(); writer.writerows(TRANSPORT_CATALOG)
    tex_path=output/"transport_catalog.tex"
    def esc(value:str)->str: return value.replace("_","\\_").replace("*","\\ast")
    lines=["\\begin{tabular}{p{0.12\\linewidth}p{0.16\\linewidth}p{0.14\\linewidth}p{0.14\\linewidth}p{0.12\\linewidth}p{0.12\\linewidth}}",
           "Family & Formula & Parameters & Fitting & Types & Complexity \\\\","\\hline"]
    for row in TRANSPORT_CATALOG:
        lines.append(" & ".join(esc(row[k]) for k in ("transport_family","formula","parameters","fitting_method","supported_feature_types","worst_case_complexity"))+" \\\\")
    lines.extend(("\\end{tabular}","")); tex_path.write_text("\n".join(lines))
    return csv_path,tex_path
