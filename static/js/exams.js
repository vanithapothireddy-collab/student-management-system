// ================================
// Load Dashboard Cards
// ================================
checkLogin();
async function loadExamDashboard() {

    try {

        const total = await fetch("/exams/total");
        const totalData = await total.json();

        document.getElementById("total-exams").innerText =
            totalData.total_exams;

        const upcoming = await fetch("/exams/upcoming");
        const upcomingData = await upcoming.json();

        document.getElementById("upcoming-exams").innerText =
            upcomingData.upcoming_exams;

        const completed = await fetch("/exams/completed");
        const completedData = await completed.json();

        document.getElementById("completed-exams").innerText =
            completedData.completed_exams;

        const subjects = await fetch("/exams/subjects-covered");
        const subjectData = await subjects.json();

        document.getElementById("subject-covered").innerText =
            subjectData.subjects_covered;

    }

    catch(error){

        console.log(error);

    }

}


// ================================
// Load Subjects
// ================================

async function loadSubjects(){

    const response = await fetch("/subjects/");

    const subjects = await response.json();

    const select = document.getElementById("subject_id");

    select.innerHTML =
    `<option value="">Select Subject</option>`;

    subjects.forEach(subject=>{

        select.innerHTML +=
        `
        <option value="${subject.subject_id}">
            ${subject.subject_name}
        </option>
        `;

    });

}


// ================================
// Load Exams
// ================================

async function loadExams(){

    const response = await fetch("/exams/");

    const exams = await response.json();

    const table = document.getElementById("examTable");

    table.innerHTML = "";

    exams.forEach(exam=>{

        table.innerHTML +=
        `
        <tr>

            <td>${exam.exam_id}</td>

            <td>${exam.subject_name}</td>

            <td>${exam.exam_name}</td>

            <td>${exam.exam_date}</td>

            <td>

                <button onclick="editExam(${exam.exam_id})">
                Edit
                </button>

                <button onclick="deleteExam(${exam.exam_id})">
                Delete
                </button>

            </td>

        </tr>

        `;

    });

}


// ================================
// Save Exam
// ================================

async function saveExam(){

    const subject_id =
    document.getElementById("subject_id").value;

    const exam_name =
    document.getElementById("exam_name").value;

    const exam_date =
    document.getElementById("exam_date").value;

    if(subject_id=="" || exam_name=="" || exam_date==""){

        alert("Fill all fields");

        return;

    }

    await fetch("/exams/",{

        method:"POST",

        headers:{

            "Content-Type":"application/json"

        },

        body:JSON.stringify({

            subject_id:Number(subject_id),

            exam_name:exam_name,

            exam_date:exam_date

        })

    });

    clearForm();

    loadExams();

    loadExamDashboard();

}


// ================================
// Edit Exam
// ================================

async function editExam(id){

    const response =
    await fetch("/exams/"+id);

    const exam =
    await response.json();

    document.getElementById("exam_id").value =
    exam.exam_id;

    document.getElementById("subject_id").value =
    exam.subject_id;

    document.getElementById("exam_name").value =
    exam.exam_name;

    document.getElementById("exam_date").value =
    exam.exam_date;

}


// ================================
// Update Exam
// ================================

async function updateExam(){

    const exam_id =
    document.getElementById("exam_id").value;

    const subject_id =
    document.getElementById("subject_id").value;

    const exam_name =
    document.getElementById("exam_name").value;

    const exam_date =
    document.getElementById("exam_date").value;

    await fetch("/exams/"+exam_id,{

        method:"PUT",

        headers:{

            "Content-Type":"application/json"

        },

        body:JSON.stringify({

            subject_id:Number(subject_id),

            exam_name:exam_name,

            exam_date:exam_date

        })

    });

    clearForm();

    loadExams();

    loadExamDashboard();

}


// ================================
// Delete Exam
// ================================

async function deleteExam(id){

    if(!confirm("Delete this exam?")){

        return;

    }

    await fetch("/exams/"+id,{

        method:"DELETE"

    });

    loadExams();

    loadExamDashboard();

}


// ================================
// Search Exam
// ================================

async function searchExam(){

    const keyword =
    document.getElementById("searchExam").value;

    if(keyword==""){

        loadExams();

        return;

    }

    const response =
    await fetch("/exams/search/"+keyword);

    const exams =
    await response.json();

    const table =
    document.getElementById("examTable");

    table.innerHTML="";

    exams.forEach(exam=>{

        table.innerHTML +=

        `
        <tr>

            <td>${exam.exam_id}</td>

            <td>${exam.subject_name}</td>

            <td>${exam.exam_name}</td>

            <td>${exam.exam_date}</td>

            <td>

                <button onclick="editExam(${exam.exam_id})">
                Edit
                </button>

                <button onclick="deleteExam(${exam.exam_id})">
                Delete
                </button>

            </td>

        </tr>

        `;

    });

}


// ================================
// Clear Form
// ================================

function clearForm(){

    document.getElementById("exam_id").value="";

    document.getElementById("subject_id").value="";

    document.getElementById("exam_name").value="";

    document.getElementById("exam_date").value="";

}


// ================================
// Initial Load
// ================================

loadSubjects();

loadExams();

loadExamDashboard();