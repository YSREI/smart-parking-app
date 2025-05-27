// ParkingHistoryScreen.tsx

import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet} from "react-native";
import { ref, onValue } from "firebase/database";
import { database } from "../firebaseConfig";
import AsyncStorage from "@react-native-async-storage/async-storage";

// interface for parking record data
interface RecordItem {
  id: string;
  entryTime: string;
  exitTime?: string;
  durationMinutes?: number;
  charge?: number;
  paid: boolean;
}

export default function ParkingHistoryScreen() {
  // State variables
  const [records, setRecords] = useState<RecordItem[]>([]);
  const [licensePlate, setLicensePlate] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState("");

  // Get the current user's license plate from AsyncStorage
  useEffect(() => {
    AsyncStorage.getItem("user").then((data) => {
      if (data) {
        const parsed = JSON.parse(data);
        setLicensePlate(parsed.licensePlate);
      } else {
        setErrorMessage("Unable to identify user.");
      }
    });
  }, []);

  // listen for parking records for the current account
  useEffect(() => {
    if (!licensePlate) return;

    // set up Firebase reference to user's parking records
    const userRef = ref(database, `parking-records/${licensePlate}`);

    // subscribe to realtime updates from Firebase
    return onValue(userRef, (snapshot) => {
      const data = snapshot.val();
      if (!data) {
        setRecords([]);
        return;
      }

      // parse and sort
      const parsed = Object.entries(data).map(([id, value]: any) => ({
        id,
        ...value,
      }));
      setRecords(parsed.reverse());
    });
  }, [licensePlate]);

   // render each parking record item
  const renderItem = ({ item }: { item: RecordItem }) => (
    <View style={styles.card}>
      <Text style={styles.title}>Record ID：{item.id}</Text>
      <Text>Entry Time: {item.entryTime}</Text>
      <Text>Exit Time: {item.exitTime ?? "Not leaving yet"}</Text>
      <Text>Duration: {item.durationMinutes ?? "–"} mintues</Text>
      <Text>Amount Due: £{item.charge?.toFixed(2) ?? "–"}</Text>
      <Text>Paid: {item.paid ? "true" : "false"}</Text>
    </View>
  );


  // render parking history screen
  return (
    <View style={styles.container}>
      <Text style={styles.header}>Parking History Record</Text>
      <FlatList data={records} keyExtractor={(item) => item.id} renderItem={renderItem} />
      {errorMessage !== "" && <Text style={{ color: "red", marginBottom: 12 }}>{errorMessage}</Text>}
    </View>
  );
}

// define styles for parking history screen
const styles = StyleSheet.create({
  container: { flex: 1, paddingTop: 60, paddingHorizontal: 16 },
  header: { fontSize: 20, fontWeight: "bold", marginBottom: 20 },
  card: {
    padding: 16, borderWidth: 1, borderColor: "#ddd",
    borderRadius: 8, marginBottom: 16, backgroundColor: "#f9f9f9"
  },
  title: { fontWeight: "bold", marginBottom: 4 },
});
