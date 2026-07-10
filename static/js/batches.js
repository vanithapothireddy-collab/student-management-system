function loadBatches() {

    fetch("/batches/")
    .then(response => response.json())
    .then(data => {

        let table = document.getElementById("batchTable");

        table.innerHTML = "";

        data.forEach(batch => {

            table.innerHTML += `

            <tr>

                <td>${batch.batch_id}</td>

                <td>${batch.batch_name}</td>

                <td>${batch.year}</td>

                <td>

                    <button onclick="editBatch(${batch.batch_id})">
                        Edit
                    </button>

                    <button onclick="deleteBatch(${batch.batch_id})">
                        Delete
                    </button>

                </td>

            </tr>

            `;

        });

    });

}

loadBatches();

document.getElementById("addBatchBtn").onclick = function () {

    document.getElementById("batchForm").style.display = "block";

    document.getElementById("batch_name").value = "";

    document.getElementById("year").value = "";

    document.getElementById("saveBtn").innerText = "Save Batch";

    document.getElementById("saveBtn").onclick = saveBatch;

};

function searchBatch() {

    let name = document.getElementById("searchBox").value.toLowerCase();

    fetch("/batches/")
    .then(response => response.json())
    .then(data => {

        let table = document.getElementById("batchTable");

        table.innerHTML = "";

        data
        .filter(batch =>
            batch.batch_name.toLowerCase().includes(name)
        )
        .forEach(batch => {

            table.innerHTML += `

            <tr>

                <td>${batch.batch_id}</td>

                <td>${batch.batch_name}</td>

                <td>${batch.year}</td>

                <td>

                    <button onclick="editBatch(${batch.batch_id})">
                        Edit
                    </button>

                    <button onclick="deleteBatch(${batch.batch_id})">
                        Delete
                    </button>

                </td>

            </tr>

            `;

        });

    });

}

async function saveBatch() {

    const batch = {

        batch_name: document.getElementById("batch_name").value,

        year: parseInt(document.getElementById("year").value)

    };

    const response = await fetch("/batches/", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(batch)

    });

    const result = await response.json();

    alert(result.message);

    loadBatches();

    document.getElementById("batchForm").style.display = "none";

}

async function editBatch(id) {

    const response = await fetch(`/batches/${id}`);

    const batch = await response.json();

    document.getElementById("batchForm").style.display = "block";

    document.getElementById("batch_name").value = batch.batch_name;

    document.getElementById("year").value = batch.year;

    document.getElementById("saveBtn").innerText = "Update Batch";

    document.getElementById("saveBtn").onclick = function () {

        updateBatch(id);

    };

}

async function updateBatch(id) {

    const batch = {

        batch_name: document.getElementById("batch_name").value,

        year: parseInt(document.getElementById("year").value)

    };

    const response = await fetch(`/batches/${id}`, {

        method: "PUT",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(batch)

    });

    const result = await response.json();

    alert(result.message);

    loadBatches();

    document.getElementById("batchForm").style.display = "none";

    document.getElementById("saveBtn").innerText = "Save Batch";

    document.getElementById("saveBtn").onclick = saveBatch;

}

async function deleteBatch(id) {

    if (!confirm("Delete this batch?"))
        return;

    const response = await fetch(`/batches/${id}`, {

        method: "DELETE"

    });

    const result = await response.json();

    alert(result.message);

    loadBatches();

}