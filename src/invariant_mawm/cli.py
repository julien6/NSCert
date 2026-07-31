import argparse, json
from .certification import effective_budget, zero_violation_bound
def main():
    p=argparse.ArgumentParser(); p.add_argument("--support",type=int,required=True); p.add_argument("--candidates",type=int,default=1)
    a=p.parse_args(); b=effective_budget(a.candidates)
    print(json.dumps({"effective_budget":b,"upper_bound":zero_violation_bound(a.support,budget=b)}))

if __name__ == "__main__":
    main()
