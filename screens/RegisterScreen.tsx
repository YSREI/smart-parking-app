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

  const handleRegister = () => {
    if (!name || !phone || !email || !licensePlate) {
      Alert.alert("Please fill in all fields");
      return;
    }

    const safeEmail = email.replace(".", "_");
    const userRef = ref(database, "users/" + safeEmail);
    set(userRef, {
      name,
      phone,
      email,
      licensePlate,
    })
      .then(() => {
        const saveUserAndNavigate = async () => {
            await AsyncStorage.setItem("user", JSON.stringify({
                email,
                licensePlate,
        }));          
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
      <TextInput placeholder="Name" style={styles.input} onChangeText={setName} />
      <TextInput placeholder="Phone" style={styles.input} onChangeText={setPhone} />
      <TextInput placeholder="Email" style={styles.input} onChangeText={setEmail} />
      <TextInput placeholder="License Plate" style={styles.input} onChangeText={setLicensePlate} />
      
      <Button title="Register" onPress={handleRegister} />
      
      {/* 👇 添加这部分按钮 */}
      <View style={{ height: 20 }} />
      <Button title="已有账户？前往登录" onPress={() => navigation.navigate("Login")} />
    </View>
  );  
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 20 },
  title: { fontSize: 24, marginBottom: 20 },
  input: { borderBottomWidth: 1, marginBottom: 16, height: 40 }
});

