# Week 3 – Self-Review: Personas and Wireframes

**Student:** [Last name, First name] | **Section:** [Section]
**App:** sPrint – Campus Print Shop Queue Management System

---

## 1. Persona Review

### What worked well

Both personas are grounded in the real campus workflow: students send their files via Facebook Messenger or Gmail and must be **physically present** to pay and receive their printout. This makes the core frustration — losing your queue position when you step away — authentic and specific rather than generic.

- **Sammy Bautista (Student)** captures the time-pressure angle well. The scenario ("I had a 10:30 class, paid the registration fee, and the line was still long — I left and came back to find myself last") is a concrete, believable event that a fellow student could immediately relate to.
- **Kuya Jun / Nestor Ramos (Staff)** focuses on the operational side: managing rush orders, avoiding verbal misunderstandings when calling out numbers, and knowing which ticket has what service type without having to re-ask the student. His "Because…, my interface must…" statements translate directly into UI requirements (service filter, Rush flag, status flow).
- Requirement IDs (FR-01 through FR-09) are linked to each top task, making traceability back to the spec straightforward.

### What could be improved

- Sammy's **tech comfort level** is described but her exact device habits (phone vs. laptop for queue registration) could be made more explicit. The wireframes assume a phone-first flow for students, but the persona itself is silent on this.
- The **pain-point quote** for Kuya Jun ("Minsan tinatawag ko na yung number, wala na sila") is authentic, but a follow-up note on *how often* this happens per day would make the frequency-of-pain more credible for a reader who isn't from the campus.

---

## 2. Wireframe Review

### Screen 1 – Join Queue Form

**What worked well**

The mobile layout stacks each input field vertically with clearly labelled form controls matching Bootstrap conventions. The required-field asterisks, the service dropdown, and the "Rush Order?" checkbox are all visible above the fold on the phone frame, which reduces scroll-before-submit friction. The desktop version moves to a two-column grid so wide screens don't leave large empty gutters — a good responsive decision.

Flow arrows from the form to the "My Ticket" screen are annotated with `→ on valid submit`, which tells a reader exactly what triggers the transition.

**Problem / What to improve**

The wireframe does not show what happens when the form is submitted with errors — there is no error-state sketch (e.g., red border + helper text under an empty required field). Adding a brief error-state annotation (even just a note on the side) would confirm that server-side validation feedback is planned.

---

### Screen 2 – My Place / Ticket

**What worked well**

The large ticket number is immediately the most prominent element on both the phone and desktop frames — good visual hierarchy. The "ahead of you" sentence and the status badge (Waiting / Serving / Done) are present on both views, satisfying the live-feedback requirement (FR-04). The "Leave Queue" button is below the status area, keeping the destructive action separated from the information.

Persona label "→ Sammy's view" is annotated on the phone frame, which helps a reviewer quickly map which persona uses this screen.

**Problem / What to improve**

The status badge is shown as a coloured pill only. Colour alone is not accessible — a screen reader user or someone with colour-vision deficiency would miss the meaning. The badge should also contain a text label ("Waiting", "Now Serving", "Done") inside it, not just a colour fill. A short annotation on the wireframe to that effect would make this an explicit design decision rather than an oversight.

---

### Screen 3 – Staff Dashboard

**What worked well**

The staff table columns (Ticket #, Name, Service, Pages, Rush, Status, Action) are all present in both the phone card-list view and the desktop table view. The Rush column uses a ★ icon as a quick visual scan aid, matching FR-06. The "Call Next" button at the top and the per-row "Mark Done" / "Skip" buttons are clearly separated in the layout.

The service-filter dropdown at the top of the page is shown in the desktop wireframe, satisfying FR-07 (filter by service type).

**Problem / What to improve**

The per-row action buttons ("Mark Done", "Skip") share the same visual label for every row. Without an `aria-label` that includes the ticket number (e.g., `aria-label="Mark Done – Ticket 014"`), assistive technology would announce each button identically, making keyboard navigation confusing. This should be flagged as a required implementation detail in Part 7.

---

## 3. Summary

| Area | Rating (1–5) | Notes |
|---|---|---|
| Persona authenticity | 4 | Real scenario and quotes; frequency data could be stronger |
| Persona–requirement traceability | 5 | FR IDs present on every top task |
| Wireframe coverage | 5 | All three screens, both breakpoints |
| Wireframe responsive logic | 4 | Column layout decisions are clear; error state missing |
| Accessibility annotations | 3 | Status badge colour-only and aria-label gap flagged |

**Overall:** The design artefacts are solid and ready to guide implementation. The two accessibility gaps (colour-only badge, missing `aria-label` on action buttons) are known issues with clear fixes planned for Parts 6 and 7.
