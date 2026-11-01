# Part 10 Validation

Validation was performed on 2026-11-01 against the local Flask app and PostgreSQL 17 database.

## Browser and application validation

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| Required fields and browser validation | Browser | Tried submitting the join form empty after removing `novalidate` | The browser blocked submission; the form was invalid and required fields reported missing values. |
| Invalid email format | Browser | Entered `not-an-email` in the email field | The browser reported an email type mismatch and blocked submission. |
| Field lengths match the database columns | Browser | Inspected the rendered name, student ID, and email controls | `maxlength` values were 100, 20, and 255, respectively. |
| Blank name is rejected | Flask | POSTed to `/join` using curl with `name=` | HTTP 400. |
| Invalid email is rejected | Flask | POSTed to `/join` using curl with `email=not-an-email` | HTTP 400. |
| Page count must be positive | Flask | POSTed to `/join` using curl with `pages_count=0` | HTTP 400. |
| Invalid submissions do not create tickets | Flask / Database | Counted tickets before and after the three invalid requests | Count remained 1 before and 1 after. |

## Database validation

Each invalid statement was run directly in `psql`. The following are the exact PostgreSQL error messages observed:

| Rule | Constraint type | Test | PostgreSQL result |
| --- | --- | --- | --- |
| Service must exist | FOREIGN KEY | Inserted a ticket with `service_id = -999999` | `ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` |
| Ticket status must be allowed | CHECK | Updated test ticket 12 to `status = 'lost'` | `ERROR: new row for relation "tickets" violates check constraint "check_ticket_status"` |
| Service code must be unique | UNIQUE | Inserted a service using the first existing service code (`print_doc`) | `ERROR: duplicate key value violates unique constraint "services_code_key"` |
| Service name is required | NOT NULL | Inserted a service with `name = NULL` | `ERROR: null value in column "name" of relation "services" violates not-null constraint` |
| A referenced service cannot be deleted | ON DELETE RESTRICT | Deleted service 1, which was referenced by a ticket | `ERROR: update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` |

A valid temporary ticket was inserted for service 1 without specifying `ticket_number`, `status`, `paper_size`, or `is_rush`. The generated ticket had id 12 and ticket number 11. The row shown in the subsequent rejected status update confirmed the stored paper size was `letter` and rush was `false`; the attempted status change to `lost` was rejected by the CHECK constraint. The temporary ticket was then deleted with `DELETE FROM tickets WHERE id = 12`, and a follow-up `SELECT` returned zero rows.

The insert omitted `status`, so PostgreSQL applied its schema default (`waiting`).

## SQL construction check

Ran the prescribed command from the repository root:

```text
git grep -nE "f[\"'].*(SELECT|INSERT|UPDATE|DELETE)" -- "*.py"
```

Result: no matches.
