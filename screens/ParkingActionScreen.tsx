import React, { useState } from "react";
import { View, Text, Button, Alert, StyleSheet } from "react-native";
import { ref, push, update } from "firebase/database";
import { database } from "../firebaseConfig";

const licensePlate = "AB12CDE";
const ratePerHour = 1.5;

export default function ParkingActionScreen() {
  const [entryKey, setEntryKey] = useState<string | null>(null);
  const [entryTime, setEntryTime] = useState<string | null>(null);

  const handleEnter = async () => {
    const now = new Date().toISOString();
    const recordRef = ref(database, `parking-records/${licensePlate}`);
    const newRecordRef = push(recordRef);

    await update(newRecordRef, {
      entryTime: now,
      paid: false,
    });

    setEntryKey(newRecordRef.key);
    setEntryTime(now);
    Alert.alert("✅ 车辆进场记录成功！");
  };

  const handleExitAndPay = async () => {
    if (!entryKey || !entryTime) {
      Alert.alert("⚠️ 请先点击“进场”按钮");
      return;
    }

    const now = new Date();
    const entry = new Date(entryTime);
    const durationMinutes = Math.round((now.getTime() - entry.getTime()) / 60000);
    const charge = parseFloat(((durationMinutes / 60) * ratePerHour).toFixed(2));

    const targetRef = ref(database, `parking-records/${licensePlate}/${entryKey}`);
    await update(targetRef, {
      exitTime: now.toISOString(),
      durationMinutes,
      charge,
      paid: true,
    });

    setEntryKey(null);
    setEntryTime(null);
    Alert.alert("💰 支付成功", `停车 ${durationMinutes} 分钟，应付 £${charge}`);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🚗 模拟停车流程</Text>
      <Button title="🅿️ 车辆进场" onPress={handleEnter} />
      <View style={{ height: 20 }} />
      <Button title="💸 出场并支付" onPress={handleExitAndPay} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  title: { fontSize: 22, marginBottom: 30 }
});
