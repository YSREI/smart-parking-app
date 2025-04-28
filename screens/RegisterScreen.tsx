import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, Alert } from "react-native";
import { ref, set, get, child } from "firebase/database";
import { database } from "../firebaseConfig";
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
  const [globalError, setGlobalError] = useState("");


  const handleRegister = async () => {
    setNameError("");
    setPhoneError("");
    setEmailError("");
    setPlateError("");
    setGlobalError("");
  
    let hasError = false;
  
    //校对输入格式
    if (!name) {
      setNameError("Name is required");
      hasError = true;
    } else if (!/^[A-Za-z\s]+$/.test(name)) {
      setNameError("Name must contain only letters");
      hasError = true;
    }
  
    if (!phone) {
      setPhoneError("Phone is required");
      hasError = true;
    } else if (!/^\d{11}$/.test(phone)) {
      setPhoneError("Phone must contain exactly 11 digits");
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
  
    const safeEmail = email.replace(".", "_");
    const usersRef = ref(database, "users/" );
    const upperPlate = licensePlate.toUpperCase();
  

    try {
      // 🔥 全局检查所有用户的license_plates，防止重复车牌
      const usersSnapshot = await get(usersRef);
      if (usersSnapshot.exists()) {
        const usersData = usersSnapshot.val();

        for (const userId in usersData) {
          const user = usersData[userId];

          const platesObj = user.license_plates || [];
          const platesArray = Array.isArray(platesObj) ? platesObj : Object.values(platesObj);
          if (platesArray.includes(upperPlate)) {
            setGlobalError("This license plate is already registered under another account.");
            return;
          }
        }
      }

      // 🔥 然后再继续注册流程
      const userRef = ref(database, "users/" + safeEmail);
      const userSnapshot = await get(userRef);

      if (userSnapshot.exists()) {
        const existingUser = userSnapshot.val();
        const updatedLicensePlates = existingUser.license_plates || [];

        if (!updatedLicensePlates.includes(upperPlate)) {
          updatedLicensePlates.push(upperPlate);
        } else {
          setGlobalError("This license plate has already been registered under your account.");
          return;
        }

        await set(userRef, {
          ...existingUser,
          license_plates: updatedLicensePlates
        });

      } else {
        await set(userRef, {
          name,
          phone,
          email,
          license_plates: [upperPlate]
        });
      }

      await AsyncStorage.setItem("user", JSON.stringify({
        email,
        licensePlate: upperPlate,
      }));

      Alert.alert("Registration successful!");
      navigation.navigate("Home");

    } catch (error) {
      Alert.alert("Registration failed", (error as any).message);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create an account</Text>


      {/* 🔥 全局错误提示 */}
      {globalError !== "" && <Text style={styles.errorText}>{globalError}</Text>}



      <Text style={styles.label}>Full Name (e.g. Tom Zhang)</Text>
      <TextInput
        style={styles.input}
        onChangeText={(text) => {
          setName(text);
          setGlobalError("");//更改input时去掉错误信息
        }}
      />
      {nameError !== "" && <Text style={styles.errorText}>{nameError}</Text>}

      <Text style={styles.label}>Phone (e.g. 01234567890)</Text>
      <TextInput
        style={styles.input}
        keyboardType="numeric"
        value={phone}
        onChangeText={(text) => {
          const onlyNumbers = text.replace(/[^0-9]/g, '');
          setPhone(onlyNumbers);
          setGlobalError("");//更改input时去掉错误信息
        }}
      />
      {phoneError !== "" && <Text style={styles.errorText}>{phoneError}</Text>}

      <Text style={styles.label}>Email (e.g. 123456@gmail.com)</Text>
      <TextInput
        style={styles.input}
        autoCapitalize="none"
        onChangeText={(text) =>{
          setEmail(text);
          setGlobalError("");//更改input时去掉错误信息
        }}
      />
      {emailError !== "" && <Text style={styles.errorText}>{emailError}</Text>}

      <Text style={styles.label}>License Plate (e.g. AB12CDE)</Text>
      <TextInput
        style={styles.input}
        value={licensePlate}
        autoCapitalize="characters"
        onChangeText={(text) => {
          const onlyLettersNumbers = text.replace(/[^A-Z0-9]/gi, '').toUpperCase();
          setLicensePlate(onlyLettersNumbers);
          setGlobalError("");//更改input时去掉错误信息
        }}
      />
      {plateError !== "" && <Text style={styles.errorText}>{plateError}</Text>}

      <Button title="Register" onPress={handleRegister} />
      <View style={{ height: 20 }} />
      <Button title="Already have an account? Sign in here" onPress={() => navigation.navigate("Login")} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 20 },
  title: { fontSize: 24, marginBottom: 20, textAlign: "center" },
  label: { fontSize: 16, marginBottom: 4 },
  input: { borderBottomWidth: 1, marginBottom: 12, height: 40, fontSize: 16 },
  errorText: { color: "red", marginBottom: 8 },
});