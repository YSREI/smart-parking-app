import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, Alert } from "react-native";
import { ref, set } from "firebase/database";
import { database } from "../firebaseConfig";0
import AsyncStorage from "@react-native-async-storage/async-storage";


export default function RegisterScreen({ navigation }: any) {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [licensePlate, setLicensePlate] = useState("");
  const [nameError, setNameError] = useState("");
  const [phoneError, setPhoneError] = useState("");
  const [emailError, setEmailError] = useState("");
  const [plateError, setPlateError] = useState("");

  const handleRegister = () => {
      // 先清空之前的错误状态
    setNameError("");
    setPhoneError("");
    setEmailError("");
    setPlateError("");

    let hasError = false;

    if (!name) {
      setNameError("Name is required");
      hasError = true;
    } else if (!/^[a-zA-Z\s]+$/.test(name)) {
      setNameError("Name must contain only letters and spaces");
      hasError = true;
    }

    if (!phone) {
      setPhoneError("Phone is required");
      hasError = true;
    } else if (!/^[0-9]{11}$/.test(phone)) {
      setPhoneError("Phone must be 11 digits UK number");
      hasError = true;
    }

    if (!email) {
      setEmailError("Email is required");
      hasError = true;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setEmailError("Please enter a valid email address");
      hasError = true;
    }

    if (!licensePlate) {
      setPlateError("License Plate is required");
      hasError = true;
    } else if (!/^[A-Z0-9]{5,12}$/.test(licensePlate)) {
      setPlateError("License plate must contain only uppercase letters and digits (no spaces)");
      hasError = true;
    }

    if (hasError) return;

    const upperPlate = licensePlate.toUpperCase();
    const safeEmail = email.replace(".", "_");
    const userRef = ref(database, "users/" + safeEmail);

    set(userRef, {
      name,
      phone,
      email,
      licensePlate:upperPlate,
    })
      .then(() => {
        const saveUserAndNavigate = async () => {
          await AsyncStorage.setItem("user", JSON.stringify({ email, licensePlate }));
          Alert.alert("Registration successful!");
          navigation.navigate("Home");
        };
        saveUserAndNavigate();
      })
      .catch((error) => {
        Alert.alert("Registration failed", error.message);
      });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create an account</Text>
  
      <Text style={styles.label}>Full Name (e.g. Tom Zhang)</Text>
      <TextInput
        //placeholder="Name"
        style={styles.input}
        onChangeText={setName}/>
      {nameError !== "" && <Text style={styles.errorText}>{nameError}</Text>}
        
      
  
      <Text style={styles.label}>Phone (e.g. 01234567890)</Text>
      <TextInput
        //placeholder="Phone"
        style={styles.input}
        keyboardType="numeric"
        onChangeText={(text) =>{
          const onlyNumbers = text.replace(/[^0-9]/g, '');
          setPhone(onlyNumbers);
        }}
        value = {phone}/>
      {phoneError !== "" && <Text style={styles.errorText}>{phoneError}</Text>}
  
      <Text style={styles.label}>Email (e.g. 123456@gmail.com)</Text>
      <TextInput
        //placeholder="Email"
        style={styles.input}
        onChangeText={setEmail}
        autoCapitalize="none"/>
      {emailError !== "" && <Text style={styles.errorText}>{emailError}</Text>}
  
      <Text style={styles.label}>License Plate (e.g. AB12 CDE)</Text>
      <TextInput
        //placeholder="License Plate"
        style={styles.input}
        autoCapitalize="characters"
        onChangeText={(text) =>{
          const onlyLettersNumbers = text.replace(/[^A-Z0-9]/gi, '').toUpperCase();
          setLicensePlate(onlyLettersNumbers);
        }}
        value={licensePlate}/>
      {plateError !== "" && <Text style={styles.errorText}>{plateError}</Text>}
  
      <Button title="Register" onPress={handleRegister} />
  
      <View style={{ height: 20 }} />
      <Button title="Already have an account? Sign in here" onPress={() => navigation.navigate("Login")} />
    </View>
  );
  
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 20 },
  title: { fontSize: 24, marginBottom: 20 },
  input: { borderBottomWidth: 1, marginBottom: 16, height: 40 },
  label: { marginBottom: 4, fontSize: 14, color: "#444"},
  errorText: { color: "red", fontSize: 13, marginBottom: 8}
});

