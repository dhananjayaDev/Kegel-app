> *This is for informational purposes only. For medical advice or diagnosis, consult a professional.*

This implementation blueprint outlines the clinical logic, scoring mechanisms, and clinical-grade recommendation algorithms required to develop a comprehensive diagnostic and therapeutic engine for male erectile dysfunction (ED) within a mobile application.

---

## Step 1: Algorithmic 32-Question Screening Questionnaire

To construct a high-resolution diagnostic profile, the app must capture symptoms across five clinical axes: the validated 15-item International Index of Erectile Function (IIEF-15), morning/nocturnal erections, cardiovascular risk factors, endocrinopathies, and structural or neurological trauma.

### Section A: Validated IIEF-15 Standard Clinical Battery (Questions 1–15)

Recall Period: Past 4 weeks

* **Q1: How often were you able to get an erection during sexual activity?**

* `0`: No sexual activity
* `1`: Almost never or never
* `2`: A few times (less than half the time)
* `3`: Sometimes (about half the time)
* `4`: Most times (more than half the time)
* `5`: Almost always or always


* **Q2: When you had erections with sexual stimulation, how often were your erections hard enough for penetration?**

* `0`: No sexual activity
* `1`: Almost never or never
* `2`: A few times (less than half the time)
* `3`: Sometimes (about half the time)
* `4`: Most times (more than half the time)
* `5`: Almost always or always


* **Q3: When you attempted sexual intercourse, how often were you able to penetrate your partner?**

* `0`: Did not attempt intercourse
* `1`: Almost never or never
* `2`: A few times (less than half the time)
* `3`: Sometimes (about half the time)
* `4`: Most times (more than half the time)
* `5`: Almost always or always


* **Q4: During sexual intercourse, how often were you able to maintain your erection after you had penetrated your partner?**

* `0`: Did not attempt intercourse
* `1`: Almost never or never
* `2`: A few times (less than half the time)
* `3`: Sometimes (about half the time)
* `4`: Most times (more than half the time)
* `5`: Almost always or always


* **Q5: During sexual intercourse, how difficult was it to maintain your erection to completion of intercourse?**

* `0`: Did not attempt intercourse
* `1`: Extremely difficult
* `2`: Very difficult
* `3`: Difficult
* `4`: Slightly difficult
* `5`: Not difficult


* **Q6: How many times have you attempted sexual intercourse?**

* `0`: No attempts
* `1`: 1 to 2 attempts
* `2`: 3 to 4 attempts
* `3`: 5 to 6 attempts
* `4`: 7 to 10 attempts
* `5`: 11 or more attempts


* **Q7: When you attempted sexual intercourse, how often was it satisfactory to you?**

* `0`: Did not attempt intercourse
* `1`: Almost never or never
* `2`: A few times (less than half the time)
* `3`: Sometimes (about half the time)
* `4`: Most times (more than half the time)
* `5`: Almost always or always


* **Q8: How much have you enjoyed sexual intercourse?**

* `0`: No intercourse
* `1`: No enjoyment at all
* `2`: Not very enjoyable
* `3`: Fairly enjoyable
* `4`: Highly enjoyable
* `5`: Very highly enjoyable


* **Q9: When you had sexual stimulation or intercourse, how often did you ejaculate?**

* `0`: No sexual stimulation or intercourse
* `1`: Almost never or never
* `2`: A few times (less than half the time)
* `3`: Sometimes (about half the time)
* `4`: Most times (more than half the time)
* `5`: Almost always or always


* **Q10: When you had sexual stimulation or intercourse, how often did you have the feeling of orgasm or climax (with or without ejaculation)?**

* `0`: No sexual stimulation or intercourse
* `1`: Almost never or never
* `2`: A few times (less than half the time)
* `3`: Sometimes (about half the time)
* `4`: Most times (more than half the time)
* `5`: Almost always or always


* **Q11: How often have you felt sexual desire?**

