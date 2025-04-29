import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet, ImageBackground, ActivityIndicator } from "react-native";
import { ref, onValue } from "firebase/database";
import { database } from "../firebaseConfig";
import lotCSpots from "../assets/camera8_spots.json";

interface Space {
  id: string;
  status: "occupied" | "empty";
}

export default function ParkingLotScreen({ route }: any) {
  const { lotId } = route.params;
  const [spaces, setSpaces] = useState<Space[]>([]);
  const [imageLoaded, setImageLoaded] = useState(false);

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

  const renderLotAItem = ({ item }: any) => (
    <View
      style={[
        styles.spaceBox,
        { backgroundColor: item.status === "occupied" ? "#ff4d4d" : "#4caf50" },
      ]}
    />
  );

  const renderLotCSpaces = () => {
    if (!imageLoaded) {
      return <ActivityIndicator size="large" color="#0000ff" style={{ marginTop: 50 }} />;
    }

    return lotCSpots.map((spot: any) => {
      const matchedSpace = spaces.find((s) => s.id === spot.id);
      const status = matchedSpace?.status || "empty";

      const xs = spot.coords.map((c: any) => c[0]);
      const ys = spot.coords.map((c: any) => c[1]);
      const left = Math.min(...xs);
      const top = Math.min(...ys);
      const width = Math.max(...xs) - Math.min(...xs);
      const height = Math.max(...ys) - Math.min(...ys);

      return (
        <View
          key={spot.id}
          style={{
            position: "absolute",
            left,
            top,
            width,
            height,
            backgroundColor: status === "occupied" ? "rgba(255,0,0,0.5)" : "rgba(0,255,0,0.5)",
            borderWidth: 1,
            borderColor: "white",
            borderRadius: 2,
          }}
        />
      );
    });
  };

  if (lotId === "lot-a") {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Car Park A Status</Text>
        <FlatList
          data={spaces}
          keyExtractor={(item) => item.id}
          numColumns={4}
          renderItem={renderLotAItem}
          contentContainerStyle={styles.grid}
        />
      </View>
    );
  }

  if (lotId === "lot-c") {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Car Park C Status</Text>
        <View style={styles.backgroundWrapper}>
          <ImageBackground
            source={require("../assets/carpark8_background.png")}
            style={styles.background}
            resizeMode="contain"
            onLoad={() => setImageLoaded(true)}
          >
            {renderLotCSpaces()}
          </ImageBackground>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Unknown Lot</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, paddingTop: 60, alignItems: "center", justifyContent: "center" },
  title: { fontSize: 20, marginBottom: 20 },
  grid: { alignItems: "center" },
  spaceBox: { width: 60, height: 60, margin: 8, borderRadius: 8 },
  backgroundWrapper: { width: 1000, height: 750, alignItems: "center", justifyContent: "center" },
  background: { width: 1000, height: 750 },
});
