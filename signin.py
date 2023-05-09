from gluon.scheduler import Scheduler
import datetime
@auth.requires_login()
def Schedule():
    user_id=auth.user.id
    name=db.students(user_id).first_name
    query=db.executesql(f'select code ,name,instructor ,days,startTime,endTime,RoomNo,student_id,id from studentschedules where student_id={user_id}',as_dict=True)
    return dict(name=name,query=query)


@auth.requires_login()
def Adminhome():
    return locals()

@auth.requires_login()
def home():
    if auth.has_membership('admin'):
        redirect(URL('Adminhome'))
    else:
        return locals()

# when user click in addcourse button in registeration then will check the capacity,time,days and then add it in schedule
@auth.requires_login()
def Addcourse(): 
    id =request.args(0)
    user_id=auth.user.id
    result=db((db.studentschedules.id==id)&(db.studentschedules.student_id==auth.user.id)).select() # check if courses exist or not 
    user_id=auth.user.id
    day=db.executesql(f'select startTime , days from studentschedules where student_id={user_id}')
    day=tuple(tuple(str(element) for element in inner_tuple) for inner_tuple in day)
    if not result:
        res=complete(id) 
        if res:
            if  db.courses(id).capacity !=0:
                a=db.courses(id) # a: have courses request information 
                b=(db.courses(id).scheduled) # b: have the courses schedule id 
                c=db.coursesschedules(db.courses(id).scheduled) # c: have the days,start,end times of request
                cc=(str(c.startTime),c.days) # tuple have the new course regestration to be added
                aa=True
                for i in day:
                    if( (cc[0] == '0'+i[0] and cc[1]==i[1]) or (cc[0]==i[0] and cc[1]==i[1])):
                        aa=False
                        response.flash='The course conflict with other course'
                        return locals()
                        break
    
                if(aa):
                    db.studentschedules.insert(code=a.code, id=a.id,name=a.name,
                    instructor=a.instructor,capacity=a.capacity,days=c.days,
                    startTime=c.startTime,endTime=c.endTime,RoomNo=c.RoomNo,student_id=auth.user.id)
                    db.studentsreg.insert(studentid=user_id,courseid=a.code)

                # update capacity by decrement
                    db.executesql('UPDATE courses SET capacity=capacity-1 WHERE ID=%s', id)
                    response.flash='ADD success!'
                    return locals()
            else:
                response.flash='The course Closed'
                return locals()
        else:
            response.flash=f'you should finish prerequisit first !'
            return locals()
    else:
        response.flash='its already exist in you Schedule '
        return locals()
    redirect(URL('courses_search'))
    
@auth.requires_login()
def course_regestration_deadline():
    if  auth.has_membership('admin'):
        from gluon.tools import Mail
        mail = Mail()
        mail = auth.settings.mailer
        mail.settings.server = "smtp.gmail.com:587"
        mail.settings.sender = "201112@ppu.edu.ps"
        mail.settings.login = "201112@ppu.edu.ps:rlmsecrbkzxpioxn"
        mail.settings.tls = True
        mail.settings.ssl = False
        students = db.executesql('select first_name,email from students ')
        message = 'Dear {name},\n\nThis is a reminder that the registration deadline for the current semester is in {deadline} . \n\nPlease make sure to complete your registration .\n\nThank you'
        for student in students:
            email_message = message.format(name=student[0], deadline='2023-05-15')
            mail.send(to=student[1],subject='Registration Deadline Reminder',message=email_message)
        response.flash='Email send'
        return locals()
        

def Courses():
    rows=db.courses.scheduled==db.coursesschedules.id
    grid=SQLFORM.grid(db(rows),fields=[db.courses.code,db.courses.name,db.courses.instructor,db.courses.capacity,db.coursesschedules.days,db.coursesschedules.startTime,db.coursesschedules.endTime,db.coursesschedules.RoomNo,],links=[lambda row:A('Add course',_href=URL('Addcourse',args=[row.courses.id],),_class="button btn btn-secondary")],deletable=False,editable=False,csv=False)
    return dict(grid=grid)
