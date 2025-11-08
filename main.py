from parcer import scrape_data


city = 'Кишинёв'


if __name__ == "__main__":
    hotels = scrape_data(city)

    for hotel in hotels:
        print(hotel)