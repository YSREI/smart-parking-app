import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";

export default function SelectLotScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>请选择停车场</Text>

      <Button title="Car Park A" onPress={() => navigation.navigate("ParkingLot", { lotId: "lot-a" })} />
      <View style={styles.spacer} />

      <Button title="Car Park C" onPress={() => navigation.navigate("ParkingLot", { lotId: "lot-c" })} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center", paddingHorizontal: 20 },
  title: { fontSize: 24, marginBottom: 30, fontWeight: "bold" },
  spacer: { height: 20 },
});
