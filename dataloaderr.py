import os  # This one helps us do things with files and folders
import numpy as np  # This one is like a calculator for big lists of numbers (arrays)
from PIL import Image  # This one helps us open and change images
from sklearn.preprocessing import LabelEncoder  # This one turns words into numbers
from tqdm import tqdm  # This one shows us a progress bar, like when you're downloading something

# Function to load the images
def load_images(parent_folder):
    # These are the lists where we will store the images and their labels
    train_images, train_labels = [], []  # Training images and their names
    test_images, test_labels = [], []  # Testing images and their names

    # Start loading images from the folders
    print("🚀 Loading Images...")  # Let's tell them we are starting
    for subfolder in ['training_data', 'testing_data']:  # Check both training and testing folders
        subfolder_path = os.path.join(parent_folder, subfolder)  # Get the path to the folder
        for class_folder in os.listdir(subfolder_path):  # Check each class (e.g., cracked/normal)
            class_path = os.path.join(subfolder_path, class_folder)  # Path to the class folder
            if os.path.isdir(class_path):  # Only proceed if it's a folder
                # Go through each image in the class folder
                for file in tqdm(os.listdir(class_path), desc=f"Processing {subfolder}/{class_folder}"):
                    file_path = os.path.join(class_path, file)  # Get the full image path
                    # Check if it's an image file we can use
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        try:
                            # Open and prepare the image
                            img = Image.open(file_path).convert('RGB').resize((128, 128))  # Fix to RGB and resize
                            img_array = np.array(img) / 255.0  # Normalize the pixel values (0 to 1) like making all the numbers small
                            if subfolder == 'training_data':  # If it's a training image, add to training
                                train_images.append(img_array)
                                train_labels.append(class_folder)  # Save the label
                            elif subfolder == 'testing_data':  # If it's for testing, add to testing
                                test_images.append(img_array)
                                test_labels.append(class_folder)  # Save the label
                        except Exception as e:  # Catch any errors (e.g., corrupted image file)
                            print(f"Haiya! Problem with image {file_path}: {e}")  # Tell us there's an error

    # Return the images and their labels for both training and testing
    return np.array(train_images), np.array(train_labels), np.array(test_images), np.array(test_labels)

# Example usage (Since you have a folder called `Tire Textures`):
parent_folder = '/content/Tire Textures'  # Where the images are
train_images, train_labels, test_images, test_labels = load_images(parent_folder)  # Load the images

# Use LabelEncoder to turn the labels (e.g., "cracked", "normal") into numbers
label_encoder = LabelEncoder()
train_labels_encoded = label_encoder.fit_transform(train_labels)  # Training labels as numbers
test_labels_encoded = label_encoder.transform(test_labels)  # Testing labels as numbers

# Show what we have
print(f"Classes: {label_encoder.classes_}")  # The different labels in the dataset
print(f"Training Data Shape: {train_images.shape}")  # Number of training images and size
print(f"Testing Data Shape: {test_images.shape}")  # Number of testing images and size

# Imagine you have a box of photos of tires.
# Some tires are cracked, some are normal.
# This code goes into the box, opens each photo, makes sure they are all the same size,
# and puts them into two piles: one for training the computer, and one for testing it.
# It also writes down if each tire is cracked or normal, but instead of writing "cracked" or "normal",
# it writes down numbers, like 0 and 1.
# Then, it tells us how many photos are in each pile and what kind of tires we have.
# Haiya! If there's a problem with a photo, it will tell us.