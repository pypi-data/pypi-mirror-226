from ploomes_client.core.ploomes_client import PloomesClient
from ploomes_client.collections.contacts import Contacts

import time
from concurrent.futures import ThreadPoolExecutor
import logging
logger = logging.getLogger(__name__)

def fetch_contact(_):  # Adding a dummy argument
    try:
        contacts = Contacts(ploomes).get_contacts(filter_="TypeId eq 1", top=1, expand="OtherProperties")
        print(contacts.first)
        return True  # Indicate a successful request
    except Exception as e:
        logger.warning(f"Failed to fetch contact: {e}")
        return False  # Indicate a failed request


ploomes = PloomesClient(
    "CA3EF1A4EA8CE9DCB3E049EE88192EA450A8ED23D414AA64A156A89D8E47EC0FC7EF6DFE1BE294A57060102DB391DA613CEE7BF410FD1304EADFADA83983D4A6"
)

start_time = time.time()
with ThreadPoolExecutor() as executor:
    results = list(executor.map(fetch_contact, range(200)))

# Count successful requests
successful_requests = results.count(True)

end_time = time.time() - start_time
print(f"Completed {successful_requests} successful requests in {end_time} seconds")

# Process the results if needed
for result in results:
    if not result:
      print(result)

# print(ploomes.rate_limit_tokens)
