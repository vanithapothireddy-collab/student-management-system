async function loadTeacherDashboard() {

    let response =
        await fetch("/teacher-subjects/dashboard/total-subjects");

    let data =
        await response.json();

    document.getElementById("teacherSubjectCount").innerText =
        data.total_subjects;


    response =
        await fetch("/dashboard/student-count");

    data =
        await response.json();

    document.getElementById("teacherStudentCount").innerText =
        data.total_students;


    response =
        await fetch("/dashboard/present-today");

    data =
        await response.json();

    document.getElementById("teacherAttendanceCount").innerText =
        data.present_today;


    response =
        await fetch("/dashboard/marks-count");

    data =
        await response.json();

    document.getElementById("teacherMarksCount").innerText =
        data.total_marks;

}

loadTeacherDashboard();