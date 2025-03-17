import requests
import pandas as pd

api_url = ''
api_key = ''
api_headers = { 'x-api-key': api_key }

def get_pools():

    try:
        response = requests.get(api_url + 'pools', headers=api_headers)

        if response.status_code == 200:
            pools = response.json()
            poolDictionary = {}
            for pool in pools:
                poolDictionary[pool['name'].lower()] = pool['id']
            return poolDictionary
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

pools = get_pools()

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}

def upsert_loan(loan):

    try:
        response = requests.post(api_url + 'loans', json = loan, headers = api_headers)

        if response.status_code == 200 or response.status_code == 201:
            print('Loan upserted')
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None  


dataframe1 = pd.read_excel('').to_dict('records')
for loan in dataframe1:
    loan['loanId'] = str(loan.pop('Loan Number'))
    loan['borrowerFirstName'] = loan['Borrower'].split()[0].capitalize()
    loan['borrowerLastName'] = loan.pop('Borrower').split()[1].capitalize()
    loan['propertyStreetAddress'] = loan.pop('Address')
    loan['propertyCity'] = loan.pop('City')
    loan['propertyState'] = loan.pop('State')
    loan['propertyZip'] = loan.pop('Zip Code')
    loan['unpaidPrincipal'] = loan.pop('Current Principal')
    loan['interestRate'] = loan.pop('Rate')
    loan['principalInterestPayment'] = loan.pop('Payment')
    loan['propertyValue'] = loan.pop('Prop Value')
    loan['originationDate'] = loan.pop('Origination Date').strftime('%m/%d/%Y')
    loan['originalPrincipal'] = loan.pop('Original Principal')
    loan['poolId'] = pools[loan.pop('Pool Name').lower()]
    upsert_loan(loan)
    
dataframe2 = pd.read_csv('').to_dict('records')
for loan in dataframe2:
    loan['loanId'] = loan.pop('Loan ID')
    loan['borrowerFirstName'] = loan.pop('First Name')
    loan['borrowerLastName'] = loan.pop('Last Name')
    loan['propertyStreetAddress'] = str(loan.pop('House number')) + " "+ loan.pop('Street')
    loan['propertyCity'] = loan.pop('City')
    loan['propertyState'] = us_state_to_abbrev[loan.pop('State')]
    loan['propertyZip'] = loan.pop('Zip')
    loan['unpaidPrincipal'] = float(loan.pop('UPB').strip().replace(',',''))
    loan['interestRate'] = float(loan.pop('Interest').replace('%',''))
    loan['principalInterestPayment'] = float(loan.pop('P&I PMT').strip().replace(',',''))
    loan['propertyValue'] = float(loan.pop('Appraisal').strip().replace(',',''))
    loan['originationDate'] = loan.pop('Note Date')
    loan['originalPrincipal'] = float(loan.pop('Original Balance').strip().replace(',',''))
    loan['poolId'] = pools[loan.pop('Pool').lower()]
    upsert_loan(loan)


