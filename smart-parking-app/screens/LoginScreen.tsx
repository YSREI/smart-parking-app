// LoginScreen.tsx
// This screen handles user login with email and passwor by checking Firebase Realtime Database
// It validates both email and car plate, and stores user info using AsyncStorage.


import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { ref, get } from "firebase/database";
import { database } from "../firebaseConfig";

export default function LoginScreen({ navigation }: any) {
  // state variables to store user inputs
  const [email, setEmail] = useState("");
  const [licensePlate, setLicensePlate] = useState("");
  //state variables to store validation error messages
  const [emailError, setEmailError] = useState("");
  const [plateError, setPlateError] = useState("");


  // handle login process
  const handleLogin = async () => {
    // reset error messages
    setEmailError("");
    setPlateError("");

    let hasError = false;

    // validate email formaet
    if (!email) {
      setEmailError("Email is required");
      hasError = true;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setEmailError("Please enter a valid email address");
      hasError = true;
    }

    // validate license plate format
    if (!licensePlate) {
      setPlateError("License Plate is required");
      hasError = true;
    } else if (!/^[A-Z0-9]{5,12}$/.test(licensePlate)) {
      setPlateError("License plate must contain only uppercase letters and digits (no spaces), and must be 5 to 12 characters long.");
      hasError = true;
    }

    // if validation fails, stop login process
    if (hasError) return;
    
    // replace dots in email with underscore for firebase path
    const safeEmail = email.replace(".", "_");
    const userRef = ref(database, `users/${safeEmail}`);

    try {
      // check if user exists in database
        const snapshot = await get(userRef);
        if (!snapshot.exists()) {
          setEmailError("This email is not registered. Please register first.");
          return;
        }
      
        const userData = snapshot.val();
        const inputPlate = licensePlate.toUpperCase();
      
        // get user's registered license plates
        const licensePlates = userData.license_plates  || [];

        // verify license plates
        if (!licensePlates.includes(inputPlate)) {
          setPlateError("License plate does not match our records.");
          return;
        }
      
        // Store user info in AsyncStorage for session 
        await AsyncStorage.setItem("user", JSON.stringify({
          email,
          licensePlate: inputPlate,
        }));
      
        // Navigate to Home screen and reset navigation stack
        navigation.reset({ index: 0, routes: [{ name: "Home" }] });
      
      } catch (error) {
        // handle login errors
        setEmailError("Login failed. Please check your network connection or try again later.");
      }
    };

  // Render login form with input fields and validation
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login to your account</Text>

      <Text style={styles.label}>Email (e.g. 123456@gmail.com)</Text>
      <TextInput 
      style={styles.input} 
      onChangeText={setEmail} 
      autoCapitalize="none" />
      {emailError !== "" && <Text style = {styles.errorText}>{emailError}</Text>}

      <Text style={styles.label}>License Plate (e.g. AB12CDE)</Text>
      <TextInput 
      style = {styles.input}
      autoCapitalize="characters"
      onChangeText={(text) => {
        // Remove non-alphanumeric characters and convert to uppercase
        const onlyLettersNumbers = text.replace(/[^A-Z0-9]/gi, '').toUpperCase(); 
        setLicensePlate(onlyLettersNumbers);
      }}
      value={licensePlate}/>
      {plateError !== "" && <Text style = {styles.errorText}>{plateError}</Text>}

      <Button title="Login" onPress={handleLogin} />
      <View style={{ height: 20 }} />
      <Button title="Don't have an account? Register now" onPress={() => navigation.navigate("Register")} />
    </View>
  );
}

// define styles for login screen
const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 20 },
  title: { fontSize: 24, marginBottom: 20 },
  input: { borderBottomWidth: 1, marginBottom: 16, height: 40 },
  label: { marginBottom: 4, fontSize: 14, color: "#444"}, 
  errorText : { color:'red', fontSize: 13, marginBottom: 8}
});
