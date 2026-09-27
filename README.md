# Built For

Enter your body measurements and see which sports your build naturally suits.

**Live:** https://nishithada.github.io/built-for/

## What it does

- Scores 35 sports against the body proportions elite athletes in each sport tend to share.
- Team sports (football/soccer, basketball, volleyball, rugby union, American football, cricket, kabaddi) are scored per position.
- Detects your region from the device time zone and shows how you rank in the sports popular there (e.g. cricket, kabaddi and hockey in India).
- **Check a sport** shows your match for one sport or position and ranks the limiting factors: how far off each measurement is, whether it is fixed (bone length) or changeable (weight, BMI), and how many points it costs.
- Shows your build as a proportional diagram with percentile gauges.
- **Measure from a photo:** estimates arm span, leg length and shoulder width from one full-body photo, scaled from your height. Uses MediaPipe Pose Landmarker running in the browser; the photo is never uploaded. Estimates are labelled and editable.
- **Next steps** (collapsible, on every sport: top 3, ranked list and the sport check): how to get started, gear, a first focus based on your limiting factors, nearby clubs and venues from OpenStreetMap (Overpass API, location rounded to ~100 m and only sent when you tap the button), and a Google Maps fallback.
- **Share** a text summary of your results.

Inputs: height and weight (required); arm span, sitting height or inseam, hand length, foot length and shoulder width (optional). Metric or imperial. Leg length is height minus sitting height; a barefoot crotch-to-floor inseam is used as leg length directly, since the two agree within about a centimetre on average (ANSUR II).

## How scoring works

Sports are ranked by **advantage**: how much more common your build is among a sport's elite athletes than in the general population (e.g. "6.6× more common among Olympic badminton players than among men in general"). **Match %** (how closely you fit their typical build) is shown alongside and drives the limiting factors. Method and trade-offs: [DECISIONS.md](DECISIONS.md).

Each measurement is converted to a percentile against approximate adult population norms for the chosen sex. Arm span and leg length are taken relative to height. Each sport or position has target values with a direction (more is better, less is better, or a sweet spot), a tolerance and a weight. Missing measurements count as neutral. A team sport scores as its best position.

Height and BMI targets for 27 sports are fitted on Olympic athletes 1992–2016 (the *120 years of Olympic history* dataset, github.com/rgriff23/Olympic_history) by `scripts/fit_olympic.py`; within an athlete's middle half scores full marks. Team-sport positions keep literature offsets around the sport's real median. Arm span, leg, hand, foot and shoulder targets, and sports without Olympic data (climbing, sumo, jockey, coxswain, rugby union, American football, cricket, kabaddi), still use approximations from sports-science literature. To refit: download `athlete_events.csv` into `data/raw/` and run `python3 scripts/fit_olympic.py`. Body shape is one factor among many; training, skill and physiology matter more.

## Run locally

It is a single static file with no build step. Open `index.html` in a browser.
