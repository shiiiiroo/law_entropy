import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from parsers.adilet_parser import AdiletParser
from parsers.egov_parser import EGovParser

if __name__ == "__main__":
    query = "налог"
    print(f"Testing AdiletParser with query: '{query}'")
    adilet = AdiletParser()
    try:
        a_res = adilet.search(query)
        print("Adilet Results:", json.dumps(a_res, ensure_ascii=False, indent=2))
    except Exception as e:
        print("Adilet Exception:", e)

    print("\n-----------------------------------\n")

    print(f"Testing EGovParser with query: '{query}'")
    egov = EGovParser()
    try:
        e_res = egov.search(query)
        print("EGov Results:", json.dumps(e_res, ensure_ascii=False, indent=2))
    except Exception as e:
        print("EGov Exception:", e)
