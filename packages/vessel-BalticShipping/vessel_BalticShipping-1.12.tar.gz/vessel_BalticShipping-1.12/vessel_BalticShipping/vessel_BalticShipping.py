import requests

# Method to obtain the vessel data in dictionary format based on the input imo number. 
def vesselData(imo):
  
  # Check if the input imo is in int format.
  if isinstance(imo, int):

    # URL of the website's API endpoint
    api_url = "https://www.balticshipping.com/"

    # Payload data
    payload = {
        "templates[]": [
            "modal_validation_errors:0",
            "modal_email_verificate:0",
            "r_vessel_types_multi:0",
            "r_positions_single:0",
            "vessel_profile:0"
        ],
        "request[0][module]": "ships",
        "request[0][action]": "list",
        "request[0][id]": "0",
        "request[0][data][0][name]": "search_id",
        "request[0][data][0][value]": "1692460259449",
        "request[0][data][1][name]": "imo",
        "request[0][data][1][value]": imo,
        "request[0][sort]": "",
        "request[0][limit]": "1",
        "request[0][stamp]": "0",
        "request[1][module]": "top_stat",
        "request[1][action]": "list",
        "request[1][id]": "0",
        "request[1][data]": "",
        "request[1][sort]": "",
        "request[1][limit]": "",
        "request[1][stamp]": "0",
        "dictionary[]": ["countrys:0", "vessel_types:0", "positions:0"]
    }

    # Perform the POST request
    response = requests.post(api_url, data=payload)

    # Parse the response as JSON
    json_response = response.json()

    # Obtaining the Ships nested json.
    ships_data = json_response['data']['request'][0]['ships']

    # Condition to validate data actually exists in the table.
    if len(ships_data) > 1:

      return ships_data
    
    # If data for onl 1 ship exists.
    elif len(ships_data) == 1:
        
      # Print the ships data
      for ship in ships_data:
          vessel_data = ship['data']

      # Remove the "gallery" data
      vessel_data.pop('gallery', None)

      # Return the vessel data for 1 ship.
      return vessel_data

    # When the imo is not found.
    else:

      return "Not found"


  else:
    raise ValueError("IMO should be in integer format.")