* `1`: Almost never or never
* `2`: A few times (less than half the time)
* `3`: Sometimes (about half the time)
* `4`: Most times (more than half the time)
* `5`: Almost always or always


* **Q12: How would you rate your level of sexual desire?**

* `1`: Very low or no desire
* `2`: Low
* `3`: Moderate
* `4`: High
* `5`: Very high


* **Q13: How satisfied have you felt with your overall sex life?**

* `1`: Very dissatisfied
* `2`: Moderately dissatisfied
* `3`: About equally satisfied and dissatisfied
* `4`: Moderately satisfied
* `5`: Very satisfied


* **Q14: How satisfied have you been with your sexual relationship with your partner?**

* `1`: Very dissatisfied
* `2`: Moderately dissatisfied
* `3`: About equally satisfied and dissatisfied
* `4`: Moderately satisfied
* `5`: Very satisfied


* **Q15: How do you rate your confidence that you can get and keep your erection?**

* `1`: Very low
* `2`: Low
* `3`: Moderate
* `4`: High
* `5`: Very high



---

### Section B: Autonomic & Morning Erection Diagnostics (Questions 16–20)

Focus: Isolating psychogenic situational variance

* **Q16: How did your erectile difficulties first develop?**

* `0`: Gradually, worsening progressively over several months or years (Organic Marker)


* `1`: Abruptly, occurring almost overnight, often correlating with a specific stressful event or change (Psychogenic Marker)




* **Q17: Over the past month, how often have you experienced a full, rigid erection upon waking up in the morning?**

* `0`: Never (Organic Marker)


* `1`: Seldom (less than 20% of the time)
* `2`: Less than half the time
* `3`: About half the time
* `4`: More than half the time
* `5`: Almost always or always (Psychogenic Marker)




* **Q18: Which statement best describes the consistency of your erections?**

* `0`: They are consistently weak in all situations (with a partner, during self-stimulation/masturbation, and upon waking)


* `1`: They vary; I can achieve rigid, sustainable erections during self-stimulation or in the morning, but struggle during intimacy with a partner




* **Q19: How often do you feel extreme anxiety, distraction, or fear of performance failure prior to or during sexual encounters?**

* `0`: Never or rarely
* `1`: Sometimes
* `2`: Frequently or almost always (Sympathetic Over-activation Marker)




* **Q20: Once achieved, how rapidly does your erection subside if stimulation is temporarily paused?**

* `0`: Almost instantly, losing significant rigidity within seconds (Veno-occlusive Failure/Venous Leak Marker)


* `1`: Gradually, behaving normally with a slow loss of rigidity over several minutes



---

### Section C: Systemic Vascular & Cardiovascular Risks (Questions 21–25)

Focus: Assessing cardiometabolic markers and vasculogenic risk

* **Q21: Do you experience cramping, tightness, or pain in your calves or thighs when walking briskly that resolves with rest (intermittent claudication)?**

* `0`: Yes (Vascular Claudication Marker; possible pelvic inflow stenosis)


* `1`: No


* **Q22: Have you been diagnosed with, or are you currently taking medication for, any of the following? (Select all that apply)**

* `0`: Hypertension, Coronary Artery Disease, Dyslipidemia, or Peripheral Vascular Disease


* `1`: None of the above


* **Q23: How would you rate your typical exercise tolerance and physical capacity?**

* `0`: Highly restricted: I experience chest pain, breathlessness, or palpitations with light exertion like climbing one flight of stairs


* `1`: Standard: I can walk briskly or engage in moderate physical work without cardiopulmonary symptoms




* **Q24: Are you currently prescribed Nitrates or Nitroglycerin for heart conditions?**

* `0`: Yes (Absolute Contraindication for PDE5i medication)


* `1`: No


* **Q25: What is your history of tobacco use (smoking/vaping)?**

* `0`: Active daily smoker or history of heavy smoking (>10 pack-years)


