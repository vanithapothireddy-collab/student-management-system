// ==========================================
// Department Management
// departments.js
// Part 1
// ==========================================
checkLogin();
let currentPage = 1;
const pageSize = 10;

let sortColumn = "department_id";
let sortOrder = "ASC";

// ==========================================
// Render Departments
// ==========================================

function renderDepartments(data){

    const table =
        document.getElementById("departmentTable");

    table.innerHTML = "";

    if(data.length === 0){

        table.innerHTML = `

        <tr>

            <td colspan="3" style="text-align:center">

                No Departments Found

            </td>

        </tr>

        `;

        return;

    }

    data.forEach(department=>{

        table.innerHTML += `

        <tr>

            <td>${department.department_id}</td>

            <td>${department.department_name}</td>

            <td>

                <button onclick="editDepartment(${department.department_id})">

                    Edit

                </button>

                <button onclick="deleteDepartment(${department.department_id})">

                    Delete

                </button>

            </td>

        </tr>

        `;

    });

}

// ==========================================
// Load Departments
// ==========================================

async function loadDepartments(page = 1){

    try{

        const response = await fetch(

            `/departments?page=${page}&page_size=${pageSize}&sort_by=${sortColumn}&sort_order=${sortOrder}`

        );

        const data = await response.json();

        renderDepartments(data);

        currentPage = page;

        document.getElementById("pageNumber").innerText =
            "Page " + currentPage;

    }

    catch(error){

        console.error(error);

    }

}

// ==========================================
// Pagination
// ==========================================

function nextPage(){

    currentPage++;

    loadDepartments(currentPage);

}

function previousPage(){

    if(currentPage > 1){

        currentPage--;

        loadDepartments(currentPage);

    }

}

// ==========================================
// Sorting
// ==========================================

function sortDepartments(column){

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

    loadDepartments(currentPage);

}

// ==========================================
// Search
// ==========================================

async function searchDepartment(){

    try{

        const name =
            document.getElementById("searchBox").value.trim();

        const response = await fetch(

            `/departments/search/?name=${encodeURIComponent(name)}`

        );

        const data = await response.json();

        renderDepartments(data);

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

    loadDepartments(1);

}
// ==========================================
// Show Add Department Form
// ==========================================

document.getElementById("addDepartmentBtn").onclick = function () {

    document.getElementById("departmentForm").style.display = "block";

    document.getElementById("department_name").value = "";

    document.getElementById("saveBtn").innerText =
        "Save Department";

    document.getElementById("saveBtn").onclick =
        saveDepartment;

};

// ==========================================
// Save Department
// ==========================================

async function saveDepartment(){

    try{

        const department = {

            department_name:
                document.getElementById("department_name").value.trim()

        };

        const response = await fetch(

            "/departments/",

            {

                method: "POST",

                headers:{

                    "Content-Type":"application/json"

                },

                body: JSON.stringify(department)

            }

        );

        const result = await response.json();

        alert(result.message);

        document.getElementById("departmentForm").style.display =
            "none";

        loadDepartments(currentPage);

    }

    catch(error){

        console.error(error);

        alert("Unable to save department.");

    }

}

// ==========================================
// Edit Department
// ==========================================
// ==========================================
// Edit Department
// ==========================================

async function editDepartment(id){

    try{

        const response = await fetch(

            `/departments/${id}`

        );

        const department = await response.json();

        document.getElementById("departmentForm").style.display = "block";

        document.getElementById("department_name").value =
            department.department_name;

        document.getElementById("saveBtn").innerText =
            "Update Department";

        document.getElementById("saveBtn").onclick = function(){

            updateDepartment(id);

        };

    }

    catch(error){

        console.error(error);

        alert("Unable to load department.");

    }

}
// ==========================================
// Update Department
// ==========================================

async function updateDepartment(id){

    const department = {

        department_name:
            document.getElementById("department_name").value

    };

    const response = await fetch(

        `/departments/${id}`,

        {

            method: "PUT",

            headers:{

                "Content-Type":"application/json"

            },

            body: JSON.stringify(department)

        }

    );

    const result = await response.json();

    alert(result.message);

    document.getElementById("departmentForm").style.display = "none";

    document.getElementById("saveBtn").innerText =
        "Save Department";

    document.getElementById("saveBtn").onclick =
        saveDepartment;

    loadDepartments();

}
// ==========================================
// Delete Department
// ==========================================

async function deleteDepartment(id){

    const ok = confirm(

        "Are you sure you want to delete this department?"

    );

    if(!ok){

        return;

    }

    try{

        const response = await fetch(

            `/departments/${id}`,

            {

                method:"DELETE"

            }

        );

        const result = await response.json();

        alert(result.message);

        loadDepartments(currentPage);

    }

    catch(error){

        console.error(error);

        alert("Delete Failed");

    }

}

// ==========================================
// Search on Enter
// ==========================================

document
.getElementById("searchBox")
.addEventListener(

    "keyup",

    function(event){

        if(event.key === "Enter"){

            searchDepartment();

        }

    }

);

// ==========================================
// Initial Load
// ==========================================

window.onload = function(){

    loadDepartments(1);

};