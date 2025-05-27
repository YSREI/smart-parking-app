// SelectLotScreen.tsx

import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";

export default function SelectLotScreen({ navigation }: any) {
  //screen to select car parks
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Please Select the Car Park</Text>

      {/* Navigate to ParkingLot screen with aligned lot ID */}
      <Button title="Car Park A" onPress={() => navigation.navigate("ParkingLot", { lotId: "lot-a" })} />
      <View style={styles.spacer} />

      <Button title="Car Park C" onPress={() => navigation.navigate("ParkingLot", { lotId: "lot-c" })} />
    </View>
  );
}

// define styles for the car park selection screen
const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center", paddingHorizontal: 20 },
  title: { fontSize: 24, marginBottom: 30, fontWeight: "bold" },
  spacer: { height: 20 },
});
