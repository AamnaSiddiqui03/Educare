Database Tables
Phase 1:
2.1 Users
Column	Type	Description
id	UUID	Primary Key
name	String	User name
email	String	Email / login
password_hash	String	Password hash
role	Enum	student / donor / mentor
verified	Boolean	True if donor/mentor verified
created_at	Timestamp	Registration 


Phase 2:
2.2 Students

Students Table (Final)
Column	Type	Description
student_id	UUID	Primary Key
user_id	UUID	FK to Users table
phone	String	Student phone number
address	Text	Student address
photo_url	String	Profile photo
video_url	String	Optional video introduction
help_text	Text	Text describing kind of help student is seeking
profile_completed	Boolean	True when phase 1 is completed
assessment_completed	Boolean	True when assessment submitted
created_at	Timestamp	Registration date
updated_at	Timestamp	Last updated date



StudentEducation Table

Allows multiple educational entries per student.

Column	Type	Description
education_id	UUID	Primary Key
student_id	UUID	FK to Students table
institution_name	String	School / University name
education_level	Enum	Class 10 / Class 12 / Undergraduate / etc.
year_of_passing	Integer	Year completed
marks_obtained	Float	Marks/percentage (optional for now)
report_card_url	String	Upload link (v3 feature)
created_at	Timestamp	Entry creation date
updated_at	Timestamp	Last update date


Updated StudentAssessment Table
Column	Type	Description
student_assessment_id	UUID	Primary Key
student_id	UUID	FK to Students table
assessment_id	UUID	FK to AssessmentMaster table
score	Float	Optional numeric score
report_pdf_url	String	Link to generated PDF report
submitted_at	Timestamp	Submission timestamp

Logic:

A student can have multiple rows for the same assessment_id.

To get the current/latest submission for a test:

SELECT * 
FROM StudentAssessment
WHERE student_id = :student_id AND assessment_id = :assessment_id
ORDER BY submitted_at DESC
LIMIT 1;

API Adjustments
Endpoint	Method	Description	Notes
/students/:id/assessments/:assessment_id/submit	POST	Submit test → generate PDF → create new row	No overwrite; backend stores multiple submissions
/students/:id/assessments/:assessment_id/latest	GET	Fetch latest submission for a test	Used for profile score/visibility
/students/:id/assessments/:assessment_id/history	GET	Fetch all past submissions	Optional for student review
Test Refresh Logic

You can add a column in AssessmentMaster:

Column	Type	Description
refresh_interval_days	Integer	After how many days the test becomes available again for reattempt

Backend can calculate availability:

last_submission = get_last_submission(student_id, assessment_id)
if today - last_submission.submitted_at >= refresh_interval_days:
    allow_test = True
else:
    allow_test = False


Frontend shows “Reattempt available in X days” if test is not yet refreshed.

This way you keep historical data, support weekly refresh, and only latest submission counts for assessment completion or reporting.