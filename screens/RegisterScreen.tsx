import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, Alert } from "react-native";
import { ref, set } from "firebase/database";
import { database } from "../firebaseConfig";

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
        Alert.alert("Registration successful!");
        navigation.navigate("Home");
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
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 20 },
  title: { fontSize: 24, marginBottom: 20 },
  input: { borderBottomWidth: 1, marginBottom: 16, height: 40 }
});
