from python.primihub.primitive.opt_paillier_c2py_warpper import *
import random
import time

check_list = [0, 0, 0, 0]

def random_plaintext(length):
    res = 0
    for i in range(length - 1):
        res = res << 1
        res = res | random.randint(0, 1)
    if random.randint(0, 1) == 0:
         res = -res
    return res

if __name__ == '__main__':
    keygen_cost = 0
    keygen_st = time.time()
    pub, prv = opt_paillier_keygen(112)
    keygen_ed = time.time()
    keygen_cost += keygen_ed - keygen_st

    print("==================KeyGen is finished==================")
    print("KeyGen costs: " + str(keygen_cost * 1000.0) + " ms.")

    _round = 1000
    encrypt_cost = 0
    decrypt_cost = 0
    add_cost = 0
    for i in range(_round):
        plain_text1 = random_plaintext(2048)
        e_st = time.time()
        cipher_text1 = opt_paillier_encrypt_crt(pub, prv, plain_text1)
        e_ed = time.time()
        encrypt_cost += e_ed - e_st

        d_st = time.time()
        decrypt_text1 = opt_paillier_decrypt_crt(pub, prv, cipher_text1)
        d_ed = time.time()
        decrypt_cost += d_ed - d_st

        if not decrypt_text1 == plain_text1:
            print("Encrypt Error")

        plain_text2 = random_plaintext(2048)
        cipher_text2 = opt_paillier_encrypt_crt(pub, prv, plain_text2)
        a_st = time.time()
        add_cipher_text = opt_paillier_add(pub, cipher_text1, cipher_text2)
        a_ed = time.time()
        add_cost += a_ed - a_st

        add_decrypt_text = opt_paillier_decrypt_crt(pub, prv, add_cipher_text)
        
        if not add_decrypt_text == plain_text1 + plain_text2:
            print("Add Error")
        
        if plain_text1 >= 0:
            if plain_text2 >= 0:
                check_list[0] = 1
            else:
                check_list[1] = 1
        else:
            if plain_text2 >= 0:
                check_list[2] = 1
            else:
                check_list[3] = 1

    print("=========================opt test=========================")
    encrypt_cost = 1.0 / _round * encrypt_cost;
    decrypt_cost = 1.0 / _round * decrypt_cost;
    add_cost     = 1.0 / _round * add_cost;

    print("The total encryption cost is " + str(encrypt_cost * 1000.0 ) + " ms.")
    print("The total decryption cost is " + str(decrypt_cost * 1000.0 ) + " ms.")
    print("The total addition   cost is " + str(add_cost     * 1000.0 ) + " ms.")
    print("checked: " + str(check_list))

    print("========================================================")
