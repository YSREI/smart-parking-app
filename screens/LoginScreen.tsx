import React, { useState } from "react";
import { View, Text, TextInput, Button, Alert, StyleSheet } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { ref, get, set } from "firebase/database";
import { database } from "../firebaseConfig";

export default function LoginScreen({ navigation }: any) {
  const [email, setEmail] = useState("");
  const [licensePlate, setLicensePlate] = useState("");
  const [emailError, setEmailError] = useState("");
  const [plateError, setPlateError] = useState("");

  const handleLogin = async () => {
    setEmailError("");
    setPlateError("");

    let hasError = false;

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
      setPlateError("License plate must contain only uppercase letters and digits (no spaces), and must be 5 to 12 characters long.");
      hasError = true;
    }

    
    if (hasError) return;
    

    const safeEmail = email.replace(".", "_");
    const userRef = ref(database, `users/${safeEmail}`);

    try {
        const snapshot = await get(userRef);
        if (!snapshot.exists()) {
          setEmailError("This email is not registered. Please register first.");
          return;
        }
      
        const userData = snapshot.val();
        const inputPlate = licensePlate.toUpperCase();
      
        const licensePlates = userData.license_plates  || [];

        if (!licensePlates.includes(inputPlate)) {
          setPlateError("License plate does not match our records.");
          return;
        }
      
        await AsyncStorage.setItem("user", JSON.stringify({
          email,
          licensePlate: inputPlate,
        }));
      
        navigation.reset({ index: 0, routes: [{ name: "Home" }] });
      
      } catch (error) {
        setEmailError("Login failed. Please check your network connection or try again later.");
      }
    };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login to your account</Text>

      <Text style={styles.label}>Email (e.g. 123456@gmail.com)</Text>
      <TextInput 
      //placeholder="邮箱" 
      style={styles.input} 
      onChangeText={setEmail} 
      autoCapitalize="none" />
      {emailError !== "" && <Text style = {styles.errorText}>{emailError}</Text>}

      <Text style={styles.label}>License Plate (e.g. AB12CDE)</Text>
      <TextInput 
      //placeholder="车牌号"
      style = {styles.input}
      autoCapitalize="characters"
      onChangeText={(text) => {
        const onlyLettersNumbers = text.replace(/[^A-Z0-9]/gi, '').toUpperCase(); // 只保留字母数字并转大写
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

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 20 },
  title: { fontSize: 24, marginBottom: 20 },
  input: { borderBottomWidth: 1, marginBottom: 16, height: 40 },
  label: { marginBottom: 4, fontSize: 14, color: "#444"}, 
  errorText : { color:'red', fontSize: 13, marginBottom: 8}
});
