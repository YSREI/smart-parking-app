// HomeScreen.tsx

import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";


export default function HomeScreen({ navigation }: any) {
    // Handle logout by removing user data from AsyncStorage
    // reset navigation to show Login screen
    const handleLogout = async () => {
      await AsyncStorage.removeItem("user");
      navigation.reset({
        index: 0,
        routes: [{ name: "Login" }],
      });
    };
  
    // main home screen with navigation options
    return (
      <View style={styles.container}>
        <Text style={[styles.title, { textAlign: "center" }]}>Welcome to the Automated Parking System</Text>
  
        <Button
          title="Car Park Live Status"
          onPress={() => navigation.navigate("SelectLot")}
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
  
  // define styles for the home screen
  const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: "center", alignItems: "center", paddingHorizontal: 20 },
    title: { fontSize: 22, marginBottom: 30, fontWeight: "bold" },
    spacer: { height: 20 },
  });