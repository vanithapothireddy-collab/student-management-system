checkLogin();

// -----------------------------
// Dashboard Cards
// -----------------------------
async function loadTeacherDashboard() {

    try {

        // Total Teachers
        let response = await fetch("/teachers/dashboard/total-teachers");
        let data = await response.json();

        console.log("Teacher Dashboard:", data);

        const totalCard = document.getElementById("totalTeachers");

        if (totalCard) {
            totalCard.textContent = data.total_teachers ?? 0;
        }

        // Assigned Subjects
        response = await fetch("/teachers/dashboard/assigned-subjects");
        data = await response.json();

        console.log("Assigned Subjects:", data);

        const subjectCard = document.getElementById("assignedSubjects");

        if (subjectCard) {
            subjectCard.textContent = data.assigned_subjects ?? 0;
        }

    } catch (err) {
        console.error("Teacher Dashboard Error:", err);
    }

}

// -----------------------------
// Load Teachers
// -----------------------------
async function loadTeachers() {

    try {

        const response = await fetch("/teachers/");
        const data = await response.json();

        const table = document.getElementById("teacherTable");

        if (!table) return;

        table.innerHTML = "";

        data.forEach(t => {

            table.innerHTML += `
            <tr>
                <td>${t.teacher_id}</td>
                <td>${t.teacher_name}</td>
                <td>${t.subject_name}</td>
                <td>${t.email}</td>
                <td>
                    <button onclick="editTeacher(${t.teacher_id})">Edit</button>
                    <button onclick="deleteTeacher(${t.teacher_id})">Delete</button>
                </td>
            </tr>
            `;

        });

    } catch (err) {
        console.error("Load Teachers Error:", err);
    }

}

// -----------------------------
// Load Subjects
// -----------------------------
async function loadSubjects() {

    try {

        const response = await fetch("/subjects/");
        const subjects = await response.json();

        const select = document.getElementById("subject_name");

        if (!select) return;

        select.innerHTML = "";

        subjects.forEach(subject => {

            select.innerHTML += `
                <option value="${subject.subject_name}">
                    ${subject.subject_name}
                </option>
            `;

        });

    } catch (err) {
        console.error(err);
    }

}

// -----------------------------
// Save Teacher
// -----------------------------
async function saveTeacher() {

    const body = {

        teacher_name: document.getElementById("teacher_name").value,
        subject_name: document.getElementById("subject_name").value,
        email: document.getElementById("email").value

    };

    await fetch("/teachers/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(body)

    });

    clearForm();
    loadTeachers();
    loadTeacherDashboard();

}

// -----------------------------
// Edit Teacher
// -----------------------------
async function editTeacher(id) {

    const response = await fetch(`/teachers/${id}`);
    const teacher = await response.json();

    document.getElementById("teacher_id").value = teacher.teacher_id;
    document.getElementById("teacher_name").value = teacher.teacher_name;
    document.getElementById("subject_name").value = teacher.subject_name;
    document.getElementById("email").value = teacher.email;

}

// -----------------------------
// Update Teacher
// -----------------------------
async function updateTeacher() {

    const id = document.getElementById("teacher_id").value;

    const body = {

        teacher_name: document.getElementById("teacher_name").value,
        subject_name: document.getElementById("subject_name").value,
        email: document.getElementById("email").value

    };

    await fetch(`/teachers/${id}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(body)

    });

    clearForm();
    loadTeachers();
    loadTeacherDashboard();

}

// -----------------------------
// Delete Teacher
// -----------------------------
async function deleteTeacher(id) {

    if (!confirm("Delete this teacher?")) return;

    await fetch(`/teachers/${id}`, {
        method: "DELETE"
    });

    loadTeachers();
    loadTeacherDashboard();

}

// -----------------------------
// Search Teacher
// -----------------------------
async function searchTeacher() {

    const keyword = document.getElementById("searchTeacher").value;

    if (keyword === "") {
        loadTeachers();
        return;
    }

    const response = await fetch(`/teachers/search/${keyword}`);
    const data = await response.json();

    const table = document.getElementById("teacherTable");

    table.innerHTML = "";

    data.forEach(t => {

        table.innerHTML += `
        <tr>
            <td>${t.teacher_id}</td>
            <td>${t.teacher_name}</td>
            <td>${t.subject_name}</td>
            <td>${t.email}</td>
            <td>
                <button onclick="editTeacher(${t.teacher_id})">Edit</button>
                <button onclick="deleteTeacher(${t.teacher_id})">Delete</button>
            </td>
        </tr>
        `;

    });

}

// -----------------------------
// Clear Form
// -----------------------------
function clearForm() {

    document.getElementById("teacher_id").value = "";
    document.getElementById("teacher_name").value = "";
    document.getElementById("subject_name").selectedIndex = 0;
    document.getElementById("email").value = "";

}

// -----------------------------
// Page Load
// -----------------------------
loadSubjects();
loadTeachers();
loadTeacherDashboard();