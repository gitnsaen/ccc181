# Proposed Application: sPrint (Campus Print Shop Queue Management System)

| | |
|---|---|
| **Student name** | [Last name, First name] |
| **Section** | [Section, e.g., IT-3A / CCC181] |
| **GitHub username** | gitnsaen |
| **Date submitted** | 2026-10-21 |

---

## 1. Problem Statement

### 1.1 Background

At our university copy center and print shops, students no longer use USB flash drives; instead, they send document files via the shop's Facebook Messenger page or Gmail account. However, print shop operators strictly enforce a policy that documents are only downloaded and printed when the student is **physically present at the counter**, ensuring payment before paper and toner are consumed. During peak hours (7:30 AM – 9:30 AM and 11:30 AM – 1:30 PM), this creates severe physical queues. Students are forced to wait in line for 20–30 minutes just to claim their prints. Stepping away for even a few minutes means losing one's spot and being sent to the back of the line, forcing students to either risk missing classes, hunt for other shops, or beg friends to print on their behalf.

### 1.2 Evidence from research

| Method | Who / where | Key finding |
|---|---|---|
| Interview | 3rd-year Biology student rushing to 8:30 AM quiz | Stated: *"I already sent my lab report PDF to their Facebook page 20 minutes ago, but Kuya said they only open and print your file when you're physically standing right in front of the counter. The line was ten people deep, so I couldn't stay or I'd miss my quiz. I had to leave and ended up begging my blockmate to print it for me."* |
| Interview | Senior Print Shop Operator (14 yrs managing campus copy center) | Stated: *"Students message files to our Facebook page and Gmail all morning, but we cannot print in advance because students change their minds, leave campus, or never show up to pay. We can only print when the customer is right here to pay. But that causes everyone to crowd the counter, and if we call someone who stepped away, it creates arguments."* |
| Observation | Student Center Copy Shop, Monday 7:45–8:45 AM | Observed 14 students crowded in a narrow hallway line. Two students stepped out to buy water and returned to find their turns skipped, resulting in a dispute with the operator and having to re-queue at the back. |
| Document review | Print Shop Daily Manual Logbook & FB Chat Inbox | The shop receives over 120 document messages via FB Messenger and Gmail between 7:30 AM and 11:00 AM. 10–15% of senders never claim their prints, explaining the shop's strict policy against printing before physical confirmation. |

### 1.3 Point-of-view (POV) statement

**College students with tight class schedules** need **a transparent queueing and notification system that holds their place while waiting remotely** because **the current policy requiring physical counter presence forces them to stand in crowded lines or lose their spot if they step away, leading to missed class deadlines and abandoned print requests.**

### 1.4 "How might we…?" question

**How might we** digitize queue registration and provide real-time queue position tracking so that students can wait anywhere on campus and approach the counter only when called, allowing operators to print on demand with guaranteed customer presence and payment?

### 1.5 Self-check

- [x] Names a real user group
- [x] States a need, not a feature
- [x] Rests on an insight from research
- [x] Is narrow enough to act on and open enough to allow different ideas

---

## 2. Target-User Profile

### 2.1 Primary persona

| | |
|---|---|
| **Name, age** | Mikaela "Mika" Santos, 20 (Fictional composite grounded in student interviews) |
| **Role / background** | 3rd-year Biology undergraduate; commutes daily; carries heavy course materials and takes back-to-back laboratory courses requiring physical paper submissions. |
| **Goals** | 1. Reserve her place in the printing queue after sending her document via the shop's Facebook Page or Gmail without being trapped in a physical line.<br>2. Track the exact number of jobs ahead so she knows if she has time to walk to her building or must stay nearby.<br>3. Receive a clear call notification to step up to the counter, pay, and collect her prints right before class. |
| **Frustrations / pain points** | 1. Physical line lock-in: Stepping out of line to go to the restroom or buy water forfeits your turn, forcing you to the very back of the line.<br>2. Wasted time standing at the counter: Having to stand in a crowded hallway just to prove physical presence while waiting for 8 other people ahead.<br>3. Desperation when running late: Leaving the queue in frustration to hunt for other campus print shops or pleading with friends to print on their behalf. |
| **Context of use** | Android smartphone on campus Wi-Fi or mobile LTE; waiting on hallway benches or walking between academic wings. |
| **Accessibility considerations** | Often holding bags and notebooks; outdoor screen glare; needs large high-contrast numbers and clear visual indicators when her number is called. |
| **Current workaround** | Sending files early and standing in line for 30 minutes, or skipping the queue and frantically asking a classmate to print it for them. |

### 2.2 User groups and stakeholders

| Group | Who | Relationship to the app |
|---|---|---|
| Primary users | Enrolled university students and campus faculty | Uses the app to join the print queue, provide their file reference (FB/Gmail), and track their real-time queue position. |
| Secondary users | Campus copy center operators and print technicians | Uses the staff dashboard to monitor incoming print jobs, filter by service, call next, and mark orders served. |
| Stakeholders | Campus Auxiliary Services / Copy Shop Management | Evaluates customer throughput, reduced hallway congestion, payment collection rate, and toner/paper efficiency. |

