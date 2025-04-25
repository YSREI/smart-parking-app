import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";


export default function HomeScreen({ navigation }: any) {
    // 退出登录函数
    const handleLogout = async () => {
      await AsyncStorage.removeItem("user");
      navigation.reset({
        index: 0,
        routes: [{ name: "Login" }],
      });
    };
  
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Welcome to the Automated Parking System</Text>
  
        <Button
          title="查看停车场状态"
          onPress={() => navigation.navigate("ParkingLot", { lotId: "lot-a" })}
        />
        <View style={styles.spacer} />
  
        <Button
          title=" 模拟停车进出流程"
          onPress={() => navigation.navigate("ParkingAction")}
        />
        <View style={styles.spacer} />
  
        <Button
          title="Parking History"
          onPress={() => navigation.navigate("History")}
        />
        <View style={styles.spacer} />
  
        <Button
          title="Logout"
          color="#f55"
          onPress={handleLogout}
        />
      </View>
    );
  }
  
  const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: "center", alignItems: "center", paddingHorizontal: 20 },
    title: { fontSize: 22, marginBottom: 30, fontWeight: "bold" },
    spacer: { height: 20 },
  });