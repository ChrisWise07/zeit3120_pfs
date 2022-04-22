import feistelcipher.FeistelCipher as fc
import feistelcipher.CryptFunctions as cfs
import feistelcipher.StandardCryptFunctions as scf

funcList = cfs.CryptFunctions()

funcList.addFunc(scf.identity)
funcList.addFunc(scf.add, [-9])
funcList.addFunc(scf.multiply, [-2])
funcList.addFunc(scf.add, [-3])

cipher = fc.FeistelCipher(funcList)

enc = fc.FeistelCipher.EncryptedObject(-15576, -12752, 4)

dec = cipher.decrypt(enc)

print(f"Decrypted Password:\n{dec}\n")
