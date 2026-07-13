
checkLogin();
let currentPage = 1;

const pageSize = 30;
async function loadTeachers(){

    const response =
        await fetch("/teachers/");

    const data =
        await response.json();

    const select =
        document.getElementById("teacher_id");

    select.innerHTML="";

    data.forEach(t=>{

        select.innerHTML+=`
            <option value="${t.teacher_id}">
                ${t.teacher_name}
            </option>
        `;

    });

}
async function loadSubjects(){

    const response =
        await fetch("/subjects/");

    const data =
        await response.json();

    const select =
        document.getElementById("subject_id");

    select.innerHTML="";

    data.forEach(s=>{

        select.innerHTML+=`
            <option value="${s.subject_id}">
                ${s.subject_name}
            </option>
        `;

    });

}
async function loadAssignments(){

    const response =
        await fetch(`/teacher-subjects/?page=${currentPage}&page_size=${pageSize}`);

    const data =
        await response.json();

    const table =
        document.getElementById("assignmentTable");

    table.innerHTML="";

    data.forEach(a=>{

        table.innerHTML+=`

        <tr>

        <td>${a.assignment_id}</td>

        <td>${a.teacher_name}</td>

        <td>${a.subject_name}</td>

        <td>

        <button onclick="editAssignment(${a.assignment_id})">

        Edit

        </button>

        <button onclick="deleteAssignment(${a.assignment_id})">

        Delete

        </button>

        </td>

        </tr>
    
        `;

    });
    document.getElementById("pageNumber").innerText =
    currentPage;

}
async function saveAssignment(){

    const body={

        teacher_id:
            parseInt(document.getElementById("teacher_id").value),

        subject_id:
            parseInt(document.getElementById("subject_id").value)

    };

    await fetch("/teacher-subjects/",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify(body)

    });

    clearForm();

    loadAssignments();
    loadDashboard();

}
async function editAssignment(id){

    const response=
        await fetch(`/teacher-subjects/${id}`);

    const data=
        await response.json();

    document.getElementById("assignment_id").value=
        data.assignment_id;

    document.getElementById("teacher_id").value=
        data.teacher_id;

    document.getElementById("subject_id").value=
        data.subject_id;

}
async function updateAssignment(){

    const id=
        document.getElementById("assignment_id").value;

    const body={

        teacher_id:
            parseInt(document.getElementById("teacher_id").value),

        subject_id:
            parseInt(document.getElementById("subject_id").value)

    };

    await fetch(`/teacher-subjects/${id}`,{

        method:"PUT",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify(body)

    });

    clearForm();

    loadAssignments();
    loadDashboard();

}
async function deleteAssignment(id){

    if(!confirm("Delete Assignment?"))
        return;

    await fetch(`/teacher-subjects/${id}`,{

        method:"DELETE"

    });

    loadAssignments();
    loadDashboard();

}
async function searchAssignment(){

    const keyword=
        document.getElementById("search").value;

    if(keyword==""){

        loadAssignments();
        loadDashboard();

        return;

    }

    const response=
        await fetch(`/teacher-subjects/search/${keyword}`);

    const data=
        await response.json();

    const table=
        document.getElementById("assignmentTable");

    table.innerHTML="";

    data.forEach(a=>{

        table.innerHTML+=`
        <tr>
            <td>${a.assignment_id}</td>
            <td>${a.teacher_name}</td>
            <td>${a.subject_name}</td>
            <td>
                <button onclick="editAssignment(${a.assignment_id})">Edit</button>
                <button onclick="deleteAssignment(${a.assignment_id})">Delete</button>
            </td>
        </tr>
        `;

    });

   
}
 function clearForm(){

    document.getElementById("assignment_id").value="";

    document.getElementById("teacher_id").selectedIndex=0;

    document.getElementById("subject_id").selectedIndex=0;

}
async function loadDashboard(){

    let response =
        await fetch("/teacher-subjects/dashboard/total-assignments");

    let data =
        await response.json();

    document.getElementById("totalAssignments").innerText =
        data.total_assignments;


    response =
        await fetch("/teacher-subjects/dashboard/total-teachers");

    data =
        await response.json();

    document.getElementById("totalTeachers").innerText =
        data.total_teachers;


    response =
        await fetch("/teacher-subjects/dashboard/total-subjects");

    data =
        await response.json();

    document.getElementById("totalSubjects").innerText =
        data.total_subjects;

}
function nextPage(){

    currentPage++;

    loadAssignments();

}

function previousPage(){

    if(currentPage>1){

        currentPage--;

        loadAssignments();

    }

}
loadTeachers()
loadSubjects()
loadAssignments()
loadDashboard();