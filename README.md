# Built For

Enter your body measurements and see which sports your build naturally suits.

**Live:** https://nishithada.github.io/built-for/

## What it does

- Scores 30 sports against the body proportions elite athletes in each sport tend to share.
- Team sports (football/soccer, basketball, volleyball, rugby union, American football) are scored per position.
- **Check a sport** shows your match for one sport or position and ranks the limiting factors: how far off each measurement is, whether it is fixed (bone length) or changeable (weight, BMI), and how many points it costs.
- Shows your build as a proportional diagram with percentile gauges.

Inputs: height and weight (required); arm span, sitting height or inseam, hand length, foot length and shoulder width (optional). Metric or imperial. Leg length is height minus sitting height; a barefoot crotch-to-floor inseam is used as leg length directly, since the two agree within about a centimetre on average (ANSUR II).

## How scoring works

Each measurement is converted to a percentile against approximate adult population norms for the chosen sex. Arm span and leg length are taken relative to height. Each sport or position has target values with a direction (more is better, less is better, or a sweet spot), a tolerance and a weight. Missing measurements count as neutral. A team sport scores as its best position.

The norms and targets are approximations drawn from sports-science literature on athlete anthropometry, not fitted to a dataset. Body shape is one factor among many; training, skill and physiology matter more.

## Run locally

It is a single static file with no build step. Open `index.html` in a browser.
