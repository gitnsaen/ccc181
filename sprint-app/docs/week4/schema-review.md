# Schema Self-Review: sPrint Database Design

**Reviewer:** Sean Jric B. Gabor  
**Date:** Week 4  
**Scope:** Evaluation of the `services`, `operators`, and `tickets` tables against CCC181 data persistence principles and real campus print shop operations.

---

## 1. Core Design Evaluation

### 1. Coverage
Looking back at our functional requirements, every single feature that needs data persistence; "*Stores data? = Yes*" (`FR-01` through `FR-05`, `FR-07` through `FR-12`, and `FR-14`) maps cleanly to specific columns across `services`, `operators`, and `tickets`. 

More importantly, the schema directly supports how people actually interact with the shop:
* **For students like Sammy:** Fields like `sent_via` and `doc_name` handle document tracking, `is_rush` flags urgent submissions before class, and `paper_size` with `pages_range` ensure exact print specifications are captured right at entry.
* **For operators like Kuya Jun:** Status tracking (`status`), operational timestamps (`called_at`, `served_at`), service filters (`service_id`), and staff tags (`operator_id`) provide the clear counter control needed to manage rush-hour chaos without losing track of who called which job.

There are no orphan columns; every field serves either an explicit feature or a necessary auditing need.

### 2. One fact in one place
We isolated service details (`name`, `code`, `is_active`) in `services` and staff information in `operators`. The `tickets` table only holds foreign key references (`service_id`, `operator_id`). This keeps our data cleanly in 3NF, if a service name changes or an operator updates their role, we update it in exactly one place without duplicating facts or risking inconsistent ticket records.

### 3. Facts, not results
One of the most tempting traps during initial design was adding a `position` or `people_ahead` column directly to the `tickets` table. However, queue position isn't a static fact but a dynamic state. 

If a student leaves the queue or gets called, every subsequent ticket's position changes. Storing position in a column would force us to run batch updates across dozens of rows continuously, creating severe race conditions. Instead, we calculate queue position on the fly using a SQL `COUNT(*)` query over active tickets with earlier sequence numbers.

### 4. Bad data
We can't rely solely on Flask or client-side JavaScript for validation because API requests can be bypassed or misconfigured. To keep the database clean, we built defensive constraints directly into PostgreSQL:
* `CHECK (pages > 0)` prevents invalid or zero-page print jobs.
* `CHECK (sent_via IN ('gmail', 'fb'))` enforces supported submission channels.
* `CHECK (print_type IN ('bw', 'color'))` and `CHECK (paper_size IN ('letter', 'a4', 'legal'))` lock down printing modes to actual shop inventory.
* `CHECK (status IN ('waiting', 'called', 'served', 'no-show', 'unreadable'))` protects the ticket lifecycle state machine.
* `UNIQUE` constraints on `services.name` and `services.code` prevent duplicate service entries on the staff dashboard.

### 5. Deletes
* **`services` $\rightarrow$ `tickets` (`ON DELETE RESTRICT`):** We must never allow a service row to be deleted if existing tickets reference it. Deleting a service would erase historical context required for end-of-day sales auditing.
* **`operators` $\rightarrow$ `tickets` (`ON DELETE SET NULL`):** If a student assistant leaves or an operator account is removed, past ticket logs remain intact for revenue reports, with the operator reference gracefully set to `NULL`.

### 6. Types
All event timestamps (`created_at`, `called_at`, `served_at`) use `TIMESTAMPTZ` (UTC with timezone offsets). This ensures time calculations remain reliable even across server restarts or container environment shifts. `student_id` uses `VARCHAR(20)` to preserve dashes and leading zeros (like `2023-14022`), and `doc_name` uses `TEXT` so long filenames aren't arbitrarily cut off.

---

## 2. Key Design Decisions & Iterations

### Finding 1: Dynamic Queue Calculation vs. Stored Positions
> **Works well:** Calculating queue position dynamically via `COUNT(*)` rather than storing a hardcoded `position` integer. When a student cancels their ticket or gets called to the counter, the rest of the queue automatically advances without requiring batch `UPDATE` queries across multiple rows.  
> **Could be better:** Running `COUNT(*)` every time a client polls for updates could slow down response times if the table accumulates thousands of historical tickets over time.  
> **What I changed:** We kept the dynamic query to honor the "store facts, not results" rule, but restricted the filter to `status = 'waiting'` and `ticket_number < current`. In an upcoming sprint, we will add a composite index on `(status, ticket_number)` to ensure polling queries remain under our target performance threshold.

---

### Finding 2: Database Constraints vs. Schema Flexibility
> **Works well:** Adding explicit `CHECK` constraints directly at the database level guarantees that malformed data gets rejected even if client-side validation is bypassed.  
> **Could be better:** Hardcoding allowed submission channels (`'gmail'`, `'fb'`) or paper sizes (`'letter'`, `'a4'`, `'legal'`) into `CHECK` constraints means that adding new options (like Google Drive links or A3 paper) will require an explicit `ALTER TABLE` migration.  
> **What I changed:** We decided to keep the strict `CHECK` constraints for our initial release. Because the shop currently only processes files via Gmail and Facebook Messenger, enforcing tight rules at the schema level gives us a clean, trustworthy dataset while we establish the core platform.

---

### Finding 3: Handling Retired Services Gracefully
> **Works well:** Enforcing `ON DELETE RESTRICT` on `service_id` prevents accidental deletion of active service types that would otherwise break past ticket records.  
> **Could be better:** If Kuya Jun temporarily stops offering binding due to broken equipment, trying to delete that service row would trigger a database error due to historical references.  
> **What I changed:** We introduced an `is_active BOOLEAN NOT NULL DEFAULT TRUE` flag to the `services` table. When equipment is down or supplies run out, operators toggle `is_active = FALSE`. This hides the option from the student submission form while preserving all past transaction history.

---

### Finding 4: Integrating Real User Feedback
> **Works well:** Reviewing the schema against actual campus print shop workflows highlighted missing options early, such as explicitly tracking paper sizes (Letter, A4, Legal) and adding an `'unreadable'` status for corrupted file attachments.  
> **Could be better:** Our earlier in-memory prototype lacked these fields, meaning initial test fixtures had to be updated to match the new PostgreSQL structure.  
> **What I changed:** We updated the schema and seed scripts to include `paper_size` with a default of `'letter'`. This keeps things simple for standard submissions while providing complete flexibility for customized print jobs.

---

## 3. Overall Reflection

Moving from a basic in-memory Python dictionary to a structured PostgreSQL database forced me to think carefully about the real-world operational realities of a campus copy shop. Designing defensively at the database level, using constraints, explicit foreign key rules, soft-delete flags, and dynamic queries guarantees that `sPrint` can handle edge cases smoothly without corrupting data or breaking queue logic during peak hours. The resulting schema provides a solid, 3NF-compliant foundation ready for production deployment.