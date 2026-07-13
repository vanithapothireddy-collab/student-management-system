checkLogin();

console.log("dashboard.js loaded");

let departmentChart = null;

async function loadDashboard() {

    try {

        // Students
        let response = await fetch("/dashboard/student-count");
        let data = await response.json();

        document.getElementById("student-count").textContent =
            data.total_students ?? 0;


        // Departments
        response = await fetch("/dashboard/department-count");
        data = await response.json();

        document.getElementById("department-count").textContent =
            data.total_departments ?? 0;


        // Teachers// 
response = await fetch("/dashboard/teacher-count");
data = await response.json();

console.log("Teacher:", data);

const teacherElement = document.getElementById("teacher-count");

if (teacherElement) {
    teacherElement.textContent = data.total_teachers ?? 0;
}


        // Subjects
        response = await fetch("/dashboard/subject-count");
        data = await response.json();

        document.getElementById("subject-count").textContent =
            data.total_subjects ?? 0;


        // Fee Collection
        response = await fetch("/dashboard/fee-summary");
        data = await response.json();

        document.getElementById("fee-count").textContent =
            "₹" + Number(data.total_fee_collected ?? 0).toLocaleString("en-IN");


        // Present Today
        response = await fetch("/dashboard/present-today");
        data = await response.json();

        document.getElementById("present-count").textContent =
            data.present_today ?? 0;


        // Absent Today
        response = await fetch("/dashboard/absent-today");
        data = await response.json();

        document.getElementById("absent-count").textContent =
            data.absent_today ?? 0;


        // Attendance Percentage
        response = await fetch("/dashboard/attendance-percentage");
        data = await response.json();

        document.getElementById("attendance-percent").textContent =
            (data.attendance_percentage ?? 0) + "%";

    }
    catch (error) {

        console.error("Dashboard Error:", error);

    }

}


async function loadDepartmentReport() {

    try {

        const response =
            await fetch("/dashboard/department-wise-students");

        const data =
            await response.json();

        const table =
            document.getElementById("departmentReport");

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
    catch (error) {

        console.error(error);

    }

}
// ------------------------
// Department Chart
// ------------------------

async function loadDepartmentChart() {

    try {

        const response =
            await fetch("/dashboard/department-wise-students");

        const data =
            await response.json();

        const labels = [];
        const values = [];

        data.forEach(row => {

            labels.push(row[0]);
            values.push(row[1]);

        });

        const canvas =
            document.getElementById("departmentChart");

        if (!canvas) return;

        if (departmentChart) {
            departmentChart.destroy();
        }

        departmentChart = new Chart(canvas, {

            type: "bar",

            data: {

                labels: labels,

                datasets: [{

                    label: "Students",

                    data: values,

                    backgroundColor: "#2563eb"

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                scales: {

                    y: {

                        beginAtZero: true,

                        ticks: {

                            precision: 0

                        }

                    }

                }

            }

        });

    }
    catch (error) {

        console.error("Department Chart Error:", error);

    }

}



// ------------------------
// Recent Students
// ------------------------

async function loadRecentStudents() {

    try {

        const response =
            await fetch("/dashboard/recent-students");

        const data =
            await response.json();

        const table =
            document.getElementById("student-table-body");

        table.innerHTML = "";

        data.forEach(student => {

            table.innerHTML += `
                <tr>
                    <td>${student[0]}</td>
                    <td>${student[1]}</td>
                    <td>${student[2]}</td>
                </tr>
            `;

        });

    }
    catch (error) {

        console.error("Recent Students Error:", error);

    }

}



// ------------------------
// Welcome User
// ------------------------

const username = localStorage.getItem("username");

const welcomeUser =
    document.getElementById("welcomeUser");

if (welcomeUser) {

    welcomeUser.textContent =
        username
            ? `Welcome ${username} 👋`
            : "Welcome 👋";

}



// ------------------------
// Initial Load
// ------------------------

window.onload = function () {

    loadDashboard();

    loadDepartmentReport();

    loadDepartmentChart();

    loadRecentStudents();

};