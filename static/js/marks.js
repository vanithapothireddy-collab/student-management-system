// ----------------------
// Load Marks
// ----------------------
checkLogin();
function loadMarks() {

    fetch("/marks/")
        .then(response => response.json())
        .then(data => {

            const table = document.getElementById("marksTable");

            table.innerHTML = "";

            data.forEach(mark => {

                table.innerHTML += `
                <tr>
                    <td>${mark.mark_id}</td>
                    <td>${mark.student_name}</td>
                    <td>${mark.exam_name}</td>
                    <td>${mark.marks}</td>
                    <td>${mark.grade}</td>
                    <td>
                        <button onclick="editMark(${mark.mark_id})">Edit</button>
                        <button onclick="deleteMark(${mark.mark_id})">Delete</button>
                    </td>
                </tr>
                `;

            });

        });

}

// ----------------------
// Load Students
// ----------------------

function loadStudents() {

    fetch("/students/")
        .then(response => response.json())
        .then(data => {

            const select = document.getElementById("student_id");

            if (!select) return;

            select.innerHTML = '<option value="">Select Student</option>';

            data.forEach(student => {

                select.innerHTML += `
                    <option value="${student.student_id}">
                        ${student.student_name}
                    </option>
                `;

            });

        })
        .catch(error => console.error(error));

}

// ----------------------
// Load Exams
// ----------------------

function loadExams() {

    fetch("/exams/")
        .then(response => response.json())
        .then(data => {

            const select = document.getElementById("exam_id");

            if (!select) return;

            select.innerHTML = '<option value="">Select Exam</option>';

            data.forEach(exam => {

                select.innerHTML += `
                    <option value="${exam.exam_id}">
                        ${exam.exam_name}
                    </option>
                `;

            });

        });

}

// ----------------------
// Add Button
// ----------------------

const addBtn = document.getElementById("addMarkBtn");

if (addBtn) {

    addBtn.onclick = function () {

        const form = document.getElementById("markForm");

        if (form)
            form.style.display = "block";

        document.getElementById("saveBtn").innerText = "Save Marks";

        document.getElementById("saveBtn").onclick = saveMark;

    };

}

// ----------------------
// Save
// ----------------------

async function saveMark() {

    const mark = {

        student_id: parseInt(document.getElementById("student_id").value),

        exam_id: parseInt(document.getElementById("exam_id").value),

        marks_obtained: parseFloat(document.getElementById("marks_obtained").value)

    };

    const response = await fetch("/marks/", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(mark)

    });

    const result = await response.json();

    alert(result.message);

    loadMarks();

    const form = document.getElementById("markForm");

    if (form)
        form.style.display = "none";

}

// ----------------------
// Edit
// ----------------------

async function editMark(id) {

    const response = await fetch(`/marks/${id}`);

    const mark = await response.json();

    const form = document.getElementById("markForm");

    if (form)
        form.style.display = "block";

    document.getElementById("student_id").value = mark.student_id;

    document.getElementById("exam_id").value = mark.exam_id;

    document.getElementById("marks_obtained").value = mark.marks_obtained;

    document.getElementById("saveBtn").innerText = "Update Marks";

    document.getElementById("saveBtn").onclick = function () {

        updateMark(id);

    };

}

// ----------------------
// Update
// ----------------------

async function updateMark(id) {

    const mark = {

        student_id: parseInt(document.getElementById("student_id").value),

        exam_id: parseInt(document.getElementById("exam_id").value),

        marks_obtained: parseFloat(document.getElementById("marks_obtained").value)

    };

    const response = await fetch(`/marks/${id}`, {

        method: "PUT",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(mark)

    });

    const result = await response.json();

    alert(result.message);

    loadMarks();

    const form = document.getElementById("markForm");

    if (form)
        form.style.display = "none";

    document.getElementById("saveBtn").innerText = "Save Marks";

    document.getElementById("saveBtn").onclick = saveMark;

}

// ----------------------
// Delete
// ----------------------

async function deleteMark(id) {

    if (!confirm("Delete this mark?"))
        return;

    const response = await fetch(`/marks/${id}`, {

        method: "DELETE"

    });

    const result = await response.json();

    alert(result.message);

    loadMarks();

}

// ----------------------
// Search
// ----------------------

function searchMarks() {

    const name = document.getElementById("searchBox").value;

    fetch(`/marks/search/${name}`)
        .then(response => response.json())
        .then(data => {

            const table = document.getElementById("marksTable");

            table.innerHTML = "";

            data.forEach(mark => {

                table.innerHTML += `
                <tr>
                    <td>${mark.mark_id}</td>
                    <td>${mark.student_name}</td>
                    <td>${mark.exam_name}</td>
                    <td>${mark.marks}</td>
                    <td>${mark.grade}</td>
                    <td>
                        <button onclick="editMark(${mark.mark_id})">Edit</button>
                        <button onclick="deleteMark(${mark.mark_id})">Delete</button>
                    </td>
                </tr>
                `;

            });

        });

}

// ----------------------
// Initial Load
// ----------------------

const searchBox = document.getElementById("searchBox");

if (searchBox) {

    searchBox.addEventListener("keyup", searchMarks);

}

loadStudents();
loadExams();
loadMarks();