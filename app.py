import requests
import json
import csv

def make_api_calls_and_write_to_csv():
    # Read the list of keys from the CSV file
    keys_list = []
    with open('keys_list.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keys_list.append(int(row['key']))

    # Define the headers for the API calls
    headers = {
        'Cookie': 'BNI_persistence=fXIFnD6qiYM0RO7hZ1Vs4sJ7rf0tLIm2oOP4_1Dzxnuac-NM--TC3PW-RXt_2T0a6D5eGCrF0M9ptu8f1VziMg=='
    }

    # Open the CSV file for writing
    with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow([
            'Key', 'CardHolderNameEn', 'CardIssueDate', 'CardExpiryDate', 'CardHolderEmail',
            'OfficeNameEn', 'CardHolderMobile', 'Transactions'
        ])

        for key in keys_list:
            url1 = f'https://gateway.dubailand.gov.ae/card/office/search?searchKey={key}&consumer-id=gkb3WvEG0rY9eilwXC0P2pTz8UzvLj9F'
            url2 = f'https://gateway.dubailand.gov.ae/brokers/transactions?brokernumber={key}&consumer-id=gkb3WvEG0rY9eilwXC0P2pTz8UzvLj9F'

            print(f'Making API call to URL1 for key: {key}')
            print(url1)
            
            try:
                # Make the first API call
                response1 = requests.get(url1, headers=headers)
                data1 = response1.json()

                # Write data from the first API call (search API)
                if data1 and 'Response' in data1 and 'Cards' in data1['Response']:
                    card = data1['Response']['Cards'][0]
                    card_data = [
                        key,
                        card['CardHolderNameEn'],
                        card['CardIssueDate'],
                        card['CardExpiryDate'],
                        card['CardHolderEmail'],
                        card['OfficeNameEn'],
                        card['CardHolderMobile']
                    ]

                    print(f'Making API call to URL2 for key: {key}')
                    print(url2)

                    # Make the second API call
                    response2 = requests.get(url2, headers=headers)
                    data2 = response2.json()

                    # Write data from the second API call (transactions API)
                    transactions = []
                    if data2 and 'Response' in data2 and isinstance(data2['Response'], list):
                        for item in data2['Response']:
                            if item['Year'] in [2022, 2023, 2024]:
                                for usage in item['Usage']:
                                    transactions.append(f"{item['Year']} - {usage['UsageTypeNameEn']} - {usage['Count']}")

                    card_data.append(' | '.join(transactions))
                    writer.writerow(card_data)
                else:
                    print('No data found for the first API call.')
                    writer.writerow([key, 'No data found'])
            except Exception as e:
                print(f'Error: {str(e)}')
                writer.writerow([key, f'Error: {str(e)}'])

# Example usage
if __name__ == "__main__":
    make_api_calls_and_write_to_csv()
