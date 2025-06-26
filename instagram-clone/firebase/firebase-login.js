// Replace with your actual Firebase project config
const firebaseConfig = {
    // apiKey: "YOUR_FIREBASE_API_KEY",
    // authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    // projectId: "YOUR_PROJECT_ID",
    // storageBucket: "YOUR_PROJECT_ID.appspot.com",
    // messagingSenderId: "YOUR_SENDER_ID",
    // appId: "YOUR_APP_ID",
    apiKey: "AIzaSyD0OoN6pZWfuF5iYEnbQvrV2QNX9p69wtg",
    authDomain: "instagram-replica-458605.firebaseapp.com",
    projectId: "instagram-replica-458605",
    storageBucket: "instagram-replica-media",
    messagingSenderId: "230823599161",
    appId: "1:230823599161:web:de048b2ad2eb788d5101e8",
    measurementId: "G-P5T7SVKZ7S"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

auth.onAuthStateChanged(user => {
    if (user) {
        user.getIdToken().then(token => {
            localStorage.setItem("idToken", token);
            document.getElementById("user-display").innerText = user.displayName || user.email;

            // Add profile link dynamically
            const uid = user.uid;
            const profileLink = document.getElementById("profile-link");
            if (profileLink) {
                profileLink.href = `/profile?uid=${uid}`;
            }
        });
    } else {
        window.location.href = "/login";
    }
});

document.getElementById("logout-btn")?.addEventListener("click", () => {
    auth.signOut().then(() => {
        localStorage.removeItem("idToken");
        window.location.href = "/login";
    });
});

