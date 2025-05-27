//App.tsx

import React, { useEffect, useState } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import AsyncStorage from "@react-native-async-storage/async-storage";

import RegisterScreen from "./screens/RegisterScreen";
import HomeScreen from "./screens/HomeScreen";
import ParkingLotScreen from "./screens/ParkingLotScreen";
import ParkingHistoryScreen from "./screens/ParkingHistoryScreen";
import LoginScreen from "./screens/LoginScreen";
import SelectLotScreen from "./screens/SelectLotScreen";

const Stack = createNativeStackNavigator();

export default function App() {
  // State to determine which screen to shwo initially
  const [initialRoute, setInitialRoute] = useState<string | null>(null);


  // check if user is logged in on app start
  // if user data exists on AsynStorage, go to Home Screen
  // Otherwise, go Login screen
  useEffect(() => {
    AsyncStorage.getItem("user").then((value) => {
      if (value) {
        setInitialRoute("Home");
      } else {
        setInitialRoute("Login");
      }
    });
  }, []);

//define all screens in the app

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Register" component={RegisterScreen} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="ParkingLot" component={ParkingLotScreen} />
        <Stack.Screen name="History" component={ParkingHistoryScreen} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="SelectLot" component={SelectLotScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
