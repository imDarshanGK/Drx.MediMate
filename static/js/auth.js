import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import {getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword} from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";
import{getFirestore, setDoc, doc} from "https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js"

// Firebase configuration and initialization
const firebaseConfig = {
    apiKey: "AIzaSyDa6_47neFJAH-I4i-ZCU0elY4cRmpyotg",
    authDomain: "aditi-pharmaceutical-assistant.firebaseapp.com",
    projectId: "aditi-pharmaceutical-assistant",
    storageBucket: "aditi-pharmaceutical-assistant.firebasestorage.app",
    messagingSenderId: "241653252150",
    appId: "1:241653252150:web:ce83fa898dc2f77a669897",
    measurementId: "G-HMJ6SD9Q9H"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth();
const db = getFirestore();

// Show message in a specific div
function showMessage(message, divId) {
    const messageDiv = document.getElementById(divId);
    messageDiv.style.display = "block";
    messageDiv.innerHTML = message;
    messageDiv.style.opacity = 1;
    setTimeout(function() {
        messageDiv.style.opacity = 0;
    }, 5000);
}

// Signup
const signUp = document.getElementById('submitSignUp');
signUp.addEventListener('click', (event) => {
    event.preventDefault();
    const email = document.getElementById('rEmail').value;
    const password = document.getElementById('rPassword').value;
    const firstName = document.getElementById('fName').value;
    const lastName = document.getElementById('lName').value;

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;
            const userData = {
                email: email,
                firstName: firstName,
                lastName: lastName
            };
            showMessage('Account Created Successfully', 'signUpMessage');
            const docRef = doc(db, "users", user.uid);
            setDoc(docRef, userData)
                .then(() => {
                    window.location.href = 'sisu.html';
                })
                .catch((error) => {
                    console.error("Error writing document", error);
                });
        })
        .catch((error) => {
            const errorCode = error.code;
            if (errorCode == 'auth/email-already-in-use') {
                showMessage('Email Address Already Exists !!!', 'signUpMessage');
            } else {
                showMessage('Unable to create User', 'signUpMessage');
            }
        });
});

// SignIn
const signIn = document.getElementById('submitSignIn');
signIn.addEventListener('click', (event) => {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            showMessage('Login is successful', 'signInMessage');
            const user = userCredential.user;
            localStorage.setItem('loggedInUserId', user.uid);
            window.location.href = "index.html";
        })
        .catch((error) => {
            const errorCode = error.code;
            if (errorCode === 'auth/invalid-credential') {
                showMessage('Incorrect Email or Password', 'signInMessage');
            } else {
                showMessage('Account does not Exist', 'signInMessage');
            }
        });
});

// Check if user is logged in
window.onload = function() {
    const userId = localStorage.getItem('loggedInUserId');
    
    // If the user is not logged in, redirect to the login page
    if (!userId) {
        window.location.href = "/";
    } else {
        // Fetch the user's profile data from Firestore
        const docRef = doc(db, "users", userId);
        getDoc(docRef)
            .then((docSnap) => {
                if (docSnap.exists()) {
                    const userData = docSnap.data();
                    document.getElementById('firstName').innerText = userData.firstName;
                    document.getElementById('lastName').innerText = userData.lastName;
                    document.getElementById('userEmail').innerText = userData.email;
                    document.getElementById('profileData').style.display = "block";
                }
            })
            .catch((error) => {
                console.error("Error fetching profile data: ", error);
            });
    }
};

// Logout function
function logout() {
    signOut(auth).then(() => {
        localStorage.removeItem('loggedInUserId');
        window.location.href = '/';
    }).catch((error) => {
        console.error("Error signing out: ", error);
    });
}
