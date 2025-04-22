// Import the functions you need from the SDKs you need
import { initializeApp, getApps } from "firebase/app";
import { getDatabase } from "firebase/database";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCteUsunrLhB-RMaXpz9v5ux4DSgqjOH1w",
  authDomain: "smartparkingapp-1d951.firebaseapp.com",
  databaseURL: "https://smartparkingapp-1d951-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "smartparkingapp-1d951",
  storageBucket: "smartparkingapp-1d951.firebasestorage.app",
  messagingSenderId: "276657162714",
  appId: "1:276657162714:web:158959a239167b1d8f58e3",
  measurementId: "G-RXRGGS98X9"
};

//  避免重复初始化
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];

const database = getDatabase(app);

export { database };