db.define_table('courses',
Field('code','string'),
Field('name','string'),
Field('description','string'),
Field('prerequisites','string'),
Field('instructor','string'),
Field('capacity','integer'),
Field('scheduled','integer'))

db.define_table('coursesschedules', 
Field('id','integer'),
Field('days','string'),
Field('startTime','time'),
Field('endTime', 'time'),
Field('RoomNo','string')
)

db.define_table('studentschedules',
Field('code','string'),
Field('id','integer'),
Field('name','string'),
Field('instructor', 'string'),
Field('capacity','integer'),
Field('days','string'),
Field('startTime','Time'),
Field('endTime','Time'),
Field('RoomNo','string'),
Field('student_id','integer')
)
db.define_table('studentsreg', 
Field('id','integer'),
Field('studentid','integer'),
Field('courseid','string'),
Field('grade','integer')
)
db.define_table('students',
Field('id','integer'),
Field('first_name','string'),
Field('last_name','string'),
Field('email','string'),
Field('password','string'),
Field('registration_key','string'),
Field('reset_password_key','string'),
Field('registration_id','string'),
)


