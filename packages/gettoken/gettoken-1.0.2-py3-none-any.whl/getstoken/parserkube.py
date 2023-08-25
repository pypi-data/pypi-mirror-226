import os
import sys
import yaml
import json

KUBE_CONFIG_PATH = "~/.kube/config"


def parse_kubeconfig(kubeconfig_path):
    with open(os.path.expanduser(kubeconfig_path), 'r') as f:
        kubeconfig = yaml.safe_load(f)
    return kubeconfig

def print_contexts():
    kubeconfig = parse_kubeconfig(KUBE_CONFIG_PATH)
    contexts = kubeconfig.get('contexts', [])
    print("Available contexts:")
    for idx, context in enumerate(contexts, start=1):
        print(f"{idx}. {context['name']}")

# def get_token():
#     kubeconfig = parse_kubeconfig(KUBE_CONFIG_PATH)
#     print_contexts(kubeconfig)
#     while True:
#         selection = input("Enter the index of the context you want to use (or 'q' to quit): ")
#         if selection.lower() == 'q':
#             break
#         try:
#             context_index = int(selection) - 1
#             contexts = kubeconfig.get('contexts', [])
#             if 0 <= context_index < len(contexts):
#                 context_name = contexts[context_index]['name']
#                 command = "kubectl config use-context "+ context_name
#                 os.system(command)
#                 print(f"Active context set to: {context_name}")
#                 command = "gcloud config config-helper --format=json | jq .credential.access_token"
#                 os.system(command)
#                 break
#             else:
#                 print("Invalid selection. Please choose a valid number.")
#         except ValueError:
#             print("Invalid input. Please enter a number or 'q' to quit.")

def get_token():
    print_contexts()
    kubeconfig = parse_kubeconfig(KUBE_CONFIG_PATH)
    while True:
        selection = input("Enter the index of the context you want to use (or 'q' to quit): ")
        if selection.lower() == 'q':
            break
        try:
            context_index = int(selection) - 1
            contexts = kubeconfig.get('contexts', [])
            if 0 <= context_index < len(contexts):
                context_name = contexts[context_index]['name']
                command = "kubectl config use-context "+ context_name
                os.system(command)
                print(f"Active contexts set to: {context_name}")

                # Run gcloud command to get access token
                gcloud_command = "gcloud config config-helper --format=json"
                gcloud_output = os.popen(gcloud_command).read()
                gcloud_json = json.loads(gcloud_output)
                access_token = gcloud_json.get("credential", {}).get("access_token")
                if access_token:
                    print(f"Access Token: {access_token}")
                else:
                    print("Failed to get access token from gcloud command.")

                break
            else:
                print("Invalid selection. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

if __name__ == "__main__":
    get_token()