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


StudentAssessment Table

Stores PDF report only (no JSON needed for now).

Column	Type	Description
assessment_id	UUID	Primary Key
student_id	UUID	FK to Students table
report_pdf_url	String	Link to generated PDF assessment report
submitted_at	Timestamp	Assessment submission timestamp