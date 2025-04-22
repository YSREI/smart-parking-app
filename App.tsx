import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import RegisterScreen from "./screens/RegisterScreen";
import HomeScreen from "./screens/HomeScreen";
import ParkingLotScreen from "./screens/ParkingLotScreen";
import ParkingActionScreen from "./screens/ParkingActionScreen";
import ParkingHistoryScreen from "./screens/ParkingHistoryScreen";

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Register">
        <Stack.Screen name="Register" component={RegisterScreen} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="ParkingLot" component={ParkingLotScreen} />
        <Stack.Screen name="ParkingAction" component={ParkingActionScreen} />
        <Stack.Screen name="History" component={ParkingHistoryScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
