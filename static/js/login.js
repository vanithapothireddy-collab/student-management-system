async function login() {

    const data = {

        username: document.getElementById("username").value,

        password: document.getElementById("password").value

    };

    const response = await fetch("/login", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(data)

    });

    const result = await response.json();

    if(result.message==="Login Successful"){

        window.location="/";

    }

    else{

        document.getElementById("message").innerHTML=result.message;

    }

}