* `1`: Non-smoker or light social history



---

### Section D: Endocrinopathies & Neurological Markers (Questions 26–29)

Focus: Mapping endocrine and neurological pathways

* **Q26: Have you noticed unexplained loss of muscle mass, significant physical fatigue, hot flashes, or breast tissue enlargement (gynecomastia)?**

* `0`: Yes (Possible Hypogonadism/Androgen Deficiency Marker)


* `1`: No


* **Q27: Have you been diagnosed with Type 1 or Type 2 Diabetes, or has a recent blood test shown elevated HbA1c levels ($>5.7\%$)?**

* `0`: Yes (Possible Diabetic Neuropathy or Endothelial Dysfunction Marker)


* `1`: No


* **Q28: Do you experience a lack of sensation, numbness, or "pins and needles" in your genitals, pelvic floor, or perineum?**

* `0`: Yes (Severe Neurological Sign)


* `1`: No


* **Q29: Have you ever undergone radical pelvic surgery (e.g., radical prostatectomy), pelvic radiotherapy, or sustained a spinal cord injury?**

* `0`: Yes (Neurogenic/Iatrogenic ED Marker)


* `1`: No



---

### Section E: Anatomical, Trauma, & Immediate Red Flag Metrics (Questions 30–32)

Focus: Hard clinical red flags and urological alerts

* **Q30: Do you feel hard, painless lumps (plaques) within your penis, or do you experience pain or a sharp, abnormal curvature ($>30^\circ$) during erections?**

