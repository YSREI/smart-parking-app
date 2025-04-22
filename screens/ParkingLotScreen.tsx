import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";
import { ref, onValue } from "firebase/database";
import { database } from "../firebaseConfig";

export default function ParkingLotScreen({ route }: any) {
  const { lotId } = route.params;
  const [spaces, setSpaces] = useState<{ id: string; status: string }[]>([]);

  useEffect(() => {
    const lotRef = ref(database, `parking-lots/${lotId}/spaces`);
    return onValue(lotRef, (snapshot) => {
      const data = snapshot.val();
      if (data) {
        const parsed = Object.entries(data).map(([id, val]: any) => ({
          id,
          status: val.status,
        }));
        setSpaces(parsed);
      }
    });
  }, [lotId]);

  const renderItem = ({ item }: any) => (
    <View
      style={[
        styles.spaceBox,
        { backgroundColor: item.status === "occupied" ? "#ff4d4d" : "#4caf50" },
      ]}
    />
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Car Park Status</Text>
      <FlatList data={spaces} keyExtractor={(item) => item.id} numColumns={4} renderItem={renderItem} contentContainerStyle={styles.grid} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, paddingTop: 60, alignItems: "center" },
  title: { fontSize: 20, marginBottom: 20 },
  grid: { alignItems: "center" },
  spaceBox: { width: 60, height: 60, margin: 8, borderRadius: 8 }
});
