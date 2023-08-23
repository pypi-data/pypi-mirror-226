import encryptme

message=encryptme.read("message.txt")
message1=encryptme.decrypt(message, 1234)
message1.show()