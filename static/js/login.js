
async function login() {

    const body = {

        username: document.getElementById("username").value,

        password: document.getElementById("password").value

    };

    const response = await fetch("/auth/login", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(body)

    });

    if (!response.ok) {

        alert("Invalid Username or Password");

        return;

    }

    const user = await response.json();

    localStorage.setItem("username", user.username);
    localStorage.setItem("role", user.role);

    if (user.role === "ADMIN") {

        window.location = "/";

    }

    else if (user.role === "TEACHER") {

        window.location = "/teacher-dashboard.html";

    }

    else {

        window.location = "/student-dashboard.html";

    }

}