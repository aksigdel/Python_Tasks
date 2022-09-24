import dbsecrets
from sqlalchemy import create_engine, MetaData, Table, Column, Date, String, Integer, ForeignKey, insert

dbuser, dbpass, dbhost, dbport, dbname = dbsecrets.dbuser, dbsecrets.dbpass, dbsecrets.dbhost, dbsecrets.dbport, dbsecrets.dbname

def create_db_schema(engine):
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)

    program = Table('program', metadata_obj,
                    Column('program_id', String(10), primary_key=True),
                    Column('name', String(255), nullable=False),
                    Column('num_years', Integer, nullable=False)
                    )


    semester = Table('semester', metadata_obj,
                    Column('semester_id', Integer, primary_key=True),
                    Column('semester_num', Integer, nullable=False),
                    Column('program_id', String(10), 
                        ForeignKey('program.program_id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
                    )
    
    section = Table('section', metadata_obj,
                    Column('section_id', Integer, primary_key=True),
                    Column('room', Integer, nullable=False),
                    Column('semester_id', Integer, 
                        ForeignKey('semester.semester_id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
                    )
    
    course = Table('course', metadata_obj,
                Column('course_id', String(20), primary_key=True),
                Column('name', String(255), nullable=False),
                Column('credit_hours', Integer, nullable=False),
                Column('marks', Integer, nullable=False),
                Column('semester_id', Integer, 
                    ForeignKey('semester.semester_id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
                )
    
    instructor = Table('instructor', metadata_obj,
                    Column('instructor_id', Integer, primary_key=True),
                    Column('name', String(255), nullable=False),
                    Column('address', String(255), nullable=False),
                    Column('dob', Date, nullable=False),
                    Column('phone_num', String(10), nullable=False),
                    Column('position', String(255), nullable=False),
                    Column('course_id', String(20), 
                        ForeignKey('course.course_id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
                    )
    
    student = Table('student', metadata_obj,
                    Column('student_id', Integer, primary_key=True),
                    Column('name', String(255), nullable=False),
                    Column('address', String(255), nullable=False),   
                    Column('dob', Date, nullable=False),
                    Column('phone_num', String(10), nullable=False),
                    Column('section_id', Integer, 
                        ForeignKey('section.section_id', onupdate="CASCADE"), nullable=True)
                    )
    
    metadata_obj.create_all(engine) 
    
def insert_records(engine):
    conn = engine.connect()
    metadata_obj = MetaData(bind=engine)
    MetaData.reflect(metadata_obj)
    
    program = Table('program', metadata_obj, autoload=True, autoload_with=engine)
    semester = Table('semester', metadata_obj, autoload=True, autoload_with=engine)
    course = Table('course', metadata_obj, autoload=True, autoload_with=engine)
    instructor = Table('instructor', metadata_obj, autoload=True, autoload_with=engine)
    section = Table('section', metadata_obj, audoload=True, autoload_with=engine)
    student = Table('student', metadata_obj, autoload=True, autoload_with=engine)
   
    program_list = [
        {'program_id': 'BCT', 'name': 'Bachelors in Computer Engineering', 'num_years': 4},
        {'program_id': 'BCE', 'name': 'Bachelors in Civil Engineering', 'num_years': 4},
        {'program_id': 'MSCS', 'name': 'Masters in Computer Science ', 'num_years': 2}
    ]

    semester_list = [
        {'semester_id': 101, 'semester_num': 1, 'program_id': 'BCE'},
        {'semester_id': 102, 'semester_num': 1, 'program_id': 'BCT'},
        {'semester_id': 103, 'semester_num': 1, 'program_id': 'MSCS'}
    ]

    course_list = [
        {'course_id': '11.00', 'name': 'Introduction to Fluid Mechanics', 'credit_hours': 45, 'marks': 80, 'semester_id': 101},
        {'course_id': '12.00', 'name': 'Digital Logic', 'credit_hours': 45, 'marks': 80, 'semester_id': 102},
        {'course_id': '13.00', 'name': 'Introduction to Quantum Computing', 'credit_hours': 45, 'marks': 80, 'semester_id': 103}
    ]


    instructor_list = [
        {'instructor_id': 201, 'name': 'Sanisha Niraula', 'address': 'Kathmandu', 'dob': '1975-03-11','phone_num': '9845011345', 'position': 'Asst. Professor',  'course_id': '11.00'},
        {'instructor_id': 202, 'name': 'Safal Koirala', 'address': 'Biratnagar', 'dob': '1968-07-23', 'phone_num': '9845699024', 'position': 'Assistant Professor', 'course_id': '12.00'},
        {'instructor_id': 203, 'name': 'Akrit Poudel', 'address': 'America', 'dob': '1972-08-09', 'phone_num': '9877433560', 'position': 'Professor', 'course_id': '13.00'}
    ]
    

    section_list = [
        {'section_id': 301,  'room': 123, 'semester_id': 101},
        {'section_id': 302,  'room': 456, 'semester_id': 102},
        {'section_id': 303,  'room': 789, 'semester_id': 103}
    ]

    student_list = [
        {'student_id': 401, 'name': 'Samip Dangol', 'address': 'Kathmandu', 'dob': '1999-01-02', 'phone_num': '9807233509', 'section_id': 301},
        {'student_id': 402, 'name': 'Himani KC', 'address': 'New York', 'dob': '2000-05-08', 'phone_num': '9865011220', 'section_id': 303},
        {'student_id': 403, 'name': 'Rajesh Hamal', 'address': 'Biratnagar', 'dob': '2002-06-09', 'phone_num': '9813355679', 'section_id': 302},
        {'student_id': 404, 'name': 'Salman Khan',  'address': 'India', 'dob': '1999-07-19', 'phone_num': '9800699123', 'section_id': 301}
    ]
    
    table_dict = {
        program: program_list,
        semester: semester_list,
        course: course_list,
        instructor: instructor_list,
        section: section_list,
        student: student_list
    }

    for (table, table_list) in table_dict.items():
        conn.execute(insert(table), table_list)
        
        
if __name__ == '__main__':
    engine = create_engine(f'mysql+pymysql://root:@127.0.0.1:3306/LMS',echo=True)
#   engine = create_engine(f'mysql+pymysql://{dbuser}:{dbpass}@{dbhost}:3306/{dbname}',echo=True)
    create_db_schema(engine)
    insert_records(engine)