function checkLogin() {

    // Don't redirect if we're already on the login page
    if (window.location.pathname === "/login") {
        return;
    }

    const username = localStorage.getItem("username");

    if (!username) {
        window.location.href = "/login";
    }

}
// -------------------------
// Logout
// -------------------------

function logout() {

    localStorage.removeItem("username");
    localStorage.removeItem("role");

    window.location.href = "/login";

}

// -------------------------
// Load Menu By Role
// -------------------------

function loadMenu() {

    const role = localStorage.getItem("role");

    // ADMIN
    if (role === "ADMIN") {

        return;

    }

    // TEACHER
    if (role === "TEACHER") {

        document.getElementById("feesMenu").style.display = "none";

        document.getElementById("reportsMenu").style.display = "none";

        document.getElementById("departmentsMenu").style.display = "none";

        document.getElementById("batchesMenu").style.display = "none";

    }

    // STUDENT
    if (role === "STUDENT") {

        document.getElementById("teachersMenu").style.display = "none";

        document.getElementById("studentsMenu").style.display = "none";

        document.getElementById("departmentsMenu").style.display = "none";

        document.getElementById("subjectsMenu").style.display = "none";

        document.getElementById("batchesMenu").style.display = "none";

        document.getElementById("attendanceMenu").style.display = "none";

        document.getElementById("examsMenu").style.display = "none";

        document.getElementById("reportsMenu").style.display = "none";

    }

}

// -------------------------
// Show Logged-in User
// -------------------------

function loadUser() {

    const username = localStorage.getItem("username");

    if (document.getElementById("welcomeUser")) {

        document.getElementById("welcomeUser").innerText =
            "Welcome " + username + " 👋";

    }

}

// -------------------------
// Initialize
// -------------------------

checkLogin();

loadMenu();

loadUser();