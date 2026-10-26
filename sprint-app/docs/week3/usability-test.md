# Week 3 – Usability Test

**Student:** Gabor, Sean Jric | **Section:** CS3B
**App:** sPrint – Campus Print Shop Queue Management System
**Test Date:** October 24, 2026, 7:37 PM

---

## 10a. Test with a Real User

**Test participant:** Montejo, Carla - 2nd year BA Sociology student
**Matches persona:** Sammy Bautista (person waiting)
**Testing method:** In-person

### Task 1: Join the Queue

**Task:** "You just arrived. Get in line for Document Printing (B&W)."

**Did they finish it?** Yes

**Time taken:** Under 1 minute

**What happened:**
- Participant executed the task smoothly and quickly
- Got confused about the "Document / File Reference" field - wasn't sure what it was for (filename)
- Got confused about the "Number of pages" field - expected that when he ticked "All" option, he wouldn't have to type the number of pages

**Persona rule check:**
- ✅ Rule held up: Large ticket number and position must be the biggest thing on My place (Task 2 confirmed this)
- ❌ Rule not held up: Because students may be using mobile and need clarity, the filename field label/placeholder wasn't clear enough

---

### Task 2: Check Position

**Task:** "How many people are ahead of you? What is your number?"

**Did they finish it?** Yes

**Time taken:** ~3 seconds

**What happened:**
- Immediately knew his number was #7
- Immediately saw there were 3 people ahead of him
- Information was apparent in the interface, very quick to read
- Got confused about the current queue at the bottom of the home page showing people who are already served - thought they were still in line

**Persona rule check:**
- ✅ Rule held up: Ticket number and position must be massive and unmistakable at a glance (confirmed - he found it instantly)
- ❌ Rule not held up: Because students need accurate information, showing served tickets in the queue list is confusing

---

### Task 3: Staff Actions

**Task:** "Pretend you are the staff member. Call the next person and mark them as served."

**Did they finish it?** Yes (with little help)

**Time taken:** Under 30 seconds

**What happened:**
- Needed a little help - had to tell him to scroll the table horizontally to find the action buttons in phone view
- Once he knew to scroll, he completed the task quickly

**Persona rule check:**
- ✅ Rule held up: Big unambiguous buttons that are easy to click (buttons were easy to use once found)
- ❌ Rule not held up: Because operators work on a shared PC with possible small screens, horizontal scroll wasn't obvious on mobile view

---

## 10b. Improvement Made

**Most serious problem found:**
The "Pages" field UX is confusing - when a user selects "All" radio button, they still have to manually type the number of pages. This is unintuitive - if you select "All", the system should automatically count or the field should be disabled/not required. Also, the home page queue list showed served tickets which was confusing.

**Fix applied:**
1. Added clear placeholders to all form fields (name, student ID, email, document, pages)
2. Added helper text to clarify that page count is needed even when printing "All"
3. Added JavaScript to disable the unused pages input field based on radio selection
4. Fixed home page to only show waiting and called tickets (not served/no-show)

**Before screenshot:** ![Before improvement](docs/week3/usability-test-photos/before.png)
**After screenshot:** ![After improvement](docs/week3/usability-test-photos/after.png)

---

## Notes

**Permission obtained for recording:** N/A (not recorded) Documentaion only: [usability-test-carla](docs/week3/usability-test-photos/usability-test-carla.jpeg)
**Other observations:**
- The filename field confusion suggests the label or placeholder needs to be clearer about what information to enter
- Horizontal scroll on staff dashboard table on mobile was not obvious - could add a visual indicator or improve the responsive layout
