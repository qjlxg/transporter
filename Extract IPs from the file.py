import re

# Download the file
url = "https://raw.githubusercontent.com/BruceWind/GcoreCDNIPSelector/refs/heads/main/result.txt"
response = requests.get(url)
data = response.text

# Extract IPs using regex
ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', data)

# Save to a file
with open("ips.txt", "w") as file:
    for ip in ips:
        file.write(ip + "\n")

print("IPs saved to ips.txt")
