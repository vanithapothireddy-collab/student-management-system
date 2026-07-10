console.log("dashboard.js loaded");

async function loadDashboard() {

    try {

        // Student Count
        const studentResponse = await fetch("/dashboard/student-count");
        const studentData = await studentResponse.json();

        document.getElementById("student-count").innerText =
            studentData.total_students;

        // Department Count
        const departmentResponse = await fetch("/dashboard/department-count");
        const departmentData = await departmentResponse.json();

        document.getElementById("department-count").innerText =
            departmentData.total_departments;

        // Subject Count
        const subjectResponse = await fetch("/dashboard/subject-count");
        const subjectData = await subjectResponse.json();

        document.getElementById("subject-count").innerText =
            subjectData.total_subjects;

        // Fee Summary
        const feeResponse = await fetch("/dashboard/fee-summary");
        const feeData = await feeResponse.json();

        document.getElementById("fee-count").innerText =
            feeData.total_fee_collected;

        // Present Today
        const presentResponse = await fetch("/dashboard/present-today");
        const presentData = await presentResponse.json();

        document.getElementById("present-count").innerText =
            presentData.present_today;

        // Absent Today
        const absentResponse = await fetch("/dashboard/absent-today");
        const absentData = await absentResponse.json();

        document.getElementById("absent-count").innerText =
            absentData.absent_today;

        // Attendance Percentage
        const attendanceResponse = await fetch("/dashboard/attendance-percentage");
        const attendanceData = await attendanceResponse.json();

        document.getElementById("attendance-percent").innerText =
            attendanceData.attendance_percentage + "%";

    }
    catch (err) {

        console.error("Dashboard Error:", err);

    }

}

async function loadRecentStudents() {

    try {

        const response = await fetch("/dashboard/recent-students");

        const students = await response.json();

        const table = document.getElementById("student-table-body");

        table.innerHTML = "";

        students.forEach(student => {

            table.innerHTML += `
                <tr>
                    <td>${student[0]}</td>
                    <td>${student[1]}</td>
                    <td>${student[2]}</td>
                </tr>
            `;

        });

    }
    catch (err) {

        console.error("Recent Students Error:", err);

    }

}

async function loadDepartmentReport() {

    try {

        const response = await fetch("/dashboard/department-wise-students");

        const data = await response.json();

        const table = document.getElementById("departmentReport");

        table.innerHTML = "";

        data.forEach(row => {

            table.innerHTML += `
                <tr>
                    <td>${row[0]}</td>
                    <td>${row[1]}</td>
                </tr>
            `;

        });

    }
    catch (err) {

        console.error("Department Report Error:", err);

    }

}

// Initial Load
loadDashboard();
loadRecentStudents();
loadDepartmentReport();