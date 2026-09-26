"""Fit per-sport height and BMI ranges from Olympic athlete data.

Input:  data/raw/athlete_events.csv  ("120 years of Olympic history",
        github.com/rgriff23/Olympic_history; not committed)
Output: data/olympic_fit.json        (aggregate statistics only)

Each athlete is counted once per app sport (their most recent Games in the
window), so relay squads and multi-event athletes don't dominate.
Medians and robust spreads (IQR / 1.349) resist outliers and data-entry errors.
"""
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data/raw/athlete_events.csv"
OUT = ROOT / "data/olympic_fit.json"

YEAR_MIN = 1992  # modern era: professional athletes, consistent measurement
MIN_N = 40       # below this, keep the literature-based targets


def athletics(*events):
    return lambda r: r["Sport"] == "Athletics" and any(e in r["Event"] for e in events)


def sport(name, exclude=()):
    return lambda r: r["Sport"] == name and not any(x in r["Event"] for x in exclude)


def rower(r):
    if r["Sport"] != "Rowing" or "Lightweight" in r["Event"]:
        return False
    # Coxes are listed as crew in coxed boats; they are far lighter than rowers.
    if "Coxed" in r["Event"] and float(r["Weight"]) <= (60 if r["Sex"] == "M" else 55):
        return False
    return True


# App sport -> row filter. Sports absent from the Olympics (or too small) are
# left out and keep their literature targets.
GROUPS = {
    "Basketball": sport("Basketball"),
    "Volleyball": sport("Volleyball"),
    "Swimming": sport("Swimming"),
    "Water polo": sport("Water Polo"),
    "Rowing": rower,
    "Distance running": athletics("5,000 metres", "10,000 metres", "Marathon", "Steeplechase"),
    "Sprinting": athletics("100 metres", "200 metres", "400 metres", "4 x 100"),
    "High jump": athletics("High Jump"),
    "Long & triple jump": athletics("Long Jump", "Triple Jump"),
    "Shot put & discus": athletics("Shot Put", "Discus Throw"),
    "Gymnastics": sport("Gymnastics"),
    "Diving": sport("Diving"),
    "Figure skating": sport("Figure Skating"),
    "Ski jumping": sport("Ski Jumping"),
    "Weightlifting": sport("Weightlifting"),
    "Wrestling & judo": lambda r: r["Sport"] in ("Wrestling", "Judo"),
    "Boxing": sport("Boxing"),
    "Fencing": sport("Fencing"),
    "Road cycling (climbing)": lambda r: r["Sport"] == "Cycling" and "Road Race" in r["Event"],
    "Tennis": sport("Tennis"),
    "Badminton": sport("Badminton"),
    "Handball": sport("Handball"),
    "Football (soccer)": sport("Football"),
    "Baseball pitcher": lambda r: r["Sport"] in ("Baseball", "Softball"),
}

# Hurdles contain "100 metres"/"400 metres" in their names; keep them out of sprinting.
_sprint = GROUPS["Sprinting"]
GROUPS["Sprinting"] = lambda r: _sprint(r) and "Hurdles" not in r["Event"]


def robust(values):
    q = statistics.quantiles(values, n=4)
    return round(statistics.median(values), 2), round((q[2] - q[0]) / 1.349, 2)


def main():
    # (sport, sex) -> athlete id -> (year, height, weight)
    seen = defaultdict(dict)
    with SRC.open() as f:
        for r in csv.DictReader(f):
            if r["Height"] == "NA" or r["Weight"] == "NA" or int(r["Year"]) < YEAR_MIN:
                continue
            if r["Age"] != "NA" and int(r["Age"]) < 18:
                continue
            for name, match in GROUPS.items():
                if match(r):
                    prev = seen[(name, r["Sex"])].get(r["ID"])
                    if prev is None or int(r["Year"]) > prev[0]:
                        seen[(name, r["Sex"])][r["ID"]] = (int(r["Year"]), float(r["Height"]), float(r["Weight"]))

    out = {}
    for (name, sex), athletes in sorted(seen.items()):
        if len(athletes) < MIN_N:
            continue
        hs = [a[1] for a in athletes.values()]
        bmis = [a[2] / (a[1] / 100) ** 2 for a in athletes.values()]
        h, h_sd = robust(hs)
        b, b_sd = robust(bmis)
        out.setdefault(name, {})[sex.lower()] = {"n": len(athletes), "h": [h, h_sd], "bmi": [b, b_sd]}

    OUT.write_text(json.dumps(out, indent=1) + "\n")
    for name, d in out.items():
        cells = "  ".join(f"{s}: n={v['n']:>4} h={v['h'][0]:.0f}±{v['h'][1]:.1f} bmi={v['bmi'][0]:.1f}±{v['bmi'][1]:.1f}" for s, v in d.items())
        print(f"{name:<26}{cells}")


if __name__ == "__main__":
    main()
