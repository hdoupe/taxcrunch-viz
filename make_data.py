import pandas as pd
from taxcrunch.multi_cruncher import Batch
import numpy as np
import os


CURRENT_PATH = os.path.abspath(os.path.dirname("file"))


def make_data(year):

    data_dict = {
        "year": [year],
        "mstat": [1, 2],
        "page": [0],
        "sage": [0],
        "depx": [0],
        "dep13": [0],
        "dep17": [0],
        "dep18": [0],
        "pwages": list(range(0, 1020000, 20000)),
        "swages": list(range(0, 1020000, 20000)),
        "dividends": [0],
        "intrec": [0],
        "stcg": [0],
        "ltcg": [0],
        "otherprop": [0],
        "nonprop": [0],
        "pensions": [0],
        "gssi": [0],
        "ui": [0],
        "proptax": [0],
        "otheritem": [0],
        "childcare": [0],
        "mortgage": list(range(0, 120000, 20000)),
        "businc": list(range(0, 1020000, 20000)),
        "sstb": [0, 1],
        "w2paid": [0],
        "qualprop": [0],
    }

    combos = [
        (
            a,
            b,
            c,
            d,
            e,
            f,
            g,
            h,
            i,
            j,
            k,
            l,
            m,
            n,
            o,
            p,
            q,
            r,
            s,
            t,
            u,
            v,
            w,
            x,
            y,
            z,
            aa,
        )
        for a in data_dict["year"]
        for b in data_dict["mstat"]
        for c in data_dict["page"]
        for d in data_dict["sage"]
        for e in data_dict["depx"]
        for f in data_dict["dep13"]
        for g in data_dict["dep17"]
        for h in data_dict["dep18"]
        for i in data_dict["pwages"]
        for j in data_dict["swages"]
        for k in data_dict["dividends"]
        for l in data_dict["intrec"]
        for m in data_dict["stcg"]
        for n in data_dict["ltcg"]
        for o in data_dict["otherprop"]
        for p in data_dict["nonprop"]
        for q in data_dict["pensions"]
        for r in data_dict["gssi"]
        for s in data_dict["ui"]
        for t in data_dict["proptax"]
        for u in data_dict["otheritem"]
        for v in data_dict["childcare"]
        for w in data_dict["mortgage"]
        for x in data_dict["businc"]
        for y in data_dict["sstb"]
        for z in data_dict["w2paid"]
        for aa in data_dict["qualprop"]
    ]

    df_combos = pd.DataFrame(combos)

    df_combos.iloc[:, 5] = df_combos.iloc[:, 4]
    df_combos.iloc[:, 6] = df_combos.iloc[:, 4]
    df_combos.iloc[:, 7] = df_combos.iloc[:, 4]
    df_combos.insert(0, "RECID", df_combos.index + 1)

    df_combos.columns = range(df_combos.shape[1])
    df_combos2 = df_combos[
        np.logical_not(np.logical_and(df_combos[2] == 1, df_combos[10] != 0))
    ]
    df_combos3 = df_combos2[
        np.logical_not(np.logical_and(df_combos2[24] == 0, df_combos2[25] == 1))
    ]

    cols = [
        "ID",
        "year",
        "mstat",
        "page",
        "sage",
        "depx",
        "dep13",
        "dep17",
        "dep18",
        "pwages",
        "swages",
        "dividends",
        "intrec",
        "stcg",
        "ltcg",
        "otherprop",
        "nonprop",
        "pensions",
        "gssi",
        "ui",
        "proptax",
        "otheritem",
        "childcare",
        "mortgage",
        "businc",
        "sstb",
        "w2paid",
        "qualprop",
    ]
    df_named = df_combos3.copy()
    df_named.columns = cols

    b = Batch(df_combos3)
    baseline = b.create_table()
    biden = b.create_table(reform_file=os.path.join(CURRENT_PATH, "biden.json"))

    baseline_merged = baseline.merge(df_named, on="ID")
    keep = [
        "ID",
        "Individual Income Tax",
        "Payroll Tax",
        "pwages",
        "swages",
        "mstat",
        "mortgage",
        "businc",
        "sstb",
        "year",
    ]
    df_baseline_temp = baseline_merged[keep]
    df_baseline = df_baseline_temp.rename(
        columns={"Individual Income Tax": "itax_base", "Payroll Tax": "payroll_base"}
    )
    df_baseline["combined_base"] = (
        df_baseline["itax_base"] + df_baseline["payroll_base"]
    )
    df_baseline.drop(columns=["itax_base", "payroll_base"], inplace=True)

    biden["combined_biden"] = biden["Individual Income Tax"] + biden["Payroll Tax"]
    df = df_baseline.merge(biden[["ID", "combined_biden"]], on="ID")
    df.drop(columns=["ID"], inplace=True)

    return df


def stack_data():
    df = pd.DataFrame()
    for year in range(2021, 2027):
        df_year = make_data(year)
        df = pd.concat([df, df_year])
    return df


if __name__ == "__main__":
    df_all = stack_data()
    df_all.to_parquet('widget_data.gzip', compression='gzip')
