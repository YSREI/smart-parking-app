import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";

export default function HomeScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Select a Car Park</Text>
      <Button title="Car Park A" onPress={() => navigation.navigate("ParkingLot", { lotId: "lot-a" })} />
      <View style={{ height: 20 }} />
      <Button title="模拟停车流程" onPress={() => navigation.navigate("ParkingAction")} />
      <View style={{ height: 20 }} />
      <Button title="查看历史停车记录" onPress={() => navigation.navigate("History")} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  title: { fontSize: 20, marginBottom: 20 }
});
