// ----------------------------
// Load Attendance
// ----------------------------
checkLogin();
function loadAttendance() {

    fetch("/attendance/")
    .then(response => response.json())
    .then(data => {

        const table = document.getElementById("attendanceTable");

        table.innerHTML = "";

        data.forEach(attendance => {

            table.innerHTML += `
            <tr>

                <td>${attendance.attendance_id}</td>

                <td>${attendance.student_name}</td>

                <td>${attendance.subject_name}</td>

                <td>${attendance.attendance_date}</td>

                <td>${attendance.status}</td>

                <td>

                    <button onclick="editAttendance(${attendance.attendance_id})">
                        Edit
                    </button>

                    <button onclick="deleteAttendance(${attendance.attendance_id})">
                        Delete
                    </button>

                </td>

            </tr>
            `;

        });

    });

}

// ----------------------------
// Load Students Dropdown
// ----------------------------

function loadStudents() {

    fetch("/students/")
    .then(response => response.json())
    .then(data => {

        const select = document.getElementById("student_id");

        select.innerHTML =
        '<option value="">Select Student</option>';

        data.forEach(student => {

            select.innerHTML += `

            <option value="${student.student_id}">

                ${student.student_name}

            </option>

            `;

        });

    });

}

// ----------------------------
// Load Subjects Dropdown
// ----------------------------

function loadSubjects() {

    fetch("/subjects/")
    .then(response => response.json())
    .then(data => {

        const select = document.getElementById("subject_id");

        select.innerHTML =
        '<option value="">Select Subject</option>';

        data.forEach(subject => {

            select.innerHTML += `

            <option value="${subject.subject_id}">

                ${subject.subject_name}

            </option>

            `;

        });

    });

}

// ----------------------------
// Show Form
// ----------------------------

document.getElementById("addAttendanceBtn").onclick = function () {

    document.getElementById("attendanceForm").style.display = "block";

    document.getElementById("saveBtn").innerText = "Save Attendance";

    document.getElementById("saveBtn").onclick = saveAttendance;

};

// ----------------------------
// Save Attendance
// ----------------------------

async function saveAttendance() {

    const attendance = {

        student_id: parseInt(document.getElementById("student_id").value),

        subject_id: parseInt(document.getElementById("subject_id").value),

        attendance_date: document.getElementById("attendance_date").value,

        status: document.getElementById("status").value

    };

    const response = await fetch("/attendance/", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(attendance)

    });

    const result = await response.json();

    alert(result.message);

    loadAttendance();

    document.getElementById("attendanceForm").style.display = "none";

}

// ----------------------------
// Edit Attendance
// ----------------------------

async function editAttendance(id) {

    const response = await fetch(`/attendance/${id}`);

    const attendance = await response.json();

    document.getElementById("attendanceForm").style.display = "block";

    document.getElementById("student_id").value = attendance.student_id;

    document.getElementById("subject_id").value = attendance.subject_id;

    document.getElementById("attendance_date").value =
        attendance.attendance_date.substring(0,10);

    document.getElementById("status").value = attendance.status;

    document.getElementById("saveBtn").innerText = "Update Attendance";

    document.getElementById("saveBtn").onclick = function () {

        updateAttendance(id);

    };

}

// ----------------------------
// Update Attendance
// ----------------------------

async function updateAttendance(id) {

    const attendance = {

        student_id: parseInt(document.getElementById("student_id").value),

        subject_id: parseInt(document.getElementById("subject_id").value),

        attendance_date: document.getElementById("attendance_date").value,

        status: document.getElementById("status").value

    };

    const response = await fetch(`/attendance/${id}`, {

        method: "PUT",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(attendance)

    });

    const result = await response.json();

    alert(result.message);

    loadAttendance();

    document.getElementById("attendanceForm").style.display = "none";

    document.getElementById("saveBtn").innerText = "Save Attendance";

    document.getElementById("saveBtn").onclick = saveAttendance;

}

// ----------------------------
// Delete Attendance
// ----------------------------

async function deleteAttendance(id) {

    if (!confirm("Delete Attendance?"))
        return;

    const response = await fetch(`/attendance/${id}`, {

        method: "DELETE"

    });

    const result = await response.json();

    alert(result.message);

    loadAttendance();

}
function searchAttendance() {

    const name = document
        .getElementById("searchBox")
        .value
        .toLowerCase();

    fetch("/attendance/")
    .then(response => response.json())
    .then(data => {

        const table = document.getElementById("attendanceTable");

        table.innerHTML = "";

        data
        .filter(attendance =>
            attendance.student_name
            .toLowerCase()
            .includes(name)
        )
        .forEach(attendance => {

            table.innerHTML += `

            <tr>

                <td>${attendance.attendance_id}</td>

                <td>${attendance.student_name}</td>

                <td>${attendance.subject_name}</td>

                <td>${attendance.attendance_date}</td>

                <td>${attendance.status}</td>

                <td>

                    <button onclick="editAttendance(${attendance.attendance_id})">
                        Edit
                    </button>

                    <button onclick="deleteAttendance(${attendance.attendance_id})">
                        Delete
                    </button>

                </td>

            </tr>

            `;

        });

    });

}
document
.getElementById("searchBox")
.addEventListener("keyup", searchAttendance);
// ----------------------------
// Initial Load
// ----------------------------

loadAttendance();

loadStudents();

loadSubjects();