// utils/userStorage.ts
import AsyncStorage from "@react-native-async-storage/async-storage";

export const saveUserInfo = async (user: any) => {
  await AsyncStorage.setItem("userInfo", JSON.stringify(user));
};

export const getUserInfo = async () => {
  const data = await AsyncStorage.getItem("userInfo");
  return data ? JSON.parse(data) : null;
};

export const clearUserInfo = async () => {
  await AsyncStorage.removeItem("userInfo");
};