* `0`: Yes (Anatomical/Structural Alert; Peyronie's Disease Marker)


* `1`: No


* **Q31: Have you sustained a blunt trauma to your groin, pelvis, or perineum (e.g., a high-impact bicycle frame injury, straddle injury, or pelvic fracture)?**

* `0`: Yes (Local Pelvic Vascular/Nerve Injury Alert)


* `1`: No


* **Q32: Have you ever experienced a painful, rigid erection that lasted longer than 4 hours without stimulation?**

* `0`: Yes (Priapism Emergency Alert)


* `1`: No



---

## Step 2: Scoring Engine & Etiology Mapping Algorithms

To calculate the user's ED severity, the app calculates the sum of the **IIEF Erectile Function (EF) Domain** using the classic 6-item scoring mechanism:

$$\text{IIEF-EF}_{\text{score}} = Q_1 + Q_2 + Q_3 + Q_4 + Q_5 + Q_{15}$$

### Clinical Severity Ranges

The numerical score is converted into a standard severity tier:

| IIEF-EF Score Range | Severity Classification | Pathophysiological Profile

 |
| --- | --- | --- |
| **$26\text{--}30$** | No Erectile Dysfunction | Normal neurovascular, somatic, and psychosexual profile. |
| **$22\text{--}25$** | Mild ED | Slight reduction in rigidity or confidence; highly responsive to PFMT.

 |
| **$17\text{--}21$** | Mild-to-Moderate ED | Occasional failure to maintain coital rigidity.

 |
| **$11\text{--}16$** | Moderate ED | Frequent failure to maintain or achieve rigidity; mixed causes common.

 |
| **$6\text{--}10$** | Severe ED | Complete or near-complete inability to achieve rigid erections.

 |

---

### Etiology Mapping Engine

The app runs a heuristic rule engine based on Section B, C, D, and E responses to identify the root cause:

```
                           [User Input Evaluated]
                                     │
             ┌───────────────────────┴───────────────────────┐
             ▼                                               ▼
  [If Q16=1 AND Q17>=4]                               [If Q16=0 OR Q17<=1]
             │                                               │
             ▼                                               ▼
   [Psychogenic Etiology]                               [Organic Etiology]
                                                             │
                                   ┌─────────────────────────┴─────────────────────────┐
                                   ▼                                                   ▼
                        [If Q2 < Q4 AND Q21=0]                              [If Q4 < Q2 OR Q20=0]
                                   │                                                   │
                                   ▼                                                   ▼
                        {Arteriogenic Profile}                               {Venogenic Profile}

```

* **Primary Psychogenic ED Profile:**
* *Trigger Rule:* $(\text{Q16} = 1) \land (\text{Q17} \ge 4) \land (\text{Q18} = 1)$

* *Somatic Context:* Penile "hardware" is intact; sympathetic autonomic tone limits blood flow during partnered intimacy.




* **Primary Arteriogenic Profile:**
* *Trigger Rule:* $(\text{Q16} = 0) \land (\text{Q17} \le 1) \land (\text{Q2} < \text{Q4})$ OR selection of any vascular comorbidity in $\text{Q22}$

* *Somatic Context:* Penile arterial inflow is restricted; struggles primarily to *achieve* initial rigidity.




* **Primary Venogenic Profile (Venous Leak / Muscular Weakness):**
* *Trigger Rule:* $(\text{Q16} = 0) \land (\text{Q17} \le 1) \land (\text{Q4} < \text{Q2})$ OR $(\text{Q20} = 0)$

* *Somatic Context:* Impairment of the passive veno-occlusive mechanism or weak superficial pelvic muscles ($\text{ICM}/\text{BSM}$) failing to compress outbound veins.




* **Neurogenic Profile:**
* *Trigger Rule:* Positive response on $\text{Q28} = 0$ OR $\text{Q29} = 0$

* *Somatic Context:* Interruption of the parasympathetic cavernous or somatic pudendal nerves.




* **Endocrinopathic Profile:**
* *Trigger Rule:* $(\text{Q11} \le 2) \land (\text{Q12} \le 2)$ AND $(\text{Q26} = 0)$

* *Somatic Context:* Hypogonadism or low circulating testosterone affecting both libido and cavernosal tissue health.




* **Anatomical / Structural Profile:**
* *Trigger Rule:* Positive response on $\text{Q30} = 0$

* *Somatic Context:* Localized fibrous plaques restricting expansion of the tunica albuginea.




* **Mixed ED Profile:**
* *Trigger Rule:* Fulfills overlapping indicators of both Psychogenic and Organic profiles (the most common clinical cohort).





---

## Step 3: Triage and Recommendation Decision Engine

Based on the severity tier, etiology, and medical safety alerts, the user is routed to a structured treatment pathway:

| Scoring & Etiology Trigger Criteria | Recommendation Pathway | Primary Clinical Action & App Output

 |
| --- | --- | --- |
| Any positive alert on **$\text{Q32} = 0$** (Priapism) or pelvic trauma **$\text{Q31} = 0$**<br> | **Pathway E: Emergency Department Transfer** | Display a critical red screen: *"Emergency Alert: Suspected ischemic priapism or acute pelvic trauma. Go to the nearest Emergency Department (A&E) immediately."*<br> |
| Any positive alert on **$\text{Q30} = 0$** (Anatomical) or **$\text{Q28} = 0$** (Neurogenic)

 | **Pathway C: Specialist Urology Referral** | Display alert: *"Urological consult required. A physician must examine your pelvic nerves or penile anatomy to evaluate conditions like Peyronie's disease."*<br> |
| High-risk vascular factors selected in **$\text{Q22}$** OR **$\text{Q23} = 0$** (Low MET capacity)

 | **Pathway D: Cardiology & Cardiovascular Screening** | Trigger Princeton III alert: *"Erectile dysfunction is an early warning sign for cardiovascular disease. Please undergo a cardiology evaluation before starting intensive exercise."*<br> |
| IIEF-EF Score $\le 10$ (Severe) with no immediate red flags

 | **Pathway C + A: Combined Medical & Urological Care** | Suggest consulting a urologist to discuss first-line medical options (PDE5i), and provide a gentle pelvic floor base-mobilization routine as support.

 |
| IIEF-EF: $11\text{--}25$ AND Primary Psychogenic Profile

 | **Pathway B: Cognitive Behavioral / Sex Therapy** | Suggest psychosexual therapy or digital CBT modules to reduce performance anxiety, with a light Kegel routine to build physical confidence.

 |
| IIEF-EF: $17\text{--}25$ AND Venogenic / Muscular Profile (No Red Flags)

 | **Pathway A: Target Pelvic Floor Muscle Training (PFMT) Alone** | Deploy the specialized male PFMT exercise engine. Dorey's clinical trials show that venous-leak-related ED is highly responsive to supervised PFMT.

 |
| IIEF-EF: $11\text{--}16$ AND Mixed/Organic Profile (No Red Flags)

 | **Pathway A + D: PFMT & Metabolic Coaching** | Recommend primary care screening for lipids and HbA1c, while starting a moderate-to-high intensity PFMT routine paired with daily walking.

 |

---

## Step 4: Standardized, Level-Specific Male PFMT Protocols

To duplicate the clinical outcomes documented in clinical trials, pelvic floor exercises must target the superficial perineal layer, specifically the **ischiocavernosus ($\text{ICM}$)** and **bulbospongiosus ($\text{BSM}$)** muscles, to compress outbound veins and raise intracavernous pressure.

### Dynamic Motor Verification (Visual & Somatic Cueing)

To isolate these muscles without tensing the core or buttocks, the app guides the user to:

1. **The Somatic Cue:** *"Voluntarily contract your pelvic floor as if trying to stop the flow of urine mid-stream and tensing to hold in gas."*

2. **Visual Verification:** Look in a mirror. A successful contraction causes a subtle upward scrotal lift and draws the base of the penis inward and upward toward the lower abdomen.


3. **Compensatory Check:** Do *not* hold your breath, pull in your upper abdomen, or squeeze your buttocks or inner thighs.



---

### Protocol 1: Mild ED Focus (IIEF-EF: 22–25)

* **Focus:** Standing postural stability and upright veno-occlusion.



```
Position: Standing upright with feet hip-width apart [cite: 34, 41, 44]
Sets per session: 2
Daily Frequency: 3 times daily (Morning, Noon, Evening) [cite: 24, 27, 44]
Weekly Cadence: 3 alternating days per week (e.g., Mon/Wed/Fri) [cite: 41, 44]

```

#### Exercise List

1. **Standing Isometric Holds (Type I Endurance):** Squeeze the pelvic floor at a steady $70\%$ maximal voluntary contraction. Hold for $6$ seconds, followed by $12$ seconds of complete muscular release. Repeat for $12$ repetitions.


2. **Standing Quick Flicks (Type II Fast-Twitch):** Perform $10$ rapid, explosive contractions (squeeze for $1$ second, then immediately release) to build quick venous trapping reflexes.


3. **Functional Urge Control Knack:** Perform a strong, submaximal $50\%$ pelvic floor contraction during everyday standing activities (such as brushing teeth).



---

### Protocol 2: Mild-to-Moderate ED Focus (IIEF-EF: 17–21)

* **Focus:** Core-pelvic isolation and progressive gravity-resisted loading.



```
Position: Seated upright on a hard-backed chair with knees apart [cite: 34, 41]
Sets per session: 3
Daily Frequency: 3 times daily [cite: 24, 27, 41]
Weekly Cadence: 4 days per week [cite: 41]

```

#### Exercise List

1. **Seated Isometric Holds (Type I Endurance):** Squeeze and lift the pelvic floor as strongly as possible without rising off the chair. Hold for $8$ seconds, followed by $16$ seconds of complete release. Repeat for $10$ repetitions.


2. **Seated Quick Flicks:** Perform $12$ explosive contractions ($1\text{-second}$ hold, immediate release) in a row.


3. **Active Pelvic Bridges:** Lie on your back, knees bent, feet flat. Lift your hips into a bridge while tensing your pelvic floor. Hold for $5$ seconds, then lower your hips and relax your pelvic floor slowly. Repeat $10$ times.



---

### Protocol 3: Moderate ED Focus (IIEF-EF: 11–16)

* **Focus:** Structural hypertrophy of the ischiocavernosus and bulbospongiosus.



```
Position: Lying supine on your back, knees bent, feet flat [cite: 27, 41, 44]
Sets per session: 3
Daily Frequency: 3 times daily [cite: 24, 27, 41]
Weekly Cadence: 5 days per week [cite: 44]

```

#### Exercise List

1. **Supine Maximal Holds:** Squeeze and lift the pelvic floor at $100\%$ maximal voluntary effort. Hold for $10$ seconds, followed by $20$ seconds of deep diaphragmatic breathing and complete pelvic release. Repeat for $12$ repetitions.


2. **Supine Quick Flicks:** Perform $15$ rapid contractions ($1\text{-second}$ squeeze, immediate release).


3. **Endothelial Walking Program:** Walk briskly for $30$ minutes daily, $5$ days a week. Aerobic exercise improves systemic nitric oxide delivery to help dilate the penile arteries.



---

### Protocol 4: Severe ED Focus (IIEF-EF: 6–10)

* **Focus:** Light somatic nerve stimulation and pelvic relaxation.



```
Position: Lying supine on your back, knees bent with a pillow under your head [cite: 24]
Sets per session: 2
Daily Frequency: 2 times daily (Morning and Evening)
Weekly Cadence: 3 days per week with rest days in between to avoid spasm [cite: 41, 44]

```

#### Exercise List

1. **Submaximal Neuromobilization Holds:** Perform a light $30\text{--}50\%$ submaximal contraction. Hold for $4$ seconds, followed by a slow, controlled $12\text{-second}$ relaxation phase. Repeat for $10$ repetitions.


2. **Diaphragmatic Perineal Release:** Spend $5$ minutes breathing deeply into your abdomen, focusing entirely on relaxing and lowering the perineal muscles.



---

### Validated Clinical Recovery Timelines & Milestone Expectations

```
[Baseline Score Recorded]
           │
           ▼
     (Weeks 1–2)  ──► Base Neural Activation: Improved muscle awareness and coordination [cite: 44].
           │
           ▼
     (Weeks 3–4)  ──► Strength & Endurance Gains: Noticeable decline in post-urination leaking [cite: 15, 44].
           │
           ▼
     (Weeks 6–8)  ──► Rigidity Progress: Noticeable improvements in erection firmness [cite: 44].
           │
           ▼
    (Weeks 8–12)  ──► Landmark Milestone: Peak muscular hypertrophy; 67% of mild-to-mod cases improve [cite: 26, 27].
           │
           ▼
     (6 Months)   ──► Long-term Resolution: 40% achieve full recovery; 34.5% show partial success [cite: 18, 34].

```

#### Landmark Trials & Success Metrics

* **The Dorey RCT Baseline (6 Months):** In the landmark randomized controlled trial evaluating $55$ men with erectile dysfunction, the active $\text{PFMT}$ cohort achieved a significant mean increase of $9.88\text{ points}$ on the IIEF erectile function domain at the $6\text{-month}$ milestone.


* **Overall Resolution Rates:** At $6\text{ months}$ of consistent practice, **$40.0\%$** of all participants achieved complete resolution of symptoms (returning to normal, unassisted erectile function), **$34.5\%$** experienced significant clinical improvement, and **$25.5\%$** showed no clinical change.


* **Why Some Do Not Respond:** Non-responders are typically patients with severe organic comorbidities—such as advanced insulin-dependent diabetes, heavy tobacco dependency, spinal nerve damage, or severe coronary artery disease. Under these conditions, the penile blood vessels and nerves are too compromised for pelvic muscle training to restore function on its own. These patients require medical or urological care alongside pelvic exercises.