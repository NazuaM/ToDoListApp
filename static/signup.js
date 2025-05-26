import { initializeApp } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyAAk-bactk5tD6TSnR0uMF8FKevvUOEaFY",
  authDomain: "todolistapp-666b6.firebaseapp.com",
  projectId: "todolistapp-666b6",
  storageBucket: "todolistapp-666b6.firebasestorage.app",
  messagingSenderId: "928757322075",
  appId: "1:928757322075:web:026a06b4c0b19d026b8a7e",
  measurementId: "G-MW0WGWGTRW"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const submit = document.getElementById('submit');
submit.addEventListener("click", function(event){
  event.preventDefault(); // to prevent page from refreshing

const email = document.getElementById('email').value;
const password = document.getElementById('password').value;

createUserWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    // Signed up 
    const user = userCredential.user;
    alert("Creating Account...")
    window.location.href = "templates\login.html";
    // ...
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
    alert(errorMessage)
    // ..
  });
});