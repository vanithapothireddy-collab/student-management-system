async function loadFees() {

    console.log("loadFees started");

    const response = await fetch("/fees/");
    const data = await response.json();

    console.log(data);

    const table = document.getElementById("feeTable");

    table.innerHTML = "";

    data.forEach(fee => {

        console.log(fee);

        table.innerHTML += `
        <tr>
            <td>${fee.fee_id}</td>
            <td>${fee.student_name}</td>
            <td>₹${fee.total_fee}</td>
            <td>₹${fee.paid_fee}</td>
            <td>₹${fee.pending_fee}</td>
            <td>${fee.status}</td>
            <td>
                <button onclick="editFee(${fee.fee_id})">Edit</button>
                <button onclick="deleteFee(${fee.fee_id})">Delete</button>
            </td>
        </tr>
        `;
    });

    console.log("loadFees finished");
}


// -----------------------------
// Load Students
// -----------------------------

async function loadStudents() {

    const response = await fetch("/students/");

    const students = await response.json();

    const select = document.getElementById("student_id");

    select.innerHTML =
        `<option value="">Select Student</option>`;

    students.forEach(student => {

        select.innerHTML += `

            <option value="${student.student_id}">

                ${student.student_name}

            </option>

        `;

    });

}


// -----------------------------
// Save Fee
// -----------------------------
// -----------------------------
// Load Fee Dashboard
// -----------------------------

async function loadFeeDashboard() {

    try {

        // Total Collection
        const totalResponse =
            await fetch("/fees/dashboard/total-collection");

        const totalData =
            await totalResponse.json();

        document.getElementById("totalCollection").innerText =
            "₹" + totalData.total_collection;


        // Pending Collection
        const pendingResponse =
            await fetch("/fees/dashboard/pending-collection");

        const pendingData =
            await pendingResponse.json();

        document.getElementById("pendingCollection").innerText =
            "₹" + pendingData.pending_collection;


        // Paid Students
        const paidResponse =
            await fetch("/fees/dashboard/paid-students");

        const paidData =
            await paidResponse.json();

        document.getElementById("paidStudents").innerText =
            paidData.paid_students;


        // Pending Students
        const pendingStudentResponse =
            await fetch("/fees/dashboard/pending-students");

        const pendingStudentData =
            await pendingStudentResponse.json();

        document.getElementById("pendingStudents").innerText =
            pendingStudentData.pending_students;

    }

    catch (err) {

        console.error("Fee Dashboard Error:", err);

    }

}

async function saveFee() {

    const body = {

        student_id:
            parseInt(document.getElementById("student_id").value),

        total_fee:
            parseFloat(document.getElementById("total_fee").value),

        paid_fee:
            parseFloat(document.getElementById("paid_fee").value),

        status:
            document.getElementById("status").value

    };

    await fetch("/fees/", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(body)

    });
clearForm();

await loadFees();
await loadFeeDashboard();
await loadFeeStatistics();
await loadPaymentReport();

}
// -----------------------------
// Edit Fee
// -----------------------------
async function editFee(id) {

    const response = await fetch(`/fees/${id}`);
    const fee = await response.json();

    document.getElementById("fee_id").value = fee.fee_id;

    document.getElementById("student_id").value = fee.student_id;

    document.getElementById("total_fee").value = fee.total_fee;

    // User enters NEW payment only
    document.getElementById("paid_fee").value = "";

    document.getElementById("pending_fee").value =
        fee.total_fee - fee.paid_fee;

    document.getElementById("status").value = fee.status;
}


// -----------------------------
// Update Fee
// -----------------------------

async function updateFee() {

    const id = document.getElementById("fee_id").value;

    const body = {

        student_id: parseInt(document.getElementById("student_id").value),

        total_fee: parseFloat(document.getElementById("total_fee").value),

        paid_fee: parseFloat(document.getElementById("paid_fee").value),

        status: document.getElementById("status").value

    };

    const response = await fetch(`/fees/${id}`, {

        method: "PUT",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(body)

    });

    const result = await response.json();

    console.log("Status:", response.status);
    console.log("Response:", result);

    if (!response.ok) {
        alert(result.detail);
        return;
    }

    clearForm();

    await loadFees();
    await loadFeeDashboard();
    await loadFeeStatistics();
    await loadPaymentReport();

}
// -----------------------------
// Delete Fee
// -----------------------------

