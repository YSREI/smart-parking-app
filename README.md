# Smart Parking Mobile App (React Native)

This mobile application is the user-facing component of the Intelligent Parking Management System. Built with React Native, it allows users to register, log in with their license plate, view parking lot availability in real-time, and review their parking history.



## Project Structure

| File/Module              | Description                     |
| ------------------------ | ------------------------------- |
| App.tsx                  | App entry point and navigator   |
| firebaseConfig.ts        | Firebase project configuration  |
| userStorage.ts           | Local storage utils (login      |
| LoginScreen.tsx          | Login form and validation       |
| RegisterScreen.tsx       | Register with email & plate     |
| HomeScreen.tsx           | Main menu to select feature     |
| SelectLotScreen.tsx      | Lot A / Lot C selector          |
| ParkingLotScreen.tsx     | Real time visual parking status |
| ParkingHistoryScreen.tsx | Historical entries of user      |



## Setup Instructions

1. Ensure Node.js and React Native CLI are installed:
```bash
npm install -g react-native-cli
```

2. Navigate to the app folder:
```bash
cd smart-parking-app
```

3. Install dependencies:
```bash
npm install
```

4. Configure Firebase:
- Replace `firebaseConfig.ts` with your Firebase web app config
- Ensure Firebase Realtime Database rules allow read/write

5. Run the app on Android:
```bash
npx expo start --dev-client
```

