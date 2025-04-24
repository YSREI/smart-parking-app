import React, { useEffect, useState } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import AsyncStorage from "@react-native-async-storage/async-storage";

import RegisterScreen from "./screens/RegisterScreen";
import HomeScreen from "./screens/HomeScreen";
import ParkingLotScreen from "./screens/ParkingLotScreen";
import ParkingActionScreen from "./screens/ParkingActionScreen";
import ParkingHistoryScreen from "./screens/ParkingHistoryScreen";
import LoginScreen from "./screens/LoginScreen";

const Stack = createNativeStackNavigator();

export default function App() {
  const [initialRoute, setInitialRoute] = useState<string | null>(null);

  useEffect(() => {
    AsyncStorage.getItem("user").then((value) => {
      if (value) {
        setInitialRoute("Home");
      } else {
        setInitialRoute("Login");
      }
    });
  }, []);

//用于确定点开app时在什么界面
  //if (!initialRoute) return null;

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Register" component={RegisterScreen} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="ParkingLot" component={ParkingLotScreen} />
        <Stack.Screen name="ParkingAction" component={ParkingActionScreen} />
        <Stack.Screen name="History" component={ParkingHistoryScreen} />
        <Stack.Screen name="Login" component={LoginScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