# registeration to view the available courses 
@auth.requires_login()
def courses_search():
    rows=db.courses.scheduled==db.coursesschedules.id
    grid=SQLFORM.grid(db(rows),fields=[db.courses.code,db.courses.name,db.courses.instructor,db.courses.capacity,db.coursesschedules.days,db.coursesschedules.startTime,db.coursesschedules.endTime,db.coursesschedules.RoomNo,],links=[lambda row:A('Add course',_href=URL('Addcourse',args=[row.courses.id],),_class="button btn btn-secondary")],deletable=False,editable=False,csv=False,create=False,details=False)
    return dict(grid=grid)

# the specialization courses of the student
@auth.requires_login()
def Specialization_courses():
    grid=SQLFORM.grid(db.courses,fields=[db.courses.id,db.courses.code,db.courses.name,db.courses.prerequisites],deletable=False,editable=False,csv=False,searchable=False,details=False,create=False)
    return dict(grid=grid)


# to show courses report
@auth.requires_login()
def reports(): # return from studentreg table no of people
    if auth.has_membership('admin'):
        query=(db.studentsreg.courseid==db.courses.code) & (db.studentsreg.studentid==db.students.id)
        rows=db(query).select(db.courses.name,db.students.id.count(),groupby= db.courses.id)
        return dict(rows=rows)
    
@auth.requires_login()    
def complete(id):
    aa=True
    a=db.courses(id).prerequisites# '5050'
    if a:
        query=f'select courseid from studentsreg where grade is not NULL  and studentid={auth.user.id}'
        completed=db.executesql(query,as_dict=True) 
        if completed: # it is contain list of dictionary like : [{'courseid': '5273'}, {'courseid': '5051'}]     
            for i in completed:
                if  int(i.get('courseid')) == int(a):
                    aa=True
                else:

                    aa=False
            return aa
        else:
            return False
    else:
        return True

@auth.requires_login()
def display():
    name=db.students(auth.user.id).first_name
    query=f'select name ,courseid from courses c ,studentsreg s  where  c.code=s.courseid and  grade is not NULL  and studentid={auth.user.id}'
    completed=db.executesql(query,as_dict=True) 
    return dict(name=name,completed=completed)



def Tables():
    if auth.has_membership('admin'):
        query=db.executesql("select first_name,id from students",as_dict=True)
        print(query)
        return dict(query=query)
@auth.requires_login()
def addnewcourse():
    if auth.has_membership('admin'):
        form = SQLFORM(db.courses)
        # form.vars.code.requires=IS_NOT_EMPTY()
        # form.vars.capacity.requires=IS_INT_IN_RANGE(0,120)
        if form.process().accepted:
            response.flash = 'form accepted'
        elif form.errors:
            response.flash = 'form has errors'
        else:
            response.flash = 'please fill out the form'

        return dict(form=form)

def add():
    if auth.has_membership('admin'):
        form = SQLFORM(db.room)
        if form.process().accepted:
            response.flash = 'form accepted'
        elif form.errors:
            response.flash = 'form has errors'
        else:
            response.flash = 'please fill out the form'

        return dict(form=form)

@auth.requires_login()
def set_session():
    session.user='hello'
    session.expire=2
    return locals()

@auth.requires_login()
def cookies():
    response.cookies['mycookies']='value'
    response.cookies['mycookies']['expires']=3600

@auth.requires_login()
def get_cookies():
    a=request.cookies.get('mycookies')
    return locals()

@auth.requires_login()
def get_session():
    user=session.user
    return locals()    

@auth.requires_login()
def addnewroom():
    if auth.has_membership('admin'):    
        form = SQLFORM(db.coursesschedules)
        if form.process().accepted:
            response.flash = 'form accepted'
        elif form.errors:
            response.flash = 'form has errors'
        else:
            response.flash = 'please fill out the form'

        return dict(form=form)

def delete():
    id=request.vars['id']#3
    studentid=request.vars['studentid']
    code=request.vars['code']
    print(code)
    db.executesql(f'delete from studentschedules where id={id} and student_id={studentid}')
    db.executesql(f'delete from studentsreg where studentid={studentid} and courseid={code}')
    redirect(URL('Schedule'))

    
@auth.requires_login()
def viewtable():
    idd=request.vars['id']
    print(idd)
    grid=SQLFORM.grid(db.studentschedules.student_id==db.students(idd),fields=[db. studentschedules.code,db. studentschedules.name,db. studentschedules.startTime, db.studentschedules.endTime, db.studentschedules.days,db.studentschedules.RoomNo],deletable=False,editable=False,csv=False,create=False,searchable=False)
    return dict(grid=grid)






