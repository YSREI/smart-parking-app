import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

import numpy as np
import cv2


import os
import json


class ParkingSpaceClassifier(nn.Module):
    """
    A classifier based on ResNet18 to classify parking spaces as occupied or empty.

    """

    def __init__(self, num_classes=2):
        super(ParkingSpaceClassifier, self).__init__()
        # load the resnet18 model
        self.resnet = models.resnet18(pretrained=True)

        # replace the early layers to reduce training time
        for param in list(self.resnet.parameters())[:-10]:
            param.requires_grad = False

        # replace final layer with a custom classifier
        num_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Sequential(
            nn.Linear(num_features, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        return self.resnet(x)


def train_model(model, train_loader, val_loader, epochs=10, learning_rate=0.001, model_save_path=None):
    """
    train the parking space classification mode;l

    Args:
        model: PyTorch model
        train_loader: DataLoader for training data
        val_loader: DataLoader for validation data
        epochs: number of training epochs
        learning_rate: learning rate for optimiser
        model_save_path: optional path to save the best model

    returns the hsitory distionary with training and validation loss & accuracyy
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.1, patience=2, min_lr=1e-6
    )

    best_val_accuracy = 0.0
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

    print(f"Training started for {epochs} epochs...")

    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0

        print(f"Epoch {epoch + 1}/{epochs} training...")
        for i, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()


            train_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()

            # Progress printout every 10 batches
            if (i + 1) % 10 == 0:
                print(f"  Batch {i + 1}/{len(train_loader)}, loss: {loss.item():.4f}")

        train_loss = train_loss / train_total
        train_accuracy = train_correct / train_total
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_accuracy)

        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        print(f"Epoch {epoch + 1}/{epochs} validating...")
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)

                outputs = model(inputs)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()

        val_loss = val_loss / val_total
        val_accuracy = val_correct / val_total
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_accuracy)

        scheduler.step(val_loss)

        print(f'Epoch {epoch + 1}/{epochs}:')
        print(f'  Train loss: {train_loss:.4f}, Train accuracy: {train_accuracy:.4f}')
        print(f'  Val loss: {val_loss:.4f}, Val accuracy: {val_accuracy:.4f}')

        # keep the best model
        if val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            if model_save_path:
                os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
                torch.save(model.state_dict(), model_save_path)
                print(f'   Best model saved with val accuracy: {val_accuracy:.4f}')

    print(f"Training complete! Best val accuracy: {best_val_accuracy:.4f}")
    return history


class ParkingDetector:
    """
    A detector class to detect parking spot occupancy based on trained model.
    """

    def __init__(self, model_path=None, device=None):
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = device

        self.model = ParkingSpaceClassifier().to(self.device)

        if model_path and os.path.exists(model_path):
            print(f"Loading model from: {model_path}")
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        else:
            print(f"Warning: model not found, using untrained model.")

        self.model.eval()
        self.parking_spots = []

    def load_parking_spots(self, config_path):
        """
        Load parking spot definitions from JSON config.
        """
        if not os.path.exists(config_path):
            print(f"Error: config file not found: {config_path}")
            return False

        with open(config_path, 'r') as f:
            self.parking_spots = json.load(f)
            print(f"Loaded {len(self.parking_spots)} parking spots.")
            return True

    def detect_image(self, image_path, output_path=None, camera_id=None):
        """
        Detect parking spot status from a single image.

        Args:
            image_path: path to input image
            output_path: path to save annotated image
            camera_id: optional camera identifier for output naming

        returns the dictionary of spot status results
        """
        if not os.path.exists(image_path):
            print(f"Error: image not found: {image_path}")
            return {}

        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: no parking spots loaded: {image_path}")
            return {}

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        original_height, original_width = image.shape[:2]

        if len(self.parking_spots) == 0:
            print("Error: no parking spots loaded")
            return {}

        from data_processing.dataset import ParkingDataset

        results = {}
        for spot in self.parking_spots:
            pts = np.array(spot["coords"], np.int32)

            valid_points = True
            for pt in pts:
                if pt[0] < 0 or pt[0] >= original_width or pt[1] < 0 or pt[1] >= original_height:
                    print(f"Warning: Spot {spot['id']} out of image bounds")
                    valid_points = False
                    break

            if not valid_points:
                continue

            warped = self._perspective_transform(image_rgb, pts)

            warped_resized = cv2.resize(warped, (150, 150))

            processed = ParkingDataset.preprocess_image(warped_resized)
            processed = processed.unsqueeze(0).to(self.device) 

            with torch.no_grad():
                outputs = self.model(processed)
                probabilities = F.softmax(outputs, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0, predicted_class].item()

            status = "occupied" if predicted_class == 1 else "empty"
            results[spot["id"]] = {
                "status": status,
                "confidence": float(confidence)
            }

            color = (0, 255, 0) if status == "empty" else (0, 0, 255)
            cv2.polylines(image, [pts], True, color, 2)
            x, y = pts[0]
            confidence_text = f"conf: {confidence:.2f}" 
            cv2.putText(image, confidence_text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        if output_path:
            kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
            sharpened = cv2.filter2D(image, -1, kernel)

            encode_params = [cv2.IMWRITE_JPEG_QUALITY, 95] 
            cv2.imwrite(output_path, sharpened, encode_params)


            # Optional: add camera_id suffix to output file name
            #if camera_id:
            #    # 提取文件名和扩展名
            #    filename, ext = os.path.splitext(os.path.basename(output_path))
            #    # 创建包含camera_id的新文件名
            #    new_filename = f"{filename}_{camera_id}{ext}"
            #    # 构建新的输出路径
            #    camera_output_path = os.path.join(os.path.dirname(output_path), new_filename)
            #    output_path = camera_output_path

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, image)
            print(f"Saved result imag: {output_path}")

        return results

    def _perspective_transform(self, image, points):
        """
        Apply perspective transform to extract top-down view of a parking spot.
        """
        target_size = (224, 224)
        dst_points = np.array([
            [0, 0],
            [target_size[0], 0],
            [target_size[0], target_size[1]],
            [0, target_size[1]]
        ], dtype=np.float32)

        points = points.astype(np.float32)
        matrix = cv2.getPerspectiveTransform(points, dst_points)
        warped = cv2.warpPerspective(image, matrix, target_size)
        return warped