from web3 import Web3
import cv2
import hashlib

# Connect to local Ethereum node (Ganache or testnet)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Replace with your contract address and ABI
contract_address = "0xYourContractAddress"
contract_abi = [
    {
        "inputs": [{"internalType": "string","name": "_hash","type": "string"}],
        "name": "storeIdentity",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address","name": "_user","type": "address"}],
        "name": "getIdentity",
        "outputs": [{"internalType": "string","name":"","type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Load contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Account
account = w3.eth.accounts[0]

# === AI Verification Part ===
# Simple face detection using OpenCV
def detect_face(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(faces) > 0

# === Example usage ===
image_path = "user_photo.jpg"

if detect_face(image_path):
    print("Face detected! Storing identity hash on blockchain...")

    # Fake identity data to hash
    identity_data = "Dipanjan KIIT 2025"
    hashed_data = hashlib.sha256(identity_data.encode()).hexdigest()
    
    # Store on blockchain
    tx_hash = contract.functions.storeIdentity(hashed_data).transact({'from': account})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Stored identity hash:", hashed_data)

else:
    print("No face detected. Verification failed.")
