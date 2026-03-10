{
    'name': 'Music School',
    'version': '18.0.0.0',
    'description': 'Manages a music school with students, teachers and classes',
    'summary': 'Manages a music school with students, teachers and classes',
    'author': 'Gerard Campos',
    'license': 'LGPL-3',
    'category': 'Music School',
    'depends': [
        'base'
    ],
    'data':[
        'data/ir_cron.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/music_school_instrument_views.xml',
        'views/music_school_student_views.xml',
        'views/music_school_teacher_views.xml',
        'views/music_school_course_views.xml',
        'views/music_school_classroom_views.xml',
        'views/music_school_lesson_views.xml',
        'views/music_school_lesson_attendance.xml',
        'views/music_school_exam_views.xml',
        'views/music_school_results_views.xml',
        'wizard/music_school_course_change_state_views.xml',
        'wizard/music_school_course_create_lesson_views.xml',
        'report/music_school_course_report.xml',
        'report/music_school_lesson_report.xml',
        'report/music_school_exam_report.xml',
        'views/music_school_menuitems.xml',
    ]
}