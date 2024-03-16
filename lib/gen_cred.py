import json









pub_key = input("Enter your Gate.io API key: ")
secret_key = input("Enter your Gate.io API Secret key: ")


# Write to ../cred/credentials.json
result_dic = {
    "pub_key": pub_key,
    "secret_key": secret_key
}

res_output = json.dumps(result_dic)
print(res_output)
with open('../cred/credentials.json', 'w') as f:
    f.write(res_output)
    print("Credentials saved successfully!")