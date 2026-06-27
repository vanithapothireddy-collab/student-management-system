fetch("http://127.0.0.1:8000/students/")
.then(response => response.json())
.then(data => {

    let table = document.getElementById("studentTable");

    data.forEach(student => {
        document.getElementById("studentTable").innerHTML += `
            <tr>
                <td>${student.student_id}</td>
                <td>${student.student_name}</td>
                <td>${student.gender}</td>
            </tr>
        `;
    });
});
function searchStudent() {

    let name = document.getElementById("searchBox").value;

    fetch(`http://127.0.0.1:8000/students/search/${name}`)
    .then(response => response.json())
    .then(data => {

        let table = document.getElementById("studentTable");

        table.innerHTML = "";

        data.forEach(student => {

            table.innerHTML += `
                <tr>
                    <td>${student.student_id}</td>
                    <td>${student.student_name}</td>
                    <td>${student.gender}</td>
                </tr>
            `;
        });

    });

}