# Request Packets

## What is it?
A request packet `rqPacket` is how the Doorbell Manager on a personal computer interfaces with the doorbell hardware and software over the network.

## Structure
An rqPacket is a variable-length array containing information such as a command or a file to be transferred.
The first four bytes indicate the type of the request (tbd).
The next eight bytes are the size of the entire packet.
