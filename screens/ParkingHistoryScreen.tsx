import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";
import { ref, onValue } from "firebase/database";
import { database } from "../firebaseConfig";

const licensePlate = "AB12CDE";

interface RecordItem {
  id: string;
  entryTime: string;
  exitTime?: string;
  durationMinutes?: number;
  charge?: number;
  paid: boolean;
}

export default function ParkingHistoryScreen() {
  const [records, setRecords] = useState<RecordItem[]>([]);

  useEffect(() => {
    const userRef = ref(database, `parking-records/${licensePlate}`);
    return onValue(userRef, (snapshot) => {
      const data = snapshot.val();
      if (!data) {
        setRecords([]);
        return;
      }

      const parsed = Object.entries(data).map(([id, value]: any) => ({
        id,
        ...value,
      }));
      setRecords(parsed.reverse());
    });
  }, []);

  const renderItem = ({ item }: { item: RecordItem }) => (
    <View style={styles.card}>
      <Text style={styles.title}>🅿️ 记录编号：{item.id}</Text>
      <Text>📥 入场时间：{item.entryTime}</Text>
      <Text>📤 出场时间：{item.exitTime ?? "尚未离场"}</Text>
      <Text>⏱️ 停车时长：{item.durationMinutes ?? "–"} 分钟</Text>
      <Text>💰 费用：£{item.charge?.toFixed(2) ?? "–"}</Text>
      <Text>✅ 支付状态：{item.paid ? "已支付" : "未支付"}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.header}>🧾 停车记录列表</Text>
      <FlatList data={records} keyExtractor={(item) => item.id} renderItem={renderItem} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, paddingTop: 60, paddingHorizontal: 16 },
  header: { fontSize: 20, fontWeight: "bold", marginBottom: 20 },
  card: {
    padding: 16, borderWidth: 1, borderColor: "#ddd",
    borderRadius: 8, marginBottom: 16, backgroundColor: "#f9f9f9"
  },
  title: { fontWeight: "bold", marginBottom: 4 },
});
