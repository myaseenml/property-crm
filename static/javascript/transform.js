const logginn = document.getElementById("Login-Form");
const Reggisterr = document.getElementById("Register-Form");
const login = document.getElementById('login');
const register= document.getElementById('register');
// const indicatorr = document.getElementById("indicator");
function Login(){
    // indicatorr.style.transform = "translateX(18rem)";
    Reggisterr.classList.add("translate-x-1/2", "hidden");
    logginn.classList.add("translate-x-0");
    login.classList.add("active");
    register.classList.remove("active");


    // logginn.classList.add("indicator");

    logginn.classList.remove("translate-x-1/2", "hidden");
    Reggisterr.classList.remove("translate-x-0");
    
}

function Register(){

//  indicatorr.style.transform = "translateX(22.5rem)";
    logginn.classList.add("translate-x-1/2", "hidden");
    logginn.classList.remove("translate-x-0");
    Reggisterr.classList.add("translate-x-0");
    register.classList.add("active");
    
    login.classList.remove("active");


    // Reggisterr.classList.add("indicator");

    Reggisterr.classList.remove("translate-x-1/2", "hidden");  
   
}