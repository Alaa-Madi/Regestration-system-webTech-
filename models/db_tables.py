db.define_table('courses',
Field('code','string',required=True, notnull=True,requires=IS_NOT_EMPTY()),
Field('name','string',requires=IS_NOT_EMPTY()),
Field('description','string'),
Field('prerequisites','string','reference courses',
		requires=IS_IN_DB(db, 'courses.code', '%(name)s')),
Field('instructor','string'),
Field('capacity','integer',requires=IS_INT_IN_RANGE(0,120)),
Field('scheduled','integer','reference coursesschedules', requires=IS_IN_DB(db, 'coursesschedules.id', '%(days)s: %(startTime)s - %(endTime)s'),primarykey=['code']),
Field('id','integer')
)

db.define_table('coursesschedules', 
Field('id','integer'),
Field('days','string',requires=IS_NOT_EMPTY()),
Field('startTime','time',requires=IS_NOT_EMPTY()),
Field('endTime', 'time',requires=IS_NOT_EMPTY()),
Field('RoomNo','string',requires=IS_NOT_EMPTY())
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
# db.define_table('students',
# Field('id','integer'),
# Field('first_name','string'),
# Field('last_name','string'),
# Field('email','string'),
# Field('password','password',readable=False),
# Field('registration_key','string'),
# Field('reset_password_key','string'),
# Field('registration_id','string'),
# )


# db.define_table('room', 
# Field('id','integer'),
# Field('RoomNo','string',requires=IS_NOT_EMPTY())
# )