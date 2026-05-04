# Request Packets

## What is it?
A request packet `rqPacket` is how the Doorbell Manager on a personal computer interfaces with the doorbell hardware and software over the network.

## Structure
An rqPacket is a variable-length array containing information such as a command or a file to be transferred.

The first four bytes indicate the type of the request.
The next eight bytes are the size of the entire packet.
The remaining bytes are the actual object being sent over the network.

## Request Types
0: Status Packet; the size should be 4 with the information field containing a 32-bit integer detailing a status code or a keep-alive code.

1: Doorbell Pin Add; the size should indicate how large the sound file is plus the size of its name and the pin associated with it. Returns whether or not the pin was added in a Status Packet.

2: Doorbell Pin Remove; the size should be how large the pin integer is. Returns whether or not the pin was removed in a Status Packet.

3: Import; the size should specify how large the code file is being sent. Returns a Status Packet.

4: Export; same as 3. Returns the code file.

## Status Codes

0x00000000: Success

0x00000001: Keep Alive

0x00000002: Add Pin Failed

0x00000003: Remove Pin Failed

0x00000004: Import Failed

0x00000005: Export Failed

0xFFFFFFFF: Unknown Failure