# COE817 Project - Secure Banking System
## Introduction
This project simulates an example of a banking system in a user interacts with an ATM which communicates with a bank server. The bank server handles requests made by the user such as deposits, withdrawals, balance inquiries. The user interacts with an ATM GUI which processes the request made by the user and forwards it to the server, the server responds with the corresponding data, then the ATM presents the data requested by the client. The user<-->ATM shall have a security protocol with login/signup, and the ATM<-->Bank shall have a protocol for all data transactions.

## To get started
git clone https://github.com/navidr08-hub/COE817-SecureBankingSystem.git
cd banking_system
python -m venv env ("env" can be changed to a different name)
env\Scripts\activate
pip install -r requirements.txt
python client\atm.py
python server\server.py