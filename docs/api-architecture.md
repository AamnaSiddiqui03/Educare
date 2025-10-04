Phase 1:

1. Suggested RESTful API Endpoints
2.1 Auth & Users
Endpoint	Method	Description
/auth/register	POST	Register a new user (role specified in payload)
/auth/login	POST	Login and return JWT token
/auth/logout	POST	Logout and invalidate session
/users/:userId
GET
Get user details (role-based response)



Phase 2:
2. Student Profile API (Phase 1)
Endpoint	Method	Description
/students/:id/profile	POST	Create student profile after registration
/students/:id/profile	GET	Fetch student profile
/students/:id/profile	PUT	Update student profile (phone, address, photo, video, help_text)
/students/:id/profile	DELETE	Delete student profile
/students/:id/profile/submit	POST	Mark Phase 1 complete (profile_completed = true)
/students/:id/profile/progress	GET	Fetch Phase 1 + Phase 2 completion status
3. Student Education API
Endpoint	Method	Description
/students/:id/education	GET	List all education entries for student
/students/:id/education	POST	Add a new education entry
/students/:id/education/:education_id	GET	Fetch specific education entry
/students/:id/education/:education_id	PUT	Update specific education entry
/students/:id/education/:education_id	DELETE	Delete specific education entry
4. AssessmentMaster API (Admin / Metadata)
Endpoint	Method	Description
/assessments	POST	Create a new test
/assessments	GET	List all tests
/assessments/:id	GET	Fetch test details
/assessments/:id	PUT	Update test info
/assessments/:id	DELETE	Delete test
5. StudentAssessment API (Phase 2)
Endpoint	Method	Description	Notes
/students/:id/assessments/available	GET	List available tests for student based on education_level and refresh interval	Backend filters tests student can currently attempt
/students/:id/assessments/:assessment_id/submit	POST	Submit answers → generate PDF → store a new row in StudentAssessment	Multiple submissions allowed; each creates a new row
/students/:id/assessments/:assessment_id/latest	GET	Fetch latest submission for a test	Only latest counts for reporting/visibility
/students/:id/assessments/:assessment_id/history	GET	Fetch all submissions for a test	Optional, for student review
/students/:id/assessments/:student_assessment_id/report	GET	Download PDF report for a submission	
6. Workflow Notes

Phase 1 (Profile Completion)

/students/:id/profile/submit → marks profile_completed = true

Phase 2 (Assessments)

/students/:id/assessments/available → shows tests eligible for attempt

/students/:id/assessments/:assessment_id/submit → stores a new submission

/students/:id/assessments/:assessment_id/latest → determines current report/score for profile visibility

Refresh logic

Backend calculates next_available_date = last_submission.submitted_at + refresh_interval_days

Only allows submission if the date has passed

This API list fully supports your flow:

Phase 1: student profile + education

Phase 2: multiple assessments per grade, weekly refresh, historical submissions stored, only latest counts

PDF reports stored per submission

If you want, I can now draw a complete visual diagram showing:
Students → Education → Assessments → Submissions + Phase tracking + API endpoints

This will make it fully dev-ready.