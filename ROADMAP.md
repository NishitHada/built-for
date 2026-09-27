# Built For — Roadmap

Goal: turn Built For from a fun quiz into a tool people trust, then into a business. The order matters: credibility first, then measurement, then growth, and a backend only once schools or academies have said they'd pay.

Legend: `[x]` done · `[ ]` to do · **(you)** needs the owner, not code

---

## Phase 0 — Shipped

- [x] Sport fit ranking for 30 sports from body measurements
- [x] Team sports scored per position (football, basketball, volleyball, rugby union, American football)
- [x] Check a sport: verdict, limiting factors (fixed vs changeable, points cost), what-if
- [x] Body diagram and percentile gauges
- [x] Sitting height or inseam for leg length, with how-to-measure diagrams
- [x] Measure from a photo (on-device MediaPipe pose, scaled from height)
- [x] Next steps on every sport: getting started, first focus, places near you (OpenStreetMap), Google Maps fallback
- [x] Share results
- [x] Mobile layout, GitHub Pages deploy

---

## Phase 1 — Credibility (static site, no backend)

Why: several sports score 99–100% for any athletic build, the targets are hand-set from literature, and photo accuracy is unmeasured. A single public debunk would sink the product.

### 1.1 Refit height and weight targets on real Olympic data
Source: *120 years of Olympic history* (`athlete_events.csv`, 271k rows, 1896–2016), mirrored at `github.com/rgriff23/Olympic_history`. Only aggregate statistics are published; the raw file is not committed.

- [x] Download the dataset locally (not committed; `data/raw/` is git-ignored)
- [x] `scripts/fit_olympic.py`: filter to Summer 1992–2016 and Winter 1994–2014, adults, rows with height and weight
- [x] Map Olympic events to app sports and positions (e.g. Athletics 100 m/200 m → Sprinting; Marathon, 10,000 m → Distance running; Judo + Wrestling → Wrestling & judo; Rowing coxed events → Coxswain only if identifiable, otherwise leave literature targets)
- [x] Per sport × sex: sample size, median and spread of height, weight and BMI
- [x] Emit `data/olympic_fit.json`; keep sports with n ≥ 40 per sex, flag the rest
- [x] Replace hand-set height and BMI targets with fitted ones (target = median, tolerance from the spread); keep literature targets for traits the data lacks (arm span, legs, hands, feet, shoulders) and for sports not in the data (climbing, sumo, jockey, American football, rugby union positions)
- [x] Fix score saturation: rank by **advantage ratio** ("6.6× more common among Olympic badminton players than among men in general"), match % secondary. See [DECISIONS.md](DECISIONS.md) #002
- [x] Region-popular sports: detect region from time zone, "Popular in <region>" section, badges; add cricket, kabaddi, field hockey, table tennis, ice hockey (35 sports). See [DECISIONS.md](DECISIONS.md) #004
- [ ] **(you)** Review the popularity lists for regions you know; ask friends abroad to sanity-check theirs
- [ ] Population selector for "people in general": Western norms (current) vs India (men ~166 cm, women ~153 cm) vs global; default from the detected region
- [ ] Model height–BMI correlation instead of treating them as independent
- [x] Show "compared with N Olympic athletes" on sports that use fitted data
- [x] Regression check: the example builds (swimmer, marathoner, gymnast, lineman, volleyball, climber) still rank their own sport near the top

### 1.2 Methodology section
- [ ] "How scoring works" section on the page: data sources, what's fitted vs literature-based, what the % means, limits
- [ ] Cite sources in the README

### 1.3 Validate photo measuring **(you + code)**
- [ ] Write a test protocol: tape-measure arm span, inseam, shoulder width; take the photo per the app's instructions
- [ ] **(you)** Collect 30–50 people (friends, a gym, a club)
- [ ] Hidden debug mode that shows the raw estimate next to the typed value, for data collection
- [x] First real-world check (1 person): arm span and leg length close; shoulder width 32 vs 40 cm → added ×1.25 correction ([DECISIONS.md](DECISIONS.md) #003)
- [ ] Compute mean error and spread per measurement; recalibrate the 0.936 eye-height, 0.902 hip-to-leg and 1.25 shoulder factors
- [ ] Publish the accuracy on the page ("arm span within ±X cm for 80% of people")

---

## Phase 2 — Measure what people do (still static)

- [ ] **(you)** Create a GoatCounter account (free, cookie-free, no consent banner) and share the site code
- [ ] Add the GoatCounter script and events: results viewed, sport checked, photo used (success/fail), places searched (found/none), share used, preset used
- [ ] Never send measurements or location in events
- [ ] "Did this match your experience?" thumbs up/down on the best fit, sent as an event

---

## Phase 3 — Engagement and growth (static)

- [ ] Share card: draw a result image in the browser (top 3 + body diagram) for Instagram/WhatsApp
- [ ] One page per sport ("Am I built for basketball?") for search traffic
- [ ] Phone-based ability tests: vertical jump from slow-motion video (flight time), 20 m sprint timer, sit-and-reach, plank; fold into scoring as a separate "ability" signal
- [ ] Youth mode: age-group norms and predicted adult height from parents' heights (Khamis–Roche), with careful framing for under-18s
- [ ] 8-week starter plans per sport, printable-free (on page), with a re-test reminder

---

## Phase 4 — Customer discovery **(you)**

- [ ] Interview 10 PE teachers and academy coaches in Bangalore: how they spot talent today, what a class screening would need, what they'd pay
- [ ] Decide the wedge: schools, academies, or parents
- [ ] Only proceed to Phase 5 if at least 3 say they would pilot

---

## Phase 5 — Backend (only after Phase 4)

- [ ] Supabase in the Mumbai region (Postgres, auth, row-level security)
- [ ] School/academy tool: teacher login, class rosters, batch screening, per-child reports, class overview, CSV export
- [ ] Verifiable parental consent for under-18s (DPDP Act 2023); store measurements only, never photos
- [ ] Cloudflare Worker to cache OpenStreetMap place searches by area
- [ ] Lead-gen partnerships with academies and booking apps, with referral tracking
