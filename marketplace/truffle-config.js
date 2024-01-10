require('babel-register');
require('babel-polyfill');

const PrivateKeyProvider = require('@truffle/hdwallet-provider');
const privateKeys = [
  '6182bf4fedd9fd8040b47125731cf0c3da99f53243014ab4c2e55a422102950f'
];
const privateKeyProvider = new PrivateKeyProvider(
  privateKeys,
  'http://10.20.30.7:8545'  
);
module.exports = {
  networks: {
    Hyperledger_Besu: {
      //host: "10.20.30.7",
      //port: 8545,
      provider: privateKeyProvider, 
      network_id: "*", // Match any network id
      gas: 6721975,
      //from: "0xCA8aB788C8ebDb68900B789D8C3BFfaf7758D8Da",
      //signer: "0xCA8aB788C8ebDb68900B789D8C3BFfaf7758D8Da"
    },
  },
  contracts_directory: './src/contracts/',
  contracts_build_directory: './src/abis/',
  compilers: {
    solc: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  }
}
