// ==========================================
// Student Management System
// students.js
// Part 1
// ==========================================
checkLogin();
let currentPage = 1;
const pageSize = 10;

let sortColumn = "student_id";
let sortOrder = "ASC";

// ==========================================
// Render Students
// ==========================================

function renderStudents(data) {

    const table = document.getElementById("studentTable");

    table.innerHTML = "";

    if (data.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="6" style="text-align:center;">
                    No Students Found
                </td>
            </tr>
        `;

        return;
    }

    data.forEach(student => {

        table.innerHTML += `

        <tr>

            <td>${student.student_id}</td>

            <td>${student.student_name}</td>

            <td>${student.gender === "M" ? "Male" : "Female"}</td>

            <td>${student.department_name}</td>

            <td>${student.batch_name}</td>

            <td>

                <button onclick="editStudent(${student.student_id})">
                    Edit
                </button>

                <button onclick="deleteStudent(${student.student_id})">
                    Delete
                </button>

            </td>

        </tr>

        `;

    });

}

// ==========================================
// Load Students
// ==========================================

async function loadStudents(page = 1) {

    try {

        const response = await fetch(

            `/students?page=${page}&page_size=${pageSize}&sort_by=${sortColumn}&sort_order=${sortOrder}`

        );

        const data = await response.json();

        renderStudents(data);

        currentPage = page;

        document.getElementById("pageNumber").innerText =
            "Page " + currentPage;

    }

    catch(error){

        console.error(error);

        alert("Unable to load students.");

    }

}

// ==========================================
// Pagination
// ==========================================

function nextPage(){

    currentPage++;

    loadStudents(currentPage);

}

function previousPage(){

    if(currentPage > 1){

        currentPage--;

        loadStudents(currentPage);

    }

}

// ==========================================
// Sorting
// ==========================================

function sortStudents(column){

    if(sortColumn === column){

        sortOrder =
            sortOrder === "ASC"
            ? "DESC"
            : "ASC";

    }

    else{

        sortColumn = column;

        sortOrder = "ASC";

    }

    loadStudents(currentPage);

}

// ==========================================
// Simple Search
// ==========================================

async function searchStudent(){

    try{

        const name =
            document.getElementById("searchBox").value.trim();

        const response =
            await fetch(

                `/students/search/?name=${encodeURIComponent(name)}`

            );

        const data =
            await response.json();

        renderStudents(data);

    }

    catch(error){

        console.error(error);

    }

}

// ==========================================
// Advanced Search
// ==========================================

async function advancedSearch(){

    try{

        const name =
            document.getElementById("searchName").value;

        const gender =
            document.getElementById("searchGender").value;

        const department =
            document.getElementById("searchDepartment").value;

        const batch =
            document.getElementById("searchBatch").value;

        const response = await fetch(

`/students/search/?name=${encodeURIComponent(name)}&gender=${encodeURIComponent(gender)}&department=${encodeURIComponent(department)}&batch=${encodeURIComponent(batch)}`

        );

        const data =
            await response.json();

        renderStudents(data);

    }

    catch(error){

        console.error(error);

    }

}

// ==========================================
// Reset Search
// ==========================================

function resetSearch(){

    document.getElementById("searchBox").value="";

    document.getElementById("searchName").value="";

    document.getElementById("searchGender").value="";

    document.getElementById("searchDepartment").value="";

    document.getElementById("searchBatch").value="";

    loadStudents(1);

}

// ==========================================
// Load Departments
// ==========================================

async function loadDepartments(){

    try{

        const response =
            await fetch("/departments/");

        const departments =
            await response.json();

        const select =
            document.getElementById("department_id");

        select.innerHTML =
            '<option value="">Select Department</option>';

        departments.forEach(department=>{

            select.innerHTML += `

                <option value="${department.department_id}">

                    ${department.department_name}

                </option>

            `;

        });

    }

    catch(error){

        console.error(error);

    }

}

// ==========================================
// Load Batches
// ==========================================

async function loadBatches(){

    try{

        const response =
            await fetch("/batches/");

        const batches =
            await response.json();

        const select =
            document.getElementById("batch_id");

        select.innerHTML =
            '<option value="">Select Batch</option>';

        batches.forEach(batch=>{

            select.innerHTML += `

                <option value="${batch.batch_id}">

                    ${batch.batch_name}

                </option>

            `;

        });

    }

    catch(error){

        console.error(error);

    }

}
// ==========================================
// Show Add Student Form
// ==========================================

document.getElementById("addStudentBtn").onclick = function () {

    document.getElementById("studentForm").style.display = "block";

    document.getElementById("saveBtn").innerText = "Save Student";

    document.getElementById("saveBtn").onclick = saveStudent;

};

// ==========================================
// Save Student
// ==========================================

async function saveStudent() {

    try {

        const student = {

            student_name: document.getElementById("student_name").value.trim(),

            gender: document.getElementById("gender").value,

            department_id: parseInt(
                document.getElementById("department_id").value
            ),

            batch_id: parseInt(
                document.getElementById("batch_id").value
            )

        };

        const response = await fetch("/students/", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(student)

        });

        const result = await response.json();

        alert(result.message);

        document.getElementById("studentForm").style.display = "none";

        loadStudents(currentPage);

    }

    catch(error){

        console.error(error);

        alert("Unable to save student.");

    }

}

// ==========================================
// Edit Student
// ==========================================

async function editStudent(id){

    try{

        const response =
            await fetch(`/students/${id}`);

        const student =
            await response.json();

        document.getElementById("studentForm").style.display =
            "block";

        document.getElementById("student_name").value =
            student.student_name;

        document.getElementById("gender").value =
            student.gender;

        document.getElementById("department_id").value =
            student.department_id;

        document.getElementById("batch_id").value =
            student.batch_id;

        document.getElementById("saveBtn").innerText =
            "Update Student";

        document.getElementById("saveBtn").onclick =
            function(){

                updateStudent(id);

            };

    }

    catch(error){

        console.error(error);

    }

}

// ==========================================
// Update Student
// ==========================================

async function updateStudent(id){

    try{

        const student = {

            student_name:
                document.getElementById("student_name").value.trim(),

            gender:
                document.getElementById("gender").value,

            department_id:
                parseInt(document.getElementById("department_id").value),

            batch_id:
                parseInt(document.getElementById("batch_id").value)

        };

        const response = await fetch(

            `/students/${id}`,

            {

                method: "PUT",

                headers: {

                    "Content-Type":"application/json"

                },

                body: JSON.stringify(student)

            }

        );

        const result =
            await response.json();

        alert(result.message);

        document.getElementById("studentForm").style.display =
            "none";

        document.getElementById("saveBtn").innerText =
            "Save Student";

        document.getElementById("saveBtn").onclick =
            saveStudent;

        loadStudents(currentPage);

    }

    catch(error){

        console.error(error);

    }

}

// ==========================================
// Delete Student
// ==========================================

async function deleteStudent(id){

    const ok = confirm(

        "Are you sure you want to delete this student?"

    );

    if(!ok){

        return;

    }

    try{

        const response = await fetch(

            `/students/${id}`,

            {

                method:"DELETE"

            }

        );

        const result =
            await response.json();

        alert(result.message);

        loadStudents(currentPage);

    }

    catch(error){

        console.error(error);

    }

}

// ==========================================
// Search Box (Enter Key)
// ==========================================

document

.getElementById("searchBox")

.addEventListener(

    "keyup",

    function(event){

        if(event.key === "Enter"){

            searchStudent();

        }

    }

);

// ==========================================
// Initial Page Load
// ==========================================

window.onload = function(){

    loadDepartments();

    loadBatches();

    loadStudents(1);

};