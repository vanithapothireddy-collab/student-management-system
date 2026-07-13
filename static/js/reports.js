checkLogin();
console.log("reports.js loaded");

// --------------------------------------
// Student Report
// --------------------------------------

async function loadStudentReport() {

    try {

        const response = await fetch("/reports/students");
        const data = await response.json();

        const table = document.getElementById("studentReportTable");

        table.innerHTML = "";

        data.forEach(student => {

            table.innerHTML += `
                <tr>
                    <td>${student[0]}</td>
                    <td>${student[1]}</td>
                    <td>${student[2]}</td>
                    <td>${student[3]}</td>
                </tr>
            `;

        });

        document.getElementById("studentReportCount").innerText = data.length;

    }

    catch (err) {

        console.error("Student Report Error:", err);

    }

}

// --------------------------------------
// Department Report
// --------------------------------------

async function loadDepartmentReport() {

    try {

        const response = await fetch("/reports/departments");
        const data = await response.json();

        const table = document.getElementById("departmentReportTable");

        table.innerHTML = "";

        data.forEach(department => {

            table.innerHTML += `
                <tr>
                    <td>${department[0]}</td>
                    <td>${department[1]}</td>
                </tr>
            `;

        });

        document.getElementById("departmentReportCount").innerText = data.length;

    }

    catch (err) {

        console.error("Department Report Error:", err);

    }

}

// --------------------------------------
// Attendance Report
// --------------------------------------

async function loadAttendanceReport() {

    try {

        const response = await fetch("/reports/attendance");
        const data = await response.json();

        const table = document.getElementById("attendanceReportTable");

        table.innerHTML = "";

        data.forEach(attendance => {

            table.innerHTML += `
                <tr>
                    <td>${attendance[0]}</td>
                    <td>${attendance[1]}</td>
                    <td>${attendance[2]}</td>
                </tr>
            `;

        });

        document.getElementById("attendanceReportCount").innerText = data.length;

    }

    catch (err) {

        console.error("Attendance Report Error:", err);

    }

}

// --------------------------------------
// Fee Report
// --------------------------------------

async function loadFeeReport() {

    try {

        const response = await fetch("/reports/fees");
        const data = await response.json();

        const table = document.getElementById("feeReportTable");

        table.innerHTML = "";

        data.forEach(fee => {

            table.innerHTML += `
                <tr>
                    <td>${fee[0]}</td>
                    <td>${fee[1]}</td>
                    <td>${fee[2]}</td>
                    <td>${fee[3]}</td>
                </tr>
            `;

        });

        document.getElementById("feeReportCount").innerText = data.length;

    }

    catch (err) {

        console.error("Fee Report Error:", err);

    }

}

// --------------------------------------
// Marks Report
// --------------------------------------

async function loadMarksReport() {

    try {

        const response = await fetch("/reports/marks");
        const data = await response.json();

        const table = document.getElementById("marksReportTable");

        table.innerHTML = "";

        data.forEach(mark => {

            table.innerHTML += `
                <tr>
                    <td>${mark[0]}</td>
                    <td>${mark[1]}</td>
                    <td>${mark[2]}</td>
                </tr>
            `;

        });

        document.getElementById("marksReportCount").innerText = data.length;

    }

    catch (err) {

        console.error("Marks Report Error:", err);

    }

}

// --------------------------------------
// Load Everything
// --------------------------------------

// --------------------------------------
// Export Reports
// --------------------------------------

function exportStudents(){

    window.open("/reports/students");

}

function exportDepartments(){

    window.open("/reports/departments");

}

function exportAttendance(){

    window.open("/reports/attendance");

}

function exportFees(){

    window.open("/reports/fees");

}

function exportMarks(){

    window.open("/reports/marks");

}
// --------------------------------------
// Print Reports
// --------------------------------------

function printStudentReport() {

    printTable("Student Report", "studentReportTable");

}

function printDepartmentReport() {

    printTable("Department Report", "departmentReportTable");

}

function printAttendanceReport() {

    printTable("Attendance Report", "attendanceReportTable");

}

function printFeeReport() {

    printTable("Fee Report", "feeReportTable");

}

function printMarksReport() {

    printTable("Marks Report", "marksReportTable");

}
function downloadStudentExcel(){

    window.location.href =
        "/reports/students/excel";

}
function downloadStudentPDF(){

    window.location.href =
        "/reports/students/pdf";

}

function printTable(title, tableId) {

    const table =
        document.getElementById(tableId).parentElement.outerHTML;

    const win = window.open("", "", "width=1000,height=700");

    win.document.write(`

        <html>

        <head>

            <title>${title}</title>

            <style>

                body{

                    font-family:Arial;

                    margin:40px;

                }

                h1{

                    text-align:center;

                }

                table{

                    width:100%;

                    border-collapse:collapse;

                    margin-top:20px;

                }

                table,th,td{

                    border:1px solid black;

                }

                th{

                    background:#0d6efd;

                    color:white;

                }

                th,td{

                    padding:10px;

                    text-align:left;

                }

            </style>

        </head>

        <body>

            <h1>Student Management System</h1>

            <h2>${title}</h2>

            ${table}

        </body>

        </html>

    `);

    win.document.close();

    win.print();

}
window.onload = function () {

    loadStudentReport();

    loadDepartmentReport();

    loadAttendanceReport();

    loadFeeReport();

    loadMarksReport();

};