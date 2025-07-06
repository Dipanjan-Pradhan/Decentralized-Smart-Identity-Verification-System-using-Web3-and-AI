const express = require('express');
const fileUpload = require('express-fileupload');
const axios = require('axios');
const Web3 = require('web3');
const fs = require('fs');
const app = express();

app.use(fileUpload());

// Connect to local blockchain
const web3 = new Web3("http://127.0.0.1:7545");
const contractABI = [ /* same ABI as before */ ];
const contractAddress = "0xYourContractAddress";
const contract = new web3.eth.Contract(contractABI, contractAddress);
const account = "0xYourAccount";

app.post('/upload', async (req, res) => {
    if (!req.files || !req.files.image) {
        return res.status(400).send('No image uploaded');
    }

    // Send image to AI service
    const formData = new FormData();
    formData.append('image', req.files.image.data, req.files.image.name);

    const verifyRes = await axios.post('http://localhost:5001/verify-face', formData, {
        headers: formData.getHeaders(),
    });

    if (verifyRes.data.verified) {
        // Hash example identity data
        const crypto = require('crypto');
        const hashedData = crypto.createHash('sha256').update("Dipanjan KIIT").digest("hex");

        const tx = await contract.methods.storeIdentity(hashedData).send({ from: account, gas: 3000000 });
        res.send(`Face verified! Identity hash stored on blockchain: ${hashedData}`);
    } else {
        res.send("Face verification failed. Try again.");
    }
});

app.listen(5000, () => console.log("Backend running on http://localhost:5000"));
