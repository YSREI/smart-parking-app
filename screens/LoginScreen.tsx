import React, { useState } from "react";
import { View, Text, TextInput, Button, Alert, StyleSheet } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { ref, get } from "firebase/database";
import { database } from "../firebaseConfig";

export default function LoginScreen({ navigation }: any) {
  const [email, setEmail] = useState("");
  const [licensePlate, setLicensePlate] = useState("");

  const handleLogin = async () => {
    if (!email || !licensePlate) {
      Alert.alert("请输入邮箱和车牌号");
      return;
    }

    const safeEmail = email.replace(".", "_");
    const userRef = ref(database, `users/${safeEmail}`);

    try {
      const snapshot = await get(userRef);
      if (!snapshot.exists()) {
        Alert.alert("用户不存在，请先注册");
        return;
      }

      const userData = snapshot.val();
      if (userData.licensePlate !== licensePlate) {
        Alert.alert("车牌号不匹配");
        return;
      }

      await AsyncStorage.setItem("user", JSON.stringify({ email, licensePlate }));
      navigation.reset({ index: 0, routes: [{ name: "Home" }] });
    } catch (error) {
      Alert.alert("登录失败", (error as any).message);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>登录账户</Text>
      <TextInput placeholder="邮箱" style={styles.input} onChangeText={setEmail} autoCapitalize="none" />
      <TextInput placeholder="车牌号" style={styles.input} onChangeText={setLicensePlate} autoCapitalize="characters" />
      <Button title="登录" onPress={handleLogin} />
      <View style={{ height: 20 }} />
      <Button title="没有账户？前往注册" onPress={() => navigation.navigate("Register")} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 20 },
  title: { fontSize: 24, marginBottom: 20 },
  input: { borderBottomWidth: 1, marginBottom: 16, height: 40 }
});