### 2.3 Organizational needs

- **Payment Security & Waste Prevention:** The shop must continue its policy of only printing once the student is verified present at the counter to prevent unpaid toner and paper waste.
- **Data Privacy Compliance (RA 10173 - Data Privacy Act of 2012):** Student identification numbers, email addresses, and document titles must only be retained for queue processing and must not be publicly broadcast on public boards.
- **Dispute Resolution:** Digital queue numbers prevent line-cutting accusations and provide objective proof of arrival order.

---

## 3. Proposed Application

### 3.1 Concept

**sPrint** is a campus print shop queue management web application designed to eliminate physical line congestion. After messaging their file to the shop's Facebook Page or Gmail, students open **sPrint** on their phone or laptop, select their print service, enter their document reference (e.g., *"Sent via Gmail: Lab_Report_Bio.pdf"*), and receive a digital queue ticket. A dynamic "My Place" tracking screen displays their ticket number, live status (Waiting, Called, Served), and the exact count of jobs ahead. When their number is called ("Please proceed to Counter 1!"), the student steps up to the desk, the operator downloads the file, prints it immediately, collects payment, and hands it over.

### 3.2 Value proposition

For **university students with urgent class deadlines**, **sPrint** is a **campus print queue management system** that **provides digital queue registration and real-time position tracking**. Unlike **physical counter lines and forfeited queue spots**, it **allows students to wait anywhere on campus without losing their place in line, ensuring they approach the counter only when called to pay and print.**

### 3.3 Value Proposition Canvas

| User side | Product side |
|---|---|
| **Jobs:** Print assignments before class; track waiting time; pick up documents without losing queue position. | **Features:** Mobile join form with file reference (FB/Gmail); live ticket status tracker with ahead count; 1-click operator queue dashboard. |
| **Pains:** Trapped standing in crowded hallway lines; losing one's place if stepping away; anxiety over missing class deadlines. | **Pain relievers:** Remote queue registration; ability to wait anywhere on campus; clear "Called to Counter" alert. |
| **Gains:** Peace of mind; freedom to study while waiting; punctual class arrivals; smooth, stress-free document collection. | **Gain creators:** Real-time auto-updating queue position; urgent Rush Order indicator; clear visual notification when called to the counter. |

### 3.4 Existing applications (from your application analysis)

| Existing app | What it does well | Where it falls short | How your app differs |
|---|---|---|---|
| **Waitwhile / Qless** | Robust enterprise virtual queuing and SMS alerts. | Overly complex; requires paid subscriptions, cellular SMS fees, and heavy onboarding. | Tailored specifically for campus print shops with print-specific metadata (page counts, B&W/color, binding) and lightweight student web access. |
| **Google Forms + Spreadsheet** | Easy to collect student document submissions. | No real-time position tracking, no automated queue advancement, and static manual refresh. | Provides dedicated live-updating "My Place" tickets, status transitions (Waiting &rarr; Called &rarr; Served), and operator-friendly controls. |
| **Physical Paper Ticket Dispenser** | Simple and familiar to walk-in customers. | Requires physical presence at the counter; zero visibility into jobs ahead or job type complexity. | Digital queueing allows students to wait safely anywhere on campus while tracking exact jobs ahead on their mobile devices. |

### 3.5 Technology choice

**Options considered:**
- **Option A:** Progressive Web App (PWA) built with Flask, Jinja2, Bootstrap 5, and vanilla JavaScript.
- **Option B:** Native Mobile App (Flutter or Android Kotlin) with Firebase backend.
- **Option C:** Single Page Application (React / Next.js) with Node.js / Express REST API.

**Weighted decision matrix** (scores 1–5, higher is better):

| Option | Solves the problem ×3 | Team skills ×2 | Cost ×2 | Privacy ×2 | Time to MVP ×1 | Total /50 |
|---|---|---|---|---|---|---|
| **Option A (Flask + Bootstrap PWA)** | 5 &times; 3 = 15 | 5 &times; 2 = 10 | 5 &times; 2 = 10 | 4 &times; 2 = 8 | 5 &times; 1 = 5 | **48 / 50** |
| **Option B (Native Mobile App)** | 4 &times; 3 = 12 | 3 &times; 2 = 6 | 4 &times; 2 = 8 | 4 &times; 2 = 8 | 3 &times; 1 = 3 | **37 / 50** |
| **Option C (React SPA + Node)** | 4 &times; 3 = 12 | 3 &times; 2 = 6 | 4 &times; 2 = 8 | 4 &times; 2 = 8 | 3 &times; 1 = 3 | **37 / 50** |

**Chosen technology and rationale:**
Option A (Flask + Bootstrap 5 + Jinja2) is selected. It delivers immediate zero-install access via any mobile or desktop web browser, achieves fast load times on spotty campus Wi-Fi, matches the course learning progression (expanding into PostgreSQL in Week 4 and REST API in Week 6), and allows rapid iteration of accessible, responsive layouts.

---

## 4. Preliminary Requirements

### 4.1 Functional requirements (user stories)