async function deleteFee(id) {

    if (!confirm("Delete this fee record?"))
        return;

    await fetch(`/fees/${id}`, {

        method: "DELETE"

    });
clearForm();

await loadFees();
await loadFeeDashboard();
await loadFeeStatistics();
await loadPaymentReport();
}
// -----------------------------
// Load Fee Statistics
// -----------------------------

async function loadFeeStatistics() {

    const response =
        await fetch("/fees/statistics");

    const data =
        await response.json();

    const table =
        document.getElementById("feeStatistics");

    table.innerHTML = "";

    table.innerHTML += `
        <tr>

            <td>Total Fee</td>

            <td>₹${data.total_fee}</td>

        </tr>

        <tr>

            <td>Collected Fee</td>

            <td>₹${data.paid_fee}</td>

        </tr>

        <tr>

            <td>Pending Fee</td>

            <td>₹${data.pending_fee}</td>

        </tr>
    `;
}

// -----------------------------
// Search Fee
// -----------------------------

async function searchFee() {

    const keyword =
        document.getElementById("searchFee").value;

    if (keyword === "") {

        loadFees();

        return;

    }

    const response =
        await fetch(`/fees/search/${keyword}`);

    const data =
        await response.json();

    const table =
        document.getElementById("feeTable");

    table.innerHTML = "";

    data.forEach(fee => {

        table.innerHTML += `
        <tr>

            <td>${fee.fee_id}</td>

            <td>${fee.student_name}</td>

            <td>₹${Number(fee.total_fee).toFixed(2)}</td>

            <td>₹${Number(fee.paid_fee).toFixed(2)}</td>

           <td>₹${Number(fee.pending_fee).toFixed(2)}</td>

            <td>${fee.status}</td>

            <td>

                <button onclick="editFee(${fee.fee_id})">
                    Edit
                </button>

                <button onclick="deleteFee(${fee.fee_id})">
                    Delete
                </button>

            </td>

        </tr>
        `;

    });

}


// -----------------------------
// Clear Form
// -----------------------------

function clearForm() {

    document.getElementById("fee_id").value = "";

    document.getElementById("student_id").value = "";

    document.getElementById("total_fee").value = "";

    document.getElementById("paid_fee").value = "";

    document.getElementById("pending_fee").value = "";

    document.getElementById("status").value = "";

}
// -----------------------------
// Auto Calculate Fee Status
// -----------------------------
// -----------------------------
// Auto Calculate Fee Details
// -----------------------------

function calculateStatus() {

    const total =
        parseFloat(document.getElementById("total_fee").value) || 0;

    const paid =
        parseFloat(document.getElementById("paid_fee").value) || 0;

    let pending = total - paid;

    if (pending < 0) {

        pending = 0;

    }

    document.getElementById("pending_fee").value = pending;

    if (pending === 0 && total > 0) {

        document.getElementById("status").value = "Paid";

    }

    else {

        document.getElementById("status").value = "Pending";

    }

}
// -----------------------------
// Payment Report
// -----------------------------

async function loadPaymentReport() {

    const response =
        await fetch("/fees/payment-report");

    const data =
        await response.json();

    const table =
        document.getElementById("paymentReport");

    table.innerHTML = "";

    data.forEach(fee => {

        table.innerHTML += `

            <tr>

                <td>${fee.student_name}</td>

                <td>₹${fee.total_fee}</td>

                <td>₹${fee.paid_fee}</td>

                <td>₹${fee.pending_fee}</td>

                <td>${fee.status}</td>

            </tr>

        `;

    });

}

// -----------------------------
// Initial Load
// -----------------------------

loadStudents();
loadFees();
loadFeeDashboard();
calculateStatus();
loadFeeStatistics();
loadPaymentReport();