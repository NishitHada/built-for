# Decisions

Short records of product and method decisions: what was decided, why, and what it costs. Newest first.

---

## 003 — Correct photo shoulder width by ×1.25

**Date:** 2026-09-26 · **Status:** accepted, provisional (one data point)

### Context
First real-world check of photo measuring: arm span and leg length came out close to tape measurements, but shoulder width read **32 cm against 40 cm** by tape.

### Cause
The pose model's shoulder landmarks sit at the shoulder **joint centres**. Shoulder width (biacromial breadth) is measured between the **bony tips** (acromion), which sit several centimetres further out on each side. The raw landmark distance therefore always under-reads.

### Decision
Multiply the landmark distance by **1.25** (40 / 32) for shoulder width only. Arm span still uses the raw distance, because the arm line genuinely runs through the joint centres.

### Consequences
Shoulder width estimates should now land near tape values for builds like the tester's. The factor rests on **one person**; photo validation (roadmap 1.3) should refit it, along with the eye-height (0.936) and hip-to-leg (0.902) factors, once 30–50 tape-vs-photo pairs are collected.

---

## 002 — Rank sports by advantage ratio, keep match % as secondary

**Date:** 2026-09-26 · **Status:** accepted

### Context
After anchoring height and BMI to Olympic data (001), an athletic build still scored 90–100% in about ten sports. The data showed why: Olympic footballers, tennis players, sprinters, fencers and badminton players all sit near 180 cm and BMI 23 (men). A "how typical are you of this sport's athletes" percentage can't separate sports whose athletes look alike, so it can't answer the app's question: *where does your body give you a natural advantage?*

Options considered:
1. **Advantage ratio**: rank by how over-represented your build is among a sport's athletes compared with the general population.
2. **Stricter match %**: score harder so fewer sports reach 90%. Rejected: real Olympians would score poorly in their own sport, and the number gets harder to explain.
3. **Leave ties**: rejected, because the top 3 would be close to arbitrary for common builds.

### Decision
Rank by **advantage** = P(your build | sport's athletes) / P(your build | general population), shown as "6.6×". Show **match %** alongside it as a secondary number. Match % still drives the limiting factors.

Wording on the page: *"Men with your build are 6.6× more common among Olympic badminton players than among men in general."*

Verdict bands: ≥3× strong natural advantage · 1.5–3× some advantage · 0.67–1.5× no clear advantage · below 0.67× built against it.

### Method
- **Height:** athlete normal (Olympic median and robust spread) vs population normal (adult norms by sex).
- **BMI:** athlete normal vs population **log-normal** (adult BMI is right-skewed): men median 25.2, women 24.7.
- **Weight-based targets** (jockey, coxswain, sumo): converted through BMI at the person's height; skipped when the sport also has a BMI target (same information).
- **Arm span, legs, hands, feet, shoulders:** literature targets with an assumed athlete spread of 0.8 population SD, counted at half strength, then **averaged into one factor**. They all track body size, so multiplying them would count the same signal several times.
- **Out-of-range guard:** if you're more than 2 athlete spreads from their median on a trait, that trait can lower your advantage but never raise it. Two thin normal tails otherwise produce huge, meaningless ratios (e.g. a 188 cm woman "401× more common" among American football receivers she's far taller than).
- **Caps:** each height, BMI or weight factor is capped at e^±6; each literature trait at e^±3. Display caps at "99×+".
- "Taller is better" style one-sided targets apply to match % only. For advantage the athletes' real spread decides (a 200 cm man is rare among 186 cm centre-backs).
- Team sports rank by their best position's advantage.

### Consequences
- Common builds honestly get about 1–2× everywhere ("no clear advantage"), instead of a wall of 95% scores.
- Archetype builds rank their own sport first or near the top: marathoner → distance running 13×, gymnast → gymnastics 14×, lineman → American football lineman, climber → rock climbing, 200 cm man → volleyball, basketball, rowing.
- Very tall or heavy builds hit "99×+" in several sports; the ranking still orders them.

### Known limitations
- Height and BMI are treated as independent; in reality they're mildly correlated.
- Position-level ratios use literature offsets around the sport's real median, not per-position data.
- Six sports have no Olympic data (climbing, sumo, jockey, coxswain, rugby union, American football); their ratios use literature targets with typical elite spreads and are labelled "elite", not "Olympic".
- **Population norms are Western adult averages** (men 175.5 cm). For users in India (men about 166 cm), "compared with men in general" should use local norms. See roadmap.

---

## 001 — Anchor height and BMI targets to Olympic athlete data

**Date:** 2026-09-26 · **Status:** accepted

### Context
All targets were hand-set from sports-science literature, and several sports saturated near 100%.

### Decision
Fit per-sport, per-sex medians and robust spreads (IQR / 1.349) of height and BMI from 1992–2016 Olympians (*120 years of Olympic history*), via `scripts/fit_olympic.py`. Each athlete counts once per sport; lightweight rowers and coxes are excluded; sports with fewer than 40 athletes per sex keep literature targets.

Match % for height and BMI: full marks inside the athletes' middle half, then falling with how rare you'd be among them (`min(1, 4·Φ(−|d|))`), so a real Olympian averages about 0.75 per trait. Team-sport positions keep their literature offsets, re-centred on the sport's real median.

### Consequences
Targets for 24 sports are now data-backed and cited on the page ("compared with 1,107 Olympic men"). Saturation was not solved by this alone; see 002.
