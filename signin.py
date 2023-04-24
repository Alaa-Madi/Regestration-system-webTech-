from gluon.scheduler import Scheduler
import datetime

# to view the courses that students add   
@auth.requires_login()
def Schedule():
    grid=SQLFORM.grid(db.studentschedules,deletable=False,editable=False,csv=False,searchable=False)
    return dict(grid=grid)

# home page
# @auth.requires_login()
def home():
    return locals()

# when user click in addcourse button in registeration then will check the capacity,time,days and then add it in schedule
@auth.requires_login()
def Addcourse(): 
    id =request.args(0)
    result=db(db.studentschedules.id==id).select() # check if courses exist or not 
    day=db.executesql('select startTime , days from studentschedules')
    if not result:
        res=complete(id)
        if res:
            if  db.courses(id).capacity !=0:
                a=db.courses(id) # a: have courses requerst information 
                b=(db.courses(id).scheduled) # b: have the courses schedule id 
                c=db.coursesschedules(db.courses(id).scheduled) # c: have the days,start,end times of request
                index=0 
                cc=(c.startTime,c.days) # tuple have the new course regestration to be added
                for i in day:
                    for r in day[index]:
                        if(cc == r ):
                            aa=False
                            print(550)
                            response.flash='This course conflicts with another course ):'
                            return locals()
                    index=index+1
                aa=True
                if(aa):
                    db.studentschedules.insert(code=a.code, id=a.id,name=a.name,
                    instructor=a.instructor,capacity=a.capacity,days=c.days,
                    startTime=c.startTime,endTime=c.endTime,RoomNo=c.RoomNo)
                # update capacity by decrement
                    db.executesql('UPDATE courses SET capacity=capacity-1 WHERE ID=%s', id)
                    response.flash='ADD success!'
                    return locals()
            else:
                response.flash='The course has been completed!'
                return locals()
        else:
            response.flash='prerequisits not completed yet'
            return locals()
    else:
        response.flash='its already exist'
        return locals()
    redirect(URL('courses_search'))
    

@auth.requires_login()
def course_regestration_deadline():
    students = db.executesql('SELECT * FROM students')
    for student in students:
        mail.send(to=student.email, subject='LAST DATE FOR REGISTRATION ', message='LAST DATE FOR REGISTRATION.')

    scheduler = Scheduler(db)
    scheduler.queue_task(course_regestration_deadline, start_time=datetime.datetime(2023, 4, 7,00, 46), period=86400)

# registeration to view the available courses 
@auth.requires_login()
def courses_search():
    rows=db.courses.scheduled==db.coursesschedules.id
    grid=SQLFORM.grid(db(rows),fields=[db.courses.code,db.courses.name,db.courses.instructor,db.courses.capacity,db.coursesschedules.days,db.coursesschedules.startTime,db.coursesschedules.endTime,db.coursesschedules.RoomNo,],links=[lambda row:A('Add course',_href=URL('Addcourse',args=[row.courses.id]),_class="button btn btn-secondary")],deletable=False,editable=False,csv=False)
    return dict(grid=grid)

# the specialization courses of the student
@auth.requires_login()
def Specialization_courses():
    grid=SQLFORM.grid(db.courses,fields=[db.courses.id,db.courses.code,db.courses.name,db.courses.prerequisites],deletable=False,editable=False,csv=False,searchable=False,details=False)
    return dict(grid=grid)


# to show courses report
@auth.requires_login()
def reports(): # return from studentreg table no of people
    query=(db.studentsreg.courseid==db.courses.code) & (db.studentsreg.studentid==db.students.id)
    rows=db(query).select(db.courses.name,db.students.id.count(),groupby=db.courses.id)
    return dict(rows=rows)

@auth.requires_login()
def complete(id):
    a=db.courses(id).prerequisites
    query='select courseid from studentsreg where grade is NULL  '
    notcompleted=db.executesql(query)
    if a in notcompleted[0]:
        return False
        return locals()
    else:
        response.flash='prerequisits is completed'
        return locals()
@auth.requires_login()
def displaypre():
    query='select courseid ,name from studentsreg s,courses c where s.grade is not NULL and s.courseid=c.code  '
    complete=db.executesql(query,as_dict=True)
    return dict(complete=complete)