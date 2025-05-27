// utils/userStorage.ts
// utility functions for managing user data in AsyncStorage

import AsyncStorage from "@react-native-async-storage/async-storage";

// save user information to AsyncStorage
export const saveUserInfo = async (user: any) => {
  await AsyncStorage.setItem("userInfo", JSON.stringify(user));
};

// retrieve user information from AsyncStorage
export const getUserInfo = async () => {
  const data = await AsyncStorage.getItem("userInfo");
  return data ? JSON.parse(data) : null;
};

// remove user information from AsyncStorage (for logout
export const clearUserInfo = async () => {
  await AsyncStorage.removeItem("userInfo");
};
