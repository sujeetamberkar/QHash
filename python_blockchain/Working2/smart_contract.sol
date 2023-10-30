// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ElectricityBillPayment {
    address public owner;
    uint public billAmount;
    uint public emiAmount;
    uint public emiFrequency; // in seconds
    uint public lastPaymentTimestamp;

    event ElectricityBillPaid(uint indexed amount, uint indexed timestamp);

    constructor(uint _billAmount, uint _emiAmount, uint _emiFrequency) {
        owner = msg.sender;
        billAmount = _billAmount;
        emiAmount = _emiAmount;
        emiFrequency = _emiFrequency;
        lastPaymentTimestamp = block.timestamp;
    }

    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Only the contract owner can call this function"
        );
        _;
    }

    function payElectricityBill() public payable {
        require(
            msg.value >= emiAmount,
            "Payment amount is less than the EMI amount"
        );
        require(
            block.timestamp >= lastPaymentTimestamp + emiFrequency,
            "EMI is not due yet"
        );

        lastPaymentTimestamp = block.timestamp;
        uint change = msg.value - emiAmount;
        if (change > 0) {
            payable(msg.sender).transfer(change);
        }

        if (msg.value > emiAmount) {
            payable(owner).transfer(emiAmount);
        }

        emit ElectricityBillPaid(emiAmount, block.timestamp);
    }

    function withdrawBalance() public onlyOwner {
        payable(owner).transfer(address(this).balance);
    }
}
