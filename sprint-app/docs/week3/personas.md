# Personas for sPrint (Campus Print Shop Queue Management System)

Grounded in field observation and student/operator interviews conducted at the University Student Center Copy & Document Shop.

---

## Sammy Bautista, the Person Waiting

> *"I already sent my lab report PDF to their Facebook page 20 minutes ago, but Kuya said they only open and print your file when you're physically standing right in front of the counter. The line was ten people deep, so I couldn't stay or I'd miss my quiz. I had to leave and ended up begging my blockmate to print it for me."* *(interview)*

| Attribute | Details |
| :--- | :--- |
| **Photo / Sketch** | 👩‍🎓 `[Sketch: 20-year-old student with a backpack, holding a phone in one hand and lecture notes in the other]` |
| **Age, role and background** | 20, 3rd-year Biology major; commutes 45 minutes daily; takes back-to-back lectures and laboratory classes requiring physical hardcopy submissions. |
| **Goals** | 1. Reserve her place in the printing queue after sending her document via the shop's Facebook Page or Gmail without being trapped in a physical line. *(interview)*<br>2. Track the exact number of jobs ahead so she knows if she has time to walk to her building or must stay nearby. *(observation)*<br>3. Receive a clear call notification to step up to the counter, pay, and collect her prints right before class. |
| **Frustrations** | 1. Physical line lock-in: Stepping out of line to go to the restroom or buy water forfeits your turn, forcing you to the very back of the line. *(interview)*<br>2. Wasted time standing at the counter: Having to stand in a crowded hallway just to prove physical presence while waiting for 8 other people ahead. *(observation)*<br>3. Desperation when running late: Leaving the queue in frustration to hunt for other campus print shops or pleading with friends to print on their behalf. |
| **Devices and context** | Mid-range Android smartphone on campus Wi-Fi or mobile LTE; waiting on hallway benches or walking between academic wings. |
| **Tech comfort** | **High** &mdash; Comfortable messaging shop FB pages, using Google Drive, Gmail, and GCash. |
| **Accessibility needs** | Often holding bags and notebooks; outdoor screen glare; needs large high-contrast numbers and clear visual indicators when her number is called. |

### Scenario

It is 8:10 AM. Sammy has already emailed her 6-page lab report to the print shop's Gmail. She arrives at the copy center and sees 12 students crowded in line. Instead of standing in line for 25 minutes and risking being late for her 8:30 AM class, Sammy opens **sPrint** on her phone. She enters her student ID, chooses "Document Printing (B&W)", references her file name (`Sent via Gmail: Lab_Report_Final.pdf`), checks the "Rush Order" box, and gets Ticket #14 showing "3 print jobs ahead". She walks over to a quiet bench nearby to review her lecture notes. At 8:22 AM, her screen turns green with **"📢 Please proceed to Counter 1 now!"**. She steps up to the counter, Kuya Jun opens her emailed PDF, prints it in 30 seconds, Sammy pays, and heads to class on time.

### Top tasks in the app

| Task | Screen | Requirement ID |
| :--- | :--- | :--- |
| Join the print queue with student ID, document reference, and rush priority | Join the queue | FR-01, FR-06 |
| Check live position and number of print jobs ahead | My place | FR-02 |
| Observe real-time status update from "Waiting" to "Called" without refreshing | My place | FR-03 |
| Cancel ticket if she decides to leave or ask a friend instead | My place | FR-07 |

### What this means for my interface

1. **Because** Sammy waits away from the crowded counter (on benches or in hallways), the ticket status and position count must be massive and unmistakable at a glance.
2. **Because** students send files via FB Messenger or Gmail, the form must have a clear "Document / File Reference" field so operators can instantly locate the file in their inbox.
3. **Because** she cannot constantly refresh while reviewing her notes, the status on My place must poll the server asynchronously and update automatically when she is called.

---

## Kuya Jun (Nestor) Ramos, the Staff Member

> *"Students message files to our Facebook page and Gmail all morning, but we cannot print in advance because students change their minds, leave campus, or never show up to pay. We can only print when the customer is right here to pay. But that causes everyone to crowd the counter, and if we call someone who stepped away, it creates arguments."* *(interview)*

| Attribute | Details |
| :--- | :--- |
| **Photo / Sketch** | 👨‍🔧 `[Sketch: 48-year-old print shop supervisor wearing an operator apron, standing beside an industrial copier and computer terminal]` |
| **Age, role and background** | 48, Head Print Operator & Shop Manager; 14 years managing campus copy centers; operates 4 multi-function laser printers and monitors the shop's Facebook Messenger and Gmail workstation. |
| **Goals** | 1. Print jobs only when the customer is confirmed present at the counter to guarantee payment. *(interview)*<br>2. Maintain an orderly, dispute-free queue so students who step away don't argue about lost places. *(observation)*<br>3. Quickly match the ticket with the student's message on the shop's Facebook Page/Gmail using their file reference and student ID. |
| **Frustrations** | 1. Abandoned unpaid prints: Wasting paper and toner when jobs were printed for students who disappeared. *(interview)*<br>2. Calling absent students: Shouting a name 3 times only to realize the student went to the bathroom, disrupting the queue. *(observation)*<br>3. Front-desk mobbing: Students blocking the shop entrance while waiting for their turn to be called. |
| **Devices and context** | Counter desktop PC (Windows 10, Chrome) connected to heavy-duty laser printers; shop Facebook Messenger and Gmail open in adjacent tabs; high ambient noise from printers and cutters. |
| **Tech comfort** | **Medium** &mdash; Skilled at downloading attachments, print spoolers, and POS cash registers. |
| **Accessibility needs** | Needs big, unambiguous buttons (Call Next, Serve, No-Show) that are easy to click with mouse or touch without misclicking. |

### Scenario

During the 8:00 AM rush, Kuya Jun's Facebook Messenger and Gmail tabs are flooded with student documents. Instead of letting students swarm the counter or guessing who arrived first, Kuya Jun checks the **sPrint Operator Dashboard**. He clicks **"📢 Call Next Job"**, which calls Ticket #14 (Sammy Bautista, file: `Sent via Gmail: Lab_Report_Final.pdf`). Within 30 seconds, Sammy approaches Counter 1 showing Ticket #14 on her phone. Kuya Jun opens her file in Gmail, clicks print, collects the payment, and clicks **Serve** on his dashboard. The transaction is complete, fair, and orderly.

### Top tasks in the app

| Task | Screen | Requirement ID |
| :--- | :--- | :--- |
| View active queue ordered by arrival time and rush urgency | Staff dashboard | FR-04 |
| Filter queue by service (Printing vs Binding vs Plotting) | Staff dashboard | FR-04a |
| Advance the queue with a single-click "Call Next Job" button | Staff dashboard | FR-05 |
| View document title / FB / Gmail file reference before downloading | Staff dashboard | FR-04, FR-06 |
| Mark completed jobs as "Served" or mark absent customers as "No-show" | Staff dashboard | FR-05 |

### What this means for my interface

1. **Because** Kuya Jun needs to locate the student's file in Messenger or Gmail quickly, the dashboard table must prominently display the document name/reference and student name.
2. **Because** operators must ensure the customer is present before printing, the "Call" action notifies the student to approach the counter *before* the job is printed and marked "Served".
3. **Because** students who step away may not return in time, the operator needs a quick "No-Show" button to advance to the next waiting customer without stalling the entire counter.

