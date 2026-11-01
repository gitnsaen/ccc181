# sPrint Requirements

**Setting:** University Student Center Copy & Document Shop (Ground floor, Student Activity Building; weekday rush hours 7:30 AM – 11:30 AM).  
**People who wait:** [Sammy Bautista](week3/personas.md#sammy-bautista-the-person-waiting) (3rd-year Biology student commuting with tight class transitions who needs hardcopy lab submissions).  
**People who serve:** [Kuya Jun (Nestor) Ramos](week3/personas.md#kuya-jun-nestor-ramos-the-staff-member) (Head print operator managing 4 multi-function copiers, counter queues, and Gmail/Facebook Messenger file channels).

**Problem statement:** A student who emails their document to the campus copy shop needs a way to join the printing queue and track their place remotely because stepping out of a physical line forfeits their turn, while operators need to ensure students are present at the single service counter before printing to prevent abandoned, unpaid paper waste.

---

## 1. Functional Requirements

| ID | Requirement | Priority | Stores data? | Status |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | A student can join the print queue by entering their name, student email, university student ID, and selecting a print service. | Must | **Yes** | Built (Week 3) |
| **FR-02 ★** | A student can provide their digital document reference (file name and submission channel: Gmail or Facebook Messenger) so staff can find the file quickly. | Must | **Yes** | Built (Week 3) |
| **FR-03 ★** | A student can specify print options, including page scope (all pages count vs specific page ranges), color mode (B&W or Color), and paper size (Letter, A4, Legal). | Must | **Yes** | Built (Week 3) |
| **FR-04 ★** | A student can flag a job as a "Rush Order" for urgent classroom deadline priority. | Should | **Yes** | Built (Week 3) |
| **FR-05** | A student can view their ticket page ("My place") showing their ticket number, status (Waiting, Called, Served, No-Show), and the count of jobs ahead of them. | Must | **Yes** | Built (Week 3) |
| **FR-06** | A student can see real-time updates of their ticket status and position count without reloading the page. | Must | No | Built (Week 3) |
| **FR-07** | A student can cancel their ticket and leave the queue before being called. | Must | **Yes** | Built (Week 3) |
| **FR-08** | An operator can view a staff dashboard displaying all active queue tickets ordered by arrival time with rush tags and document references clearly visible. | Must | **Yes** | Built (Week 3) |
| **FR-09** | An operator can filter the queue dashboard by specific service type (Document Printing, Binding, Plotting, Scanning). | Should | **Yes** | Built (Week 3) |
| **FR-10** | An operator can call the next waiting ticket for a service to the counter. | Must | **Yes** | Built (Week 3) |
| **FR-11** | An operator can mark a called ticket as served upon payment or as a no-show if absent. | Must | **Yes** | Built (Week 3) |
| **FR-12 ★** | An operator can flag a customer's document reference as "Unreadable" or "Missing File", notifying the student to re-send. | Should | **Yes** | Later |
| **FR-13 ★** | A student can receive an audio chime and phone vibration alert when their ticket status changes to "Called", allowing them to wait without staring at their screen. | Should | No | Later |
| **FR-14** | An operator can manage services by adding, renaming, or deactivating a service when equipment or supplies are temporarily unavailable. | Must | **Yes** | Built (Week 4) |
| **FR-15 ★** | A student can see an estimated wait time and estimated print cost calculated from their page count and color rate. | Could | No | Later |

> **★** indicates requirements specific to the campus copy center setting (document channel references, custom print parameters, rush priority tags, unreadable file flags, and mobile call alerts).

---

## 2. Non-Functional Requirements

| ID | Requirement | Category | Priority |
| :--- | :--- | :--- | :--- |
| **NFR-01** | No ticket data, customer information, or queue status is lost when the Flask web server or the PostgreSQL Docker container restarts. | Reliability | Must |
| **NFR-02** | Concurrency control ensures two students submitting simultaneously receive distinct, monotonically increasing ticket numbers without race conditions. | Data integrity | Must |
| **NFR-03** | Ticket status polling endpoint (`/queue/<ticket_id>/status.json`) responds in under 300 ms over campus mobile LTE or campus Wi-Fi connections. | Performance | Should |
| **NFR-04** | All public student and staff pages maintain a Google Lighthouse accessibility score of 90 or higher, with high-contrast text and status colors (yellow/orange for waiting, green for called, red for no-show) readable in bright outdoor glare. | Accessibility | Must |
| **NFR-05** | Database credentials, database passwords, and session secrets are loaded via environment variables (`.env`) and are never committed to version control. | Security | Must |

---

## 3. Scope & Planning

### Minimum Viable Product (MVP)
The MVP consists of **FR-01, FR-02, FR-03, FR-05, FR-06, FR-07, FR-08, FR-10, FR-11, FR-14** together with all **Must** non-functional requirements (**NFR-01, NFR-02, NFR-04, NFR-05**).  
This forms the smallest viable loop: students join the queue with their document references, track their place live, operators call and process jobs sequentially from a persisted database at the counter, and no data is lost during unexpected server restarts.

### Out of Scope (This Semester)
1. **Direct In-Browser File Upload & Cloud Storage:** Handling large PDF uploads and cloud object storage (e.g. AWS S3) introduces server disk quotas and privacy liabilities for student documents. Students will continue using the print shop's official Gmail inbox and Facebook Messenger page, referencing file names in sPrint.
2. **Integrated Online E-Wallet Payment Gateway:** Integrating direct GCash or Maya payment APIs requires third-party merchant accounts and sandbox credentials. In-person payment (cash or shop QR code) upon document inspection at the counter remains the standard operating procedure.
3. **Native OS Push Notification Services:** Background push notifications when the browser tab is fully closed require service workers, push servers, and HTTPS VAPID credentials. For this semester, client-side vibration and audio chimes via the Web Vibration / Audio API while the tab is open satisfy the notification need.

---

## 4. User Validation & Feedback

The requirements were checked with a student who regularly waits in line at the campus print shop:

| Who (role only) | What they said | What I changed |
| :--- | :--- | :--- |
| College Student (Regular campus print shop customer) | 1. **Needs call notification:** *"Mag tutok rami sa app otherwise; need notification or vibration when called so I can browse TikTok or review while waiting."*<br>2. **Setting adjustments:** Clarified that the shop has only a single counter window. Suggested showing estimated wait times, page rates (B&W vs color price), paper sizes (A4 vs Letter), and an option for staff to flag unreadable files.<br>3. **Clear status coloring:** Recommended high-contrast color badges (green for called, orange for waiting, red for no-show) similar to familiar university student portals.<br>4. **Top 3 features:** Live queue tracking, phone vibration/alert when called, and the ability to cancel if running late. | 1. **Removed multi-counter assignment** (previously FR-11) because the physical shop operates through a single counter window.<br>2. **Added FR-03 paper sizes** (Letter, A4, Legal) to print options.<br>3. **Added FR-12 ★ (Unreadable file flag)** so operators can signal students if an emailed file fails to open.<br>4. **Added FR-13 ★ (Audio chime & vibration alert on call)** to solve the problem of students having to stare at their phones.<br>5. **Added FR-15 ★ (Estimated wait time & price calculation)** as a future enhancement.<br>6. **Enhanced NFR-04** to mandate high-contrast status colors (green/yellow/red). |
