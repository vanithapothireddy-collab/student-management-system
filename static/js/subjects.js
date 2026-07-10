// ==========================================
// Subject Management System
// subjects.js
// ==========================================

let currentPage = 1;
const pageSize = 10;

let sortColumn = "subject_id";
let sortOrder = "ASC";

// ==========================================
// Render Subjects
// ==========================================

function renderSubjects(data) {

    const table = document.getElementById("subjectTable");

    table.innerHTML = "";

    if (data.length === 0) {

        table.innerHTML = `
        <tr>
            <td colspan="3" style="text-align:center;">
                No Subjects Found
            </td>
        </tr>
        `;

        return;
    }

    data.forEach(subject => {

        table.innerHTML += `

        <tr>

            <td>${subject.subject_id}</td>

            <td>${subject.subject_name}</td>

            <td>

                <button onclick="editSubject(${subject.subject_id})">

                    Edit

                </button>

                <button onclick="deleteSubject(${subject.subject_id})">

                    Delete

                </button>

            </td>

        </tr>

        `;

    });

}

// ==========================================
// Load Subjects
// ==========================================

async function loadSubjects(page = 1) {

    try {

        const response = await fetch(

            `/subjects?page=${page}&page_size=${pageSize}&sort_by=${sortColumn}&sort_order=${sortOrder}`

        );

        const data = await response.json();

        renderSubjects(data);

        currentPage = page;

        document.getElementById("pageNumber").innerText =
            `Page ${currentPage}`;

    }

    catch (error) {

        console.error(error);

        alert("Unable to load subjects.");

    }

}

// ==========================================
// Pagination
// ==========================================

function nextPage() {

    currentPage++;

    loadSubjects(currentPage);

}

function previousPage() {

    if (currentPage > 1) {

        currentPage--;

        loadSubjects(currentPage);

    }

}

// ==========================================
// Sorting
// ==========================================

function sortSubjects(column) {

    if (sortColumn === column) {

        sortOrder =
            sortOrder === "ASC"
            ? "DESC"
            : "ASC";

    }

    else {

        sortColumn = column;

        sortOrder = "ASC";

    }

    loadSubjects(currentPage);

}

// ==========================================
// Search
// ==========================================

async function searchSubject() {

    try {

        const name =
            document.getElementById("searchBox").value.trim();

        const response = await fetch(

            `/subjects/search/?name=${encodeURIComponent(name)}`

        );

        const data = await response.json();

        renderSubjects(data);

    }

    catch (error) {

        console.error(error);

        alert("Search Failed");

    }

}

// ==========================================
// Reset Search
// ==========================================

function resetSearch() {

    document.getElementById("searchBox").value = "";

    loadSubjects(1);

}

// ==========================================
// Show Add Form
// ==========================================

document.getElementById("addSubjectBtn").onclick = function () {

    document.getElementById("subjectForm").style.display = "block";

    document.getElementById("subject_name").value = "";

    document.getElementById("saveBtn").innerText =
        "Save Subject";

    document.getElementById("saveBtn").onclick =
        saveSubject;

};

// ==========================================
// Save Subject
// ==========================================

async function saveSubject() {

    const subject = {

        subject_name:
            document.getElementById("subject_name").value

    };

    const response = await fetch("/subjects/", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(subject)

    });

    const result = await response.json();

    alert(result.message);

    document.getElementById("subjectForm").style.display =
        "none";

    loadSubjects(currentPage);

}

// ==========================================
// Edit Subject
// ==========================================

async function editSubject(id) {

    const response =
        await fetch(`/subjects/${id}`);

    const subject =
        await response.json();

    document.getElementById("subjectForm").style.display =
        "block";

    document.getElementById("subject_name").value =
        subject.subject_name;

    document.getElementById("saveBtn").innerText =
        "Update Subject";

    document.getElementById("saveBtn").onclick =
        function () {

            updateSubject(id);

        };

}

// ==========================================
// Update Subject
// ==========================================

async function updateSubject(id) {

    const subject = {

        subject_name:
            document.getElementById("subject_name").value

    };

    const response =
        await fetch(`/subjects/${id}`, {

            method: "PUT",

            headers: {

                "Content-Type":
                    "application/json"

            },

            body:
                JSON.stringify(subject)

        });

    const result =
        await response.json();

    alert(result.message);

    document.getElementById("subjectForm").style.display =
        "none";

    loadSubjects(currentPage);

}

// ==========================================
// Delete Subject
// ==========================================

async function deleteSubject(id) {

    const ok =
        confirm("Delete this subject?");

    if (!ok)
        return;

    const response =
        await fetch(`/subjects/${id}`, {

            method: "DELETE"

        });

    const result =
        await response.json();

    alert(result.message);

    loadSubjects(currentPage);

}

// ==========================================
// Search on Enter Key
// ==========================================

document
    .getElementById("searchBox")
    .addEventListener("keyup", function (event) {

        if (event.key === "Enter") {

            searchSubject();

        }

    });

// ==========================================
// Initial Load
// ==========================================

loadSubjects();