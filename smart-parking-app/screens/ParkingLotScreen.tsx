//ParkingLotScreen.tsx

import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, ImageBackground, ScrollView, ActivityIndicator } from "react-native";
import { getDatabase, ref, onValue } from "firebase/database";
import { useRoute } from "@react-navigation/native";
import lotCSpotsData from "../assets/camera8_spots.json";

// interface for parking spot coordinates
interface Spot {
  id: string;
  coords: number[][];
}

//interface for parking space status
interface Space {
  id: string;
  status: string;
}

const ParkingLotScreen = () => {
  // get lot ID from navigation parameters
  const route = useRoute();
  const { lotId } = route.params as { lotId: string };

  // state variables
  const [spaces, setSpaces] = useState<Space[]>([]);
  const [lotCSpots, setLotCSpots] = useState<Spot[]>([]);
  const [imageLayout, setImageLayout] = useState({ width: 1000, height: 750 });
  const [loading, setLoading] = useState(true);


  // fetch realtime parking spaces data from Firebase
  useEffect(() => {
    const db = getDatabase();
    const spacesRef = ref(db, `parking-lots/${lotId}/spaces`);

    // subscribe to realtime updates from Firebase
    const unsubscribe = onValue(spacesRef, (snapshot) => {
      const data = snapshot.val();
      if (data) {
        const parsedSpaces = Object.entries(data).map(([id, value]: [string, any]) => ({
          id,
          status: value.status,
        }));
        setSpaces(parsedSpaces);
      } else {
        setSpaces([]);
      }
      setLoading(false);
    });

    // cleanup subscription
    return () => unsubscribe();
  }, [lotId]);

  // load spot coordinates for lot C
  useEffect(() => {
    // Only process lot-c background image and coordinate
    if (lotId === "lot-c") {
      setLotCSpots(lotCSpotsData || []);
  }}, [lotId]);

  // render parking spaces on the background image
  const renderParkingSpaces = () => {
    // scaling
    const scaleX = imageLayout.width / 1000;
    const scaleY = imageLayout.height / 750;

    //render each parking spot with red/green colour based on status
    return lotCSpots.map((spot) => {
      const matchedSpace = spaces.find((s) => s.id === spot.id);
      const status = matchedSpace?.status ?? "empty";
      const backgroundColor = status === "occupied" ? "red" : "lime";

      // Calculate position and dimensions based on coordinates
      const xs = spot.coords.map((c) => c[0]);
      const ys = spot.coords.map((c) => c[1]);
      const left = Math.min(...xs) * scaleX;
      const top = Math.min(...ys) * scaleY;
      const width = (Math.max(...xs) - Math.min(...xs)) * scaleX;
      const height = (Math.max(...ys) - Math.min(...ys)) * scaleY;

      // render parking spot overlay
      return (
        <View
          key={spot.id}
          style={{
            position: "absolute",
            left,
            top,
            width,
            height,
            backgroundColor,
            opacity: 0.5,
            borderWidth: 1,
            borderColor: "white",
          }}
        />
      );
    });
  };


  // show loading indicator while data is fetching
  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  // render parking lot with background image and space overlays
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Car Park C Status</Text>
      <ImageBackground
        source={require("../assets/carpark8_background.png")}
        style={{ width: "100%", aspectRatio: 1000 / 750, maxWidth: 1000, alignSelf:"center" }}
        onLayout={(event) => {
          // Get actual rendered dimensions for scaling calculations
          const { width, height } = event.nativeEvent.layout;
          setImageLayout({ width, height });
        }}
      >
        {renderParkingSpaces()}
      </ImageBackground>
    </ScrollView>
  );
};

// define styles for parking lot screen
const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 10,
    alignItems: "center",
    backgroundColor: "#f4f4f4",
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginVertical: 10,
  },
  centered: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
});

export default ParkingLotScreen;
