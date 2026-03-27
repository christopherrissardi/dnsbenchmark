# 🧠 GlobalDNS Benchmark
Test the best DNS servers for your home or workplace
![1230_1_](https://github.com/user-attachments/assets/1c90bb0f-998d-4d50-b29b-7a407b644513)

## 📄 Relevant information

Tool developed to perform DNS Benchmarking. It has an interactive menu so that the user can choose which type of test to perform. There are currently 3 types of tests

For all types of tests, the response time of an available DNS server for a known public domain is queried. Among the domains, the most well-known globally are listed, such as Google, Amazon, Netflix, and others. (You can check the available domains in the `src/config.py` file.)

Feel free to customize the sites you prefer or include more sites in the test. I focused on including only the most well-known globally so that everyone would benefit during the test!

1. Benchmark test of most well-known DNSs.
The algorithm tests the most popular alternative "TOP DNSs", such as Google 8.8.8.8, Cloudflare 1.1.1.1, and several others.

2. Benchmark test of local DNS servers.
The test covers most local DNS servers, which are provided by local internet providers or private DNS servers. It is worth noting that some of these DNS servers can often be public DNS servers from local internet provider, which may not perform as well as alternative servers. Depending on your city, even your internet provider's DNS may be on the test list!

📄 Note: Your city is automatically recognized in the tool due to the use of an IP location API to make it easier for the user to not have to manually type in your city, so usually if you live in a more remote location and/or a lesser known city, it is natural that the city is where your internet provider is hosted. 

3. Test all DNS servers in your country.

This performance test aims to test all DNS servers in the country where you are located. The same example from the topic above also fits this topic, the difference is that this test will test all domains in your country.

📄 Note: This test may take a few hours depending on the number of servers available in your country!

4. Benchmark all DNS servers available in the world
While this is a bit of an ambitious idea and it is certainly unlikely that anyone will ever do this type of testing, I will be implementing it in the tool soon as well! It is worth noting that this type of testing can take many days to complete and may not make sense in most cases, but I will be implementing it soon.


---

## ✅ Requirements

 - [Python3](https://www.python.org/download/releases/3.0/) (Install the python language on your computer)


---

## 💣 How to use


1. Clone this repository using [git](https://git-scm.com/) or download the repository in ZIP

```bash
git clone https://github.com/christopherrissardi/GlobalDNS-Perf.git
```

2. Enter the cloned repository folder.

```bash
cd /GlobalDNS-Perf
```

3. Install the `requirements.txt` to use the tool

```bash
pip install -r requirements.txt
```

4. Run the `main.py` script

```bash
python3 main.py
```


### 🎯 Adding and modifying for better experience

As an open source tool distributed under the GNU General Public License, it allows anyone to modify, enhance, and experiment with its features to suit individual preferences. The following sections explain how modifications can be made to include new DNS servers, expand the number of tested sites, and adjust other benchmarking parameters.

#### 🏆 Adding new DNS servers to the TOP-DNS list

To add additional DNS servers to the benchmark test:

1. Locate the DNS configuration file within the tool’s directory `(data/top_dns.json)`.

`Original Format:`
```json  
  {
    "ip": "8.8.8.8",
    "name": "dns.google.",
    "status": "success",
    "continent": "North America",
    "continentCode": "NA",
    "country": "United States",
    "country_id": "US",
    "region": "VA",
    "regionName": "Virginia",
    "city": "Ashburn",
    "district": "",
    "zip": "20149",
    "lat": 39.03,
    "lon": -77.5,
    "timezone": "America/New_York",
    "offset": -18000,
    "currency": "USD",
    "isp": "Google LLC",
    "org": "Google Public DNS",
    "as": "AS15169 Google LLC",
    "asname": "GOOGLE",
    "version": "",
    "error": "",
    "dnssec": true,
    "reliability": 1,
    "checked_at": "2022-04-17T08:03:50.419919Z",
    "created_at": "2020-07-16T14:19:04.514857Z"
  }
```

The most important fields in this case are the `ip`, `country_id`, `city` fields and also the `isp` field, the other fields are not needed for the TOP-DNS test! I included them just to make it more complete!

You can include it as follows:

```json
  {
    "ip": "The DNS IP you want",
    "country_id": "Country code",
    "city": "The city of DNS",
    "isp": "DNS Provider"
  },
```

Exemple:

```json
  {
    "ip": "1.1.1.1",
    "country_id": "AU",
    "city": "South Brisbane",
    "isp": "Cloudflare, Inc"
  },
```

What is really important in this case is just the `ip` field... as well as other information, if you wish, you can put something random! However, I recommend that you fill it out correctly to make it more organized.
If you don't know how to get this information, you can easily retrieve it on this website: [IP Geolocation API](https://ip-api.com/)


---

#### Including DNS Servers in the City/Country Benchmark

To include a new DNS in the City/Country benchmark, you must access the respective country file that you want to include in `data/{country_id}.json`.

Let's take an example that you want to add a DNS in the *United States* benchmark

Then you should access the json file of the corresponding country.
Example: `data/us.json`

If you do not know the ID of each country, here you can check which country you want and what the ID of that country is: [Country Codes Alpha-2](https://www.iban.com/country-codes)

`Original Information`
```json
  {
    "ip": "199.255.137.34",
    "name": "",
    "as_number": 31863,
    "isp": "DACEN-2",
    "country_id": "US",
    "city": "",
    "version": "dnsmasq-pi-hole-2.81",
    "error": "",
    "dnssec": false,
    "reliability": 1,
    "checked_at": "2020-07-15T09:33:33.92154Z",
    "created_at": "2020-07-15T09:33:33.92154Z"
  }
```

The required fields are the same: `ip`, `country_id`, `city` and `isp`

```json
  {
    "ip": "The DNS IP you want",
    "country_id": "Country code",
    "city": "The city of DNS",
    "isp": "DNS Provider"
  },
```

Note:
1. I recommend filling in all fields to avoid errors!
2. If you have a private DNS from your internet provider and want to test against the DNS benchmark across your city, make sure the DNS is strictly in the same city where you/your provider is located!

Example: If you query your public IP address and it is in New York, your DNS must also be in New York for DNS by city to work properly!

You can query your city from your IP address here: [DNSLeakTest](https://dnsleaktest.com/).
You can query your DNS city here: [IP Geolocation API](https://ip-api.com/)

If you are not in the same region as your DNS, add it to the TOP-DNS list and perform the benchmark using it and it will work correctly!

If you are a more basic user and don't know how `.json` files work, you can learn how it works here: [W3schools - JSON](https://www.w3schools.com/js/js_json_intro.asp)

### 💉 Increasing the Number of Websites Tested

To expand the list of websites included in the benchmark:

1. Open the file containing the list of websites `domains.py`.
2. Add the URLs of additional websites, ensuring each entry is on a new line.

```python
# Original Format

websites = [
    
    "google.com", 
    "amazon.com", 
    "facebook.com", 
    "x.com", 
    "wikipedia.org", 
    "cnn.com", 
    "bbc.com", 
    "netflix.com", 
    "microsoft.com", 
    "twitch.tv", 
    "linkedin.com",
    "github.com",
    "zoom.us"
    
    ]
```

Add one site below the other in quotation marks (" ") and make sure they are separated by a comma.

Example:

```python
    "exemple.com",
    "iana.org",
    "discord.gg",
    "razer.com" # the last site to be added to the directory/list must not contain a comma
```

## 🔬 Final remarks

The script is fully adaptive, feel free to edit and modify it according to your needs! If you have any questions, please contact us. For any improvements to the code, feel free to contribute by opening an `issue` or even a `Pull request` 🙂
