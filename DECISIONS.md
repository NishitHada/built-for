# Decisions

Short records of product and method decisions: what was decided, why, and what it costs. Newest first.

---

## 008 — Unpaid "creator's picks": Playo and Decathlon, subtle and in context

**Date:** 2026-09-28 · **Status:** accepted

### Context
The owner uses and likes Playo (court booking) and Decathlon (sports gear) and wanted them featured, without it reading as an ad or pushing users.

### Decision
- **Only where they help, only in India** (both are India-specific links; Playo operates only there).
- **Decathlon:** a small "Beginner options at Decathlon" link at the end of each sport's Gear line, searching decathlon.in for that sport's gear. Skipped for sports it doesn't sensibly stock (coxing, ski jumping, sumo, kabaddi, fencing, ice hockey, American football).
- **Playo:** one line under the venue results after "Find places near me", and only for the 8 sports Playo lists (badminton, football, cricket, tennis, table tennis, basketball, volleyball, swimming), and only when the visitor is within 60 km of a city Playo serves. It links to that city and sport. It also appears if the map search fails, when it's most useful.
- Plain text links in the page's normal style: no logos, badges or buttons.
- Links carry `utm_source=builtfor` so either brand can see referrals in its own analytics; clicks are counted as `evt/playo/<sport>` and `evt/decathlon/<sport>`.
- Disclosed on the Methodology page: "the creator's own picks. There's no payment or partnership."
- **Rule carried forward:** these links never affect rankings, scores or which sports are shown.

### Related change
Places search now tries a second public OpenStreetMap server (overpass.kumi.systems) with a 12-second limit per server, because the main server was refusing requests. A Russian mirror (maps.mail.ru) also works but was left out because it would receive visitors' approximate locations.

---

## 007 — Deep dive is a results tab

**Date:** 2026-09-27 · **Status:** accepted (amends 006)

### Context
After 006 moved the deep dive to a separate sport page, the owner found it hard to reach and asked for it to be a tab.

### Decision
Results have three tabs: **Sports · Deep dive · Your build**. The Deep dive tab holds the sport picker, your fit, positions, limiting factors and next steps. Tapping any sport (list row, top 3, explore card) opens it in that tab. The tab keeps the shareable address `#s-<sport>`; "← All sports" and the browser Back button return to the Sports tab at the same list position. Before you've measured there are no results, so a sport opens as its own page showing what the sport rewards. The separate "Deep dive into any sport" bar is removed because the tab carries the picker.

---

## 006 — Sport pages, explore strip, and a landing page in the house style

**Date:** 2026-09-27 · **Status:** accepted

### Context
The deep dive sat under the ranked list, so tapping a sport jumped far down the page with no way back to your place, it was always on screen, and it couldn't be linked. The owner also supplied a new landing mockup (dark navy and electric blue) and chose to keep the existing visual style (option A).

### Decision
- **Sport pages** at `#s-<sport>` (e.g. `#s-cricket`), opened from the explore cards, the top 3 and the ranked list. With measurements they show the personal fit (advantage, positions, limiting factors, next steps). Without them they show what the sport rewards: typical height, BMI and helpful traits per position, a call to measure, and next steps. "← All sports" and the browser Back button return to the exact list position; a switcher moves between sports.
- **Landing** follows the mockup's structure in the house style: new headline, icon trust row, two primary actions, the owner's body illustration, and an **Explore** strip that leads with the region's popular sports, shows each one's typical elite height, and expands to all 35.
- **Methodology** becomes its own page (`#method`), reachable from the header before measuring; results keep two tabs (Sports, Your build).

### Trade-offs
- The first illustration drew "Arm span" and "Shoulder width" in the wrong places; replaced on 2026-09-27 with the owner's corrected artwork (arms out, fingertip to fingertip; shoulder tips).
- Explore cards use a colour per sport, a coloured icon, a colour wash and a faded large icon. Athlete artwork per sport (as in the mockup) would need to be commissioned for all 35.
- Sport cards are typographic; athlete artwork for each sport would need to be commissioned.

---

## 005 — Three screens, one filterable list, next steps only in the deep dive

**Date:** 2026-09-27 · **Status:** accepted

### Context
A UX review of the single long page found: controls far from what they change (the region dropdown sat above the top 3 but controlled a list further down); two lists answering the same question ("Popular in India" and "All sports"); Next steps repeated 39 times; the form burying results on phones; no methodology page. The owner proposed a landing / measurements / results flow; this adopts its structure and keeps the existing visual style.

### Decision
- **Landing** (first visit only): promise, trust points (about 2 minutes, no account, photos stay on device), Get started, See an example, photo shortcut, three-step "how it works".
- **Measure**: two-step progress bar; Basics (required) and Sharper result (optional, with the photo card) cards; "See my results" with inline validation and a count of measurements entered; a live preview of top sports on desktop. First visits start with an empty form; example values are flagged with a "Clear and enter mine" notice so they can't silently mix with real ones.
- **Results** with tabs **Sports · Your build · Methodology** and a summary bar (measurements, Edit, Share).
  - Sports: top 3 → **one ranked list with filter chips** (Popular in <region>, All, Team, Individual) with the region dropdown beside them → a single **deep dive**, the only place with Next steps.
  - Popular-in-region is the default filter outside "Worldwide", so local sports stay visible without a second list.
- Returning visitors go straight to Results. Screens map to `#measure` / `#results` so the browser Back button works.

### Consequences
One list instead of two, one Next steps block instead of 39, the region control sits on the list it filters, and the phone flow is measure → results rather than one long scroll. Methodology (roadmap 1.2) now has a home. Trade-off: the deep dive and your build are one tap further away than before.

---

## 004 — Show region-popular sports; add cricket, kabaddi, field hockey, table tennis, ice hockey

**Date:** 2026-09-27 · **Status:** accepted

### Context
Rankings were global. In India, cricket (the biggest sport) wasn't in the app at all, and a user's best local options could sit far below the top 3 without being noticed.

### Decision
- **Add five sports** (30 → 35): cricket (fast bowler, spin bowler, batter, wicketkeeper), kabaddi (raider, defender), field hockey, table tennis, ice hockey. The last three have Olympic data and are fitted like the others; cricket and kabaddi use literature targets.
- **Detect the region from the device's time zone** (no permission prompt), falling back to the browser language, then "Worldwide". A dropdown lets people change it; a manual choice is remembered.
- **Show a "Popular in <region>" section** under the top 3, listing that region's popular sports ranked by the user's advantage, with each sport's overall rank. Popular sports also get a "popular here" badge in the top 3 and ranked list, and head the sport picker.
- **Region never changes the global ranking or scores.** It only decides which sports are surfaced.

### Trade-offs
- The popularity lists (16 regions) are **editorial**, based on general knowledge of participation and viewership, not a dataset. They should be reviewed by people from each region.
- Time zone is a rough proxy (e.g. all of continental Europe maps to one list; Latin America except Brazil is one list).
- Population norms are still Western, so for Indian users the advantage in "tall" sports is understated. The population selector (roadmap) is the natural follow-up and can default from the same region.

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
