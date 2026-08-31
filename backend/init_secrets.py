from backend.security.vault import Vault
v = Vault()
v.encrypt_and_store('level_1_pass', '121')
v.encrypt_and_store('level_2_pass', '637531')
print("Secrets initialized.")
