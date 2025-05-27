import os
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
import cv2


class ParkingDataset(Dataset):
    """
    停车位数据集类
    """

    def __init__(self, root_dir, transform=None, split='train'):
        """
        初始化数据集

        Args:
            root_dir: 数据集根目录，应包含 occupied 和 empty 两个子文件夹
            transform: 图像变换
            split: 数据集分割 ('train', 'val', 或 'test')
        """
        self.root_dir = root_dir
        self.transform = transform
        self.classes = ['empty', 'occupied']
        self.class_to_idx = {cls: i for i, cls in enumerate(self.classes)}

        # 收集所有图像路径和标签
        self.samples = []
        for class_name in self.classes:
            class_path = os.path.join(self.root_dir, class_name)
            if os.path.exists(class_path):
                for img_name in os.listdir(class_path):
                    if img_name.endswith(('.jpg', '.jpeg', '.png')):
                        img_path = os.path.join(class_path, img_name)
                        self.samples.append((img_path, self.class_to_idx[class_name]))

        # 如果需要分割数据集
        if split != 'all' and len(self.samples) > 0:
            # 按照训练集:验证集:测试集 = 7:1.5:1.5的比例划分
            np.random.seed(42)  # 固定随机种子以确保可重复性
            indices = np.random.permutation(len(self.samples))
            if split == 'train':
                split_indices = indices[:int(0.7 * len(indices))]
            elif split == 'val':
                split_indices = indices[int(0.7 * len(indices)):int(0.85 * len(indices))]
            elif split == 'test':
                split_indices = indices[int(0.85 * len(indices)):]
            else:
                raise ValueError(f"Invalid split: {split}")

            self.samples = [self.samples[i] for i in split_indices]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]

        # 读取图像
        image = Image.open(img_path).convert('RGB')

        # 应用变换
        if self.transform:
            image = self.transform(image)

        return image, label

    @staticmethod
    def preprocess_image(image):
        """预处理单张图片"""
        if isinstance(image, str):
            image = cv2.imread(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 调整大小
        image = cv2.resize(image, (224, 224))

        # 转换为PIL图像以便使用torchvision变换
        image = Image.fromarray(image.astype('uint8'))

        # 应用标准变换
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        return transform(image)


def get_data_loaders(data_dir, batch_size=32, img_size=224):
    """
    创建训练、验证和测试数据加载器

    Args:
        data_dir: 数据集目录
        batch_size: 批次大小
        img_size: 输入图像大小

    Returns:
        train_loader, val_loader, test_loader
    """
    # 检查数据集目录是否存在
    if not os.path.exists(data_dir):
        print(f"错误：数据目录不存在: {data_dir}")
        return None, None, None

    # 检查empty和occupied文件夹是否存在
    empty_dir = os.path.join(data_dir, 'empty')
    occupied_dir = os.path.join(data_dir, 'occupied')

    if not os.path.exists(empty_dir) or not os.path.exists(occupied_dir):
        print(f"错误：数据目录结构不正确，需要包含'empty'和'occupied'子文件夹")
        return None, None, None

    # 定义数据变换
    train_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    val_test_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # 创建数据集
    train_dataset = ParkingDataset(data_dir, transform=train_transform, split='train')
    val_dataset = ParkingDataset(data_dir, transform=val_test_transform, split='val')
    test_dataset = ParkingDataset(data_dir, transform=val_test_transform, split='test')

    # 检查数据集是否为空
    if len(train_dataset) == 0:
        print("警告：训练集为空，请确保数据目录中有图像文件")
        return None, None, None

    # 创建数据加载器
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    print(f"训练集大小: {len(train_dataset)}")
    print(f"验证集大小: {len(val_dataset)}")
    print(f"测试集大小: {len(test_dataset)}")

    return train_loader, val_loader, test_loader