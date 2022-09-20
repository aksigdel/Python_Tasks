from flask import Flask, jsonify, request
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, insert
from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker
import dbsecrets
from exceptions import ValueNotFound

app=Flask(__name__)

dbuser, dbpass, dbhost, dbport, dbname = dbsecrets.dbuser, dbsecrets.dbpass, dbsecrets.dbhost, dbsecrets.dbport, dbsecrets.dbname
    
#inserting/creating new program(input should follow program table schema)
@app.route('/insert_programs', methods=['POST'])
def insert_program():
#    data= request.get_json()
    data = [
        {'program_id': 'BBT', 'name': 'Bachelors ', 'num_years': 4}
    ]
    engine = create_engine(f'mysql+pymysql://root:Aksheysigdel$10@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)

    program = Table('program', metadata_obj, autoload=True, autoload_with=engine)
    stmt = insert(program)
    try:
        conn.execute(stmt,data)

        return jsonify(
            {
            'status': 200,
            'message': 'Program insertion successful',
            'data': {
                'num_of_program_inserted': len(data),
                'recods_inserted': data
            }
        })
    except:
        return jsonify({
            'status': 400,
            'message': "Input should be valid non duplicate with proper schema",
            'data': {}
        })
        
#inserting/creating new semester into program(input should follow semester table schema)
@app.route('/insert_semester', methods=['POST'])
def insert_semester():
#    data= request.get_json()
    data= [
        {'semester_id': 1110, 'semester_num': 2, 'program_id': 'BCT'},
    ]
    engine = create_engine(f'mysql+pymysql://root:Aksheysigdel$10@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)
    semester = Table('semester', metadata_obj, autoload=True, autoload_with=engine)
    stmt = insert(semester)
    try:
        conn.execute(stmt,data)
        return jsonify(
            {
            'status': 200,
            'message': 'Program insertion successful',
            'data': {
                'num_of_program_inserted': len(data),
                'recods_inserted': data
            }
        })
    except:
        return jsonify({
            'status': 400,
            'message': "Input should be valid non duplicate with proper schema",
            'data': {}
        })

#inserting courses in each semester(input should follow course and semester table schema)
@app.route('/insert_courses', methods=['POST'])
def insert_course():
    #data= request.get_json
    data = [
        {'course_id': '16.00', 'name': 'Data Science', 'credit_hours': 45, 'marks': 80,'semester_id':102},

    ]
    engine = create_engine(f'mysql+pymysql://root:Aksheysigdel$10@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)

    semester = Table('semester', metadata_obj, autoload=True, autoload_with=engine)
    course = Table('course', metadata_obj, autoload=True, autolaod_with=engine)
    
    try:
        record_lst = []
        for record in data:
            course_dict = dict()
            course_dict['course_id']= record['course_id']
            course_dict['name'] = record['name']
            course_dict['credit_hours'] = record['credit_hours']
            course_dict['marks'] = record['marks']
            course_dict['semester_id'] = record['semester_id']
            stmt = insert(course)
            conn.execute(stmt, course_dict)
            record_lst.append(course_dict)
            
            return jsonify({
                'status': 200,
                'message': "Course insertion successful",
                'data': {
                'num_of_course_insertions': len(record_lst),
                'records_inserted': record_lst
            }
        })
    except:
        return jsonify({
            'status': 400,
            'message': "Input should be valid non duplicate with proper schema",
            'data': {}
        })
        
#inserting sections in each semester(input should follow section and semester table schema)
@app.route('/insert_sections', methods=['POST'])
def insert_section():
    #data= request.get_json
    data = [
        {'section_id': 304,  'room': 457, 'semester_id':102}
    ]
    engine = create_engine(f'mysql+pymysql://root:@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)
    
    section = Table('section', metadata_obj, autoload=True, autoloadwith=engine)    
    try:
        record_lst=[]
        for record in data:
            section_dict = dict()
            section_dict['section_id']=record['section_id']
            section_dict['room'] = record['room']
            section_dict['semester_id'] = record['semester_id']
            stmt = insert(section)
            conn.execute(stmt, section_dict)
            record_lst.append(section_dict)

        return jsonify({
            'status': 200,
            'message': "Section insertion successful",
            'data': {
                'num_of_section_insertions': len(record_lst),
                'records_inserted': record_lst
            }
        })
        
    except:
        return jsonify({
            'status': 400,
            'message': "Input should be valid non duplicate with proper schema",
            'data': {}
        })

#inserting student in each semester(input should follow student, section and semester table schema)
@app.route('/insert_students', methods=['POST'])
def insert_student():
    #data= request.get_json
    data =[
        {'student_id': 405, 'name': 'Rakesh Roshan', 'address': 'Biratnagar', 'dob': '2002-06-09', 'phone_num': '9813355679', 'section_id': 304}    ]
    engine = create_engine(f'mysql+pymysql://root:@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)

    student = Table('student', metadata_obj, autoload=True, autoloadwith=engine)
    
    try:
        record_lst = []
        for record in data:
            student_dict = dict()
            student_dict['student_id'] = record['student_id']            
            student_dict['name'] = record['name']
            student_dict['address'] = record['address']
            student_dict['dob'] = record['dob']
            student_dict['phone_num'] = record['phone_num']
            student_dict['section_id'] = record['section_id']            
            stmt = insert(student)
            conn.execute(stmt, student_dict)
            record_lst.append(student_dict)
            
            return jsonify({
                'status': 200,
                'message': "Student insertion successful",
                'data': {
                'num_of_student_insertions': len(record_lst),
                'records_inserted': record_lst
            }
        })

    except:
        return jsonify({
            'status': 400,
            'message': "Input should be valid non duplicate with proper schema",
            'data': {}
        })
    
#inserting instructor(input should follow instructor and course table schema)
@app.route('/insert_instructors', methods=['POST'])
def insert_instructor():
    #data= request.get_json()
    data=  [
        {'instructor_id': 204, 'name': 'Sandarbha Niraula', 'address': 'Kathmandu', 'dob': '1975-03-11','phone_num': '9845011345', 'position': 'Asst. Professor',  'course_id': '14.00'}
    ]
    engine = create_engine(f'mysql+pymysql://root:@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)

    instructor = Table('instructor', metadata_obj, autoload=True, autoload_with=engine)
    course = Table('course', metadata_obj, autoload=True, autoload_with=engine) 
    
    try:
        record_lst =[]
        for record in data:
            instructor_dict = dict()
            instructor_dict['instructor_id'] = record['instructor_id']
            instructor_dict['name'] = record['name']
            instructor_dict['address'] = record['address']
            instructor_dict['dob'] = record['dob']
            instructor_dict['phone_num'] = record['phone_num']
            instructor_dict['position'] = record['position']   
            instructor_dict['course_id'] = record['course_id']
            stmt = insert(instructor)
            conn.execute(stmt, instructor_dict)
            record_lst.append(instructor_dict)
            
            return jsonify({
            'status': 200,
            'message': "Instructor insertion successful",
            'data': {
                'num_of_section_insertions': len(record_lst),
                'records_inserted': record_lst
            }
        })

    except:
        return jsonify({
            'status': 400,
            'message': "Input should be valid non duplicate with proper schema",
            'data': {}
        })
        
# retrieve all records of programs
@app.route('/programs', methods=['GET'])
def programs():
    engine = create_engine(f'mysql+pymysql://root:Aksheysigdel$10@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)

    program = Table('program', metadata_obj, autoload=True, autoload_with=engine)
    stmt = select([program])
    results = conn.execute(stmt).fetchall()

    response = []
    for result in results:
        program_dict = dict()
        program_dict['program_id'] = result.program_id
        program_dict['name'] = result.name
        program_dict['num_years'] = result.num_years
        response.append(program_dict)
        
    return jsonify({
        'status': 200,
        'message': 'Retrieval successful',
        'data': {
            'no_of_records': len(results),
            'records': response
        }
    })

# retrieve all student records
@app.route('/students', methods=['GET'])
def students():
    engine = create_engine(f'mysql+pymysql://root:Aksheysigdel$10@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)

    student = Table('student', metadata_obj, autoload=True, autoload_with=engine)
    stmt = select([student])
    results = conn.execute(stmt).fetchall()

    response = []
    for result in results:
        student_dict = dict()
        student_dict['student_id'] = result.student_id
        student_dict['name'] = result.name
        student_dict['address'] = result.address
        student_dict['dob'] = result.dob
        student_dict['phone_num'] = result.phone_num
        student_dict['section_id'] = result.section_id
        response.append(student_dict)
    
    return jsonify({
        'status': 200,
        'message': 'Retrieval successful',
        'data': {
            'no_of_records': len(results),
            'records': response
        }
    })
    
# retrieve all instructor records
@app.route('/instructors', methods=['GET'])
def instructors():
    engine = create_engine(f'mysql+pymysql://root:@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)

    instructor = Table('instructor', metadata_obj, autoload=True, autoload_with=engine)
    stmt = select([instructor])
    results = conn.execute(stmt).fetchall()

    response = []
    for result in results:
        instructor_dict = dict()
        instructor_dict['instructor_id'] = result.instructor_id
        instructor_dict['name'] = result.name
        instructor_dict['address'] = result.address
        instructor_dict['dob'] = result.dob
        instructor_dict['phone_num'] = result.phone_num
        instructor_dict['position'] = result.position
        instructor_dict['course_id'] = result.course_id
        response.append(instructor_dict)

    return jsonify({
        'status': 200,
        'message': 'Retrieval successful',
        'data': {
            'no_of_records': len(results),
            'records': response
        }
    })

# retrieve number of students in each program
@app.route('/program/students', methods=['GET'])
def program_students():
    engine = create_engine(f'mysql+pymysql://root:Aksheysigdel$10@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)
    
    program = Table('program', metadata_obj, autoload=True, autoload_with=engine)
    semester = Table('semester', metadata_obj, autoload=True, autoload_with=engine)
    section = Table('section', metadata_obj, autoload=True, autoload_with=engine)
    student = Table('student', metadata_obj, autolaod=True, autoload_with=engine)
    
    stmt = select([program, func.count(student.columns.student_id).label('num_of_students')])
    stmt = stmt.select_from(((program\
                    .join(semester, program.columns.program_id == semester.columns.program_id))\
                    .join(section, semester.columns.semester_id == section.columns.semester_id))\
                    .join(student, section.columns.section_id == student.columns.section_id)
                    )
    stmt = stmt.group_by(program.columns.program_id,
                         program.columns.name,
                         program.columns.num_years)

    results = conn.execute(stmt).fetchall()
    response = []
    for result in results:
        first_dict = dict()
        second_dict = dict()
        first_dict['program_id'] = result.program_id
        first_dict['name'] = result.name
        first_dict['num_years'] = result.num_years
        second_dict['program'] = first_dict
        second_dict['num_of_students'] = result.num_of_students
        response.append(second_dict)

    return jsonify({
        'status': 200,
        'message': 'Retrieval successful',
        'data': {
            'no_of_records': len(results),
            'records': response
        }
    })

# retrieve number of students in each semester
@app.route('/semester/students', methods=['GET'])
def semester_students():
    engine = create_engine(f'mysql+pymysql://root:@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)
    
    semester = Table('semester', metadata_obj, autoload=True, autoload_with=engine)
    section = Table('section', metadata_obj, autolaod=True, autoload_with=engine)
    student = Table('student', metadata_obj, autoload=True, autoload_with=engine)
    
    stmt = select([semester, func.count(student.columns.student_id).label('num_of_students')])
    stmt = stmt.select_from((semester\
            .join(section, semester.columns.semester_id == section.columns.semester_id))\
            .join(student, section.columns.section_id == student.columns.section_id))
    stmt = stmt.group_by(semester.columns.semester_id,
                         semester.columns.program_id,
                         semester.columns.semester_num)
    results = conn.execute(stmt).fetchall()
    response= []
    for result in results:
        first_dict = dict()
        second_dict = dict()
        first_dict['semester_id'] = result.semester_id
        first_dict['program_id'] = result.program_id
        first_dict['semester_num'] = result.semester_num
        second_dict['semester'] = first_dict
        second_dict['num_of_students'] = result.num_of_students
        response.append(second_dict)

    return jsonify({
        'status': 200,
        'message': 'Retrieval successful',
        'data': {
            'num_of_records': len(results),
            'records': response
        }
    })
    
# retrieve number of students in each section    
@app.route('/section/students', methods=['GET'])
def section_students():
    engine = create_engine(f'mysql+pymysql://root:@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)

    section = Table('section', metadata_obj, autolaod=True, autoload_with=engine)
    student = Table('student', metadata_obj, autoload=True, autoload_with=engine)
    
    stmt = select([section, func.count(student.columns.student_id).label('num_of_students')])
    stmt = stmt.select_from(section.join(student, section.columns.section_id == student.columns.section_id))
    stmt = stmt.group_by(section.columns.section_id,
                         section.columns.room,
                         section.columns.semester_id)
    
    results = conn.execute(stmt).fetchall()
    response = []
    for result in results:
        first_dict = dict()
        second_dict = dict()
        first_dict['section_id'] = result.section_id
        first_dict['room'] = result.room
        first_dict['semester_id'] = result.semester_id
        second_dict['section'] = first_dict
        second_dict['num_of_students'] = result.num_of_students
        response.append(second_dict)

    return jsonify({
        'status': 200,
        'message': 'Retrieval successful',
        'data': {
            'num_of_section_records': len(results),
            'records': response
        }
    })
    
    
#retrieve sections in each semester
@app.route('/semester/section', methods=['GET'])
def section_sem():
    engine = create_engine(f'mysql+pymysql://root:Aksheysigdel$10@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)
    
    semester = Table('semester', metadata_obj, autoload=True, autoload_with=engine)
    section = Table('section', metadata_obj, autoload=True, autoload_with=engine)
    
    stmt = select([section])
    stmt = stmt.select_from(semester.join(section, semester.columns.semester_id == section.columns.semester_id))

    results =conn.execute(stmt).fetchall()
    sem_lst=[]
    for record in results:
            sem_lst.append( record.semester_id)
    
    sem_tup=list(set(sem_lst))

    final_dct= dict()
    final_lst=[]
    
    for i in range(len(sem_tup)):
            semdct=dict()
            lst=[]
            for j in range (len(results)):
                if sem_tup[i]==results[j].semester_id:
                    semdct['semester_id']=results[j].semester_id
                    section_dict = dict()
                    section_dict['section_id'] = results[j].section_id
                    section_dict['room'] = results[j].room
                    lst.append(section_dict)  
            final_dct={
                'semester_id':sem_tup[i],
                'section': lst
            }
            final_lst.append(final_dct)
    return jsonify({
            'output': final_lst
        })
            
#retrieve course in each semester
@app.route('/semester/course', methods=['GET'])
def course_sem():
    engine = create_engine(f'mysql+pymysql://root:Aksheysigdel$10@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)
    
    semester = Table('semester', metadata_obj, autoload=True, autoload_with=engine)
    course = Table('course', metadata_obj, autoload=True, autoload_with=engine)
    
    stmt = select([course])
    stmt = stmt.select_from(semester.join(course, semester.columns.semester_id == course.columns.semester_id))

    results =conn.execute(stmt).fetchall()
    print(results)
    sem_lst=[]
    for i in range(len(results)):
            sem_lst.append(results[i].semester_id)
    sem_tup=list(set(sem_lst))
    final_dct= dict()
    final_lst=[]
    for i in range(len(sem_tup)):
            semdct=dict()
            lst=[]
            for j in range (len(results)):
                if sem_tup[i]==results[j].semester_id:
                    semdct['semester_id']=results[j].semester_id
                    course_dict = dict()
                    course_dict['course_id'] = results[j].course_id
                    course_dict['name'] = results[j].name
                    lst.append(course_dict)   
            final_dct={
                'semester_id':sem_tup[i],
                'course': lst
            }
            final_lst.append(final_dct)
    return jsonify({
            'output': final_lst
        })
            
#retrieve instructor in each semester
@app.route('/semester/instructor', methods=['GET'])
def instructor_sem():
    engine = create_engine(f'mysql+pymysql://root:Aksheysigdel$10@127.0.0.1:3306/LMS',echo=True)
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)
    
    semester = Table('semester', metadata_obj, autoload=True, autoload_with=engine)
    course = Table('course', metadata_obj, autoload=True, autoload_with=engine)
    instructor = Table('instructor', metadata_obj, autoload=True, autoload_with=engine)
    
    stmt = select([instructor, course.columns.semester_id])
    stmt = stmt.select_from(((semester\
                        .join(course, course.columns.semester_id == semester.columns.semester_id))\
                        .join(instructor, course.columns.course_id == instructor.columns.course_id)
                        ))    

    results =conn.execute(stmt).fetchall()
    print(results)
    sem_lst=[]
    for i in range(len(results)):
            sem_lst.append( results[i].semester_id)
    sem_tup=list(set(sem_lst))

    final_dct= dict()
    final_lst=[]

    for i in range(len(sem_tup)):
            semdct=dict()
            lst=[]
            for j in range (len(results)):
                if sem_tup[i]==results[j].semester_id:
                    semdct['semester_id']=results[j].semester_id
                    instructor_dict = dict()
                    instructor_dict['instructor_id'] = results[j].instructor_id
                    instructor_dict['name'] = results[j].name
                    lst.append(instructor_dict)   
            final_dct={
                'semester_id':sem_tup[i],
                'section': lst
            }
            final_lst.append(final_dct)
    return jsonify({
            'output': final_lst
        })
            

        
if __name__ == '__main__':
    app.run(debug=True)