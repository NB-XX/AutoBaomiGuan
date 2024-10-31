const JSEncrypt = require('nodejs-jsencrypt').default;

function encrypt(data,publicKey) {
    const encryptor = new JSEncrypt();
    encryptor.setPublicKey(publicKey);
    return encryptor.encrypt(data);
}

module.exports = { encrypt };