| ID | User story | Priority (MoSCoW) |
|---|---|---|
| **FR-01** | As a student, I want to submit my document specifications and file reference (FB/Gmail) online so that I get a queue ticket without standing at the counter. | Must |
| **FR-02** | As a student, I want to view my ticket number, current status, and the number of jobs ahead so that I know exactly when to walk to the print counter. | Must |
| **FR-03** | As a student, I want my ticket status to update automatically on my screen without refreshing so that I see immediately when my order is called. | Should |
| **FR-04** | As a print operator, I want to view active queue orders in order and filter them by service type so that I can manage print machinery efficiently. | Must |
| **FR-05** | As a print operator, I want to call, complete (serve), or dismiss (no-show) orders with single-click actions so that order turnaround remains fast. | Must |
| **FR-06** | As a student with an urgent class deadline, I want to flag my order as a Rush Order (★) so that operators can process urgent handouts at the express counter. | Should |
| **FR-07** | As a student, I want to cancel my ticket and leave the queue if my plans change so that I do not hold up the line for others. | Could |

### 4.2 Non-functional requirements

| ID | Category | Requirement |
|---|---|---|
| **NFR-01** | Performance | Ticket status polling response time must be under 500 ms, with live UI updates reflecting on screen within 10 seconds of operator action. |
| **NFR-02** | Usability & Responsiveness | The interface must be fully operable at a 375 px mobile screen width without horizontal window scrolling, and all interactive buttons must have a minimum touch target of 44 &times; 44 px. |
| **NFR-03** | Security / Privacy | System must comply with RA 10173 (Data Privacy Act of 2012). Student contact emails and ID numbers must not be exposed on public customer-facing screens. |
| **NFR-04** | Accessibility | All form fields must feature explicit associated `<label>` tags, status changes must be announced to assistive tech via `aria-live`, and the system must achieve a Lighthouse Accessibility score &ge; 90. |

### 4.3 MoSCoW summary

- **Must have:** FR-01 (Join queue form with validation), FR-02 (Live ticket position tracking), FR-04 (Operator queue view with service filter), FR-05 (Operator 1-click status transitions).
- **Should have:** FR-03 (Automated background status polling), FR-06 (Rush Order priority tagging ★).
- **Could have:** FR-07 (Student voluntary queue exit).
- **Won't have (this time):** Direct file upload and cloud PDF conversion; integrated payment gateway (GCash / Maya); automated SMS notifications.

---

## 5. Minimum Viable Product (MVP)

### 5.1 MVP features

1. **Digital Join Queue Form:** Responsive submission form collecting student name, email, student ID, service category, document/file reference (FB/Gmail), pages, and color preference with full server-side validation.
2. **My Place Ticket View:** Live screen displaying large ticket number, dynamic status badge, exact count of jobs ahead, and order specification summary.
3. **Staff Operator Dashboard:** Real-time table of active orders with service filter tabs, rush order indicator badges (★), and 1-click POST actions (Call Next, Serve, No-show).

### 5.2 Out of scope

- **Online Payment Integration:** Payment will be handled at the physical counter via cash or student card during the MVP phase.
- **Direct File Storage & Cloud Spooling:** Students register their document name and specifications digitally; file transfer happens via direct campus portal link or counter workstation.
- **SMS Gateway Alerts:** Notifications rely on web-based live status updates and polling rather than paid cellular SMS APIs.

### 5.3 Constraints and assumptions

- **Constraints:** One-semester development timeframe; individual student development; deployment on local Flask server transitioning to PostgreSQL and Flutter in subsequent weeks.
- **Assumptions:** Students possess a smartphone or laptop with access to campus Wi-Fi or mobile data; operators possess a counter desktop PC or tablet with a modern web browser.

### 5.4 Feasibility check (TELOS)

| Dimension | Key question | Your assessment |
|---|---|---|
| **Technical** | Can I build it with my skills and tools? | **High:** Flask, Jinja2, Bootstrap 5, and JavaScript fetch are standard, robust tools directly aligned with CCC181 skills. |
| **Economic** | Do the benefits justify the costs? | **High:** Uses open-source software and free hosting tiers; reduces wasted paper from unclaimed prints and increases copy shop throughput. |
| **Legal** | Does it comply with law and policy (e.g., RA 10173)? | **High:** Complies with RA 10173 by avoiding public exposure of private student contact details and keeping in-memory session data localized. |
| **Operational** | Will people use it, and can it be run? | **High:** Solves a documented daily pain point for both students and copy shop operators with zero client installation required. |
| **Schedule** | Can I deliver the MVP this semester? | **High:** Clear modular progression from Week 3 (UI prototype) through Week 4 (Database), Week 6 (API), and Week 8 (Flutter). |

**Verdict:** **Feasible.** The project scope is well-bounded, addresses a high-friction campus problem with proven technology, and directly satisfies all course milestones.

---

## Submission Checklist

- [x] File saved as `docs/week1/README.md` in my CCC181 repository
- [x] All `[bracketed placeholders]` replaced (fill student name and section upon submission)
- [x] Sections 1–5 complete
- [x] Aligned with Week 3 sPrint requirements and personas
