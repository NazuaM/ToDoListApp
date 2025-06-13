import { initializeApp } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-app.js";
import {
  getAuth,
  signInWithEmailAndPassword,
} from "https://www.gstatic.com/firebasejs/11.8.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyAAk-bactk5tD6TSnR0uMF8FKevvUOEaFY",
  authDomain: "todolistapp-666b6.firebaseapp.com",
  projectId: "todolistapp-666b6",
  storageBucket: "todolistapp-666b6.firebasestorage.app",
  messagingSenderId: "928757322075",
  appId: "1:928757322075:web:026a06b4c0b19d026b8a7e",
  measurementId: "G-MW0WGWGTRW",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const submit = document.getElementById("submit");

submit.addEventListener("click", (event) => {
  event.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const user = userCredential.user;
      alert("Login successful!");
      // Redirect to Flask app home page with user uid param
      window.location.href = `/?uid=${user.uid}`;
    })
    .catch((error) => {
      alert(error.message);
    });
});