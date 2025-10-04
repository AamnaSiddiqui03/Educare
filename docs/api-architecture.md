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
2.Student Profile API (Students Table)
Endpoint	Method	Description	Notes
/students/:id/profile	POST	Create student profile after registration	payload: phone, address, photo_url, video_url, help_text
/students/:id/profile	GET	Fetch student profile	used in portal for display
/students/:id/profile	PUT	Update student profile	phone, address, photo/video, help_text
/students/:id/profile	DELETE	Delete student profile	admin/internal use
/students/:id/profile/submit	POST	Mark profile completed (profile_completed = true)	triggers Phase 2 in portal
/students/:id/profile/progress	GET	Fetch profile + assessment completion status	returns profile_completed + assessment_completed for frontend tracker
3. Student Education API (StudentEducation Table)
Endpoint	Method	Description	Notes
/students/:id/education	GET	List all education entries for a student	
/students/:id/education	POST	Add new education entry	payload: institution_name, education_level, year_of_passing, marks_obtained, report_card_url
/students/:id/education/:education_id	GET	Fetch specific education entry	
/students/:id/education/:education_id	PUT	Update specific education entry	
/students/:id/education/:education_id	DELETE	Delete specific education entry	

Sample Education Payload:

{
  "institution_name": "New Middle East International School",
  "education_level": "Class 10",
  "year_of_passing": 2019,
  "marks_obtained": 91.6,
  "report_card_url": "https://storage.example.com/report_card.pdf"
}

4. Student Assessment API (StudentAssessment Table)
Endpoint	Method	Description	Notes
/students/:id/assessment/start	GET	Fetch assessment questions (external JSON)	backend returns questions for frontend
/students/:id/assessment/submit	POST	Submit answers → generate PDF → save in StudentAssessment → mark assessment_completed = true	payload: answers JSON
/students/:id/assessment/report	GET	Download PDF report	backend retrieves report_pdf_url from StudentAssessment table
/students/:id/assessment/:assessment_id	GET	Fetch specific assessment record	optional, internal/admin use
/students/:id/assessment/:assessment_id	DELETE	Delete assessment record	internal/admin use

Sample Assessment Submission Payload:

{
  "answers": {
    "q1": "B",
    "q2": "A"
  }
}


Sample Response:

{
  "assessment_id": "123e4567-e89b-12d3-a456-426614174000",
  "assessment_completed": true,
  "report_pdf_url": "https://storage.example.com/assessment_123.pdf",
  "message": "Assessment submitted successfully. Profile is now visible to donors."
}
